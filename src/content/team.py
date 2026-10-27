"""
Team page content (team.html).

Portraits: leaders use assets/img/leader-N.jpg (shared with company.html);
everyone else uses assets/img/team/<slug>.jpg at 600×750 (4:5).
Department counts must add up to the 85 crew quoted across the site.
"""

LEADERS = [
    {
        "name": "Pieter van der Merwe",
        "role": "Founder &amp; Managing Director",
        "img": "leader-1.jpg",
        "img_alt": "Portrait of Pieter van der Merwe in a red hard hat",
        "credentials": "22 years at Boland Structures",
        "bio": "Pieter started the company in 2004 with two bakkies and a packing-shed contract in De Doorns. He still signs every quote, and still visits every active site once a week.",
        "email": "pieter@bolandstructures.co.za",
    },
    {
        "name": "Riaan Jacobs",
        "role": "Operations Director",
        "img": "leader-2.jpg",
        "img_alt": "Portrait of Riaan Jacobs in a white hard hat",
        "credentials": "Pr. CM · 18 years in construction",
        "bio": "Riaan runs programmes, crews and suppliers across every site. He joined in 2012 from a national contractor and built the weekly photo-report system our clients rely on.",
        "email": "riaan@bolandstructures.co.za",
    },
    {
        "name": "Sipho Ndlovu",
        "role": "Health &amp; Safety Manager",
        "img": "leader-3.jpg",
        "img_alt": "Portrait of Sipho Ndlovu in orange hi-vis and a white hard hat",
        "credentials": "SACPCMP Pr. CHSA · 15 years in site safety",
        "bio": "Sipho is responsible for every person on every site going home safely. Under his programme, Boland Structures recorded zero lost-time injuries in 2025.",
        "email": "sipho@bolandstructures.co.za",
    },
]

PEOPLE = [
    {"slug": "elzette-kruger", "name": "Elzette Kruger", "role": "Head of Planning",
     "credentials": "Pr. Arch. T · 11 years", "focus": "Leads plan drawing and municipal submissions across four municipalities.",
     "img_alt": "Elzette Kruger holding rolled building plans on site"},
    {"slug": "lizelle-pretorius", "name": "Lizelle Pretorius", "role": "Structural Engineer",
     "credentials": "Pr. Eng. · 9 years", "focus": "Designs foundations, slabs and steel, and inspects every structural pour.",
     "img_alt": "Lizelle Pretorius in an orange hard hat and safety glasses"},
    {"slug": "thandiwe-nkosi", "name": "Thandiwe Nkosi", "role": "Quantity Surveyor",
     "credentials": "Pr. QS · 7 years", "focus": "Prices every project and makes sure the fixed quote holds to the end.",
     "img_alt": "Thandiwe Nkosi in an orange hard hat on a building site"},
    {"slug": "johan-swart", "name": "Johan Swart", "role": "Senior Site Manager",
     "credentials": "Residential &amp; agricultural · 16 years", "focus": "Has run more than 60 of our homes, cellars and packhouses from first peg to handover.",
     "img_alt": "Johan Swart in a hard hat with safety gear on site"},
    {"slug": "abdul-hendricks", "name": "Abdul Hendricks", "role": "Site Manager",
     "credentials": "Commercial &amp; public · 10 years", "focus": "Manages our business parks, schools and clinics, including work on occupied sites.",
     "img_alt": "Abdul Hendricks in a red hard hat setting out a site with a GPS rover"},
    {"slug": "mandla-zulu", "name": "Mandla Zulu", "role": "Concrete Foreman",
     "credentials": "Concrete crew lead · 14 years", "focus": "Leads our 14-person concrete crew on every foundation, slab and industrial floor.",
     "img_alt": "Mandla Zulu in a blue work uniform with arms crossed"},
]

DEPARTMENTS = [
    ("48", "Site crews", "Bricklayers, carpenters, roofers and general builders"),
    ("14", "Concrete crew", "Formwork, steel fixing and finishing"),
    ("9", "Planning &amp; design", "Architectural, engineering and quantity surveying"),
    ("14", "Safety, office &amp; yard", "Safety, procurement, admin and plant"),
]

APPRENTICE_POINTS = [
    "3-year apprenticeships in bricklaying, carpentry and plumbing",
    "Paid from day one, with trade-test fees covered",
    "Each apprentice paired with a senior tradesperson",
    "18 apprentices qualified since 2015, and 15 still work with us",
]

JOBS = [
    {
        "title": "Site Manager: Residential",
        "type": "Full-time",
        "location": "Worcester and Boland sites",
        "summary": "Run two to three residential builds at a time, from site handover to final snag walk.",
        "requirements": [
            "5+ years managing residential builds in South Africa",
            "Working knowledge of NHBRC and SANS 10400 requirements",
            "Valid driver's licence and own reliable transport",
            "Afrikaans and English. isiXhosa is a plus.",
        ],
        "employment_type": "FULL_TIME",
    },
    {
        "title": "Qualified Bricklayer",
        "type": "Full-time",
        "location": "Boland sites",
        "summary": "Face-brick and plaster work on homes, cellars and commercial buildings across the Boland.",
        "requirements": [
            "Trade test certificate or 5+ years' proven experience",
            "Face-brick experience is essential",
            "Able to read building plans",
            "Live within 40 km of Worcester",
        ],
        "employment_type": "FULL_TIME",
    },
    {
        "title": "Apprentice Carpenter (2027 intake)",
        "type": "3-year apprenticeship",
        "location": "Worcester",
        "summary": "Learn roof, formwork and finishing carpentry on site, with a paid apprenticeship and a trade test at the end.",
        "requirements": [
            "Grade 12 with Mathematics or Technical Mathematics",
            "Aged 18 to 25",
            "Live in the Breede Valley",
            "Applications close 30 November 2026",
        ],
        "employment_type": "INTERN",
    },
]

CAREERS_EMAIL = "careers@bolandstructures.co.za"
