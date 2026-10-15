# Prompt: Fiona's Bakery website, direction A "Romantisk & elegant"

Build a complete, working prototype of a new website for Fiona's Bakery, a one-person custom-cake studio in Arlöv/Malmö, Sweden. The site is in Swedish, hosted on GitHub Pages, and has two jobs: show off Fiona's work and bring in orders (weddings, children's birthdays, christenings/babyshowers, möhippor, company events and catering). Price positioning: in between, skilled and personal but with open prices, never luxury-distant.

## Design direction A: Romantic & elegant

Visual territory: **a florist's workbench in soft morning light.** Sugar flowers are the hero. The site should feel like a wedding stationery suite: airy, delicate, confident, still welcoming to a parent planning a kids' party.

- Palette: warm white ground (not cream-beige cliché; aim near `#FCFAF7`), deep plum-ink text (`#2E2430`), one accent in dusty rose (`#B0626F`, check AA contrast for text use, darken if needed), sage `#8A9A7E` only as a quiet secondary tint for backgrounds. No gold foil, no glitter.
- Type: an elegant high-contrast serif for headings (choose from Cormorant Garamond, Playfair Display or EB Garamond; NOT Fraunces or Instrument Serif), paired with a clean humanist sans for body (e.g. Hanken Grotesk or Figtree). Use italics of the same serif for emphasis.
- Layout: generous whitespace, asymmetric editorial grid, tall portrait photos, thin hairline dividers, gentle overlaps of image and text. Rounded corners small (4-8 px) or none.
- Motion: slow, soft fade/rise reveals on scroll (400-600 ms), subtle image zoom on hover. Respect reduced motion.
- Logo: an original elegant wordmark "Fiona's Bakery" in the heading serif plus a small monogram "F" framed by a single drawn sugar-flower petal or a simple oval. SVG, works in one color.
- Homepage hero: large portrait photo of the tiered sugar-rose wedding cake, headline "Tårtor som ser ut som festen känns." Wedding page is the most elaborate page; the kids/party page should be warmer and slightly more colourful but stay within the palette.
- Dials: variance 6, motion 4, density 3.

## Business facts (use exactly, do not invent more)

- Name: Fiona's Bakery. Domain: fionasbakery.se
- Fiona: konditor, sugarpaste decorator, cake and sugar-flower designer. One-person business.
- Address (pickup by appointment, no shop): Trossgatan 25, 232 36 Arlöv
- Phone: 073-874 03 78 (tel:+46738740378). Email: kontakt@fionasbakery.se
- Instagram: https://www.instagram.com/fionasbakery/
- Godkänd för F-skatt. Payment: företags-Swish.
- Opening hours: enligt överenskommelse (by agreement). No walk-in.
- Delivery: Malmö with surroundings (Arlöv/Burlöv, Lund, Lomma, Staffanstorp, Vellinge). Further away for a fee, by agreement.
- Lead times: decorated cakes 1-2 weeks; cakes with sugar flowers about 1 month; urgent orders sometimes possible, ask.

## Prices and flavours (current, keep)

- Tårta: 60 kr per bit. Decorations priced by number and complexity.
- Bottnar: vanilj eller choklad.
- Mousse 1: blåbär, hallon, mango, passion, skogsbär, jordgubb, jordgubb/rabarber, pistage (+5 kr/bit).
- Mousse 2: vit chokladmousse, mjölkchokladmousse, mörk chokladmousse, pannacotta, citron, nougat (+5 kr/bit).
- Cupcakes: vanilj- eller chokladkaka, marängsmörkräm.
- Bakelser 1, 25 kr/st (min 12): cake pops, macarons, mini-cupcakes. Logo/theme/special piping +10 kr.
- Bakelser 2, 45 kr/st (min 4): pannacotta/moussebakelse i glas, maränglollipop, mini popsicles, stora cupcakes. Logo/theme +10 kr.
- Bageritårtor, 60 kr/bit: tiramisu, moussetårta, vit choklad-cheesecake (bakad, mördegsbotten), prinsesstårta.

## Photos

Use Fiona's own photos, from the current site (https://fionasbakery.se) and Instagram. Group them:
- Weddings / sugar flowers: tiered white cakes with sugar roses, peonies, cherry blossom; close-ups of sugar flowers.
- Kids' parties: farm-animal cake, cat cake, butterfly cake, teddy-bear babyshower cakes, "It's a boy" cake.
- Bakes / companies: cupcakes with monograms, hot-air-balloon cupcakes, macarons, cake cut open showing layers.
Do NOT feature cakes that reproduce other brands' logos or licensed characters (Dior, Gucci, Louis Vuitton, Burberry, Jägermeister, Nintendo, Paw Patrol) in hero or category images.
Convert to WebP in 640 px and 1200 px widths, use srcset, width/height attributes, lazy-load below the fold. Every image gets a descriptive Swedish alt text.

## Language and voice

- All visible copy in Swedish. First person singular: Fiona speaks ("jag bakar", "berätta om festen").
- Warm, clear, short sentences. Concrete flavour and price facts. No exclamation marks in headings.
- Never fabricate reviews, ratings, years of experience or counts.
- Never use em-dashes in copy.

## Information architecture (Swedish slugs, keep it to these pages)

1. `/` Hem: hero, occasions overview, sugar-flower signature, how ordering works (3 steps), selected work, short about, delivery area, order CTA.
2. `/brollopstartor/` Bröllopstårtor & sockerblommor i Malmö.
3. `/tartor-till-fest/` Födelsedag, barnkalas, dop, babyshower, möhippa.
4. `/foretag-och-catering/` Fika, logo-cupcakes, event, catering.
5. `/priser/` Priser & smaker, including an FAQ (lead time, delivery, allergies, payment, how many slices).
6. `/om-fiona/` About Fiona.
7. `/bestall/` Offertförfrågan (the order form).
8. `/integritet/` Integritetspolicy (short; explains how form data is used). Plus a branded `404.html`.

One primary CTA label everywhere: "Begär offert" (links to /bestall/).

## Order form (improved from today's 5-field form)

Fields, labels above inputs, inline Swedish error messages, no placeholder-as-label:
- Tillfälle (select: Bröllop, Födelsedag / barnkalas, Dop / babyshower, Möhippa / fest, Företag / event, Annat)
- Datum för festen (date, required) with a gentle warning if fewer than 7 days away (or 30 days for weddings)
- Antal gäster / bitar (number, required)
- Hämtning eller leverans (radio; if leverans, show Leveransadress / ort)
- Önskade smaker (optional free text, with link to /priser/#smaker)
- Inspiration (optional URL to Instagram/Pinterest) + Meddelande (textarea)
- Namn, Telefon, E-post (required), consent checkbox linking to /integritet/
Pre-select Tillfälle from a `?tillfalle=` query parameter so each occasion page can deep-link.
Submission: GitHub Pages is static. Support a configurable endpoint (Formspree/Web3Forms, `data-endpoint` attribute) via fetch POST; when no endpoint is configured, fall back to opening the visitor's mail app with a pre-filled email to kontakt@fionasbakery.se. Show a proper success state.

## Local SEO (required)

- `<html lang="sv">`, unique `<title>` and meta description per page, written for searches like "bröllopstårta Malmö", "tårta beställa Malmö", "barnkalas tårta Malmö", "cupcakes företag Malmö", "sockerblommor tårta".
- One H1 per page containing the main keyword naturally. Logical H2/H3.
- Canonical URLs on https://fionasbakery.se/, Open Graph + Twitter card tags with a real cake photo.
- JSON-LD: `Bakery` (LocalBusiness) with name, address, telephone, email, url, image, priceRange "$$", areaServed list, sameAs Instagram. Leave out `geo` unless the coordinates are verified. `FAQPage` on /priser/. `BreadcrumbList` on subpages.
- `sitemap.xml`, `robots.txt`, descriptive Swedish alt text, internal links between occasion pages and /priser/ and /bestall/.
- Fast: self-hosted fonts (no Google Fonts CDN for GDPR), WebP images, no framework runtime, Lighthouse 95+.

## Tech

- Static site for GitHub Pages, no framework required. Plain HTML/CSS/JS, optional tiny build script (Python or Node) to share header/footer across pages; output folder deployed by GitHub Actions or served from `/docs`.
- Self-hosted variable fonts (Fontsource packages). Icons from Phosphor (copied SVGs, one weight). No hand-drawn icons.
- Light and dark mode via `prefers-color-scheme`. Respect `prefers-reduced-motion`.
- Accessibility: WCAG 2.2 AA, skip link, visible focus, active nav state, keyboard-friendly mobile menu.
- New logo: design an original SVG wordmark + simple mark (no existing logo to keep). Provide favicon.svg.
