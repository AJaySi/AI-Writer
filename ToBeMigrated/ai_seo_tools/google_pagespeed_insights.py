import requests
import streamlit as st
import json
import pandas as pd
import plotly.express as px
from tenacity import retry, stop_after_attempt, wait_random_exponential
from datetime import datetime

def run_pagespeed(url, api_key=None, strategy='DESKTOP', locale='en'):
    """Fetches and processes PageSpeed Insights data."""
    serviceurl = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed'
    base_url = f"{serviceurl}?url={url}&strategy={strategy}&locale={locale}&category=performance&category=accessibility&category=best-practices&category=seo"
    
    if api_key:
        base_url += f"&key={api_key}"

    try:
        response = requests.get(base_url)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching PageSpeed Insights data: {e}")
        return None

def display_results(data):
    """Presents PageSpeed Insights data in a user-friendly format."""
    st.subheader("PageSpeed Insights Report")

    # Extract scores from the PageSpeed Insights data
    scores = {
        "Performance": data['lighthouseResult']['categories']['performance']['score'] * 100,
        "Accessibility": data['lighthouseResult']['categories']['accessibility']['score'] * 100,
        "SEO": data['lighthouseResult']['categories']['seo']['score'] * 100,
        "Best Practices": data['lighthouseResult']['categories']['best-practices']['score'] * 100
    }

    descriptions = {
        "Performance": data['lighthouseResult']['categories']['performance'].get('description', "This score represents Google's assessment of your page's speed. A higher percentage indicates better performance."),
        "Accessibility": data['lighthouseResult']['categories']['accessibility'].get('description', "This score evaluates how accessible your page is to users with disabilities. A higher percentage means better accessibility."),
        "SEO": data['lighthouseResult']['categories']['seo'].get('description', "This score measures how well your page is optimized for search engines. A higher percentage indicates better SEO practices."),
        "Best Practices": data['lighthouseResult']['categories']['best-practices'].get('description', "This score reflects how well your page follows best practices for web development. A higher percentage signifies adherence to best practices.")
    }

    for category, score in scores.items():
        st.metric(label=f"Overall {category} Score", value=f"{score:.0f}%", help=descriptions[category])

    # Display additional metrics
    st.subheader("Additional Metrics")
    additional_metrics = {
        "First Contentful Paint (FCP)": data['lighthouseResult']['audits']['first-contentful-paint']['displayValue'],
        "Largest Contentful Paint (LCP)": data['lighthouseResult']['audits']['largest-contentful-paint']['displayValue'],
        "Time to Interactive (TTI)": data['lighthouseResult']['audits']['interactive']['displayValue'],
        "Total Blocking Time (TBT)": data['lighthouseResult']['audits']['total-blocking-time']['displayValue'],
        "Cumulative Layout Shift (CLS)": data['lighthouseResult']['audits']['cumulative-layout-shift']['displayValue']
    }

    st.table(pd.DataFrame(additional_metrics.items(), columns=["Metric", "Value"]))

    # Display Network Requests
    st.subheader("Network Requests")
    if 'network-requests' in data['lighthouseResult']['audits']:
        network_requests = [
            {
                "End Time": item.get("endTime", "N/A"),
                "Start Time": item.get("startTime", "N/A"),
                "Transfer Size (MB)": round(item.get("transferSize", 0) / 1048576, 2),
                "Resource Size (MB)": round(item.get("resourceSize", 0) / 1048576, 2),
                "URL": item.get("url", "N/A")
            }
            for item in data["lighthouseResult"]["audits"]["network-requests"]["details"]["items"]
            if item.get("transferSize", 0) > 100000 or item.get("resourceSize", 0) > 100000
        ]
        if network_requests:
            st.dataframe(pd.DataFrame(network_requests), use_container_width=True)
        else:
            st.write("No significant network requests found.")

    # Display Mainthread Work Breakdown
    st.subheader("Mainthread Work Breakdown")
    if 'mainthread-work-breakdown' in data['lighthouseResult']['audits']:
        mainthread_data = [
            {"Process": item.get("groupLabel", "N/A"), "Duration (ms)": item.get("duration", "N/A")}
            for item in data["lighthouseResult"]["audits"]["mainthread-work-breakdown"]["details"]["items"] if item.get("duration", "N/A") != "N/A"
        ]
        if mainthread_data:
            fig = px.bar(pd.DataFrame(mainthread_data), x="Process", y="Duration (ms)", title="Mainthread Work Breakdown", labels={"Process": "Process", "Duration (ms)": "Duration (ms)"})
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("No significant main thread work breakdown data found.")

    # Display other metrics
    metrics = [
        ("Use of Passive Event Listeners", 'uses-passive-event-listeners', ["URL", "Code Line"]),
        ("DOM Size", 'dom-size', ["Score", "DOM Size"]),
        ("Offscreen Images", 'offscreen-images', ["URL", "Total Bytes", "Wasted Bytes", "Wasted Percentage"]),
        ("Critical Request Chains", 'critical-request-chains', ["URL", "Start Time", "End Time", "Transfer Size", "Chain"]),
        ("Total Bytes Weight", 'total-byte-weight', ["URL", "Total Bytes"]),
        ("Render Blocking Resources", 'render-blocking-resources', ["URL", "Total Bytes", "Wasted Milliseconds"]),
        ("Use of Rel Preload", 'uses-rel-preload', ["URL", "Wasted Milliseconds"])
    ]

    for metric_title, audit_key, columns in metrics:
        st.subheader(metric_title)
        if audit_key in data['lighthouseResult']['audits']:
            details = data['lighthouseResult']['audits'][audit_key].get("details", {}).get("items", [])
            if details:
                st.table(pd.DataFrame(details, columns=columns))
            else:
                st.write(f"No significant {metric_title.lower()} data found.")

def google_pagespeed_insights():
    st.markdown("<h1 style='text-align: center; color: #1565C0;'>PageSpeed Insights Analyzer</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Get detailed insights into your website's performance! Powered by Google PageSpeed Insights <a href='https://developer.chrome.com/docs/lighthouse/overview/'>[Learn More]</a></h3>", unsafe_allow_html=True)

    # User Input
    with st.form("pagespeed_form"):
        url = st.text_input("Enter Website URL", placeholder="https://www.example.com")
        api_key = st.text_input("Enter Google API Key (Optional)", placeholder="Your API Key", help="Get your API key here: [https://developers.google.com/speed/docs/insights/v5/get-started#key]")
        device = st.selectbox("Choose Device", ["Mobile", "Desktop"])
        locale = st.selectbox("Choose Locale", ["en", "fr", "es", "de", "ja"])
        categories = st.multiselect("Select Categories to Analyze", ['PERFORMANCE', 'ACCESSIBILITY', 'BEST_PRACTICES', 'SEO'], default=['PERFORMANCE', 'ACCESSIBILITY', 'BEST_PRACTICES', 'SEO'])

        submitted = st.form_submit_button("Analyze")

    if submitted:
        if not url:
            st.error("Please provide the website URL.")
        else:
            strategy = 'mobile' if device == "Mobile" else 'desktop'
            data = run_pagespeed(url, api_key, strategy=strategy, locale=locale)
            if data:
                display_results(data)
            else:
                st.error("Failed to retrieve PageSpeed Insights data.")
