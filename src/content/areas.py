"""
Location pages: areas.html (hub) and areas/<slug>.html (one per town).

Rule for adding a town: only add one when you can fill every field with
content that is true for THAT town (projects built there, local building
conditions, municipality, real FAQs). If swapping the town name for another
town still reads correctly, it's a doorway page and will hurt rankings.

`location` must match the "location" field in projects.py so the town's
projects are pulled in automatically.

Images in assets/img/areas/:
  <slug>-hero.jpg   1920×800   page banner
  <slug>-local.jpg  1200×900   "building in <town>" section
"""

AREAS = [
    {
        "slug": "worcester",
        "town": "Worcester",
        "location": "Worcester",
        "title": "Builders in Worcester | Building Contractor | Boland Structures",
        "description": "Worcester-based building contractor since 2004. New builds, renovations, building plans and concrete work across Worcester, with a free site visit and a fixed-price quote.",
        "h1": "Builders in <span>Worcester</span>",
        "hero_lead": "Our yard is on Durban Street, so Worcester is home. We've built more than 140 homes, cellars, schools and business units here since 2004.",
        "intro_h2": "Your local <span>Worcester builder</span>",
        "lede": "Boland Structures is a building contractor based in Worcester, with our yard and office at 18 Durban Street. We build, renovate and plan homes, commercial buildings, schools and wine cellars across town and the farms around it.",
        "intro_paras": [
            "Being based here means short travel, quick site visits and a site manager who can be at your build within 15 minutes. It also means we know which suburbs sit on clay, how long Breede Valley Municipality takes to approve plans, and which suppliers deliver on time.",
        ],
        "facts": [("From our yard", "0–15 min"), ("Projects here", "140+"), ("Municipality", "Breede Valley")],
        "local_h2": "Building in <span>Worcester</span>: what to know",
        "local_intro": "Four things that shape almost every Worcester build, and how we handle them.",
        "local_points": [
            ("Summer heat", "Worcester regularly passes 38 °C in summer. We pour concrete before 10:00, wet-cure it for 7 days and shade fresh slabs so they don't crack."),
            ("Clay near the river", "Plots closer to the Hex and Breede rivers often sit on expansive clay. We soil-test before quoting and price the right foundation from day one."),
            ("Breede Valley approvals", "Standard residential plans take 6 to 12 weeks after a complete submission. We submit complete packages and follow up weekly."),
            ("Older town-centre buildings", "Buildings older than 60 years around Church Street and the town centre may need a heritage permit before alterations."),
        ],
        "local_alt": "Crew finishing a concrete slab on a hot day",
        "service_lines": {
            "construction": "Homes in Worcester's suburbs, business units in the industrial area and cellars on the surrounding farms.",
            "renovation": "Extensions and second storeys on Worcester homes, plus refits of older town-centre buildings.",
            "planning": "Plans drawn and submitted to Breede Valley Municipality, with our office just down the road.",
            "concrete": "Foundations, slabs and power-floated floors, poured by our crew based right here in town.",
        },
        "faqs": [
            ("Where is your yard in Worcester?", "At 18 Durban Street, Worcester, 6850. Visitors can park inside the yard gate. Call ahead so the right project manager is in."),
            ("Do you charge travel for Worcester projects?", "No. Worcester is our home base, so there's no travel charge on site visits or quotes in town and on nearby farms."),
            ("How long does building plan approval take in Worcester?", "Breede Valley Municipality usually takes 6 to 12 weeks for standard residential plans after a complete submission. Larger or non-standard applications take longer."),
            ("Can I see a finished project in Worcester?", "Yes. We can arrange a visit to a completed project in Worcester, with the owner's permission, so you can see the quality for yourself."),
        ],
    },
    {
        "slug": "de-doorns",
        "town": "De Doorns",
        "location": "De Doorns",
        "title": "Builders in De Doorns & the Hex River Valley | Boland Structures",
        "description": "Building contractor for De Doorns and the Hex River Valley: packhouses, cold stores, farmhouses and homes built for the valley's wind, frost and harvest season.",
        "h1": "Builders in <span>De Doorns</span>",
        "hero_lead": "Packhouses, cold stores, farmhouses and family homes across the Hex River Valley, built around the table-grape season.",
        "intro_h2": "Building for the <span>Hex River Valley</span>",
        "lede": "Boland Structures builds in De Doorns and across the Hex River Valley, 32 km from our Worcester yard on the N1. Most of our work here is for table-grape farms: packhouses, cold stores, staff housing and farmhouses, plus new homes in town.",
        "intro_paras": [
            "Our first contract in 2004 was a packing shed in De Doorns, and we've built in the valley every year since. We know the farms run on the harvest calendar, so we plan builds to finish before packing starts in November.",
        ],
        "facts": [("From our yard", "30 min · 32 km"), ("Projects here", "45+"), ("Municipality", "Breede Valley")],
        "local_h2": "Building in the <span>Hex River Valley</span>",
        "local_intro": "The valley's weather and farming calendar make building here different from Worcester, 30 minutes away.",
        "local_points": [
            ("Strong south-easter", "The valley channels strong winds. Roofs, roller doors and large windows are designed for higher wind loads, and roof sheeting gets extra fixings."),
            ("Winter frost", "The valley floor gets hard frost. Cold-room floors are insulated against frost heave, and we protect fresh concrete on cold nights."),
            ("The harvest calendar", "Table-grape packing runs from about November to April. Packhouse and cold-store work is programmed to finish before the first grapes come in."),
            ("Steep vineyard slopes", "Homes on the valley slopes need cut-and-fill platforms and retaining walls, which we design and build ourselves."),
        ],
        "local_alt": "Table grapes growing under protective netting in the Hex River Valley",
        "service_lines": {
            "construction": "Packhouses, cold stores, staff housing and farmhouses for Hex River Valley farms.",
            "renovation": "Extending farmhouses and converting old farm stores into offices and staff accommodation.",
            "planning": "Plans for farm buildings and homes on sloped valley plots, submitted to Breede Valley Municipality.",
            "concrete": "Forklift-ready packhouse floors and insulated cold-room slabs that won't heave in the frost.",
        },
        "faqs": [
            ("Do you build packhouses in De Doorns?", "Yes. Packhouses and cold stores for table-grape farms are a large part of our Hex River Valley work, including power-floated floors and insulated cold-room slabs."),
            ("Can you finish before packing season?", "That's how we plan every farm build in the valley. We agree a completion date before November and programme the work backwards from it."),
            ("Do you charge travel to De Doorns?", "No. De Doorns is 30 minutes from our yard and part of our regular area, so site visits and quotes are free."),
            ("How do you handle the wind in the valley?", "We design roofs, doors and glazing for the higher wind loads in the Hex River Valley, and add extra fixings to roof sheeting."),
        ],
    },
    {
        "slug": "rawsonville",
        "town": "Rawsonville",
        "location": "Rawsonville",
        "title": "Builders in Rawsonville | Homes, Cellars & Farm Buildings | Boland Structures",
        "description": "Building contractor in Rawsonville for family homes, wine cellars and farm buildings. Foundations designed for Breede River clay and flood lines. Free site visit.",
        "h1": "Builders in <span>Rawsonville</span>",
        "hero_lead": "Family homes, wine cellars and farm buildings on the Breede River, with foundations designed for the clay and the flood lines.",
        "intro_h2": "Building on the <span>Breede River</span>",
        "lede": "Boland Structures builds homes, wine cellars and farm buildings in Rawsonville and on the wine farms along the Breede River, 18 km from our Worcester yard.",
        "intro_paras": [
            "Rawsonville's ground is the main challenge. Much of the town and the farms around it sit on expansive clay, and some plots fall inside the river's flood lines. We test the soil and check flood lines before we price anything, so the foundation is right the first time and stays inside the fixed quote.",
        ],
        "facts": [("From our yard", "20 min · 18 km"), ("Projects here", "35+"), ("Municipality", "Breede Valley")],
        "local_h2": "Building in <span>Rawsonville</span>: what to know",
        "local_intro": "What makes a Rawsonville build different, and what we do about it.",
        "local_points": [
            ("Expansive clay", "Clay swells in winter and shrinks in summer, cracking standard foundations. We use stiffened rafts or deeper footings, priced into the quote from the start."),
            ("Breede River flood lines", "Plots near the river may fall inside the 1-in-50 or 1-in-100-year flood line. We check this before design, because it decides where and how high you can build."),
            ("Wine cellars", "Rawsonville is wine country. Cellar floors are graded to drains with acid-resistant finishes, and walls are insulated to keep temperatures stable."),
            ("Farm access", "Many sites are reached by gravel farm roads. We plan concrete deliveries and pump hire around access and travel time."),
        ],
        "local_alt": "Steel reinforcement for a raft foundation on clay soil",
        "service_lines": {
            "construction": "Family homes in town and wine cellars, stores and staff housing on Breede River farms.",
            "renovation": "Extensions and kitchen refits for Rawsonville homes, and upgrades to older farm cellars.",
            "planning": "Soil tests, flood-line checks and plans submitted to Breede Valley Municipality.",
            "concrete": "Raft foundations for clay soil and drained, acid-resistant cellar floors.",
        },
        "faqs": [
            ("Is the soil in Rawsonville a problem for building?", "It can be. Much of Rawsonville sits on expansive clay. A soil test before quoting tells us which foundation you need, and we include it in the fixed price."),
            ("Can I build near the Breede River?", "It depends on where the flood lines fall on your plot. We check the 1-in-50 and 1-in-100-year flood lines before design so there are no surprises at approval."),
            ("Do you build wine cellars in Rawsonville?", "Yes. We build and upgrade cellars with graded, acid-resistant floors and insulated walls for stable temperatures."),
            ("Do you charge travel to Rawsonville?", "No. Rawsonville is 20 minutes from our yard, so site visits and quotes are free."),
        ],
    },
    {
        "slug": "tulbagh",
        "town": "Tulbagh",
        "location": "Tulbagh",
        "title": "Builders in Tulbagh | Heritage Restoration & New Builds | Boland Structures",
        "description": "Building contractor in Tulbagh for Cape Dutch heritage restorations, renovations and new homes. Heritage permits, lime plaster and seismic-aware structural design.",
        "h1": "Builders in <span>Tulbagh</span>",
        "hero_lead": "Restoring Cape Dutch homesteads and building new homes in one of the Western Cape's most historic towns.",
        "intro_h2": "Respecting <span>Tulbagh's heritage</span>",
        "lede": "Boland Structures restores, renovates and builds in Tulbagh and the surrounding valley, about an hour from our Worcester yard. Much of our work here is on Cape Dutch buildings that need heritage permits and traditional materials.",
        "intro_paras": [
            "Tulbagh is famous for Church Street, where many historic buildings were restored after the 1969 earthquake. Building here means working with heritage rules, older materials and Witzenberg Municipality, and designing structures with the area's earthquake history in mind.",
        ],
        "facts": [("From our yard", "1 hour · 60 km"), ("Projects here", "20+"), ("Municipality", "Witzenberg")],
        "local_h2": "Building in <span>Tulbagh</span>: what to know",
        "local_intro": "Tulbagh asks more of a builder than most Boland towns. Here's how we approach it.",
        "local_points": [
            ("Heritage permits", "Structures older than 60 years need a permit from Heritage Western Cape before alterations. We prepare the application with a registered heritage practitioner."),
            ("Traditional materials", "Old walls need to breathe. We strip trapped cement plaster and re-plaster with lime, and match original gables, shutters and yellowwood details."),
            ("Earthquake history", "The 1969 Tulbagh earthquake was the strongest in South Africa's recorded history. Our engineers design new structures and major alterations with seismic loads in mind."),
            ("Witzenberg approvals", "Plans go to Witzenberg Municipality, not Breede Valley. We know its process and submit complete packages to avoid delays."),
        ],
        "local_alt": "Renovated passage in a restored farmhouse with new timber floors",
        "service_lines": {
            "construction": "New homes and cottages designed to sit comfortably beside Tulbagh's historic buildings.",
            "renovation": "Cape Dutch restorations with lime plaster, matched gables and modern kitchens and bathrooms.",
            "planning": "Heritage permit applications and plans submitted to Witzenberg Municipality.",
            "concrete": "Foundations and slabs designed with Tulbagh's seismic history in mind.",
        },
        "faqs": [
            ("Do I need a heritage permit to renovate in Tulbagh?", "If any part of the building is older than 60 years, yes. A permit from Heritage Western Cape is needed before alterations. We prepare the application with a registered heritage practitioner."),
            ("Can you restore a Cape Dutch house?", "Yes. We've restored Cape Dutch homesteads in the Tulbagh valley, including stripping cement plaster, re-plastering with lime and matching original gables."),
            ("Who approves building plans in Tulbagh?", "Witzenberg Municipality. We prepare and submit plans and follow them through to approval."),
            ("Do you charge travel to Tulbagh?", "The first site visit is free. Because Tulbagh is about an hour from our yard, travel is listed as a separate line in your quote, so you can see exactly what it costs."),
        ],
    },
]

# Towns we work in without a dedicated page yet (listed on the hub)
OTHER_TOWNS = ["Touws River", "Robertson", "Ashton", "Montagu", "Ceres", "Wolseley", "Wellington", "Paarl"]
