# Club Soda Growth Lab

**Independent digital sales, customer journey and conversion optimisation portfolio prototype**

This project shows how I would approach the **Part-Time Digital Sales and Marketing Specialist** brief for Club Soda: connect acquisition, event discovery, booking, post-event engagement and the upcoming online shop into one measurable growth system.

> **Important:** This is an independent portfolio case study. It uses publicly available Club Soda website information and **synthetic demonstration data**. I do not have access to Club Soda's internal analytics, CRM, ad accounts, customer data or sales performance.

## What the app demonstrates

- Public-site customer journey audit
- End-to-end measurement blueprint
- Interactive booking and revenue funnel simulator
- Behavioural segmentation and lifecycle messaging
- Campaign-to-landing-page planning
- Short-form content storyboard
- Shop waitlist / launch strategy
- CRO experiment backlog
- Approximate A/B-test sizing
- 90-day execution roadmap and weekly growth scorecard

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

A separate customer-analytics assignment used a **3,000-customer** dataset for descriptive analysis, correlation, customer segmentation, retention inputs and segment-level CLV modelling.

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
source .venv/bin/activate  # Windows: .venv\Scripts\activate
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

## Builder

**Abhishek Kumar**  
MSc Business Analytics, Maynooth University  
GitHub: https://github.com/iamabhishek841  
LinkedIn: https://www.linkedin.com/in/iamabhishek841

---

Club Soda is a third-party business and is not affiliated with this repository. Brand names are referenced only to explain the independent portfolio case study.
