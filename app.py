from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.content import (
    EXPERIMENTS,
    MEASUREMENT_EVENTS,
    PUBLIC_OBSERVATIONS,
    ROADMAP,
    SEGMENTS,
)
from src.growth_model import (
    FunnelInputs,
    FunnelUplifts,
    compare_scenarios,
    two_proportion_sample_size,
)

st.set_page_config(
    page_title="Club Soda Growth Lab",
    page_icon="↗",
    layout="wide",
    initial_sidebar_state="expanded",
)

CUSTOM_CSS = """
<style>
    .block-container {padding-top: 1.7rem; padding-bottom: 4rem; max-width: 1240px;}
    h1, h2, h3 {letter-spacing: -0.025em;}
    .hero {
        padding: 2rem 2.2rem;
        border: 1px solid rgba(120,120,120,.22);
        border-radius: 22px;
        background: linear-gradient(135deg, rgba(124,58,237,.13), rgba(20,184,166,.10));
        margin-bottom: 1.1rem;
    }
    .hero-kicker {font-size: .82rem; font-weight: 700; text-transform: uppercase; letter-spacing: .11em; opacity: .72;}
    .hero-title {font-size: 2.4rem; line-height: 1.04; font-weight: 800; margin: .45rem 0 .65rem 0;}
    .hero-copy {font-size: 1.05rem; max-width: 850px; opacity: .88;}
    .pill {display:inline-block; padding:.34rem .72rem; border-radius:999px; margin:.18rem .22rem .18rem 0; background:rgba(124,58,237,.11); border:1px solid rgba(124,58,237,.18); font-size:.85rem;}
    .callout {padding: 1rem 1.1rem; border-left: 4px solid #14b8a6; background: rgba(20,184,166,.08); border-radius: 8px;}
    .small-note {font-size: .82rem; opacity:.72;}
    .journey-step {padding:.85rem 1rem; border-radius:14px; border:1px solid rgba(120,120,120,.2); min-height:110px;}
    .section-label {font-size:.78rem; font-weight:700; text-transform:uppercase; letter-spacing:.09em; opacity:.62; margin-bottom:.2rem;}
    .metric-card {padding: 1rem 1.05rem; border:1px solid rgba(120,120,120,.18); border-radius:16px; background:rgba(255,255,255,.72); min-height:104px;}
    .metric-label {font-size:.72rem; font-weight:700; text-transform:uppercase; letter-spacing:.06em; opacity:.58; margin-bottom:.45rem;}
    .metric-value {font-size:1.22rem; line-height:1.18; font-weight:760; letter-spacing:-.02em; overflow-wrap:anywhere;}
    .role-line {margin-top:1.05rem; padding-top:.9rem; border-top:1px solid rgba(90,90,120,.15); font-size:.92rem; opacity:.86;}
    .case-note {padding:.58rem .78rem; border:1px solid rgba(120,120,120,.14); background:rgba(120,120,120,.045); border-radius:10px; font-size:.80rem; opacity:.76; margin:.15rem 0 1.25rem 0;}
    .footer {margin-top:3rem; padding-top:1.2rem; border-top:1px solid rgba(120,120,120,.2); font-size:.85rem; opacity:.74;}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def fmt_int(value: float) -> str:
    return f"{value:,.0f}"


def fmt_eur(value: float) -> str:
    return f"€{value:,.0f}"


def render_disclaimer() -> None:
    st.markdown(
        """
        <div class="case-note">
        Independent portfolio case study using public Club Soda information and synthetic demonstration data. No internal analytics, ad-account or customer data is used.
        </div>
        """,
        unsafe_allow_html=True,
    )


with st.sidebar:
    st.markdown("### Club Soda Growth Lab")
    st.caption("Digital sales, customer journey & conversion prototype")
    section = st.radio(
        "Explore",
        [
            "Executive overview",
            "Website & journey audit",
            "Funnel simulator",
            "Segments & lifecycle",
            "Campaign lab",
            "Experiment lab",
            "90-day plan",
            "Methods & sources",
        ],
        label_visibility="collapsed",
    )
    st.divider()
    st.markdown("**Built by Abhishek Kumar**")
    st.caption("MSc Business Analytics · consumer research · growth analytics · experimentation")
    st.markdown("[View source](https://github.com/iamabhishek841/club-soda-growth-lab) · [LinkedIn](https://www.linkedin.com/in/iamabhishek841)")


st.markdown(
    """
    <div class="hero">
      <div class="hero-kicker">Independent growth case study</div>
      <div class="hero-title">Club Soda Growth Lab</div>
      <div class="hero-copy">A hands-on prototype for turning awareness into measurable event bookings, shop demand and repeat engagement — with a clear measurement plan behind every recommendation.</div>
      <div style="margin-top:.9rem">
        <span class="pill">Customer journey</span>
        <span class="pill">Sales funnels</span>
        <span class="pill">CRO</span>
        <span class="pill">Lifecycle marketing</span>
        <span class="pill">Experimentation</span>
        <span class="pill">Growth analytics</span>
      </div>
      <div class="role-line"><b>Built for the Digital Sales &amp; Marketing Specialist brief:</b> how I would connect Club Soda's social, website, booking, lifecycle and shop activity into one measurable growth system from day one.</div>
    </div>
    """,
    unsafe_allow_html=True,
)
render_disclaimer()


if section == "Executive overview":
    st.subheader("What I would optimise first")
    st.write(
        "The opportunity is not just to create more content. It is to connect acquisition, event discovery, booking, post-event engagement and the upcoming shop into one measurable customer journey."
    )

    c1, c2, c3, c4 = st.columns(4)
    metric_cards = [
        (c1, "Growth system", "Discover → Repeat"),
        (c2, "Primary conversion", "Completed booking"),
        (c3, "Secondary conversion", "Shop waitlist"),
        (c4, "Retention signal", "Repeat booking"),
    ]
    for col, label, value in metric_cards:
        with col:
            st.markdown(
                f"<div class='metric-card'><div class='metric-label'>{label}</div><div class='metric-value'>{value}</div></div>",
                unsafe_allow_html=True,
            )

    st.markdown("### Three growth loops")
    cols = st.columns(3)
    loops = [
        (
            "1 · Event conversion",
            "Social / search → relevant event page → checkout → booking",
            "Measure drop-off and remove friction between intent and purchase.",
        ),
        (
            "2 · Post-event retention",
            "Attendance → follow-up → next relevant event → repeat booking",
            "Treat the event as the start of a lifecycle, not the end of one.",
        ),
        (
            "3 · Shop launch",
            "Existing community → waitlist → product reveal → launch → cross-sell",
            "Validate demand before launch and use owned audiences first.",
        ),
    ]
    for col, (title, flow, copy) in zip(cols, loops):
        with col:
            st.markdown(f"**{title}**")
            st.caption(flow)
            st.write(copy)

    st.markdown("### Why this approach is credible")
    st.markdown(
        """
        <div class="callout">
        My prior Data Driven Marketing work used mixed-method consumer research: six in-depth interviews, a survey with 71 valid respondents, conjoint analysis and segment-level preference modelling. A separate customer-analytics assignment segmented a 3,000-customer dataset and extended the analysis into retention and CLV. This prototype applies the same evidence-first mindset to a live growth problem.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Decision principle")
    st.write(
        "Every marketing activity should answer one of four questions: **Who is this for? What behaviour should change? How will we measure it? What do we do next if it works?**"
    )

elif section == "Website & journey audit":
    st.subheader("Public-site observations → measurable opportunities")
    audit_df = pd.DataFrame(PUBLIC_OBSERVATIONS)
    st.dataframe(
        audit_df[["observation", "why_it_matters", "proposed_test", "primary_metric"]],
        use_container_width=True,
        hide_index=True,
        column_config={
            "observation": "Public observation",
            "why_it_matters": "Why it matters",
            "proposed_test": "What I would test",
            "primary_metric": "Primary metric",
        },
    )

    st.markdown("### Proposed end-to-end journey")
    steps = [
        ("1", "Discover", "Instagram / TikTok / Meta / search / referral"),
        ("2", "Explore", "Location + age-relevant event discovery"),
        ("3", "Consider", "Event detail, reassurance, social proof, FAQ"),
        ("4", "Convert", "Checkout and ticket / product purchase"),
        ("5", "Experience", "Event attendance + post-event connection"),
        ("6", "Retain", "Next-event recommendation + shop / community"),
    ]
    cols = st.columns(3)
    for i, (num, title, copy) in enumerate(steps):
        with cols[i % 3]:
            st.markdown(
                f"<div class='journey-step'><div class='section-label'>Step {num}</div><b>{title}</b><br><span class='small-note'>{copy}</span></div>",
                unsafe_allow_html=True,
            )
            st.write("")

    st.markdown("### Measurement blueprint")
    measure_df = pd.DataFrame(MEASUREMENT_EVENTS, columns=["Event", "Definition", "Journey stage"])
    st.dataframe(measure_df, use_container_width=True, hide_index=True)
    st.caption(
        "These are proposed analytics events. The prototype does not claim that Club Soda currently tracks them."
    )

elif section == "Funnel simulator":
    st.subheader("Interactive booking & revenue simulator")
    st.write(
        "Use this to translate small conversion improvements into commercial impact. All starting values below are synthetic scenario inputs, not company performance data."
    )

    left, right = st.columns([1, 1])
    with left:
        st.markdown("#### Baseline assumptions")
        monthly_visitors = st.slider("Monthly website visitors", 1000, 50000, 8000, step=500)
        event_view_rate = st.slider("Visitor → event/product view", 5, 80, 42) / 100
        checkout_start_rate = st.slider("View → checkout start", 2, 50, 16) / 100
        purchase_completion_rate = st.slider("Checkout → purchase", 10, 95, 62) / 100
        average_order_value = st.slider("Average order value (€)", 10, 120, 32)
        repeat_booking_rate = st.slider("30-day repeat booking rate", 1, 50, 18) / 100

    with right:
        st.markdown("#### Improvement scenario")
        event_view_uplift = st.slider("Relative uplift: event-page engagement", 0, 40, 8) / 100
        checkout_start_uplift = st.slider("Relative uplift: checkout starts", 0, 40, 10) / 100
        purchase_completion_uplift = st.slider("Relative uplift: checkout completion", 0, 40, 12) / 100
        repeat_booking_uplift = st.slider("Relative uplift: repeat bookings", 0, 50, 15) / 100

    baseline_inputs = FunnelInputs(
        monthly_visitors=monthly_visitors,
        event_view_rate=event_view_rate,
        checkout_start_rate=checkout_start_rate,
        purchase_completion_rate=purchase_completion_rate,
        average_order_value=float(average_order_value),
        repeat_booking_rate=repeat_booking_rate,
    )
    uplifts = FunnelUplifts(
        event_view_uplift=event_view_uplift,
        checkout_start_uplift=checkout_start_uplift,
        purchase_completion_uplift=purchase_completion_uplift,
        repeat_booking_uplift=repeat_booking_uplift,
    )
    results = compare_scenarios(baseline_inputs, uplifts)
    base = results["baseline"]
    improved = results["improved"]
    delta = results["delta"]

    st.markdown("### Commercial impact")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Baseline purchases", fmt_int(base["Purchases"]), delta=fmt_int(delta["Purchases"]))
    m2.metric("Baseline revenue", fmt_eur(base["Revenue"]), delta=fmt_eur(delta["Revenue"]))
    m3.metric(
        "Visitor → purchase",
        f"{base['Visitor-to-purchase conversion']:.2%}",
        delta=f"{delta['Visitor-to-purchase conversion']:.2%}",
    )
    m4.metric("Repeat bookings", fmt_int(base["Repeat bookings"]), delta=fmt_int(delta["Repeat bookings"]))

    funnel_labels = ["Visitors", "Event / product views", "Checkout starts", "Purchases"]
    fig = go.Figure()
    fig.add_trace(
        go.Funnel(
            name="Baseline",
            y=funnel_labels,
            x=[base[x] for x in funnel_labels],
            textinfo="value+percent initial",
        )
    )
    fig.add_trace(
        go.Funnel(
            name="Improved scenario",
            y=funnel_labels,
            x=[improved[x] for x in funnel_labels],
            textinfo="value+percent initial",
        )
    )
    fig.update_layout(height=460, margin=dict(l=10, r=10, t=40, b=10))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### How I would use this in the role")
    st.write(
        "The point is not to forecast revenue from invented data. The point is to make trade-offs explicit: identify the largest drop-off, prioritise one intervention, measure the lift, and then decide whether to scale it."
    )

elif section == "Segments & lifecycle":
    st.subheader("Behavioural segments for lifecycle marketing")
    st.write(
        "These are proposed activation segments built around observable behaviour — not demographic assumptions."
    )
    seg_df = pd.DataFrame(SEGMENTS)
    st.dataframe(seg_df, use_container_width=True, hide_index=True)

    st.markdown("### Journey playbook")
    selected = st.selectbox("Choose a proposed segment", [s["segment"] for s in SEGMENTS])
    item = next(s for s in SEGMENTS if s["segment"] == selected)
    a, b, c = st.columns(3)
    a.markdown(f"**Signal**\n\n{item['signal']}")
    b.markdown(f"**Commercial goal**\n\n{item['goal']}")
    c.markdown(f"**Primary CTA**\n\n{item['cta']}")
    st.markdown("**Message strategy**")
    st.write(item["message"])

    st.markdown("### Example lifecycle sequence")
    sequence = pd.DataFrame(
        [
            ["T+0", "Booking confirmation", "Reduce uncertainty", "Event details + what to expect"],
            ["T-2 days", "Event reminder", "Increase attendance", "Practical reminder + confidence cues"],
            ["T+1 day", "Post-event follow-up", "Capture feedback / connection", "Feedback + post-event tools"],
            ["T+4 days", "Next-event recommendation", "Drive repeat booking", "Location / age-relevant recommendation"],
            ["T+10 days", "Community / shop touchpoint", "Broaden relationship", "Upcoming events or shop waitlist"],
        ],
        columns=["Timing", "Touchpoint", "Goal", "Content"],
    )
    st.dataframe(sequence, use_container_width=True, hide_index=True)
    st.caption("Illustrative lifecycle design; channel frequency should be adapted to consent, engagement and actual customer behaviour.")

elif section == "Campaign lab":
    st.subheader("Campaign → landing page → measurable action")
    campaign = st.selectbox(
        "Campaign objective",
        ["Fill an upcoming event", "Launch the shop waitlist", "Recover high-intent visitors", "Drive repeat bookings"],
    )
    channel = st.selectbox("Primary channel", ["Instagram / TikTok organic", "Meta paid social", "Email", "Cross-channel"])

    templates = {
        "Fill an upcoming event": {
            "hook": "Dating apps are not the only way to meet someone new.",
            "offer": "Show a real-life Club Soda event with a clear location, audience fit and what-to-expect reassurance.",
            "landing": "Campaign-specific event page with date, location, availability, FAQs and a single booking CTA.",
            "measure": "Qualified landing visits → begin checkout → completed booking",
        },
        "Launch the shop waitlist": {
            "hook": "Take a piece of the Club Soda experience with you.",
            "offer": "Preview upcoming merchandise categories and invite people to choose what they are most interested in.",
            "landing": "Shop waitlist with interest capture rather than a generic newsletter signup.",
            "measure": "Waitlist conversion → launch email engagement → first purchase",
        },
        "Recover high-intent visitors": {
            "hook": "Still thinking about joining us? Here is exactly what to expect.",
            "offer": "Address uncertainty and make returning to the booking journey easy.",
            "landing": "Deep-link back to the relevant event or checkout state where technically possible.",
            "measure": "Recovered sessions → purchase completion",
        },
        "Drive repeat bookings": {
            "hook": "Your next real-life connection could be at the next event near you.",
            "offer": "Recommend the next relevant event based on previous participation and location.",
            "landing": "Curated event recommendation rather than generic homepage traffic.",
            "measure": "Click-through → repeat booking → 30/60-day repeat rate",
        },
    }
    plan = templates[campaign]
    st.markdown(f"**Channel:** {channel}")
    p1, p2 = st.columns(2)
    with p1:
        st.markdown("#### Creative brief")
        st.markdown(f"**Hook**  \n{plan['hook']}")
        st.markdown(f"**Offer / story**  \n{plan['offer']}")
    with p2:
        st.markdown("#### Conversion design")
        st.markdown(f"**Landing experience**  \n{plan['landing']}")
        st.markdown(f"**Measurement**  \n{plan['measure']}")

    st.markdown("### Short-form video storyboard")
    storyboard = pd.DataFrame(
        [
            ["0–3s", "Pattern interrupt", "Show the problem / emotional tension quickly"],
            ["3–8s", "Real experience", "People, setting, movement, genuine interactions"],
            ["8–14s", "Reassurance", "What to expect + who the event is for"],
            ["14–20s", "Action", "One clear CTA linked to the campaign landing page"],
        ],
        columns=["Timing", "Job", "Creative direction"],
    )
    st.dataframe(storyboard, use_container_width=True, hide_index=True)

    st.markdown("### Tracking checklist")
    st.code(
        "utm_source=instagram\nutm_medium=paid_social\nutm_campaign=<event_or_shop_launch>\nutm_content=<creative_variant>",
        language="text",
    )
    st.caption("UTM names are illustrative. A real implementation would use one documented naming convention across channels.")

elif section == "Experiment lab":
    st.subheader("CRO experiment backlog")
    exp_df = pd.DataFrame(EXPERIMENTS)
    st.dataframe(exp_df, use_container_width=True, hide_index=True)

    st.markdown("### Quick A/B test sizing")
    st.write("Planning-only calculator for a binary conversion metric.")
    a, b = st.columns(2)
    with a:
        baseline = st.slider("Baseline conversion rate", 1.0, 50.0, 12.0, step=0.5) / 100
    with b:
        relative_lift = st.slider("Minimum relative uplift worth detecting", 5, 50, 15) / 100
    sample = two_proportion_sample_size(baseline, relative_lift)
    if sample:
        st.metric("Approx. sample required per variant", f"{sample:,}")
        st.caption("Approximation assumes a two-sided 5% significance level and ~80% power. Validate with the production analytics / experimentation stack before launch.")
    else:
        st.warning("Choose a baseline and uplift that keep the target conversion between 0% and 100%.")

    st.markdown("### Experiment operating rule")
    st.write(
        "One hypothesis → one primary metric → one guardrail → pre-agreed decision rule. Avoid changing a page and a campaign simultaneously if you need to know what caused the result."
    )

elif section == "90-day plan":
    st.subheader("First 90 days: build the system, then scale it")
    for phase in ROADMAP:
        st.markdown(f"### {phase['phase']}")
        st.caption(phase["focus"])
        for item in phase["deliverables"]:
            st.markdown(f"- {item}")

    st.markdown("### Weekly growth scorecard")
    scorecard = pd.DataFrame(
        [
            ["Acquisition", "Qualified landing sessions", "Are campaigns bringing the right people?"],
            ["Engagement", "Event-detail CTR", "Can visitors find something relevant quickly?"],
            ["Intent", "Begin-checkout rate", "Does the event page create enough confidence to act?"],
            ["Conversion", "Checkout completion", "Where is late-stage friction?"],
            ["Economics", "CAC / revenue contribution", "Are paid channels commercially sensible?"],
            ["Retention", "30/60-day repeat booking", "Are we building a relationship, not one-off transactions?"],
            ["Shop", "Waitlist → first purchase", "Is launch demand translating into revenue?"],
        ],
        columns=["Stage", "Metric", "Decision question"],
    )
    st.dataframe(scorecard, use_container_width=True, hide_index=True)

elif section == "Methods & sources":
    st.subheader("Methodology")
    st.write(
        "This prototype deliberately separates **observations** (what is visible on the public website), **proposals** (what I would build or test) and **synthetic scenarios** (illustrative numbers used in calculators)."
    )
    method_df = pd.DataFrame(
        [
            ["Public observation", "Club Soda website", "Describe the current customer-facing experience"],
            ["Proposed strategy", "Independent analysis", "Show how I would approach the role"],
            ["Synthetic data", "Generated scenario inputs", "Demonstrate funnel economics without inventing company results"],
            ["Prior research evidence", "My Data Driven Marketing coursework", "Demonstrate consumer-research and segmentation capability"],
        ],
        columns=["Layer", "Basis", "Purpose"],
    )
    st.dataframe(method_df, use_container_width=True, hide_index=True)

    st.markdown("### Public sources reviewed")
    seen = set()
    for item in PUBLIC_OBSERVATIONS:
        if item["source"] not in seen:
            st.markdown(f"- {item['source']}")
            seen.add(item["source"])

    st.markdown("### Relevant prior consumer-research evidence")
    st.write(
        "In my Data Driven Marketing coursework, a sustainable-backpack preference study combined six semi-structured interviews with a 71-respondent cleaned survey, conjoint analysis and sustainability-based segmentation. A separate customer-analytics assignment used a 3,000-customer dataset for descriptive analysis, correlation, segmentation, retention inputs and segment-level CLV modelling."
    )

    st.markdown("### What this prototype does not claim")
    st.markdown(
        "- It does not claim access to Club Soda's GA4, CRM, Shopify, Meta Ads or email-platform data.\n"
        "- It does not claim that any proposed uplift has already been achieved.\n"
        "- It does not reproduce private customer data or infer sensitive attributes.\n"
        "- It is not affiliated with or commissioned by Club Soda."
    )

st.markdown(
    """
    <div class="footer">
    <b>Abhishek Kumar</b> · Independent portfolio case study · Built for demonstration of digital sales, marketing analytics and customer-journey thinking.<br>
    Public-site observations were reviewed from Club Soda's website. All numeric performance scenarios in this app are synthetic.
    </div>
    """,
    unsafe_allow_html=True,
)
