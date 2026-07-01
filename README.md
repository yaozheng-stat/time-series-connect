# Time Series Connect — GitHub Pages site

This is a GitHub Pages-ready Jekyll site for Time Series Connect.

## What changed in this version

- The homepage keeps the cleaner future structure, without long event details.
- The visual style is closer to the original Google Sites page: banner image, Google-style typography, blue link/button styling, white sections, and original homepage text.
- Each webinar lives in `_webinars/` as its own Markdown post.
- Upcoming and past webinars are generated from the webinar collection.

## Deploy on GitHub Pages

1. Upload these files to a GitHub repository.
2. In GitHub, go to **Settings → Pages**.
3. Select **Deploy from a branch**.
4. Choose `main` and `/ (root)`.
5. Save and wait for the Pages URL to appear.

## Editing webinars

Duplicate an existing file in `_webinars/`, update the front matter, and add the abstract/materials in Markdown.

## Education Blog workflow

Education posts now live in the `_education/` collection. To add a new post, create a Markdown or HTML file in `_education/` with front matter such as:

```yaml
---
title: "Post title"
date: 2026-07-01
author: "Author name"
summary: "One-sentence summary."
topics:
  - Topic one
  - Topic two
math: true
reading_time: "10 min read"
---
```

The `/education-blog/` page automatically lists all education posts by date. Figures for education posts should be stored under `assets/images/education/<post-slug>/`; downloadable source files can be stored under `assets/downloads/education/<post-slug>/`.
