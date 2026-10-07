from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src.content import MEASUREMENT_EVENTS
from src.growth_model import FunnelInputs, FunnelUplifts, compare_scenarios

st.set_page_config(page_title="Club Soda Growth Lab", page_icon="↗", layout="wide", initial_sidebar_state="expanded")

CUSTOM_CSS = """
<style>
.block-container{padding-top:1.55rem;padding-bottom:3rem;max-width:1220px}h1,h2,h3{letter-spacing:-.025em}[data-testid="stSidebar"]{border-right:1px solid rgba(120,120,120,.12)}
.hero{padding:2.15rem 2.25rem;border:1px solid rgba(100,100,130,.16);border-radius:24px;background:linear-gradient(135deg,rgba(124,58,237,.12),rgba(20,184,166,.09));margin-bottom:1.15rem}.hero-kicker{font-size:.78rem;font-weight:800;text-transform:uppercase;letter-spacing:.12em;opacity:.62}.hero-title{font-size:2.55rem;line-height:1.03;font-weight:820;margin:.45rem 0 .55rem}.hero-copy{font-size:1.05rem;line-height:1.65;max-width:900px;opacity:.86}.role-badge{display:inline-block;margin-top:1rem;padding:.42rem .72rem;border-radius:999px;background:rgba(255,255,255,.72);border:1px solid rgba(100,100,130,.14);font-size:.84rem;font-weight:700}.micro-note{font-size:.76rem;opacity:.58;margin:.35rem 0 1.15rem}
.focus-card,.opportunity-card,.step-card{padding:1.05rem 1.08rem;border:1px solid rgba(120,120,120,.16);border-radius:18px;background:rgba(255,255,255,.76);height:100%}.card-kicker{font-size:.70rem;font-weight:800;text-transform:uppercase;letter-spacing:.08em;opacity:.54;margin-bottom:.42rem}.card-title{font-size:1.08rem;line-height:1.2;font-weight:780;margin-bottom:.45rem}.card-copy{font-size:.91rem;line-height:1.55;opacity:.78}.card-metric{font-size:.80rem;font-weight:700;margin-top:.75rem;opacity:.72}
.flow-wrap{display:flex;gap:.55rem;align-items:stretch;margin:.55rem 0 1rem}.flow-box{flex:1;padding:.82rem .8rem;border:1px solid rgba(120,120,120,.14);border-radius:14px;background:rgba(124,58,237,.045);text-align:center;min-width:0}.flow-box b{font-size:.91rem}.flow-box span{display:block;margin-top:.22rem;font-size:.73rem;opacity:.60;line-height:1.35}.kpi-card{padding:.85rem .95rem;border:1px solid rgba(120,120,120,.14);border-radius:15px;background:rgba(255,255,255,.70);min-height:88px}.kpi-label{font-size:.68rem;font-weight:800;text-transform:uppercase;letter-spacing:.07em;opacity:.50}.kpi-value{font-size:.98rem;font-weight:760;margin-top:.32rem;line-height:1.2}.impact-box{padding:1rem 1.1rem;border-radius:16px;background:linear-gradient(135deg,rgba(20,184,166,.09),rgba(124,58,237,.06));border:1px solid rgba(20,184,166,.16)}.impact-grid{display:grid;grid-template-columns:1fr 1fr;gap:.65rem;margin-top:.9rem}.impact-stat{padding:.82rem .9rem;border:1px solid rgba(120,120,120,.15);border-radius:15px;background:rgba(255,255,255,.72)}.impact-stat.accent{background:rgba(109,93,251,.07);border-color:rgba(109,93,251,.18)}.impact-stat.wide{grid-column:1/-1;background:linear-gradient(135deg,rgba(20,184,166,.08),rgba(109,93,251,.05));border-color:rgba(20,184,166,.15)}.impact-stat-label{font-size:.69rem;font-weight:800;text-transform:uppercase;letter-spacing:.06em;opacity:.52}.impact-stat-value{font-size:1.75rem;font-weight:780;letter-spacing:-.035em;line-height:1.1;margin-top:.28rem}.impact-stat-delta{display:inline-block;margin-top:.38rem;padding:.16rem .43rem;border-radius:999px;background:rgba(22,163,74,.10);color:#16834a;font-size:.72rem;font-weight:800}.impact-note{font-size:.71rem;line-height:1.45;opacity:.52;margin-top:.65rem}.phase-card{padding:1.05rem;border:1px solid rgba(120,120,120,.15);border-radius:17px;min-height:265px;background:rgba(255,255,255,.74)}.phase-title{font-size:1.02rem;font-weight:800;margin-bottom:.2rem}.section-intro{max-width:900px;font-size:.96rem;line-height:1.55;opacity:.80;margin-bottom:1rem}.footer{margin-top:2.6rem;padding-top:1rem;border-top:1px solid rgba(120,120,120,.14);font-size:.80rem;opacity:.62}
@media(max-width:900px){.flow-wrap{display:grid;grid-template-columns:1fr 1fr}.hero-title{font-size:2rem}}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

def money(value: float) -> str: return f"€{value:,.0f}"
def number(value: float) -> str: return f"{value:,.0f}"

with st.sidebar:
    st.markdown("### Club Soda Growth Lab")
    st.caption("Practical digital sales & growth case study")
    section = st.radio("Explore", ["Growth overview","Website opportunities","Funnel simulator","Campaign studio","Customer journey","90-day action plan"], label_visibility="collapsed")
    st.divider()
    st.markdown("**Built by Abhishek Kumar**")
    st.caption("MSc Business Analytics · consumer research · growth analytics")
    st.markdown("[Live app](https://club-soda-growth-lab.streamlit.app/) · [View source](https://github.com/iamabhishek841/club-soda-growth-lab)")
    st.markdown("[LinkedIn](https://www.linkedin.com/in/iamabhishek841)")
    with st.expander("About this case study"):
        st.caption("Independent portfolio work based on public Club Soda website information. Any performance numbers shown in the simulator are synthetic demonstration inputs, not Club Soda results.")
        st.markdown("Public pages reviewed: [Home](https://www.clubsoda.ie/) · [Events](https://www.clubsoda.ie/events/) · [Shop](https://www.clubsoda.ie/shop/) · [FAQ](https://www.clubsoda.ie/events/faq-s/)")

st.markdown("""<div class="hero"><div class="hero-kicker">Club Soda · Digital sales & marketing case study</div><div class="hero-title">Turn more interest into bookings, sales and repeat customers.</div><div class="hero-copy">A practical growth plan showing how I would connect social content, the website, event booking, email follow-up and the upcoming shop into one simple, measurable customer journey.</div><div class="role-badge">Built specifically for the Digital Sales &amp; Marketing Specialist role</div></div>""", unsafe_allow_html=True)
st.markdown('<div class="micro-note">Independent portfolio case study · public website information · synthetic simulator inputs</div>', unsafe_allow_html=True)

if section == "Growth overview":
    st.subheader("Where I would focus first")
    st.markdown('<div class="section-intro">The role is about more than posting content. The biggest opportunity is to make each step — discovery, booking, follow-up and the shop — work together toward a measurable business outcome.</div>', unsafe_allow_html=True)
    cols=st.columns(3)
    focus=[("1 · Event conversion","Convert more event interest","Help the right visitor find a relevant event quickly, reduce hesitation and make the path to booking clearer.","Measure: event page → checkout → booking"),("2 · Shop launch","Build demand before launch","Use a shop-specific waitlist and simple launch sequence to learn what people want before the store goes live.","Measure: waitlist → launch engagement → first purchase"),("3 · Retention","Create more repeat customers","Use post-event communication to recommend the next relevant event instead of ending the relationship after one booking.","Measure: 30/60-day repeat booking")]
    for col,(kicker,title,copy,metric) in zip(cols,focus):
        with col: st.markdown(f"<div class='focus-card'><div class='card-kicker'>{kicker}</div><div class='card-title'>{title}</div><div class='card-copy'>{copy}</div><div class='card-metric'>{metric}</div></div>", unsafe_allow_html=True)

    st.markdown("### See the value of improving the journey")
    st.markdown('<div class="section-intro">Small conversion gains can create more bookings without more traffic. Adjust the slider to see an illustrative 1,000-visitor scenario. The same relative uplift is applied to both checkout-start and checkout-completion rates.</div>', unsafe_allow_html=True)
    chart_col, impact_col = st.columns([1.35, 1])
    with impact_col:
        home_uplift = st.slider(
            "Relative uplift at each checkout stage",
            0,
            20,
            10,
            step=1,
            format="%d%%",
            key="home_conversion_uplift",
            help="Applies the same relative uplift to checkout-start and checkout-completion rates. For example, 10% changes a 16% rate to 17.6%, not 26%.",
        ) / 100
        home_result = compare_scenarios(
            FunnelInputs(
                monthly_visitors=1000,
                event_view_rate=0.42,
                checkout_start_rate=0.16,
                purchase_completion_rate=0.62,
                average_order_value=32.0,
                repeat_booking_rate=0.18,
            ),
            FunnelUplifts(
                event_view_uplift=0.0,
                checkout_start_uplift=home_uplift,
                purchase_completion_uplift=home_uplift,
                repeat_booking_uplift=0.0,
            ),
        )
        hb, hi, hd = home_result["baseline"], home_result["improved"], home_result["delta"]
        st.markdown(
            f"""
            <div class="impact-grid">
              <div class="impact-stat">
                <div class="impact-stat-label">Current bookings</div>
                <div class="impact-stat-value">{number(hb["Purchases"])}</div>
              </div>
              <div class="impact-stat accent">
                <div class="impact-stat-label">Improved bookings</div>
                <div class="impact-stat-value">{number(hi["Purchases"])}</div>
                <div class="impact-stat-delta">+{number(hd["Purchases"])} bookings</div>
              </div>
              <div class="impact-stat wide">
                <div class="impact-stat-label">Potential additional revenue</div>
                <div class="impact-stat-value">{money(hd["Revenue"])}</div>
              </div>
            </div>
            <div class="impact-note">Illustrative scenario only · synthetic inputs · not Club Soda performance data.</div>
            """,
            unsafe_allow_html=True,
        )

    with chart_col:
        home_chart = go.Figure()
        home_chart.add_trace(
            go.Bar(
                x=["Current journey"],
                y=[hb["Purchases"]],
                text=[f'{number(hb["Purchases"])} bookings'],
                textposition="outside",
                marker_color="#D8D6E4",
                hovertemplate="Current journey: %{y:.0f} bookings<extra></extra>",
            )
        )
        home_chart.add_trace(
            go.Bar(
                x=["Improved journey"],
                y=[hi["Purchases"]],
                text=[f'{number(hi["Purchases"])} bookings'],
                textposition="outside",
                marker_color="#6D5DFB",
                hovertemplate="Improved journey: %{y:.0f} bookings<extra></extra>",
            )
        )
        home_chart.update_layout(
            height=290,
            margin=dict(l=8, r=8, t=24, b=8),
            yaxis_title="Bookings",
            xaxis_title="",
            showlegend=False,
            bargap=0.38,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(size=12, color="#34333D"),
            yaxis=dict(
                gridcolor="rgba(100,100,120,.10)",
                zeroline=False,
                rangemode="tozero",
                range=[0, max(hi["Purchases"], hb["Purchases"]) * 1.28],
                title_standoff=8,
            ),
            xaxis=dict(showgrid=False, tickfont=dict(color="#6B6874")),
        )
        st.plotly_chart(home_chart, use_container_width=True, config={"displayModeBar": False})

    st.markdown("### One connected growth system")
    st.markdown("""<div class="flow-wrap"><div class="flow-box"><b>Discover</b><span>Social, Meta, TikTok, search</span></div><div class="flow-box"><b>Explore</b><span>Relevant event / product page</span></div><div class="flow-box"><b>Convert</b><span>Booking or purchase</span></div><div class="flow-box"><b>Follow up</b><span>Email + post-event journey</span></div><div class="flow-box"><b>Return</b><span>Next event or shop purchase</span></div></div>""", unsafe_allow_html=True)
    st.markdown("### What I would watch every week")
    kpis=st.columns(5)
    for col,label,value in zip(kpis,["Traffic quality","Event engagement","Booking intent","Conversion","Retention"],["Qualified visits","Event-page CTR","Checkout starts","Completed bookings","Repeat bookings"]):
        with col: st.markdown(f"<div class='kpi-card'><div class='kpi-label'>{label}</div><div class='kpi-value'>{value}</div></div>", unsafe_allow_html=True)
    st.markdown("### Why this helps the business")
    st.markdown("""<div class="impact-box"><b>Simple goal:</b> understand where customers drop off, fix the biggest friction points first, and use the same measurement system to decide which campaigns, pages and follow-ups are worth scaling.</div>""", unsafe_allow_html=True)

elif section == "Website opportunities":
    st.subheader("Four practical opportunities from the current customer journey")
    st.markdown('<div class="section-intro">These are deliberately simple: one visible opportunity, one action, one business measure.</div>', unsafe_allow_html=True)
    opportunities=[("Event discovery","Make relevance obvious sooner","Use location and age / event relevance earlier so visitors can reach the right event faster.","Business benefit: more qualified event-page visits","Primary measure: event-detail click-through rate"),("Event page → checkout","Reduce hesitation before booking","Make 'what to expect', key reassurance and the booking CTA easy to understand without adding clutter.","Business benefit: more checkout starts from the same traffic","Primary measure: begin-checkout rate"),("Shop pre-launch","Capture product demand now","Replace a generic 'coming soon' moment with a shop-specific waitlist that asks what visitors are interested in.","Business benefit: launch to an audience that already showed intent","Primary measure: qualified waitlist signup rate"),("Post-event follow-up","Turn attendance into another booking","Use feedback and next-event recommendations to build a repeat-booking loop after the event.","Business benefit: higher customer lifetime value","Primary measure: 30/60-day repeat booking rate")]
    for row in [opportunities[:2],opportunities[2:]]:
        cols=st.columns(2)
        for col,(kicker,title,copy,benefit,metric) in zip(cols,row):
            with col: st.markdown(f"<div class='opportunity-card'><div class='card-kicker'>{kicker}</div><div class='card-title'>{title}</div><div class='card-copy'>{copy}</div><div class='card-metric'>{benefit}</div><div class='card-metric'>{metric}</div></div>", unsafe_allow_html=True)
        st.write("")
    with st.expander("Measurement detail (for implementation)"):
        st.dataframe(pd.DataFrame(MEASUREMENT_EVENTS,columns=["Analytics event","What it means","Journey stage"]),use_container_width=True,hide_index=True)
        st.caption("Proposed event taxonomy only. This prototype does not claim that Club Soda currently tracks these events.")

elif section == "Funnel simulator":
    st.subheader("What could small conversion improvements mean commercially?")
    st.markdown('<div class="section-intro">Change the assumptions below to see how a better event journey could affect bookings and revenue. The numbers are illustrative — the purpose is to show the decision framework, not to predict Club Soda results.</div>', unsafe_allow_html=True)
    left,right=st.columns(2)
    with left:
        st.markdown("#### Current scenario")
        visitors=st.slider("Monthly website visitors",1000,50000,8000,step=500); event_view=st.slider("Visitors who reach an event / product page",5,80,42)/100; checkout_start=st.slider("Event views that start checkout",2,50,16)/100; purchase_complete=st.slider("Checkouts that complete",10,95,62)/100; aov=st.slider("Average order value (€)",10,120,32); repeat_rate=st.slider("30-day repeat booking rate",1,50,18)/100
    with right:
        st.markdown("#### Improvement scenario")
        event_uplift=st.slider("Improve event-page engagement",0,40,8)/100; checkout_uplift=st.slider("Improve checkout starts",0,40,10)/100; completion_uplift=st.slider("Improve checkout completion",0,40,12)/100; repeat_uplift=st.slider("Improve repeat bookings",0,50,15)/100
    result=compare_scenarios(FunnelInputs(monthly_visitors=visitors,event_view_rate=event_view,checkout_start_rate=checkout_start,purchase_completion_rate=purchase_complete,average_order_value=float(aov),repeat_booking_rate=repeat_rate),FunnelUplifts(event_view_uplift=event_uplift,checkout_start_uplift=checkout_uplift,purchase_completion_uplift=completion_uplift,repeat_booking_uplift=repeat_uplift))
    base,improved,delta=result["baseline"],result["improved"],result["delta"]
    st.markdown("### Illustrative business impact")
    m1,m2,m3,m4=st.columns(4); m1.metric("Current bookings",number(base["Purchases"])); m2.metric("Improved bookings",number(improved["Purchases"]),delta=f"+{number(delta['Purchases'])}"); m3.metric("Additional revenue",money(delta["Revenue"])); m4.metric("Additional repeat bookings",number(delta["Repeat bookings"]))
    labels=["Visitors","Event / product views","Checkout starts","Purchases"]; fig=go.Figure(); fig.add_trace(go.Funnel(name="Current scenario",y=labels,x=[base[x] for x in labels],textinfo="value+percent initial")); fig.add_trace(go.Funnel(name="Improved scenario",y=labels,x=[improved[x] for x in labels],textinfo="value+percent initial")); fig.update_layout(height=440,margin=dict(l=10,r=10,t=35,b=10),legend_title_text=""); st.plotly_chart(fig,use_container_width=True)
    st.markdown("""<div class="impact-box"><b>How I would use this:</b> identify the largest drop-off, choose one improvement, run a controlled test, and scale only when the data shows a meaningful commercial gain.</div>""", unsafe_allow_html=True)

elif section == "Campaign studio":
    st.subheader("Campaign ideas designed to end in a measurable action")
    st.markdown('<div class="section-intro">Content should not stop at engagement. Each campaign should have one audience, one message, one landing experience and one business outcome.</div>', unsafe_allow_html=True)
    campaign=st.selectbox("Choose an objective",["Fill an upcoming event","Launch the shop waitlist","Recover high-intent visitors","Drive repeat bookings"]); channel=st.selectbox("Primary channel",["Instagram / TikTok","Meta paid social","Email","Cross-channel"])
    plans={"Fill an upcoming event":{"hook":"Meet people in real life — not just through another app.","story":"Show the atmosphere, what to expect, who the event is for and the practical details that reduce uncertainty.","landing":"Send people directly to the relevant event page rather than a generic homepage.","follow":"Retarget high-intent visitors and follow up with people who opted in but did not book.","metric":"Completed event bookings"},"Launch the shop waitlist":{"hook":"Be first to know when Club Soda's shop goes live.","story":"Preview product categories and ask people what they are most interested in buying.","landing":"A simple product-interest waitlist, not a generic newsletter form.","follow":"Product reveal → early access → launch reminder → first-purchase follow-up.","metric":"Waitlist-to-purchase conversion"},"Recover high-intent visitors":{"hook":"Still thinking about joining? Here is exactly what to expect.","story":"Address the questions that may be stopping a visitor from completing a booking.","landing":"Return them to the relevant event or checkout journey with minimal friction.","follow":"One useful reminder rather than repeated generic messaging.","metric":"Recovered bookings"},"Drive repeat bookings":{"hook":"Ready for your next Club Soda event?","story":"Use the previous event as context and recommend the next relevant option.","landing":"A curated event recommendation based on observable behaviour and location relevance.","follow":"Feedback → recommendation → reminder → booking.","metric":"30/60-day repeat booking rate"}}
    p=plans[campaign]; st.markdown(f"**Channel:** {channel}"); c1,c2=st.columns(2)
    with c1: st.markdown("#### Message"); st.markdown(f"**Hook**  \n{p['hook']}"); st.markdown(f"**Creative direction**  \n{p['story']}")
    with c2: st.markdown("#### Conversion path"); st.markdown(f"**Landing experience**  \n{p['landing']}"); st.markdown(f"**Follow-up**  \n{p['follow']}"); st.markdown(f"**Business measure**  \n{p['metric']}")
    st.markdown("### Simple short-form content structure")
    st.dataframe(pd.DataFrame([["0–3 sec","Hook","Give one reason to stop scrolling"],["3–8 sec","Show the experience","Real setting, people, movement, atmosphere"],["8–14 sec","Reduce uncertainty","Who it is for + what to expect"],["14–20 sec","One action","Book, join waitlist or see the relevant event"]],columns=["Timing","Purpose","What the viewer should understand"]),use_container_width=True,hide_index=True)

elif section == "Customer journey":
    st.subheader("Different customers need different next steps")
    st.markdown('<div class="section-intro">I would keep segmentation practical and behaviour-based: what did the person do, what is the likely next useful step, and what business outcome are we trying to create?</div>', unsafe_allow_html=True)
    segments=[("New visitor","Browses but has not booked","Explain what Club Soda is and show relevant events","See events near me"),("High-intent visitor","Views the same event / starts checkout","Remove the last reasons not to book","Finish booking"),("Booked attendee","Has an upcoming or recent event","Build confidence, then continue the relationship","Prepare / give feedback"),("Returning customer","Has booked before","Recommend the next relevant event or shop offer","Book again")]
    cols=st.columns(4)
    for col,(title,signal,goal,cta) in zip(cols,segments):
        with col: st.markdown(f"<div class='step-card'><div class='card-title'>{title}</div><div class='card-copy'><b>Signal:</b> {signal}<br><br><b>Next step:</b> {goal}</div><div class='card-metric'>CTA: {cta}</div></div>", unsafe_allow_html=True)
    st.markdown("### Example post-booking lifecycle")
    st.dataframe(pd.DataFrame([["Immediately","Booking confirmation","Reduce uncertainty","Event details + what to expect"],["2 days before","Event reminder","Increase attendance","Practical reminder + confidence cues"],["1 day after","Follow-up","Continue engagement","Feedback + post-event tools"],["4–7 days after","Next-event recommendation","Create repeat booking","Relevant event recommendation"]],columns=["When","Touchpoint","Business goal","Content"]),use_container_width=True,hide_index=True)

elif section == "90-day action plan":
    st.subheader("First 90 days: measure → test → scale")
    st.markdown('<div class="section-intro">The first goal would be to create a simple measurement baseline, then test a small number of high-impact changes before scaling what works.</div>', unsafe_allow_html=True)
    phases=[("Days 1–30","Measure",["Map social → website → event page → checkout → booking","Set clear UTM and analytics naming","Baseline conversion and repeat-booking metrics","Identify the biggest event-page and checkout drop-offs"]),("Days 31–60","Test",["Run one event landing-page / reassurance test","Create shop waitlist MVP","Launch one measurable short-form campaign","Build simple post-event recommendation follow-up"]),("Days 61–90","Scale",["Scale the best-performing campaign / landing journey","Improve lifecycle segmentation","Connect event audiences to the shop launch","Create a weekly growth scorecard for decisions"])]
    cols=st.columns(3)
    for col,(period,title,items) in zip(cols,phases):
        bullets="".join(f"<li>{item}</li>" for item in items)
        with col: st.markdown(f"<div class='phase-card'><div class='card-kicker'>{period}</div><div class='phase-title'>{title}</div><ul class='card-copy'>{bullets}</ul></div>", unsafe_allow_html=True)
    st.markdown("### What success should look like")
    st.markdown("""<div class="impact-box"><b>A simple operating system for growth:</b> everyone can see where demand comes from, where customers drop off, which campaigns create bookings, what improves repeat behaviour, and what should be tested next.</div>""", unsafe_allow_html=True)
    st.markdown("### Relevant capability I bring")
    st.write("My MSc Business Analytics work includes Data Driven Marketing, consumer research, conjoint analysis, segmentation, marketing mix modelling and experimentation. I would bring that analytical discipline into a hands-on marketing role without treating the business like an academic exercise.")

st.markdown("""<div class="footer"><b>Abhishek Kumar</b> · Independent portfolio case study for the Club Soda Digital Sales &amp; Marketing Specialist opportunity. Public-site observations are separated from proposed strategy, and all simulator performance numbers are synthetic.</div>""", unsafe_allow_html=True)
