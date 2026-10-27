"""
Boland Structures static site builder.

Run:  python build.py

Builds every page from shared partials so the header, nav, footer and icon
set live in one place:

  src/partials/   head, sprite, header, footer (use {{root}} for relative paths)
  src/pages/      page bodies (<main>) with a <!--meta {...} --> JSON header
  src/content/    data for templated pages (service detail pages)

Output goes to the project root (index.html, company.html, ...) and to
services/ for the individual service pages.
"""
import html
import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
SITE = "https://bolandstructures.co.za/"

BUSINESS = {
    "@type": "GeneralContractor",
    "@id": SITE + "#business",
    "name": "Boland Structures",
    "url": SITE,
    "logo": SITE + "assets/img/favicon.svg",
    "image": SITE + "assets/img/hero-excavator.jpg",
    "telephone": "+27233470000",
    "email": "hello@bolandstructures.co.za",
    "foundingDate": "2004",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "18 Durban Street",
        "addressLocality": "Worcester",
        "addressRegion": "Western Cape",
        "postalCode": "6850",
        "addressCountry": "ZA",
    },
    "geo": {"@type": "GeoCoordinates", "latitude": -33.6465, "longitude": 19.4485},
    "openingHours": "Mo-Fr 07:00-17:00",
    "areaServed": ["Worcester", "Rawsonville", "De Doorns", "Robertson", "Ceres",
                   "Tulbagh", "Wellington", "Paarl", "Breede River Valley", "Boland"],
}


def read(path):
    return (SRC / path).read_text(encoding="utf-8")


PARTS = {name: read(f"partials/{name}.html") for name in ("head", "sprite", "header", "footer")}


def jsonld(data):
    payload = json.dumps(data, ensure_ascii=False, indent=2)
    return f'  <script type="application/ld+json">\n{payload}\n  </script>\n'


def render(main, meta, out_path):
    depth = out_path.count("/")
    root = "../" * depth
    nav = meta["nav"]
    page = PARTS["head"] + PARTS["sprite"] + "\n" + PARTS["header"] + main.strip() + "\n" + PARTS["footer"]

    def current(m):
        key = m.group(1)
        if key == nav:
            return ' aria-current="page"'
        if key == "services" and nav.startswith("svc-"):
            return ' aria-current="true"'
        if key == "projects" and nav == "project-detail":
            return ' aria-current="true"'
        return ""

    page = re.sub(r"\{\{cur:([\w-]+)\}\}", current, page)
    values = {
        "title": html.escape(meta["title"]),
        "description": html.escape(meta["description"]),
        "preload": meta["preload"],
        "path": meta["path"],
        "site": SITE,
        "head_extra": meta.get("head_extra", ""),
        "scripts": "".join(f'<script src="{root}{src}"></script>\n' for src in meta.get("scripts", [])),
        "root": root,
    }
    for key, val in values.items():
        page = page.replace("{{" + key + "}}", val)
    leftover = re.findall(r"\{\{[^}]+\}\}", page)
    if leftover:
        raise ValueError(f"{out_path}: unreplaced placeholders {set(leftover)}")
    target = ROOT / out_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(page, encoding="utf-8")
    print("built", out_path)


# ---------------------------------------------------------------------------
# Content
# ---------------------------------------------------------------------------
def load(name):
    spec = importlib.util.spec_from_file_location(name, SRC / "content" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


SERVICES_MOD = load("services")
PROJECTS_MOD = load("projects")
SERVICES = SERVICES_MOD.SERVICES
AREAS = SERVICES_MOD.AREAS
PROJECTS = PROJECTS_MOD.PROJECTS
PROJECTS_BY_KEY = {p["key"]: p for p in PROJECTS}
SERVICE_NAMES = {s["slug"]: s["short"] for s in SERVICES}


def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s)


def project_card(p, show_services=False, filterable=False):
    """Project card used on the home page, service pages and the projects listing."""
    R = "{{root}}"
    services = ""
    if show_services:
        services = '<p class="project-card__services">' + " · ".join(SERVICE_NAMES[s] for s in p["services"]) + "</p>"
    attr = f' data-sector="{p["sector"]}"' if filterable else ""
    return f'''
        <a class="project-card" href="{R}projects/{p["slug"]}.html"{attr}>
          <img src="{R}assets/img/projects/{p["slug"]}-cover.jpg" alt="{p["cover_alt"]}" width="1600" height="1200" loading="lazy">
          <div class="project-card__body">
            <span class="project-card__tag">{p["sector"]}</span>
            <h3>{p["name"]}</h3>
            <p class="project-card__meta">{p["location"]} · {p["size"]} · {p["year"]}</p>{services}
          </div>
        </a>'''


def expand_project_tokens(main):
    """Replace {{projects:key1,key2}} in page bodies with rendered cards."""
    return re.sub(r"\{\{projects:([\w,]+)\}\}",
                  lambda m: "".join(project_card(PROJECTS_BY_KEY[k]) for k in m.group(1).split(",")) + "\n      ",
                  main)


# ---------------------------------------------------------------------------
# Plain pages
# ---------------------------------------------------------------------------
def build_pages():
    for src in sorted((SRC / "pages").glob("*.html")):
        text = src.read_text(encoding="utf-8")
        m = re.match(r"<!--meta (\{.*?\}) -->\n", text, re.S)
        meta = json.loads(m.group(1))
        main = expand_project_tokens(text[m.end():])
        if src.stem == "index":
            meta["head_extra"] = jsonld({"@context": "https://schema.org", **BUSINESS})
        elif meta.get("schema") == "contact":
            meta["head_extra"] = jsonld({"@context": "https://schema.org", "@type": "ContactPage",
                                         "url": SITE + "contact.html", "mainEntity": BUSINESS})
        elif meta.get("schema") == "quote":
            meta["head_extra"] = jsonld({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE},
                {"@type": "ListItem", "position": 2, "name": "Get a quote", "item": SITE + "quote.html"}]})
        render(main, meta, src.name)


# ---------------------------------------------------------------------------
# Service detail pages
# ---------------------------------------------------------------------------


def check_item(text):
    return f'<li><svg aria-hidden="true"><use href="#i-check"/></svg>{text}</li>'


def service_main(s, all_services, areas):
    R = "{{root}}"
    facts = "".join(f"<div><dt>{dt}</dt><dd>{dd}</dd></div>" for dt, dd in s["facts"])
    paras = "".join(f"<p>{p}</p>" for p in s["intro_paras"])
    types = "".join(
        f'''
        <article class="type-card reveal">
          <span class="type-card__num">{i:02d}</span>
          <h3>{t}</h3>
          <p>{p}</p>
        </article>''' for i, (t, p) in enumerate(s["types"], 1))
    steps = "".join(f"<li class=\"step\"><h3>{h}</h3><p>{p}</p></li>" for h, p in s["steps"])
    factors = "".join(f"<li><strong>{h}</strong><span>{p}</span></li>" for h, p in s["factors"])
    area_items = "".join(
        f'<li{" class=\"is-base\"" if a == "Worcester" else ""}><svg aria-hidden="true"><use href="#i-pin"/></svg>{a}</li>'
        for a in areas)
    proj_cards = "".join(project_card(PROJECTS_BY_KEY[k]) for k in s["projects"])
    faqs = "".join(
        f"""
        <details{" open" if i == 0 else ""}>
          <summary>{q}</summary>
          <p>{a}</p>
        </details>""" for i, (q, a) in enumerate(s["faqs"]))
    related = "".join(
        f'''
        <a class="value-card reveal" href="{R}services/{o["slug"]}.html">
          <svg aria-hidden="true"><use href="#{o["icon"]}"/></svg>
          <h3>{o["short"]}</h3>
          <p>{o["card"]}</p>
          <span class="text-link">Learn more <svg><use href="#i-arrow"/></svg></span>
        </a>''' for o in all_services if o["slug"] != s["slug"])

    return f'''<main id="main">

  <!-- Page hero -->
  <section class="page-hero" aria-labelledby="page-title">
    <div class="page-hero__inner">
      <div class="page-hero__bg" style="--focus: {s.get("hero_focus", "50% 50%")}" aria-hidden="true">
        <img src="{R}assets/img/{s["hero_img"]}" alt="" width="1920" height="800" fetchpriority="high">
      </div>
      <div class="container">
        <nav class="breadcrumb" aria-label="Breadcrumb">
          <ol>
            <li><a href="{R}index.html">Home</a></li>
            <li><a href="{R}services.html">Services</a></li>
            <li><span aria-current="page">{s["short"]}</span></li>
          </ol>
        </nav>
        <h1 class="page-hero__title" id="page-title">{s["h1"]}</h1>
        <p class="page-hero__lead">{s["hero_lead"]}</p>
      </div>
    </div>
  </section>

  <!-- Answer / intro -->
  <section class="section" aria-labelledby="intro-title">
    <div class="container split">
      <div class="split__media reveal">
        <img src="{R}assets/img/{s["intro_img"]}" alt="{s["intro_alt"]}" width="1200" height="900" loading="lazy">
        <div class="split__badge"><strong>5 yr</strong><span>Workmanship guarantee</span></div>
      </div>
      <div class="split__body reveal">
        <span class="eyebrow">{s["eyebrow"]}</span>
        <h2 class="section-title" id="intro-title">{s["intro_h2"]}</h2>
        <p class="lede">{s["lede"]}</p>
        {paras}
        <dl class="facts">{facts}</dl>
        <div class="svc-detail__actions">
          <a class="btn btn--rust" href="{R}quote.html?service={s["slug"]}">{s["quote_label"]} <svg><use href="#i-arrow"/></svg></a>
          <a class="text-link" href="tel:+27233470000">Call +27 23 347 0000 <svg><use href="#i-arrow"/></svg></a>
        </div>
      </div>
    </div>
  </section>

  <!-- Types of work -->
  <section class="section process" aria-labelledby="types-title">
    <div class="container">
      <h2 class="section-title section-title--center reveal" id="types-title">{s["types_title"]}</h2>
      <p class="section-lead section-lead--center reveal">{s["types_lead"]}</p>
      <div class="type-grid">{types}
      </div>
    </div>
  </section>

  <!-- Process -->
  <section class="section" aria-labelledby="process-title">
    <div class="container">
      <h2 class="section-title section-title--center reveal" id="process-title">{s["process_title"]}</h2>
      <p class="section-lead section-lead--center reveal">{s["process_lead"]}</p>
      <ol class="process__grid reveal" style="list-style:none;padding:0;margin-bottom:0">{steps}</ol>
    </div>
  </section>

  <!-- Cost factors -->
  <section class="section process" aria-labelledby="cost-title">
    <div class="container split split--reverse">
      <div class="split__media reveal">
        <img src="{R}assets/img/{s["cost_img"]}" alt="{s["cost_alt"]}" width="1200" height="900" loading="lazy">
      </div>
      <div class="split__body reveal">
        <span class="eyebrow">Costs &amp; timing</span>
        <h2 class="section-title" id="cost-title">{s["cost_h2"]}</h2>
        <p>{s["cost_intro"]}</p>
        <ol class="factors">{factors}</ol>
      </div>
    </div>
  </section>

  <!-- Areas -->
  <section class="band" aria-labelledby="areas-title">
    <div class="band__bg" aria-hidden="true"><img src="{R}assets/img/band-dusk.jpg" alt="" width="1920" height="900" loading="lazy"></div>
    <div class="container band__inner">
      <div class="band__top reveal">
        <div>
          <span class="band__rule"></span>
          <h2 class="band__title" id="areas-title">Areas <span>we serve</span></h2>
          <p class="band__sub">{s["areas_sub"]}</p>
        </div>
      </div>
      <p class="areas__intro reveal">{s["areas_intro"]}</p>
      <ul class="areas reveal">{area_items}</ul>
    </div>
  </section>

  <!-- Related projects -->
  <section class="section" aria-labelledby="projects-title">
    <div class="container">
      <div class="projects__head reveal">
        <div>
          <span class="eyebrow">Recent work</span>
          <h2 class="section-title" id="projects-title" style="margin-top:12px">{s["projects_title"]}</h2>
        </div>
        <a class="text-link" href="{R}projects.html">All projects <svg><use href="#i-arrow"/></svg></a>
      </div>
      <div class="projects__grid projects__grid--three reveal">{proj_cards}
      </div>
    </div>
  </section>

  <!-- FAQ -->
  <section class="section process" aria-labelledby="faq-title">
    <div class="container">
      <h2 class="section-title section-title--center reveal" id="faq-title">{s["faq_title"]}</h2>
      <div class="faq reveal">{faqs}
      </div>
    </div>
  </section>

  <!-- Related services -->
  <section class="section" aria-labelledby="related-title">
    <div class="container">
      <h2 class="section-title section-title--center reveal" id="related-title">Other <span>services</span></h2>
      <div class="value-grid value-grid--three">{related}
      </div>
    </div>
  </section>

  <!-- CTA -->
  <section class="cta" aria-labelledby="cta-title">
    <div class="cta__bg" aria-hidden="true"><img src="{R}assets/img/cta-cranes.jpg" alt="" width="1920" height="900" loading="lazy"></div>
    <div class="container cta__inner">
      <div>
        <h2 id="cta-title">{s["cta_h2"]}</h2>
        <p>{s["cta_p"]}</p>
      </div>
      <div class="cta__actions">
        <a class="btn btn--navy" href="{R}quote.html?service={s["slug"]}">{s["quote_label"]} <svg><use href="#i-arrow"/></svg></a>
        <a class="btn btn--ghost" href="tel:+27233470000">Call us</a>
      </div>
    </div>
  </section>
</main>'''


def service_schema(s, areas):
    url = f"{SITE}services/{s['slug']}.html"
    return {
        "@context": "https://schema.org",
        "@graph": [
            BUSINESS,
            {
                "@type": "Service",
                "@id": url + "#service",
                "name": strip_tags(s["h1"]),
                "serviceType": s["service_type"],
                "description": s["description"],
                "url": url,
                "provider": {"@id": BUSINESS["@id"]},
                "areaServed": [{"@type": "City", "name": a} for a in areas],
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE},
                    {"@type": "ListItem", "position": 2, "name": "Services", "item": SITE + "services.html"},
                    {"@type": "ListItem", "position": 3, "name": s["short"], "item": url},
                ],
            },
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {"@type": "Question", "name": q,
                     "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}}
                    for q, a in s["faqs"]
                ],
            },
        ],
    }


def build_services():
    services, areas = SERVICES, AREAS
    for s in services:
        meta = {
            "title": s["title"],
            "description": s["description"],
            "preload": "assets/img/" + s["hero_img"],
            "nav": "svc-" + s["slug"],
            "path": f"services/{s['slug']}.html",
            "head_extra": jsonld(service_schema(s, areas)),
        }
        render(service_main(s, services, areas), meta, meta["path"])


# ---------------------------------------------------------------------------
# Projects: listing + detail pages
# ---------------------------------------------------------------------------
def cta_block(h2, p, label, href):
    R = "{{root}}"
    return f'''
  <section class="cta" aria-labelledby="cta-title">
    <div class="cta__bg" aria-hidden="true"><img src="{R}assets/img/cta-cranes.jpg" alt="" width="1920" height="900" loading="lazy"></div>
    <div class="container cta__inner">
      <div>
        <h2 id="cta-title">{h2}</h2>
        <p>{p}</p>
      </div>
      <div class="cta__actions">
        <a class="btn btn--navy" href="{href}">{label} <svg><use href="#i-arrow"/></svg></a>
        <a class="btn btn--ghost" href="tel:+27233470000">Call us</a>
      </div>
    </div>
  </section>'''


def projects_listing_main():
    R = "{{root}}"
    counts = {s: sum(p["sector"] == s for p in PROJECTS) for s in PROJECTS_MOD.SECTORS}
    buttons = f'<button class="filter" type="button" data-filter="all" aria-pressed="true">All <span class="filter__count">{len(PROJECTS)}</span></button>'
    buttons += "".join(
        f'<button class="filter" type="button" data-filter="{s}" aria-pressed="false">{s} <span class="filter__count">{n}</span></button>'
        for s, n in counts.items())
    cards = "".join(project_card(p, show_services=True, filterable=True) for p in PROJECTS)
    total_m2 = sum(int(p["size"].split(" m²")[0].replace(" ", "")) for p in PROJECTS)
    return f'''<main id="main">

  <!-- Page hero -->
  <section class="page-hero" aria-labelledby="page-title">
    <div class="page-hero__inner">
      <div class="page-hero__bg" style="--focus: 50% 40%" aria-hidden="true">
        <img src="{R}assets/img/page-hero-projects.jpg" alt="" width="1920" height="800" fetchpriority="high">
      </div>
      <div class="container">
        <nav class="breadcrumb" aria-label="Breadcrumb">
          <ol>
            <li><a href="{R}index.html">Home</a></li>
            <li><span aria-current="page">Projects</span></li>
          </ol>
        </nav>
        <h1 class="page-hero__title" id="page-title">Our <span>projects</span></h1>
        <p class="page-hero__lead">Cellars, homes, packhouses, schools and business parks we've built across the Boland and Breede River Valley.</p>
      </div>
    </div>
  </section>

  <!-- Listing -->
  <section class="section" aria-labelledby="listing-title">
    <div class="container">
      <h2 class="section-title section-title--center reveal" id="listing-title">Built <span>by us</span></h2>
      <p class="section-lead section-lead--center reveal">A selection of {len(PROJECTS)} recent projects from more than 340 completed since 2004. Filter by sector or open a project for the full story.</p>
      <div class="filters" role="group" aria-label="Filter projects by sector" data-filters>{buttons}</div>
      <p class="filter-status" aria-live="polite"></p>
      <div class="project-grid">{cards}
      </div>
    </div>
  </section>

  <!-- Stats band -->
  <section class="band" aria-labelledby="band-title">
    <div class="band__bg" aria-hidden="true"><img src="{R}assets/img/band-dusk.jpg" alt="" width="1920" height="900" loading="lazy"></div>
    <div class="container band__inner">
      <div class="band__top reveal">
        <div>
          <span class="band__rule"></span>
          <h2 class="band__title" id="band-title">Building <span>better</span></h2>
          <p class="band__sub">From the ground up</p>
        </div>
        <p class="band__words"><span>Quality</span><span>People</span><span>Progress</span></p>
      </div>
      <div class="stats reveal">
        <div class="stat"><div class="stat__num"><span data-count="340">0</span><sup>+</sup></div><div class="stat__label">Projects completed since 2004</div></div>
        <div class="stat"><div class="stat__num"><span data-count="{total_m2}">0</span><sup>m²</sup></div><div class="stat__label">Built across the projects on this page</div></div>
        <div class="stat"><div class="stat__num"><span data-count="96">0</span><sup>%</sup></div><div class="stat__label">Delivered on or before deadline</div></div>
        <div class="stat"><div class="stat__num"><span data-count="12">0</span></div><div class="stat__label">Boland towns we've built in</div></div>
      </div>
    </div>
  </section>
{cta_block("Your project could be next", "Tell us what you want to build and get a fixed-price quote within 5 working days.", "Get a quote", R + "quote.html")}
</main>'''


def project_main(p, prev_p, next_p):
    R = "{{root}}"
    slug = p["slug"]
    services_links = ", ".join(f'<a href="{R}services/{s}.html">{SERVICE_NAMES[s]}</a>' for s in p["services"])
    facts = [("Sector", p["sector"]), ("Location", p["location"]), ("Size", p["size"]),
             ("Duration", p["duration"]), ("Completed", p["year"]), ("Services", services_links)]
    facts_html = "".join(f"<div><dt>{dt}</dt><dd>{dd}</dd></div>" for dt, dd in facts)
    results = "".join(
        f'<div class="stat"><div class="stat__num">{n}</div><div class="stat__label">{label}</div></div>'
        for n, label in p["results"])
    gallery = "".join(
        f'''
        <a class="gallery__item" href="{R}assets/img/projects/{slug}-{i}.jpg" data-lightbox>
          <img src="{R}assets/img/projects/{slug}-{i}.jpg" alt="{alt}" width="1200" height="900" loading="lazy">
        </a>''' for i, alt in enumerate(p["gallery_alts"], 1))
    q_text, q_name, q_role = p["quote"]
    initials = "".join(w[0] for w in q_name.replace("Dr ", "").split()[:2])
    used = [s for s in SERVICES if s["slug"] in p["services"]]
    service_cards = "".join(
        f'''
        <a class="value-card reveal" href="{R}services/{s["slug"]}.html">
          <svg aria-hidden="true"><use href="#{s["icon"]}"/></svg>
          <h3>{s["short"]}</h3>
          <p>{s["card"]}</p>
          <span class="text-link">Learn more <svg><use href="#i-arrow"/></svg></span>
        </a>''' for s in used)
    grid_mod = {2: " value-grid--two", 3: " value-grid--three"}.get(len(used), "")

    return f'''<main id="main">

  <!-- Page hero -->
  <section class="page-hero" aria-labelledby="page-title">
    <div class="page-hero__inner">
      <div class="page-hero__bg" aria-hidden="true">
        <img src="{R}assets/img/projects/{slug}-cover.jpg" alt="" width="1600" height="1200" fetchpriority="high">
      </div>
      <div class="container">
        <nav class="breadcrumb" aria-label="Breadcrumb">
          <ol>
            <li><a href="{R}index.html">Home</a></li>
            <li><a href="{R}projects.html">Projects</a></li>
            <li><span aria-current="page">{p["name"]}</span></li>
          </ol>
        </nav>
        <span class="project-card__tag page-hero__tag">{p["sector"]}</span>
        <h1 class="page-hero__title" id="page-title">{p["name"]}</h1>
        <p class="page-hero__lead">{p["summary"]}</p>
      </div>
    </div>
  </section>

  <!-- Key facts -->
  <section class="section" style="padding-bottom:0" aria-label="Project facts">
    <div class="container"><dl class="project-facts reveal">{facts_html}</dl></div>
  </section>

  <!-- Story -->
  <section class="section" aria-labelledby="story-title">
    <div class="container split">
      <div class="split__media reveal">
        <img src="{R}assets/img/projects/{slug}-cover.jpg" alt="{p["cover_alt"]}" width="1600" height="1200" loading="lazy">
        <div class="split__badge"><strong>{p["year"]}</strong><span>Completed</span></div>
      </div>
      <div class="split__body reveal">
        <span class="eyebrow">Case study</span>
        <h2 class="section-title" id="story-title">The <span>project</span></h2>
        <h3 class="sub">The brief</h3>
        <p>{p["brief"]}</p>
        <h3 class="sub">The challenge</h3>
        <p>{p["challenge"]}</p>
        <h3 class="sub">Our solution</h3>
        <p>{p["solution"]}</p>
      </div>
    </div>
  </section>

  <!-- Results -->
  <section class="band" aria-labelledby="results-title">
    <div class="band__bg" aria-hidden="true"><img src="{R}assets/img/band-dusk.jpg" alt="" width="1920" height="900" loading="lazy"></div>
    <div class="container band__inner">
      <div class="band__top reveal">
        <div>
          <span class="band__rule"></span>
          <h2 class="band__title" id="results-title">The <span>results</span></h2>
          <p class="band__sub">{p["location"]} · {p["year"]}</p>
        </div>
      </div>
      <div class="stats stats--three reveal">{results}</div>
    </div>
  </section>

  <!-- Gallery + quote -->
  <section class="section" aria-labelledby="gallery-title">
    <div class="container">
      <h2 class="section-title section-title--center reveal" id="gallery-title">On <span>site</span></h2>
      <div class="gallery reveal">{gallery}
      </div>
      <figure class="quote-card quote-single reveal">
        <span class="quote-card__mark" aria-hidden="true"><svg><use href="#i-quote"/></svg></span>
        <blockquote>{q_text}</blockquote>
        <figcaption><span class="quote-card__avatar" aria-hidden="true">{initials}</span><div><cite>{q_name}</cite><span>{q_role}</span></div></figcaption>
      </figure>
    </div>
  </section>

  <!-- Services used -->
  <section class="section process" aria-labelledby="used-title">
    <div class="container">
      <h2 class="section-title section-title--center reveal" id="used-title">Services <span>on this project</span></h2>
      <div class="value-grid{grid_mod}">{service_cards}
      </div>
    </div>
  </section>

  <!-- Previous / next -->
  <nav class="pager" aria-label="More projects">
    <a class="pager__prev" href="{R}projects/{prev_p["slug"]}.html"><svg aria-hidden="true"><use href="#i-chev-l"/></svg><div><span>Previous project</span><strong>{prev_p["name"]}</strong></div></a>
    <a class="pager__next" href="{R}projects/{next_p["slug"]}.html"><div><span>Next project</span><strong>{next_p["name"]}</strong></div><svg aria-hidden="true"><use href="#i-chev-r"/></svg></a>
  </nav>
{cta_block("Planning something similar?", "Tell us about your project and get a fixed-price quote within 5 working days.", "Get a quote", R + "quote.html")}
</main>

<dialog class="lightbox" id="lightbox" aria-label="Project photo">
  <figure>
    <img src="" alt="">
    <figcaption><span class="lightbox__count"></span><span class="lightbox__caption"></span></figcaption>
  </figure>
  <button class="lightbox__btn lightbox__close" type="button" aria-label="Close">&times;</button>
  <button class="lightbox__btn lightbox__prev" type="button" aria-label="Previous photo"><svg><use href="#i-chev-l"/></svg></button>
  <button class="lightbox__btn lightbox__next" type="button" aria-label="Next photo"><svg><use href="#i-chev-r"/></svg></button>
</dialog>'''


def build_projects():
    breadcrumb = lambda items: {
        "@type": "BreadcrumbList",
        "itemListElement": [{"@type": "ListItem", "position": i, "name": n, "item": u}
                            for i, (n, u) in enumerate(items, 1)],
    }
    render(projects_listing_main(), {
        "title": "Construction Projects in Worcester & the Boland | Boland Structures",
        "description": "Wine cellars, homes, packhouses, schools, clinics and business parks built by Boland Structures across Worcester and the Breede River Valley.",
        "preload": "assets/img/page-hero-projects.jpg",
        "nav": "projects",
        "path": "projects.html",
        "head_extra": jsonld({"@context": "https://schema.org", **breadcrumb(
            [("Home", SITE), ("Projects", SITE + "projects.html")])}),
    }, "projects.html")

    n = len(PROJECTS)
    for i, p in enumerate(PROJECTS):
        path = f"projects/{p['slug']}.html"
        render(project_main(p, PROJECTS[i - 1], PROJECTS[(i + 1) % n]), {
            "title": f"{p['name']}, {p['location']} | Boland Structures Projects",
            "description": p["summary"] + f" A {p['sector'].lower()} project by Boland Structures in {p['location']}.",
            "preload": f"assets/img/projects/{p['slug']}-cover.jpg",
            "nav": "project-detail",
            "path": path,
            "head_extra": jsonld({"@context": "https://schema.org", **breadcrumb(
                [("Home", SITE), ("Projects", SITE + "projects.html"), (p["name"], SITE + path)])}),
        }, path)


# ---------------------------------------------------------------------------
# Team page
# ---------------------------------------------------------------------------
def team_main(t):
    from urllib.parse import quote
    R = "{{root}}"
    leaders = "".join(
        f'''
        <article class="leader reveal">
          <div class="leader__media"><img src="{R}assets/img/{l["img"]}" alt="{l["img_alt"]}" width="600" height="750" loading="lazy"></div>
          <div class="leader__body">
            <h3>{l["name"]}</h3>
            <p class="leader__role">{l["role"]}</p>
            <p class="leader__creds">{l["credentials"]}</p>
            <p>{l["bio"]}</p>
            <a class="leader__link" href="mailto:{l["email"]}"><svg aria-hidden="true"><use href="#i-mail"/></svg>{l["email"]}</a>
          </div>
        </article>''' for l in t.LEADERS)
    people = "".join(
        f'''
        <article class="person reveal">
          <div class="person__media"><img src="{R}assets/img/team/{p["slug"]}.jpg" alt="{p["img_alt"]}" width="600" height="750" loading="lazy"></div>
          <div class="person__body">
            <h3>{p["name"]}</h3>
            <p class="person__role">{p["role"]}</p>
            <p class="person__creds">{p["credentials"]}</p>
            <p class="person__focus">{p["focus"]}</p>
          </div>
        </article>''' for p in t.PEOPLE)
    total = sum(int(n) for n, _, _ in t.DEPARTMENTS)
    depts = "".join(
        f'<div class="stat"><div class="stat__num"><span data-count="{n}">0</span></div><div class="stat__label"><strong style="color:#fff;display:block">{name}</strong>{desc}</div></div>'
        for n, name, desc in t.DEPARTMENTS)
    points = "".join(check_item(p) for p in t.APPRENTICE_POINTS)
    jobs = "".join(
        f'''
        <details class="job">
          <summary><span class="job__title">{j["title"]}</span><span class="job__meta"><span>{j["type"]}</span><span>{j["location"]}</span></span></summary>
          <div class="job__body">
            <p>{j["summary"]}</p>
            <ul class="checklist">{"".join(check_item(r) for r in j["requirements"])}</ul>
            <a class="btn btn--rust" href="mailto:{t.CAREERS_EMAIL}?subject={quote("Application: " + j["title"])}">Apply for this role <svg><use href="#i-arrow"/></svg></a>
          </div>
        </details>''' for j in t.JOBS)

    return f'''<main id="main">

  <!-- Page hero -->
  <section class="page-hero" aria-labelledby="page-title">
    <div class="page-hero__inner">
      <div class="page-hero__bg" style="--focus: 50% 40%" aria-hidden="true">
        <img src="{R}assets/img/page-hero-team.jpg" alt="" width="1920" height="800" fetchpriority="high">
      </div>
      <div class="container">
        <nav class="breadcrumb" aria-label="Breadcrumb">
          <ol>
            <li><a href="{R}index.html">Home</a></li>
            <li><span aria-current="page">Team</span></li>
          </ol>
        </nav>
        <h1 class="page-hero__title" id="page-title">The people <span>behind the build</span></h1>
        <p class="page-hero__lead">{total} builders, engineers, planners and safety specialists, most of whom live within 40 km of our Worcester yard.</p>
      </div>
    </div>
  </section>

  <!-- Intro -->
  <section class="section" aria-labelledby="intro-title">
    <div class="container split">
      <div class="split__media reveal">
        <img src="{R}assets/img/about-team.jpg" alt="Boland Structures site crew together on a cleared building plot" width="1200" height="900" loading="lazy">
        <div class="split__badge"><strong>{total}</strong><span>People on our team</span></div>
      </div>
      <div class="split__body reveal">
        <span class="eyebrow">Our team</span>
        <h2 class="section-title" id="intro-title">Local crews, <span>one standard</span></h2>
        <p class="lede">Every Boland Structures project is built by our own people, not a chain of subcontractors you've never met.</p>
        <p>Our crews live in Worcester, Rawsonville, De Doorns and Robertson. They build in the towns they live in, so they care about doing it properly. The average crew member has been with us for nine years.</p>
        <dl class="facts">
          <div><dt>Live locally</dt><dd>91%</dd></div>
          <div><dt>Average tenure</dt><dd>9 years</dd></div>
          <div><dt>Lost-time injuries</dt><dd>0 in 2025</dd></div>
        </dl>
      </div>
    </div>
  </section>

  <!-- Leadership -->
  <section class="section process" aria-labelledby="leaders-title">
    <div class="container">
      <h2 class="section-title section-title--center reveal" id="leaders-title">Our <span>leadership</span></h2>
      <p class="section-lead section-lead--center reveal">The three people who sign off on every Boland Structures project.</p>
      <div class="leaders">{leaders}
      </div>
    </div>
  </section>

  <!-- Key people -->
  <section class="section" aria-labelledby="people-title">
    <div class="container">
      <h2 class="section-title section-title--center reveal" id="people-title">Who you'll <span>work with</span></h2>
      <p class="section-lead section-lead--center reveal">The planners, engineers and site managers who run your project day to day.</p>
      <div class="people">{people}
      </div>
    </div>
  </section>

  <!-- Departments -->
  <section class="band" aria-labelledby="band-title">
    <div class="band__bg" aria-hidden="true"><img src="{R}assets/img/band-dusk.jpg" alt="" width="1920" height="900" loading="lazy"></div>
    <div class="container band__inner">
      <div class="band__top reveal">
        <div>
          <span class="band__rule"></span>
          <h2 class="band__title" id="band-title">{total} people, <span>four teams</span></h2>
          <p class="band__sub">Everyone on our payroll</p>
        </div>
        <p class="band__words"><span>Quality</span><span>People</span><span>Progress</span></p>
      </div>
      <div class="stats reveal">{depts}</div>
    </div>
  </section>

  <!-- Apprenticeships -->
  <section class="section" aria-labelledby="apprentice-title">
    <div class="container split split--reverse">
      <div class="split__media reveal">
        <img src="{R}assets/img/team-apprentices.jpg" alt="Senior bricklayer checking an apprentice's block wall with a spirit level" width="1200" height="900" loading="lazy">
      </div>
      <div class="split__body reveal">
        <span class="eyebrow">Apprenticeships</span>
        <h2 class="section-title" id="apprentice-title">Training the <span>next generation</span></h2>
        <p>The Boland is short of qualified tradespeople, so we train our own. Every year we take on apprentices from the Breede Valley and pair them with our most experienced builders.</p>
        <ul class="checklist">{points}</ul>
      </div>
    </div>
  </section>

  <!-- Careers -->
  <section class="section process" id="careers" aria-labelledby="careers-title">
    <div class="container">
      <h2 class="section-title section-title--center reveal" id="careers-title">Join <span>the crew</span></h2>
      <p class="section-lead section-lead--center reveal">We're hiring for {len(t.JOBS)} roles. Open a role to see what it involves and how to apply.</p>
      <div class="faq jobs reveal">{jobs}
      </div>
      <p class="jobs__note reveal">Don't see your trade? Send your CV to <a href="mailto:{t.CAREERS_EMAIL}">{t.CAREERS_EMAIL}</a> and we'll keep it on file.</p>
    </div>
  </section>
{cta_block("Want this team on your project?", "Tell us what you're building and get a fixed-price quote within 5 working days.", "Get a quote", R + "quote.html")}
</main>'''


def build_team():
    t = load("team")
    org = {"@id": BUSINESS["@id"], "@type": "GeneralContractor", "name": BUSINESS["name"], "sameAs": SITE}
    graph = [
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE},
            {"@type": "ListItem", "position": 2, "name": "Team", "item": SITE + "team.html"}]},
    ]
    for j in t.JOBS:
        graph.append({
            "@type": "JobPosting",
            "title": j["title"],
            "description": "<p>" + j["summary"] + "</p><ul>" + "".join(f"<li>{r}</li>" for r in j["requirements"]) + "</ul>",
            "datePosted": "2026-10-28",
            "validThrough": "2026-11-30T17:00:00+02:00",
            "employmentType": j["employment_type"],
            "hiringOrganization": org,
            "jobLocation": {"@type": "Place", "address": BUSINESS["address"]},
        })
    render(team_main(t), {
        "title": "Our Team | Builders & Engineers in Worcester | Boland Structures",
        "description": "Meet the 85 builders, engineers, planners and safety specialists at Boland Structures in Worcester, plus open jobs and apprenticeships in the Boland.",
        "preload": "assets/img/page-hero-team.jpg",
        "nav": "team",
        "path": "team.html",
        "head_extra": jsonld({"@context": "https://schema.org", "@graph": graph}),
    }, "team.html")


if __name__ == "__main__":
    build_pages()
    build_services()
    build_projects()
    build_team()
