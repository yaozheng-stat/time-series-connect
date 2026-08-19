# Webinar Flyer Generator

This generator creates a one-page, content-height Time Series Connect webinar flyer from a webinar Markdown file in `_webinars/`.

## Install

```bash
python3 -m pip install -r scripts/requirements-flyers.txt
```

`reportlab` and `pillow` are required to generate the PDF. `pypdf` and `pymupdf` are useful for checking links and rendering a preview during QA.

## Generate A Flyer

```bash
python3 scripts/generate_webinar_flyer.py _webinars/2026-09-28-rebecca-killick.md
```

By default, the output is written to:

```text
output/pdf/<webinar-slug>-webinar-flyer.pdf
```

For example, Rebecca Killick's webinar becomes:

```text
output/pdf/rebecca-killick-webinar-flyer.pdf
```

## Common Options

Use a custom output path:

```bash
python3 scripts/generate_webinar_flyer.py _webinars/2026-10-26-rob-hyndman.md \
  --output output/pdf/rob-hyndman-webinar-flyer.pdf
```

Change the flyer label:

```bash
python3 scripts/generate_webinar_flyer.py _webinars/2026-10-26-rob-hyndman.md \
  --label "Upcoming Webinar"
```

Override the public event URL:

```bash
python3 scripts/generate_webinar_flyer.py _webinars/2026-10-26-rob-hyndman.md \
  --event-url https://yaozheng-stat.github.io/time-series-connect/webinars/rob-hyndman/
```

Generate without a headshot:

```bash
python3 scripts/generate_webinar_flyer.py _webinars/2026-10-26-rob-hyndman.md --no-headshot
```

## Required Webinar Fields

The script reads these fields from the webinar front matter:

```yaml
title: "Webinar title"
speaker: "Speaker Name"
affiliation: "Speaker affiliation"
date: 2026-09-28
permalink: /webinars/speaker-slug/
time: "12:00 PM - 1:30 PM ET"
speaker_image: "/assets/images/speakers/speaker-image.jpg"
registration_url: "https://..."
```

The abstract must appear under a `## Abstract` heading in the Markdown body.

## Template Assets

The default template uses:

```text
assets/images/TSC-logo.jpg
assets/images/ASA-BES-logo.jpg
assets/images/UConn-wordmark.png
```

You can override these with `--tsc-logo`, `--asa-logo`, or `--uconn-wordmark`.
