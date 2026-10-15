# Fiona's Bakery: ny webbplats

En ny webbplats för [fionasbakery.se](https://fionasbakery.se) på svenska, byggd som
en statisk sajt för GitHub Pages. Den här versionen är riktning B,
"Varm & modern skandinavisk".

## Struktur

```
brand/BRAND.md                     Varumärket: position, röst, färger, typsnitt
brand/prompts/A-romantisk-elegant.md   Fristående prompt för riktning A (annat repo)
brand/prompts/B-varm-skandinavisk.md   Fristående prompt för riktning B (den här)
DESIGN.md                          Hur varumärket används på webben
src/pages/*.html                   Sidornas innehåll
src/assets/                        CSS, JS, typsnitt, bilder, ikoner
tools/build.py                     Bygger src/ till docs/
docs/                              Färdig sajt som GitHub Pages serverar
```

## Bygga

```sh
pip install pillow
python3 tools/build.py
cd docs && python3 -m http.server 8000   # http://localhost:8000
```

Kör alltid bygget och committa `docs/` efter ändringar i `src/`.

## Publicera på GitHub Pages

1. Settings > Pages > Build and deployment: "Deploy from a branch", branch `main`, mapp `/docs`.
2. När allt ser rätt ut: lägg till domänen `fionasbakery.se` under Custom domain
   (det skapar `docs/CNAME`; lägg även in filen i `src/` eller i bygget så den inte försvinner)
   och peka DNS hos one.com till GitHub Pages enligt
   [GitHub-guiden](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site).
3. Skicka `https://fionasbakery.se/sitemap.xml` till Google Search Console.

Sidorna använder relativa länkar och fungerar därför även på
`https://<användare>.github.io/fionas-bakery/` innan domänen flyttas. Bara 404-sidan
förutsätter den egna domänen.

## Beställningsformuläret

GitHub Pages kan inte ta emot formulär. Utan inställning öppnar formuläret
besökarens e-postprogram med förfrågan ifylld till kontakt@fionasbakery.se.
För att skicka direkt: skapa ett formulär hos till exempel Formspree eller Web3Forms
och lägg in adressen i `data-endpoint` i `src/pages/bestall.html`.

## Att göra innan lansering

- Porträtt av Fiona till "Om Fiona" (se TODO i `src/pages/om-fiona.html`).
- Fler och nyare bilder från Instagram (Instagram blockerade automatisk hämtning).
- Fiona läser igenom texterna, särskilt integritetspolicyn och leveransområdet.
- Riktiga kundcitat, om Fiona har några att dela med lov.
