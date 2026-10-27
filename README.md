# Boland Structures: construction website (portfolio concept)

A 24-page static website for a fictional construction company in Worcester, Western Cape. It's built mobile-first in plain HTML, CSS and JavaScript, with no framework and no dependencies.

## Pages

| Page | File |
|---|---|
| Home | `index.html` |
| Company | `company.html` |
| Services hub + 4 service pages | `services.html`, `services/*.html` |
| Projects listing + 8 case studies | `projects.html`, `projects/*.html` |
| Team | `team.html` |
| Areas hub + 4 town pages | `areas.html`, `areas/*.html` |
| Contact | `contact.html` |
| Quote (4-step form) | `quote.html` |

## Editing

Never edit the built `.html` files directly. They're generated. Edit the source, then rebuild:

```
python build.py
```

| To change… | Edit |
|---|---|
| Header, nav, footer, icons | `src/partials/` |
| Home, Company, Services hub, Contact, Quote | `src/pages/*.html` |
| Service pages | `src/content/services.py` |
| Projects and case studies | `src/content/projects.py` |
| Team, jobs, apprenticeships | `src/content/team.py` |
| Location (town) pages | `src/content/areas.py` |
| Styles | `assets/css/main.css` (colour tokens at the top) |
| Scripts | `assets/js/main.js` (site), `assets/js/forms.js` (forms) |

Python 3 is the only requirement.

## Adding a location page

Add a town to `src/content/areas.py` and rebuild. The page, the hub card, the town links on service and project pages, and the sitemap all update.

Only add a town when you can write content that is true for that town alone: projects built there, local building conditions, its municipality and real FAQs. The test is this: if you swap the town name for another town and the page still reads correctly, it's a doorway page. Google treats those as spam, so don't publish it.

## Run locally

```
python -m http.server 5173
```

Then open http://localhost:5173.

## Images

All photos are Unsplash placeholders. `IMAGE-PROMPTS.md` lists every image slot with its filename, size and a gen-AI prompt. To swap one, save the new image over the old file with the same name; no code changes are needed.

## Forms

The Contact and Quote forms run in **demo mode**: they validate input and show the success screen, but don't send anything. To make them live, add a form endpoint (for example Formspree or Netlify Forms) to each `<form>` in `src/pages/contact.html` and `src/pages/quote.html`, then rebuild:

```html
<form ... data-endpoint="https://formspree.io/f/your-id">
```

## SEO built in

- A unique title, description, canonical URL and Open Graph tags on every page
- Structured data: GeneralContractor (home), Service + FAQPage + BreadcrumbList (service pages), BreadcrumbList (projects), JobPosting (team), ContactPage (contact)
- Each service page targets one local search phrase (see `keyword` in `src/content/services.py`)

- `sitemap.xml` and `robots.txt` are generated on every build

Live at https://boland-structures.netlify.app/. If the domain changes, update `SITE` in `build.py` and rebuild. Every canonical URL, social preview and the sitemap follow it.
