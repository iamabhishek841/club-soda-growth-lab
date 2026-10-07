Live Demo: https://club-soda-growth-lab.streamlit.app/
# Club Soda Growth Lab

**Independent digital sales, customer journey and conversion optimisation portfolio prototype**

This project shows how I would approach the **Part-Time Digital Sales and Marketing Specialist** brief for Club Soda: connect acquisition, event discovery, booking, post-event engagement and the upcoming online shop into one measurable growth system.

> **Important:** This is an independent portfolio case study. It uses publicly available Club Soda website information and **synthetic demonstration data**. I do not have access to Club Soda's internal analytics, CRM, ad accounts, customer data or sales performance.

## What the app demonstrates

The app is intentionally simple and business-facing:

- **Growth overview** — three priorities: event conversion, shop demand and repeat bookings
- **Website opportunities** — clear actions tied to a business benefit and metric
- **Funnel simulator** — illustrative impact of improving conversion at key stages
- **Campaign studio** — event, shop, recovery and repeat-booking campaign ideas
- **Customer journey** — practical behaviour-based next steps and lifecycle follow-up
- **90-day action plan** — measure, test and scale

Technical measurement detail is kept secondary so the main experience stays easy to understand for a business user.

## Core idea

Instead of treating social content, paid advertising, email, the website and the shop as separate tasks, the prototype treats them as one connected journey:

**Discover → Explore → Consider → Book / Buy → Experience → Return**

Every recommendation is tied to a measurable behaviour and a decision metric.

## Why this is relevant to my background

My MSc Business Analytics work includes **Data Driven Marketing** and consumer analytics. In a sustainable-backpack preference study, my group combined:

- 6 semi-structured consumer interviews
- a cleaned survey with 71 valid respondents
- conjoint analysis
- segment-level preference analysis

A separate marketing mix modelling project used **200 weekly observations** with geometric adstock, Hill saturation and trend/seasonality controls, then extended the analysis with Google Meridian Bayesian MMM to examine channel contribution, ROI and response curves.

This project applies that evidence-first approach to a live digital-growth problem.

## Public Club Soda observations used

The app separates what is publicly observable from what I am proposing.

Public pages reviewed:

- https://www.clubsoda.ie/
- https://www.clubsoda.ie/events/
- https://www.clubsoda.ie/shop/
- https://www.clubsoda.ie/events/faq-s/
- https://www.clubsoda.ie/terms-of-service/

Examples of source-backed observations include:

- Club Soda promotes ticketed events across multiple Irish locations and age groups.
- Website registration is part of the event booking flow and booking confirmation is sent by email.
- The public Club Soda Shop page is currently marked **Coming Soon** and points users toward newsletter / social updates.
- Club Soda describes post-event connection tools including a 7-day social group and a mutual-match process.
- The brand proposition is strongly centred on real-life connection, confidence, friendship and a welcoming experience.

Everything beyond those observations is presented as an **independent proposal** or a **synthetic scenario**.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Push this repository to GitHub.
2. In Streamlit Community Cloud choose **New app**.
3. Select the repository and branch.
4. Set the main file path to `app.py`.
5. Deploy. No secrets are required.

## Repository structure

```text
club-soda-growth-lab/
├── app.py
├── src/
│   ├── content.py
│   └── growth_model.py
├── tests/
│   └── test_growth_model.py
├── .streamlit/
│   └── config.toml
├── requirements.txt
├── LICENSE
└── README.md
```

## Design principles

1. **No invented company results** — commercial numbers are explicitly synthetic.
2. **Behaviour before vanity metrics** — optimise booking, repeat use and qualified demand, not impressions alone.
3. **Segmentation based on observable behaviour** — avoid unnecessary personal inference.
4. **One hypothesis, one primary metric** — make experiments interpretable.
5. **Owned audience matters** — connect events, lifecycle messaging and the future shop.
6. **Uplifts are relative, not percentage points** — simulator improvement controls apply relative changes to the selected funnel rates.

## Builder

**Abhishek Kumar**  
MSc Business Analytics, Maynooth University  
GitHub: https://github.com/iamabhishek841  
LinkedIn: https://www.linkedin.com/in/iamabhishek841

---

Club Soda is a third-party business and is not affiliated with this repository. Brand names are referenced only to explain the independent portfolio case study.
