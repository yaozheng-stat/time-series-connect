#!/usr/bin/env python3
"""Generate a Time Series Connect webinar flyer PDF from a webinar Markdown file."""

from __future__ import annotations

import argparse
import ast
import html
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SITE_URL = "https://yaozheng-stat.github.io/time-series-connect/"
DEFAULT_FOOTER = (
    "Time Series Connect Webinar | ASA Business & Economic Statistics Section "
    "& University of Connecticut"
)
BIO_SECTION_TITLES = {
    "bio",
    "biography",
    "speaker bio",
    "speaker biography",
    "about the speaker",
}


@dataclass(frozen=True)
class FlyerBlock:
    kind: str
    markup: str


@dataclass(frozen=True)
class FlyerSection:
    title: str
    blocks: list[FlyerBlock]


@dataclass(frozen=True)
class Webinar:
    title: str
    speaker: str
    affiliation: str
    date_display: str
    time: str
    permalink: str
    registration_url: str
    speaker_image: Path | None
    sections: list[FlyerSection]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a Time Series Connect webinar flyer PDF."
    )
    parser.add_argument(
        "webinar_markdown",
        type=Path,
        help="Path to a webinar Markdown file, such as _webinars/2026-09-28-rebecca-killick.md.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output PDF path. Defaults to output/pdf/<webinar-slug>-webinar-flyer.pdf.",
    )
    parser.add_argument(
        "--site-url",
        default=DEFAULT_SITE_URL,
        help=f"Public site URL used for header and event links. Default: {DEFAULT_SITE_URL}",
    )
    parser.add_argument(
        "--event-url",
        help="Override the event website URL. Defaults to site URL plus webinar permalink.",
    )
    parser.add_argument(
        "--label",
        default="Upcoming Webinar",
        help='Main flyer label. Default: "Upcoming Webinar".',
    )
    parser.add_argument(
        "--footer",
        default=DEFAULT_FOOTER,
        help="Footer text printed at the bottom of the flyer.",
    )
    parser.add_argument(
        "--tsc-logo",
        type=Path,
        default=REPO_ROOT / "assets/images/TSC-logo.jpg",
        help="Path to the Time Series Connect logo.",
    )
    parser.add_argument(
        "--asa-logo",
        type=Path,
        default=REPO_ROOT / "assets/images/ASA-BES-logo.jpg",
        help="Path to the ASA-BES logo.",
    )
    parser.add_argument(
        "--uconn-wordmark",
        type=Path,
        default=REPO_ROOT / "assets/images/UConn-wordmark.png",
        help="Path to the UConn wordmark logo.",
    )
    parser.add_argument(
        "--no-headshot",
        action="store_true",
        help="Do not include the speaker headshot even if speaker_image is set.",
    )
    return parser.parse_args()


def split_front_matter(markdown: str) -> tuple[str, str]:
    if not markdown.startswith("---"):
        raise ValueError("Expected YAML front matter delimited by --- at the top.")
    parts = markdown.split("---", 2)
    if len(parts) < 3:
        raise ValueError("Could not find closing --- for front matter.")
    return parts[1], parts[2]


def parse_scalar_front_matter(front_matter: str) -> dict[str, str]:
    """Parse simple scalar YAML fields used by the webinar files.

    This intentionally ignores nested lists such as `materials`, because the flyer
    template only needs scalar event metadata plus the abstract body.
    """
    data: dict[str, str] = {}
    for raw_line in front_matter.splitlines():
        if not raw_line.strip() or raw_line.startswith((" ", "-")):
            continue
        if ":" not in raw_line:
            continue
        key, value = raw_line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            continue
        if len(value) >= 2 and value[0] in {"'", '"'} and value[-1] == value[0]:
            try:
                value = ast.literal_eval(value)
            except (SyntaxError, ValueError):
                value = value[1:-1]
        data[key] = str(value)
    return data


def clean_text(text: str) -> str:
    replacements = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u2011": "-",
        "\u00a0": " ",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return re.sub(r"\s+", " ", text).strip()


def normalize_inline_text(text: str) -> str:
    replacements = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u2011": "-",
        "\u00a0": " ",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return re.sub(r"\s+", " ", text)


def strip_html_comments(text: str) -> str:
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    return text.strip()


def strip_inline_markdown(text: str) -> str:
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"__([^_]+)__", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    text = re.sub(r"_([^_]+)_", r"\1", text)
    return text


def escape_reportlab_text(text: str) -> str:
    return html.escape(strip_inline_markdown(clean_text(text)), quote=False)


def escape_reportlab_fragment(text: str) -> str:
    return html.escape(strip_inline_markdown(normalize_inline_text(text)), quote=False)


def reportlab_link(label: str, url: str) -> str:
    safe_label = escape_reportlab_text(label)
    safe_url = html.escape(clean_text(url), quote=True)
    return f'<link href="{safe_url}" color="#006CB8"><u>{safe_label}</u></link>'


def link_bare_urls(text: str) -> str:
    url_pattern = re.compile(r"(?<![\"'=])(https?://[^\s<]+)")
    output: list[str] = []
    last = 0
    for match in url_pattern.finditer(text):
        output.append(escape_reportlab_fragment(text[last : match.start()]))
        url = match.group(1).rstrip(".,;)")
        trailing = match.group(1)[len(url) :]
        output.append(reportlab_link(url, url))
        output.append(escape_reportlab_fragment(trailing))
        last = match.end()
    output.append(escape_reportlab_fragment(text[last:]))
    return "".join(output)


def markdown_inline_to_reportlab(text: str) -> str:
    text = strip_html_comments(text)
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return ""
    link_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
    output: list[str] = []
    last = 0
    for match in link_pattern.finditer(text):
        output.append(link_bare_urls(text[last : match.start()]))
        output.append(reportlab_link(match.group(1), match.group(2)))
        last = match.end()
    output.append(link_bare_urls(text[last:]))
    return "".join(output).strip()


def is_bio_section(title: str) -> bool:
    normalized = clean_text(title).lower()
    return normalized in BIO_SECTION_TITLES


def parse_section_blocks(section_content: str) -> list[FlyerBlock]:
    section_content = strip_html_comments(section_content)
    blocks: list[FlyerBlock] = []
    for chunk in re.split(r"\n\s*\n", section_content):
        lines = [line.strip() for line in chunk.splitlines() if line.strip()]
        if not lines:
            continue
        if all(line.startswith(("- ", "* ")) for line in lines):
            for line in lines:
                markup = markdown_inline_to_reportlab(line[2:])
                if markup:
                    blocks.append(FlyerBlock("bullet", markup))
        else:
            markup = markdown_inline_to_reportlab(" ".join(lines))
            if markup:
                blocks.append(FlyerBlock("paragraph", markup))
    return blocks


def body_sections(body: str) -> list[FlyerSection]:
    headings = list(re.finditer(r"^##\s+(.+?)\s*$", body, flags=re.M))
    sections: list[FlyerSection] = []
    for index, heading in enumerate(headings):
        title = clean_text(heading.group(1))
        start = heading.end()
        end = headings[index + 1].start() if index + 1 < len(headings) else len(body)
        if is_bio_section(title):
            continue
        blocks = parse_section_blocks(body[start:end])
        if blocks:
            sections.append(FlyerSection(title, blocks))
    return sections


def format_date(raw_date: str) -> str:
    raw_date = clean_text(raw_date)
    if not raw_date:
        return ""
    for fmt in ("%Y-%m-%d", "%Y/%m/%d"):
        try:
            parsed = datetime.strptime(raw_date, fmt)
            return f"{parsed:%A}, {parsed:%B} {parsed.day}, {parsed:%Y}"
        except ValueError:
            pass
    return raw_date


def path_from_site_value(value: str, root: Path) -> Path | None:
    value = clean_text(value)
    if not value or value.startswith(("http://", "https://")):
        return None
    if value.startswith("/"):
        return root / value.lstrip("/")
    return (root / value).resolve()


def slug_from_webinar(input_path: Path, permalink: str) -> str:
    permalink = permalink.strip("/")
    if permalink:
        return permalink.split("/")[-1]
    slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", input_path.stem)
    return slug or input_path.stem


def event_url(site_url: str, permalink: str, override: str | None) -> str:
    if override:
        return override
    base = site_url.rstrip("/") + "/"
    return urljoin(base, permalink.lstrip("/"))


def load_webinar(path: Path, include_headshot: bool) -> Webinar:
    markdown = path.read_text(encoding="utf-8")
    front, body = split_front_matter(markdown)
    data = parse_scalar_front_matter(front)
    speaker_image = path_from_site_value(data.get("speaker_image", ""), REPO_ROOT)
    if not include_headshot:
        speaker_image = None
    if speaker_image and not speaker_image.exists():
        raise FileNotFoundError(f"speaker_image does not exist: {speaker_image}")
    return Webinar(
        title=clean_text(data.get("title", "")),
        speaker=clean_text(data.get("speaker", "")),
        affiliation=clean_text(data.get("affiliation", "")),
        date_display=format_date(data.get("date", "")),
        time=clean_text(data.get("time", "")),
        permalink=clean_text(data.get("permalink", "")),
        registration_url=clean_text(data.get("registration_url", "")),
        speaker_image=speaker_image,
        sections=body_sections(body),
    )


def image_aspect(path: Path) -> float:
    width, height = ImageReader(str(path)).getSize()
    return width / height


def make_para(markup: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(markup, style)


def wrap_height(markup: str, style: ParagraphStyle, width: float) -> float:
    paragraph = make_para(markup, style)
    _, height = paragraph.wrap(width, 10000)
    return height


def draw_para(
    pdf: canvas.Canvas,
    markup: str,
    style: ParagraphStyle,
    x: float,
    y_top: float,
    width: float,
) -> float:
    paragraph = make_para(markup, style)
    _, height = paragraph.wrap(width, 10000)
    paragraph.drawOn(pdf, x, y_top - height)
    return height


def centered_baseline(y: float, height: float, font_name: str, font_size: float) -> float:
    ascent, descent = pdfmetrics.getAscentDescent(font_name, font_size)
    return y + (height - (ascent - descent)) / 2 - descent


def draw_button(
    pdf: canvas.Canvas,
    label: str,
    url: str,
    x: float,
    y: float,
    width: float,
    height: float,
    fill: colors.Color,
    text_color: colors.Color,
    stroke: colors.Color | None = None,
) -> None:
    pdf.setFillColor(fill)
    if stroke:
        pdf.setStrokeColor(stroke)
        pdf.setLineWidth(1.4)
        pdf.roundRect(x, y, width, height, 7, fill=1, stroke=1)
    else:
        pdf.roundRect(x, y, width, height, 7, fill=1, stroke=0)
    font = "Helvetica-Bold"
    size = 12.4
    pdf.setFillColor(text_color)
    pdf.setFont(font, size)
    pdf.drawCentredString(x + width / 2, centered_baseline(y, height, font, size), label)
    if url:
        pdf.linkURL(url, (x, y, x + width, y + height), relative=0, thickness=0)


def generate_flyer(
    webinar: Webinar,
    output: Path,
    site_url: str,
    event_url_value: str,
    label: str,
    footer: str,
    tsc_logo: Path,
    asa_logo: Path,
    uconn_wordmark: Path,
) -> None:
    for required in (tsc_logo, asa_logo, uconn_wordmark):
        if not required.exists():
            raise FileNotFoundError(f"Required logo does not exist: {required}")

    page_width = letter[0]
    margin_x = 30
    top_margin = 24
    bottom_margin = 22
    header_h = 62
    brand_logo = 34
    blue = colors.HexColor("#006CB8")
    navy = colors.HexColor("#081F36")
    gold = colors.HexColor("#F0B400")
    text = colors.HexColor("#1F2933")
    muted = colors.HexColor("#52606D")
    light_blue = colors.HexColor("#EEF7FC")
    light_gold = colors.HexColor("#FFF7D6")
    line = colors.HexColor("#D8E1E8")

    styles = {
        "label": ParagraphStyle(
            "label", fontName="Helvetica-Bold", fontSize=26, leading=30, textColor=blue
        ),
        "title": ParagraphStyle(
            "title", fontName="Helvetica-Bold", fontSize=28, leading=31.5, textColor=navy
        ),
        "speaker": ParagraphStyle(
            "speaker", fontName="Helvetica-Bold", fontSize=23, leading=26, textColor=navy
        ),
        "affiliation": ParagraphStyle(
            "affiliation", fontName="Helvetica", fontSize=14, leading=17.2, textColor=text
        ),
        "section": ParagraphStyle(
            "section", fontName="Helvetica-Bold", fontSize=18, leading=22, textColor=navy
        ),
        "body": ParagraphStyle(
            "body",
            fontName="Helvetica",
            fontSize=13.2,
            leading=16.6,
            textColor=text,
            alignment=TA_LEFT,
        ),
        "abstract_body": ParagraphStyle(
            "abstract_body",
            fontName="Helvetica",
            fontSize=13.2,
            leading=16.6,
            textColor=text,
            alignment=TA_JUSTIFY,
        ),
        "bullet": ParagraphStyle(
            "bullet",
            fontName="Helvetica",
            fontSize=13.2,
            leading=16.6,
            textColor=text,
            alignment=TA_LEFT,
            leftIndent=14,
            firstLineIndent=-10,
        ),
        "footer": ParagraphStyle(
            "footer",
            fontName="Helvetica",
            fontSize=10.2,
            leading=12.4,
            alignment=TA_CENTER,
            textColor=muted,
        ),
    }

    def block_style_name(section: FlyerSection, block: FlyerBlock) -> str:
        if block.kind == "bullet":
            return "bullet"
        if clean_text(section.title).lower() == "abstract":
            return "abstract_body"
        return "body"

    content_w = page_width - 2 * margin_x
    label_h = wrap_height(escape_reportlab_text(label), styles["label"], content_w)
    title_h = wrap_height(escape_reportlab_text(webinar.title), styles["title"], content_w)
    head_w = 86
    head_h = 103
    speaker_gap = 18 if webinar.speaker_image else 0
    speaker_image_w = head_w if webinar.speaker_image else 0
    speaker_text_w = content_w - speaker_image_w - speaker_gap
    speaker_h = max(
        head_h if webinar.speaker_image else 0,
        wrap_height(escape_reportlab_text(webinar.speaker), styles["speaker"], speaker_text_w)
        + 8
        + wrap_height(
            escape_reportlab_text(webinar.affiliation),
            styles["affiliation"],
            speaker_text_w,
        ),
    )
    sections_h = 0
    for section_index, section in enumerate(webinar.sections):
        sections_h += wrap_height(escape_reportlab_text(section.title), styles["section"], content_w) + 7
        for block_index, block in enumerate(section.blocks):
            style_name = block_style_name(section, block)
            block_markup = "- " + block.markup if block.kind == "bullet" else block.markup
            sections_h += wrap_height(block_markup, styles[style_name], content_w)
            if block_index < len(section.blocks) - 1:
                sections_h += 8 if block.kind != "bullet" else 5
        if section_index < len(webinar.sections) - 1:
            sections_h += 17
    footer_h = wrap_height(escape_reportlab_text(footer), styles["footer"], content_w)
    button_h = 34

    content_after_header = (
        18
        + label_h
        + 8
        + title_h
        + 15
        + 64
        + 17
        + speaker_h
        + 17
        + button_h
        + 20
        + sections_h
        + 20
        + 1
        + 9
        + footer_h
    )
    page_h = int(top_margin + header_h + content_after_header + bottom_margin + 0.999)

    output.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(output), pagesize=(page_width, page_h))
    pdf.setTitle(f"{webinar.speaker} Time Series Connect Webinar Flyer")
    pdf.setAuthor("Time Series Connect")
    pdf.setSubject("Webinar flyer")

    pdf.setFillColor(colors.white)
    pdf.rect(0, 0, page_width, page_h, fill=1, stroke=0)

    header_top = page_h - top_margin
    header_y = header_top - header_h
    pdf.setFillColor(colors.white)
    pdf.rect(0, header_y, page_width, header_h + top_margin, fill=1, stroke=0)
    pdf.setStrokeColor(line)
    pdf.setLineWidth(0.7)
    pdf.line(margin_x, header_y, page_width - margin_x, header_y)

    logo_x = margin_x
    logo_y = header_y + (header_h - brand_logo) / 2
    pdf.drawImage(
        str(tsc_logo),
        logo_x,
        logo_y,
        brand_logo,
        brand_logo,
        preserveAspectRatio=True,
        mask="auto",
    )
    brand_text = "Time Series Connect"
    brand_x = logo_x + brand_logo + 10
    brand_font_size = 14.3
    brand_y = header_y + header_h / 2 - 5

    partner_gap = 12
    asa_w = 220
    asa_h = asa_w / image_aspect(asa_logo)
    uconn_h = 18.5
    uconn_w = uconn_h * image_aspect(uconn_wordmark)
    partners_w = asa_w + partner_gap + uconn_w
    partners_x = page_width - margin_x - partners_w

    while (
        brand_x + stringWidth(brand_text, "Helvetica-Bold", brand_font_size)
        > partners_x - 16
        and brand_font_size > 10
    ):
        brand_font_size -= 0.5

    pdf.setFont("Helvetica-Bold", brand_font_size)
    pdf.setFillColor(navy)
    pdf.drawString(brand_x, brand_y, brand_text)
    brand_w = stringWidth(brand_text, "Helvetica-Bold", brand_font_size)
    pdf.linkURL(site_url, (logo_x, logo_y, brand_x + brand_w, logo_y + brand_logo), relative=0, thickness=0)

    center_y = header_y + header_h / 2
    pdf.drawImage(
        str(asa_logo),
        partners_x,
        center_y - asa_h / 2,
        asa_w,
        asa_h,
        preserveAspectRatio=True,
        mask="auto",
    )
    pdf.drawImage(
        str(uconn_wordmark),
        partners_x + asa_w + partner_gap,
        center_y - uconn_h / 2,
        uconn_w,
        uconn_h,
        preserveAspectRatio=True,
        mask="auto",
    )

    y = header_y - 18
    h = draw_para(pdf, escape_reportlab_text(label), styles["label"], margin_x, y, content_w)
    y -= h + 8
    h = draw_para(pdf, escape_reportlab_text(webinar.title), styles["title"], margin_x, y, content_w)
    y -= h + 15

    row_h = 64
    row_gap = 12
    date_w = 320
    time_w = content_w - date_w - row_gap
    date_time_blocks = [
        (margin_x, date_w, "Date", webinar.date_display, light_blue, blue),
        (margin_x + date_w + row_gap, time_w, "Time", webinar.time, light_gold, gold),
    ]
    for x, width, block_label, value, fill, accent in date_time_blocks:
        pdf.setFillColor(fill)
        pdf.roundRect(x, y - row_h, width, row_h, 7, fill=1, stroke=0)
        pdf.setFillColor(accent)
        pdf.rect(x, y - row_h, 5, row_h, fill=1, stroke=0)
        pdf.setFillColor(muted)
        pdf.setFont("Helvetica-Bold", 9.2)
        pdf.drawString(x + 14, y - 19, block_label.upper())
        pdf.setFillColor(navy)
        pdf.setFont("Helvetica-Bold", 16.4)
        pdf.drawString(x + 14, y - 43, value)
    y -= row_h + 17

    speaker_text_x = margin_x
    if webinar.speaker_image:
        head_x = margin_x
        head_y = y - head_h
        pdf.drawImage(
            str(webinar.speaker_image),
            head_x,
            head_y,
            head_w,
            head_h,
            preserveAspectRatio=True,
            anchor="c",
            mask="auto",
        )
        pdf.setStrokeColor(line)
        pdf.setLineWidth(0.8)
        pdf.rect(head_x, head_y, head_w, head_h, fill=0, stroke=1)
        speaker_text_x = head_x + head_w + speaker_gap
    h1 = draw_para(
        pdf,
        escape_reportlab_text(webinar.speaker),
        styles["speaker"],
        speaker_text_x,
        y - 3,
        speaker_text_w,
    )
    draw_para(
        pdf,
        escape_reportlab_text(webinar.affiliation),
        styles["affiliation"],
        speaker_text_x,
        y - 3 - h1 - 8,
        speaker_text_w,
    )
    y -= speaker_h + 17

    buttons: list[tuple[str, str, colors.Color, colors.Color, colors.Color | None, float]] = []
    if webinar.registration_url:
        buttons.append(("Sign up", webinar.registration_url, blue, colors.white, None, 96))
    buttons.append(("Event website", event_url_value, colors.white, blue, blue, 128))

    x = margin_x
    button_gap = 12
    button_y = y - button_h
    for button_label, url, fill, text_color, stroke, width in buttons:
        draw_button(pdf, button_label, url, x, button_y, width, button_h, fill, text_color, stroke)
        x += width + button_gap
    y -= button_h + 20

    for section_index, section in enumerate(webinar.sections):
        h = draw_para(
            pdf,
            escape_reportlab_text(section.title),
            styles["section"],
            margin_x,
            y,
            content_w,
        )
        y -= h + 7
        for block_index, block in enumerate(section.blocks):
            style_name = block_style_name(section, block)
            block_markup = "- " + block.markup if block.kind == "bullet" else block.markup
            h = draw_para(pdf, block_markup, styles[style_name], margin_x, y, content_w)
            y -= h
            if block_index < len(section.blocks) - 1:
                y -= 8 if block.kind != "bullet" else 5
        if section_index < len(webinar.sections) - 1:
            y -= 17

    y -= 20
    pdf.setStrokeColor(line)
    pdf.setLineWidth(0.7)
    pdf.line(margin_x, y, page_width - margin_x, y)
    y -= 9
    draw_para(pdf, escape_reportlab_text(footer), styles["footer"], margin_x, y, content_w)

    pdf.showPage()
    pdf.save()


def main() -> int:
    args = parse_args()
    webinar_path = args.webinar_markdown.resolve()
    webinar = load_webinar(webinar_path, include_headshot=not args.no_headshot)
    site_url = args.site_url.rstrip("/") + "/"
    event_url_value = event_url(site_url, webinar.permalink, args.event_url)
    output = args.output
    if output is None:
        slug = slug_from_webinar(webinar_path, webinar.permalink)
        output = REPO_ROOT / "output/pdf" / f"{slug}-webinar-flyer.pdf"
    generate_flyer(
        webinar=webinar,
        output=output.resolve(),
        site_url=site_url,
        event_url_value=event_url_value,
        label=args.label,
        footer=args.footer,
        tsc_logo=args.tsc_logo.resolve(),
        asa_logo=args.asa_logo.resolve(),
        uconn_wordmark=args.uconn_wordmark.resolve(),
    )
    print(output.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
