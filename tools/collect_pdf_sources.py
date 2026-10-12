"""Collecte de galeries produit pour les fiches PDF, sans achat ni modification du budget."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from io import BytesIO
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
from PIL import Image
import requests

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "tmp/pdfs/pages"
STAMP = datetime.now(timezone.utc).isoformat()
HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36",
           "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8"}


def request(url):
    response = requests.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()
    return response


def amazon_images(soup, raw):
    urls = []
    for match in re.finditer(r"['\"]colorImages['\"]\s*:\s*\{[^\[]*", raw):
        try:
            gallery, _ = json.JSONDecoder().raw_decode(raw[match.end():])
            for item in gallery:
                url = item.get("hiRes") or item.get("large")
                if url:
                    urls.append(url)
        except (ValueError, TypeError, AttributeError):
            pass
    for selector in ("#landingImage", "#imgBlkFront", "#imageBlock img", "#altImages img"):
        for image in soup.select(selector):
            if image.get("data-a-dynamic-image"):
                try:
                    urls.extend(json.loads(image["data-a-dynamic-image"]))
                except ValueError:
                    pass
            for key in ("data-old-hires", "data-src", "src"):
                if image.get(key):
                    urls.append(image[key])
    unique = {}
    for url in urls:
        match = re.search(r"/images/I/([^/.]+)", url)
        if match:
            unique.setdefault(match[1], f"https://m.media-amazon.com/images/I/{match[1]}.jpg")
    return list(unique.values())


def product_images(soup, base):
    urls = []
    for image in soup.select(".product-images img, .product-cover img, .product-images a"):
        src = image.get("data-image-large-src") or image.get("data-full-size-image-url")
        src = src or image.get("href") or image.get("src")
        if src:
            urls.append(urljoin(base, src))
    for link in soup.find_all("a", href=True):
        if "assets.raspberrypi.com" in link["href"] and re.search(r"\.(jpg|png|webp)", link["href"]):
            urls.append(link["href"])
    if not urls:
        meta = soup.find("meta", property="og:image")
        if meta:
            urls.append(urljoin(base, meta["content"]))
    return list(dict.fromkeys(urls))


def download_photos(slug, urls, page, credit, exact=True):
    directory = ROOT / "Composants" / slug / "photos"
    directory.mkdir(parents=True, exist_ok=True)
    photos, failures, hashes = [], [], set()
    for url in urls:
        try:
            response = request(url)
            picture = Image.open(BytesIO(response.content))
            picture.load()
            if min(picture.size) < 100:
                continue
            # Deduplicate decoded pixels: strip thumbnails, sizes and duplicate carousel entries.
            fingerprint = hashlib.sha256(picture.convert("RGB").tobytes()).hexdigest()
            if fingerprint in hashes:
                continue
            hashes.add(fingerprint)
            path = directory / f"vue-{len(photos) + 1:02d}.jpg"
            picture.convert("RGB").save(path, quality=96)
            photos.append({"file": str(path.relative_to(ROOT)), "url": url, "source_page": page,
                           "credit": credit, "exact_product_listing": exact,
                           "width_px": picture.width, "height_px": picture.height,
                           "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                           "consulted_at_utc": STAMP,
                           "caption": "Vue produit de l'annonce ; variante à confirmer à réception"})
        except (OSError, ValueError, requests.RequestException) as error:
            failures.append({"url": url, "error": str(error)})
    return photos, failures


def collect(component):
    slug, page = component["slug"], component["purchase_url"]
    result = {"slug": slug, "consulted_at_utc": STAMP, "purchase_page": page,
              "photos": [], "retrieval_errors": [], "product_details": {}, "documents": []}
    try:
        response = request(page)
        raw = response.text
        CACHE.mkdir(parents=True, exist_ok=True)
        (CACHE / f"{slug}.html").write_text(raw, encoding="utf8")
        soup = BeautifulSoup(raw, "html.parser")
        title = soup.select_one("#productTitle") or soup.find("h1")
        result["page_title"] = title.get_text(" ", strip=True) if title else ""
        result["resolved_page"] = response.url
        for selector in ("#feature-bullets", "#productDescription", "#productDetails_techSpec_section_1",
                         "#productDetails_detailBullets_sections1", "#detailBullets_feature_div"):
            element = soup.select_one(selector)
            if element:
                result["product_details"][selector] = element.get_text(" ", strip=True)
        amazon = "amazon." in urlparse(page).hostname
        urls = amazon_images(soup, raw) if amazon else product_images(soup, page)
        if not urls:
            result["retrieval_errors"].append({"url": page, "error": "Galerie produit inaccessible"})
        result["photos"], failures = download_photos(slug, urls, page,
                                                   "Annonce Amazon / marque du produit" if amazon
                                                   else "Letmeknow / Raspberry Pi")
        result["retrieval_errors"].extend(failures)
    except (requests.RequestException, OSError, ValueError) as error:
        result["retrieval_errors"].append({"url": page, "error": str(error)})
    (ROOT / "Composants" / slug / "documentation.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf8")
    return {"slug": slug, "photos": len(result["photos"]), "title": result.get("page_title", ""),
            "errors": len(result["retrieval_errors"])}


if __name__ == "__main__":
    data = json.loads((ROOT / "achats.json").read_text(encoding="utf8"))
    with ThreadPoolExecutor(max_workers=5) as pool:
        for result in pool.map(collect, data["components"]):
            print(json.dumps(result, ensure_ascii=False), flush=True)
