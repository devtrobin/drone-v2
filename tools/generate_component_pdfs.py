"""Crée les 19 fiches A4 depuis les achats et les sources locales revues ; aucun accès réseau."""
from datetime import datetime, timezone
from io import BytesIO
import hashlib
import html
import json
from pathlib import Path

from PIL import Image as PILImage, ImageDraw, ImageFont
import pymupdf as fitz
import reportlab
from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Flowable, Image, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate,
    Spacer, Table, TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "Composants"
QA = ROOT / "tmp/pdfs/rendered"
WIDTH = A4[0] - 88
FONT_DIR = Path(reportlab.__file__).parent / "fonts"
pdfmetrics.registerFont(TTFont("Vera", str(FONT_DIR / "Vera.ttf")))
pdfmetrics.registerFont(TTFont("VeraBold", str(FONT_DIR / "VeraBd.ttf")))
pdfmetrics.registerFontFamily("Vera", normal="Vera", bold="VeraBold", italic="Vera", boldItalic="VeraBold")
INK, TEAL, MUTED = (HexColor(color) for color in ("#173747", "#137e83", "#58717c"))
PALE, LINE = HexColor("#f0f5f7"), HexColor("#d7e3e8")
BODY = ParagraphStyle("Body", fontName="Vera", fontSize=9, leading=12.7, textColor=INK)
SMALL = ParagraphStyle("Small", parent=BODY, fontSize=7.4, leading=10.2, textColor=MUTED)
TITLE = ParagraphStyle("Title", parent=BODY, fontName="VeraBold", fontSize=21, leading=26,
                       spaceAfter=12)
HEADING = ParagraphStyle("Heading", parent=BODY, fontName="VeraBold", fontSize=12, leading=16,
                         spaceBefore=10, spaceAfter=8, textColor=TEAL, keepWithNext=True)
KEY = ParagraphStyle("Key", parent=BODY, fontName="VeraBold", fontSize=8.5, leading=12)


def clean(text):
    return str(text).replace("—", "-").replace("–", "-").replace("\u2011", "-").replace("\xa0", " ")


def para(text, style=BODY):
    return Paragraph(html.escape(clean(text)), style)


def link(label, url, show_url=False):
    text = f'<a href="{html.escape(url, quote=True)}" color="#137e83">{html.escape(clean(label))}</a>'
    if show_url:
        text += "<br/>" + html.escape(url)
    return Paragraph(text, SMALL)


def money(value):
    return f"{float(value):.2f}".replace(".", ",") + " €"


def table(rows, widths, headings=None):
    cells = [[para(cell, KEY if i == 0 else SMALL if i == len(row) - 1 and len(row) == 3
                   else BODY) for i, cell in enumerate(row)] for row in rows]
    if headings:
        cells.insert(0, [para(heading, KEY) for heading in headings])
    result = Table(cells, colWidths=widths, hAlign="LEFT", repeatRows=int(bool(headings)))
    result.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [PALE, white]),
        ("LINEBELOW", (0, 0), (-1, -1), 0.35, LINE),
    ]))
    return result


class Photo(Flowable):
    def __init__(self, photo, number, width=WIDTH / 2 - 7, height=300):
        super().__init__()
        self.photo, self.number = photo, number
        self.width, self.height = width, height

    def draw(self):
        canvas = self.canv
        canvas.setFillColor(white)
        canvas.setStrokeColor(LINE)
        canvas.roundRect(0, 0, self.width, self.height, 6, fill=1, stroke=1)
        path = ROOT / self.photo["file"]
        canvas.drawImage(ImageReader(str(path)), 9, 54, width=self.width - 18,
                         height=self.height - 68, preserveAspectRatio=True, anchor="c", mask="auto")
        caption = link(f"Vue {self.number:02d} - {self.photo['credit']}", self.photo["source_page"])
        _, height = caption.wrap(self.width - 18, 36)
        caption.drawOn(canvas, 9, 28 - max(0, height - 10))
        raw = link("Image source haute définition", self.photo["url"])
        raw.wrap(self.width - 18, 18)
        raw.drawOn(canvas, 9, 9)


def footer(canvas, document):
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.line(44, 43, A4[0] - 44, 43)
    canvas.setFillColor(MUTED)
    canvas.setFont("Vera", 7)
    canvas.drawString(44, 30, "DRONE V2 | FICHE COMPOSANT | SOURCES : 11/10/2026")
    canvas.drawRightString(A4[0] - 44, 30, str(document.page))
    canvas.restoreState()


def plan_image(profile, slug):
    spec = profile["plan"]
    source = fitz.open(ROOT / spec["file"])
    page = source[spec["page"]]
    clip = fitz.Rect(spec["clip"]) if spec.get("clip") else page.rect
    pixmap = page.get_pixmap(matrix=fitz.Matrix(3, 3), clip=clip)
    image = Image(BytesIO(pixmap.tobytes("png")), width=WIDTH, height=WIDTH * clip.height / clip.width)
    source.close()
    return image


def add_sources(story, component, profile, collected):
    story.append(para("Documentation et provenance", HEADING))
    story.append(link("A - Annonce de la référence retenue", component["purchase_url"], True))
    for code, label, url in profile["sources"]:
        story.extend([Spacer(1, 6), link(f"{code} - {label}", url, True)])
    if collected["documents"]:
        story.append(Spacer(1, 6))
        notice = "Notices originales conservées dans le sous-dossier notices du composant."
        if component["slug"] == "drv8833":
            notice += " La notice TI décrit la puce et ne certifie pas la carte du vendeur."
        story.append(para(notice, SMALL))
    elif not profile["sources"]:
        story.append(Spacer(1, 6))
        story.append(para("Aucune notice technique de la série exacte identifiée dans les sources "
                          "consultées. Les valeurs vendeur et les cotes d’image restent à confirmer.", SMALL))
    story.append(Spacer(1, 6))
    story.append(para("V5 = sélection d’achat historique ; Projet = choix ou cible, sans mesure. "
                      "A = annonce vendeur, pas certification fabricant. R = source officielle "
                      "ou norme de famille. Les dimensions du colis ne sont pas celles du composant.", SMALL))


def mm_values(values):
    return " × ".join(str(value).replace(".", ",") for value in values)


def mm_ranges(ranges):
    return " / ".join(f"{mm_values([low])}-{mm_values([high])}" for low, high in ranges)


def add_estimates(story, dimensions):
    estimates = dimensions["estimates"]
    if not estimates:
        return
    story.extend([PageBreak(), para("Dimensions estimées", TITLE),
                  para("ESTIMATIONS PROVISOIRES - aucune mesure physique. Valeurs en mm.", HEADING),
                  para("Les plages expriment l’incertitude de la méthode et de la variante, "
                       "pas des tolérances fabricant. Elles servent à préparer l’implantation.", BODY),
                  Spacer(1, 12)])
    rows = [[e["label"], mm_values(e["nominal_mm"]), mm_ranges(e["ranges_mm"]), e["confidence"]]
            for e in estimates]
    story.append(table(rows, [122, 102, WIDTH - 293, 69],
                       ["Élément", "Hypothèse (mm)", "Plages (mm)", "Confiance"]))
    story.append(Spacer(1, 10))
    for note in dimensions["notes"]:
        story.extend([para(note, SMALL), Spacer(1, 5)])
    if len(estimates) > 4:
        story.extend([PageBreak(), para("Méthodes et références", TITLE)])
    else:
        story.append(para("Méthodes et références", HEADING))
    for estimate in estimates:
        refs = ", ".join(estimate["sources"])
        axes = " / ".join(estimate["axes"])
        story.append(para(f"{estimate['label']} - axes : {axes}. "
                          f"{estimate['method']} ({refs}).", KEY))
        story.extend([para(estimate["basis"], SMALL), Spacer(1, 7)])
    for source in dimensions["comparison_sources"]:
        story.extend([link(f"{source['code']} - {source['label']}", source["url"], True),
                      para(source["reference_facts"], SMALL), Spacer(1, 6)])
    story.append(para("A = photos ou annonce du lot retenu, créditées dans la galerie. "
                      "E = source de comparaison : aucune équivalence commerciale confirmée.", SMALL))
    story.append(Spacer(1, 7))
    story.append(para("Confirmer dimensions, entraxes et dégagements avant perçage ou fabrication. "
                      "Les masses et supports à créer restent à relever.", BODY))


def build(component, profile, collected):
    slug = component["slug"]
    dimensions = json.loads((OUTPUT / slug / "dimensions.json").read_text(encoding="utf8"))
    photos = [collected["photos"][i - 1] for i in profile["selected"]]
    for photo in photos:
        assert hashlib.sha256((ROOT / photo["file"]).read_bytes()).hexdigest() == photo["sha256"]
    story = [para("DRONE TERRESTRE V2 / DOSSIER COMPOSANT", SMALL), Spacer(1, 9),
             para(profile["title"], TITLE)]
    condition = "Complément à confirmer" if component["conditional"] else "Composant prévu"
    story.append(para(f"{condition} - non acheté, intégration et mesures à valider.", BODY))
    story.append(Spacer(1, 12))
    hero = Photo(photos[0], 1, width=245, height=190)
    summary = [para("ACHAT DE RÉFÉRENCE V5", KEY), Spacer(1, 10),
               para(money(component["total_eur"]), TITLE),
               para("TTC hors livraison, total des lots prévus.", SMALL), Spacer(1, 9),
               para(f"{len(photos)} visuels retenus, sans doublons de miniature.", BODY),
               Spacer(1, 8), para("Prix historique, non actualisé par cette fiche.", SMALL)]
    hero_table = Table([[hero, summary]], colWidths=[258, WIDTH - 258])
    hero_table.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                                   ("LEFTPADDING", (0, 0), (-1, -1), 0)]))
    story.extend([hero_table, Spacer(1, 8), para("Référence et contenu", HEADING)])
    rows = [["Référence", component.get("asin") or "Pi Zero 2 W seul"],
            ["Vendeur V5", component["seller"]], ["Variante", component["variant"]],
            ["Quantité", f"{component['order_lots']} lot(s) ; besoin : {component['needed']}"],
            ["Contenu annoncé", component["lot_contents"]]]
    story.append(table(rows, [105, WIDTH - 105]))
    story.append(para("Points essentiels pour cette version", HEADING))
    for note in profile["notes"]:
        story.extend([para(note), Spacer(1, 5)])
    story.extend([PageBreak(), para("Dimensions et caractéristiques", TITLE),
                  para("Sources A / R : voir les liens ci-dessous. Aucune cote mesurée sur le robot.", SMALL),
                  para("Dimensions utiles", HEADING),
                  table(profile["dimensions"], [113, WIDTH - 203, 90], ["Élément", "Cote / réserve", "Source"]),
                  para("Données techniques", HEADING),
                  table(profile["specs"], [113, WIDTH - 203, 90], ["Paramètre", "Valeur / condition", "Source"])])
    add_sources(story, component, profile, collected)
    if profile.get("assortment"):
        story.extend([PageBreak(), para("Valeurs et cotes de l’assortiment", TITLE),
                      para("Tableau vendeur A ; diamètre × hauteur des corps en mm, hors fils. "
                           "Les dimensions restent à vérifier à réception.", BODY), Spacer(1, 12),
                      table(profile["assortment"], [110, 90, 90, WIDTH - 290],
                            ["Capacité (µF)", "Tension (V)", "Quantité", "Corps (mm)"]),
                      Spacer(1, 12), para("Total annoncé : 145 pièces. Le choix d’un condensateur "
                           "pour le 5 V dépend aussi de l’ESR, du courant d’ondulation et des essais.")])
    if profile.get("plan"):
        story.extend([PageBreak(), para("Plan mécanique du fabricant", TITLE),
                      para(profile["plan"]["credit"], SMALL), Spacer(1, 16),
                      plan_image(profile, slug), Spacer(1, 16),
                      para("Ce plan décrit la référence du fabricant. Contrôler le matériel reçu "
                           "et les dégagements des connecteurs avant de dessiner les fixations.")])
    add_estimates(story, dimensions)
    for start in range(0, len(photos), 4):
        group = photos[start:start + 4]
        story.extend([PageBreak(), para(f"Galerie - vues {start + 1} à {start + len(group)}", TITLE),
                      para("Visuels publiés par le fournisseur : vues produit, détails et infographies. "
                           "Leur contenu promotionnel ne remplace pas une mesure ou une notice.", SMALL),
                      Spacer(1, 12)])
        for row_start in range(0, len(group), 2):
            cards = [Photo(photo, start + row_start + offset + 1)
                     for offset, photo in enumerate(group[row_start:row_start + 2])]
            if len(cards) == 1:
                cards.append("")
            gallery = Table([cards], colWidths=[WIDTH / 2, WIDTH / 2])
            gallery.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                                        ("LEFTPADDING", (0, 0), (-1, -1), 0),
                                        ("TOPPADDING", (0, 0), (-1, -1), 0),
                                        ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))
            story.append(KeepTogether(gallery))
    path = OUTPUT / slug / f"{slug}.pdf"
    document = SimpleDocTemplate(str(path), pagesize=A4, leftMargin=44, rightMargin=44,
                                 topMargin=38, bottomMargin=57, title=profile["title"],
                                 author="Projet Drone terrestre V2", pageCompression=1)
    document.build(story, onFirstPage=footer, onLaterPages=footer)
    pdf = fitz.open(path)
    text = " ".join(page.get_text() for page in pdf)
    def normalized(value):
        return " ".join(clean(value).split())
    expected = [profile["title"], component.get("asin") or "Pi Zero 2 W", money(component["total_eur"])]
    expected += [cell for rows in (profile["dimensions"], profile["specs"]) for row in rows for cell in row]
    expected += [e["basis"] for e in dimensions["estimates"]]
    expected += [mm_values(e["nominal_mm"]) for e in dimensions["estimates"]]
    expected += [mm_ranges(e["ranges_mm"]) for e in dimensions["estimates"]]
    missing = [value for value in expected if normalized(value) not in normalized(text)]
    if missing:
        raise RuntimeError(f"Texte absent dans {slug} : {missing}")
    if "\ufffd" in text or "■" in text:
        raise RuntimeError(f"Glyphe non rendu dans {slug}")
    urls = [item["uri"] for page in pdf for item in page.get_links() if item.get("uri")]
    assert component["purchase_url"] in urls
    for source in profile["sources"]:
        assert source[2] in urls, (slug, source)
    for source in dimensions["comparison_sources"]:
        assert source["url"] in urls, (slug, source)
    for photo in photos:
        assert photo["url"] in urls, (slug, photo["url"])
    for number, page in enumerate(pdf, 1):
        page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5)).save(QA / f"{slug}-{number:02d}.png")
        for block in page.get_text("blocks"):
            if block[6] == 0 and (block[0] < 40 or block[2] > A4[0] - 40 or block[1] < 25
                                  or block[3] > A4[1] - 20):
                raise RuntimeError(f"Texte hors marges : {slug} page {number}")
    record = {"slug": slug, "file": str(path.relative_to(ROOT)), "pages": len(pdf),
              "photos_selected": len(photos), "photos_downloaded": len(collected["photos"]),
              "dimension_estimates": len(dimensions["estimates"]),
              "dimensions_sha256": hashlib.sha256((OUTPUT / slug / "dimensions.json").read_bytes()).hexdigest(),
              "missing_text": missing, "url_annotations": len(urls),
              "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
    pdf.close()
    return record


def contact_sheets():
    paths = sorted(QA.glob("*.png"))
    font = ImageFont.truetype(str(FONT_DIR / "Vera.ttf"), 12)
    for start in range(0, len(paths), 8):
        sheet = PILImage.new("RGB", (1400, 2000), "#dce6ea")
        draw = ImageDraw.Draw(sheet)
        for i, path in enumerate(paths[start:start + 8]):
            image = PILImage.open(path)
            image.thumbnail((640, 440))
            x, y = 30 + (i % 2) * 700, 20 + (i // 2) * 495
            sheet.paste(image, (x + (640 - image.width) // 2, y))
            draw.text((x, y + 452), path.stem, font=font, fill="#173747")
        sheet.save(QA / f"contact-{start // 8 + 1:02d}.jpg", quality=95)


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)
    for path in QA.glob("*.png"):
        path.unlink()
    for path in QA.glob("contact-*.jpg"):
        path.unlink()
    purchases = json.loads((ROOT / "achats.json").read_text(encoding="utf8"))
    profiles = json.loads((ROOT / "Sources/fiches-techniques.json").read_text(encoding="utf8"))["profiles"]
    report = []
    for component in purchases["components"]:
        slug = component["slug"]
        collected = json.loads((ROOT / "Composants" / slug / "documentation.json").read_text(encoding="utf8"))
        result = build(component, profiles[slug], collected)
        report.append(result)
        print(json.dumps(result, ensure_ascii=False), flush=True)
    contact_sheets()
    path = ROOT / "Validation/resultats/fiches-pdf.json"
    path.write_text(json.dumps({"generated_at_utc": datetime.now(timezone.utc).isoformat(),
                               "hardware_verified": False, "visual_review": "à réaliser",
                               "documents": report}, ensure_ascii=False, indent=2) + "\n", encoding="utf8")
    print(f"Terminé : {len(report)} fiches, {sum(item['pages'] for item in report)} pages.")


if __name__ == "__main__":
    main()
