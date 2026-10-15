---
brand: brand/BRAND.md
surface: website (fionasbakery.se)
direction: B "Varm & modern skandinavisk"
---

# DESIGN.md: fionasbakery.se

How the identity in [`brand/BRAND.md`](brand/BRAND.md) is applied to the website.
Direction B. Direction A ("Romantisk & elegant") is specified as a standalone
prompt in [`brand/prompts/A-romantisk-elegant.md`](brand/prompts/A-romantisk-elegant.md).

Design read: local-business marketing site for families, couples and companies in
Malmö, with a warm modern Scandinavian language; native CSS, self-hosted fonts,
no framework. Dials: variance 6, motion 4, density 3.

## Tokens (`src/assets/css/site.css`)

| Role | Light | Dark |
|---|---|---|
| `--bg` page ground | `#fbf7f0` Mjölvit | `#1d1613` |
| `--surface` quiet panels | `#f3eadb` | `#2a201b` |
| `--field` warm color blocks | `#f3d98b` Smörgul | `#3a2d1c` |
| `--ink` text | `#2a201b` Kakao | `#f5ede2` |
| `--muted` secondary text | `#65554b` | `#c9b9aa` |
| `--accent` the only accent | `#a9482a` Terrakotta | `#e3906d` |

Butter yellow is a field color only, never text. One accent per page.

Type: Bricolage Grotesque 750-780 for headings (tight negative tracking),
Hanken Grotesk for body. Fonts are self-hosted (no Google Fonts requests).

Shape: cards 20 px, images 16 px, inputs 12 px, buttons and chips fully pill.

Motion: reveal on scroll (fade + 16 px rise, staggered 70 ms), button press
feedback, image scale on hover. Everything off under `prefers-reduced-motion`.
Hero images never animate, so the largest image paints immediately.

## Components

- Header: sticky, one-line nav, one CTA "Begär offert" (the only CTA label on the site).
- Hero: asymmetric split, main photo plus overlapping inset photo and a price badge.
- Occasion bento: six tiles, mixed sizes, four with photos, one butter field CTA.
- Signature band: butter field with a three-photo collage.
- Steps: three columns with a top rule, numbered by CSS counter.
- Gallery: CSS columns masonry.
- CTA band: terracotta block at the end of each page.
- Order form: labels above fields, inline Swedish errors, conditional delivery address.

## Photography

All photos are Fiona's own, taken from the current site. Cakes that reproduce
other brands' logos or licensed characters are not used.
