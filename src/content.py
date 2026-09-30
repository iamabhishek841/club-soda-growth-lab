PUBLIC_OBSERVATIONS = [
    {
        "observation": "Events are promoted across multiple Irish locations and age groups.",
        "why_it_matters": "Discovery can be personalised by geography, age band and event intent instead of sending every visitor to one generic journey.",
        "proposed_test": "Location-first landing pages with age/event filters and campaign-specific UTMs.",
        "primary_metric": "Event-detail click-through rate",
        "source": "https://www.clubsoda.ie/events/",
    },
    {
        "observation": "Event registration is completed on the website and a confirmation email is sent after booking.",
        "why_it_matters": "The booking journey already contains measurable intent and conversion steps that can be instrumented end-to-end.",
        "proposed_test": "Track view_event → begin_checkout → purchase and trigger an abandonment follow-up where consent permits.",
        "primary_metric": "Checkout completion rate",
        "source": "https://www.clubsoda.ie/terms-of-service/",
    },
    {
        "observation": "The public shop page is currently marked 'Coming Soon' and invites visitors to join the newsletter / follow social channels.",
        "why_it_matters": "A pre-launch waitlist can validate demand before inventory and create an owned audience for launch day.",
        "proposed_test": "Waitlist landing page with product-interest capture and launch sequence.",
        "primary_metric": "Waitlist signup rate",
        "source": "https://www.clubsoda.ie/shop/",
    },
    {
        "observation": "Club Soda describes post-event connection tools including a 7-day social group and a mutual-match form.",
        "why_it_matters": "Post-event engagement can become a retention loop rather than the end of the customer journey.",
        "proposed_test": "Post-event lifecycle messaging that asks for feedback, recommends the next relevant event and measures repeat booking.",
        "primary_metric": "30-day repeat booking rate",
        "source": "https://www.clubsoda.ie/events/faq-s/",
    },
    {
        "observation": "The brand proposition emphasises real-life connection, confidence, friendship and a welcoming environment.",
        "why_it_matters": "Campaign creative can sell the emotional outcome, not just the event format.",
        "proposed_test": "Compare feature-led creative vs outcome-led creative in short-form social campaigns.",
        "primary_metric": "Qualified landing-page visit rate",
        "source": "https://www.clubsoda.ie/",
    },
]

MEASUREMENT_EVENTS = [
    ("view_home", "Landing / home page viewed", "Acquisition"),
    ("view_event", "Specific event page viewed", "Consideration"),
    ("select_event", "Event / date selected", "Intent"),
    ("begin_checkout", "Checkout started", "Intent"),
    ("purchase", "Ticket / product purchase completed", "Conversion"),
    ("newsletter_signup", "Newsletter signup completed", "Lead capture"),
    ("shop_waitlist_signup", "Shop waitlist signup completed", "Lead capture"),
    ("post_event_engagement", "Post-event group / match / feedback action", "Retention"),
    ("repeat_booking", "A returning customer books again", "Retention"),
]

SEGMENTS = [
    {
        "segment": "New Explorer",
        "signal": "First visit; browses 1–2 events",
        "goal": "Reduce uncertainty",
        "message": "Show what to expect, social proof, safety and the next relevant event nearby.",
        "cta": "See events near me",
    },
    {
        "segment": "Event-Ready Local",
        "signal": "Repeated event views in one location / age band",
        "goal": "Convert high intent",
        "message": "Lead with availability, date, venue context and a friction-light path to booking.",
        "cta": "Book my place",
    },
    {
        "segment": "High-Intent Abandoner",
        "signal": "Checkout started but no purchase",
        "goal": "Recover lost demand",
        "message": "Answer likely blockers, remind them what is included and make return-to-checkout easy.",
        "cta": "Finish booking",
    },
    {
        "segment": "Returning Attendee",
        "signal": "Previous purchase / event attendance",
        "goal": "Increase repeat frequency",
        "message": "Recommend the next event based on location, age band and past participation.",
        "cta": "Choose my next event",
    },
    {
        "segment": "Shop Waitlist Lead",
        "signal": "Signed up for merchandise launch updates",
        "goal": "Convert launch interest",
        "message": "Use product reveal, early access and event-community context rather than generic ecommerce blasts.",
        "cta": "Get launch access",
    },
]

EXPERIMENTS = [
    {
        "area": "Event discovery",
        "hypothesis": "Visitors will engage more when the landing experience starts with location and age relevance.",
        "variant": "Generic event listing vs location-first event finder",
        "primary_metric": "Event-detail CTR",
        "guardrail": "Bounce rate",
    },
    {
        "area": "Event page",
        "hypothesis": "Outcome-led proof will reduce uncertainty for first-time attendees.",
        "variant": "Standard event copy vs copy + 'what to expect' + attendee proof",
        "primary_metric": "Begin-checkout rate",
        "guardrail": "Support/contact rate",
    },
    {
        "area": "Checkout",
        "hypothesis": "A clearer summary of what is included will reduce late-stage hesitation.",
        "variant": "Current checkout vs checkout with concise value / reassurance block",
        "primary_metric": "Purchase completion",
        "guardrail": "Refund / cancellation rate",
    },
    {
        "area": "Shop launch",
        "hypothesis": "Interest-based waitlist capture will outperform a generic newsletter CTA for merchandise launch intent.",
        "variant": "Generic newsletter signup vs shop-specific waitlist",
        "primary_metric": "Qualified signup rate",
        "guardrail": "Email unsubscribe rate",
    },
    {
        "area": "Retention",
        "hypothesis": "A personalised next-event recommendation after attendance will increase repeat bookings.",
        "variant": "Generic newsletter vs post-event recommendation sequence",
        "primary_metric": "30-day repeat booking",
        "guardrail": "Email unsubscribe rate",
    },
]

ROADMAP = [
    {
        "phase": "Days 1–30 · Measure",
        "focus": "Instrument the journey and establish baselines",
        "deliverables": [
            "Map acquisition → event discovery → checkout → purchase → repeat booking",
            "Define GA4 / analytics event taxonomy and UTM naming conventions",
            "Create baseline funnel and channel dashboard",
            "Audit top event pages, checkout friction and newsletter capture",
        ],
    },
    {
        "phase": "Days 31–60 · Test",
        "focus": "Launch a small set of high-signal experiments",
        "deliverables": [
            "Location / age-specific landing-page test",
            "High-intent checkout recovery journey",
            "Shop waitlist MVP with product-interest capture",
            "Short-form social creative test with measurable campaign UTMs",
        ],
    },
    {
        "phase": "Days 61–90 · Scale",
        "focus": "Scale winners and build lifecycle loops",
        "deliverables": [
            "Scale winning acquisition and landing-page variants",
            "Launch repeat-booking lifecycle segmentation",
            "Connect shop launch to existing event audiences",
            "Weekly growth review: CAC, conversion, repeat rate, revenue contribution",
        ],
    },
]
