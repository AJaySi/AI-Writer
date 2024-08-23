import requests
import streamlit as st
import json
import pandas as pd
import base64
import plotly.express as px
import time
from datetime import datetime

def run_pagespeed(url, api_key=None, strategy='DESKTOP', locale='en'):
    """Fetches and processes PageSpeed Insights data."""

    serviceurl = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed'
    base_url = f"{serviceurl}?url={url}&strategy={strategy}&locale={locale}&category=performance&category=accessibility&category=best-practices&category=seo"

    if api_key:
        base_url += f"&key={api_key}"

    #if categories:
    #    base_url += f"&category={','.join(categories)}" 

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
    # Credits: https://www.danielherediamejias.com/pagespeed-insights-api-with-python/
    st.subheader("PageSpeed Insights Report")

    # Extract scores from the PageSpeed Insights data
    performance_overall_score = data['lighthouseResult']['categories']['performance']['score'] * 100
    accessibility_overall_score = data['lighthouseResult']['categories']['accessibility']['score'] * 100
    seo_overall_score = data['lighthouseResult']['categories']['seo']['score'] * 100
    best_practices_score = data['lighthouseResult']['categories']['best-practices']['score'] * 100

    col1, col2 = st.columns([5, 5])
    with col1:
        # Display metrics with improved help messages
        st.subheader("Performance")
        category_description = data['lighthouseResult']['categories']['performance'].get('description', "No description available")
        if "No description available" in category_description:
            category_description = "This score represents Google's assessment of your page's speed. A higher percentage indicates better performance."
        st.metric(
            label="Overall Performance Score",
            value=f"{performance_overall_score:.0f}%",
            help=category_description
        )
    with col2:
        st.subheader("Accessibility")
        category_description = data['lighthouseResult']['categories']['accessibility'].get('description', "No description available")
        if "No description available" in category_description:
            category_description = "This score evaluates how accessible your page is to users with disabilities. A higher percentage means better accessibility."
        st.metric(
            label="Overall Accessibility Score",
            value=f"{accessibility_overall_score:.0f}%",
            help=category_description
        )

    col1, col2 = st.columns([5, 5])
    with col1:
        st.subheader("SEO")
        category_description = data['lighthouseResult']['categories']['seo'].get('description', "No description available")
        if "No description available" in category_description:
            category_description = "This score measures how well your page is optimized for search engines. A higher percentage indicates better SEO practices."
        st.metric(
            label="Overall SEO Score",
            value=f"{seo_overall_score:.0f}%",
            help=category_description
        )

    with col2:
        st.subheader("Best Practises")
        category_description = data['lighthouseResult']['categories']['best-practices'].get('description', "No description available")
        if "No description available" in category_description:
            category_description = "This score reflects how well your page follows best practices for web development. A higher percentage signifies adherence to best practices."
        st.metric(
            label="Overall Best Practices Score",
            value=f"{best_practices_score:.0f}%",
            help=category_description
        )
    
    # Display additional metrics from the article
    st.subheader("Additional Metrics")
    additional_metrics = []
    for metric_name, metric_value in {
        "First Contentful Paint (FCP)": data['lighthouseResult']['audits']['first-contentful-paint']['displayValue'],
        "Largest Contentful Paint (LCP)": data['lighthouseResult']['audits']['largest-contentful-paint']['displayValue'],
        "Time to Interactive (TTI)": data['lighthouseResult']['audits']['interactive']['displayValue'],
        "Total Blocking Time (TBT)": data['lighthouseResult']['audits']['total-blocking-time']['displayValue'],
        "Cumulative Layout Shift (CLS)": data['lighthouseResult']['audits']['cumulative-layout-shift']['displayValue']
    }.items():
        additional_metrics.append({"Metric": metric_name, "Value": metric_value})
    st.table(pd.DataFrame(additional_metrics))

    # 2.4.1.- Network Requests
    st.subheader("Network Requests")
    if 'network-requests' in data['lighthouseResult']['audits']:
        listrequests = []
        for item in data["lighthouseResult"]["audits"]["network-requests"]["details"]["items"]:
            endtime = item.get("endTime", "N/A")
            starttime = item.get("startTime", "N/A")
            transfersize = item.get("transferSize", "N/A")
            resourcesize = item.get("resourceSize", "N/A")
            url = item.get("url", "N/A")

            # Filter for significant requests (adjust thresholds as needed)
            if transfersize != "N/A" and transfersize > 100000 or resourcesize != "N/A" and resourcesize > 100000:
                # Convert bytes to MBs
                transfersize_mb = round(transfersize / 1048576, 2)  # 1 MB = 1048576 bytes
                resourcesize_mb = round(resourcesize / 1048576, 2)
                list1 = [endtime, starttime, transfersize_mb, resourcesize_mb, url]
                listrequests.append(list1)

        if listrequests:
            st.dataframe(pd.DataFrame(listrequests, columns=["End Time", "Start Time", "Transfer Size (MB)", "Resource Size (MB)", "URL"]), use_container_width=True)
        else:
            st.write("No significant network requests found.")

    # 2.4.2.- Mainthread Work Breakdown
    st.subheader("Mainthread Work Breakdown")
    if 'mainthread-work-breakdown' in data['lighthouseResult']['audits']:
        mainthread_score = data["lighthouseResult"]["audits"]["mainthread-work-breakdown"]["score"]
        mainthread_duration = data["lighthouseResult"]["audits"]["mainthread-work-breakdown"]["displayValue"]
        st.write(f"Score: {mainthread_score}, Duration: {mainthread_duration}")

        # Extract data for visualization
        breakdown_data = []
        for item in data["lighthouseResult"]["audits"]["mainthread-work-breakdown"]["details"]["items"]:
            duration = item.get("duration", "N/A")
            process = item.get("groupLabel", "N/A")
            if duration != "N/A":  # Only include non-N/A values
                breakdown_data.append({"Process": process, "Duration (ms)": duration})  # Make sure the column name is "Process"

        # Create a bar chart using Streamlit
        if breakdown_data:
            fig = px.bar(
                pd.DataFrame(breakdown_data),
                x="Process",  # Now using the "Process" column
                y="Duration (ms)",
                title="Mainthread Work Breakdown",
                labels={"Process": "Process", "Duration (ms)": "Duration (ms)"},
                hover_data=["Process", "Duration (ms)"]
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("No significant main thread work breakdown data found.")

    # 2.4.3.- Use of Passive Event Listeners
    st.subheader("Use of Passive Event Listeners")
    if 'uses-passive-event-listeners' in data['lighthouseResult']['audits']:
        event_listeners = data["lighthouseResult"]["audits"]["uses-passive-event-listeners"]["score"]
        st.write(f"Score: {event_listeners}")
        listevents = []
        for item in data["lighthouseResult"]["audits"]["uses-passive-event-listeners"]["details"]["items"]:
            url = item.get("url", "N/A")
            line = item.get("label", "N/A")
            if url != "N/A" and line != "N/A":
                list1 = [url, line]
                listevents.append(list1)
        if listevents:
            st.table(pd.DataFrame(listevents, columns=["URL", "Code Line"]))
        else:
            st.write("No significant passive event listener data found.")

    # 2.4.4.- Dom Size
    st.subheader("DOM Size")
    if 'dom-size' in data['lighthouseResult']['audits']:
        dom_size_score = data["lighthouseResult"]["audits"]["dom-size"]["score"]
        dom_size_elements = data["lighthouseResult"]["audits"]["dom-size"]["displayValue"]
        st.write(f"Score: {dom_size_score}, DOM Size: {dom_size_elements}")
        st.info("A large DOM can impact performance, especially for mobile devices. Consider optimizing your HTML structure and using techniques like lazy loading to improve page load times.")

    # 2.4.5.- OffScreen Images
    st.subheader("Offscreen Images")
    if 'offscreen-images' in data['lighthouseResult']['audits']:
        offscreen_images_score = data["lighthouseResult"]["audits"]["offscreen-images"]["score"]
        offscreen_images = data["lighthouseResult"]["audits"]["offscreen-images"]["displayValue"]
        st.write(f"Score: {offscreen_images_score}, Offscreen Images: {offscreen_images}")
        listoffscreenimages = []
        for item in data["lighthouseResult"]["audits"]["offscreen-images"]["details"]["items"]:
            url = item.get("url", "N/A")
            totalbytes = item.get("totalBytes", "N/A")
            wastedbytes = item.get("wastedBytes", "N/A")
            wastedpercent = item.get("wastedPercent", "N/A")
            if url != "N/A":
                list1 = [url, totalbytes, wastedbytes, wastedpercent]
                listoffscreenimages.append(list1)
        if listoffscreenimages:
            st.table(pd.DataFrame(listoffscreenimages, columns=["URL", "Total Bytes", "Wasted Bytes", "Wasted Percentage"]))
            st.info("Consider using lazy loading for offscreen images. This will delay their loading until they are visible in the viewport, improving initial page load times.")
        else:
            st.write("No significant offscreen image data found.")

    # 2.4.6.- Critical Requests Chains
    st.subheader("Critical Request Chains")
    if 'critical-request-chains' in data['lighthouseResult']['audits']:
        critical_requests = data["lighthouseResult"]["audits"]["critical-request-chains"]["displayValue"]
        st.write(f"Number of Critical Request Chains: {critical_requests}")
        listchains = []
        for keys in data["lighthouseResult"]["audits"]["critical-request-chains"]["details"]["chains"].keys():
            try: 
                for values in data["lighthouseResult"]["audits"]["critical-request-chains"]["details"]["chains"][keys]["children"].values():
                    url = values["request"]["url"]
                    startime = values["request"]["startTime"]
                    endtime = values["request"]["endTime"]
                    transfersize = values["request"]["transferSize"]
                    list1 = [url,startime,endtime,transfersize, keys]
                    listchains.append(list1)
            except:
                continue
        if listchains:
            st.table(pd.DataFrame(listchains, columns=["URL", "Start Time", "End Time", "Transfer Size", "Chain"]))
            st.info("Optimizing the critical request chains can significantly improve the loading time of your website.  Consider prioritizing essential resources and deferring non-critical ones.")
        else:
            st.write("No significant critical request chain data found.")

    # 2.4.7.- Total Bytes Weight
    st.subheader("Total Bytes Weight")
    if 'total-byte-weight' in data['lighthouseResult']['audits']:
        bytes_weight_score = data["lighthouseResult"]["audits"]["total-byte-weight"]["score"]
        bytes_weight = data["lighthouseResult"]["audits"]["total-byte-weight"]["displayValue"]
        st.write(f"Score: {bytes_weight_score}, Total Bytes Weight: {bytes_weight}")
        listbytes = []
        for item in data["lighthouseResult"]["audits"]["total-byte-weight"]["details"]["items"]:
            url = item.get("url", "N/A")
            bytes_total = item.get("totalBytes", "N/A")
            if url != "N/A":
                list1 = [url, bytes_total]
                listbytes.append(list1)
        if listbytes:
            st.table(pd.DataFrame(listbytes, columns=["URL", "Total Bytes"]))
            st.info("Reducing the total bytes weight of your website is crucial for improving performance, especially on mobile devices and for users with slower internet connections.")
        else:
            st.write("No significant total bytes weight data found.")

#    # 2.4.8.- Use of responsive images
#    st.subheader("Use of Responsive Images")
#    if 'uses-responsive-images' in data['lighthouseResult']['audits']:
#        responsive_images_score = data["lighthouseResult"]["audits"]["uses-responsive-images"]["score"]
#        responsive_image_savings = data["lighthouseResult"]["audits"]["uses-responsive-images"]["displayValue"]
#        st.write(f"Score: {responsive_images_score}, Potential Savings: {responsive_image_savings}")
#        listresponsivesavings = []
#        for item in data["lighthouseResult"]["audits"]["uses-responsive-images"]["details"]["items"]:
#            url = item.get("url", "N/A")
#            wastedbytes = item.get("wastedBytes", "N/A")
#            totalbytes = item.get("totalBytes", "N/A")
#            if url != "N/A":
#                list1 = [url, wastedbytes, totalbytes]
#                listresponsivesavings.append(list1)
#        if listresponsivesavings:
#            st.table(pd.DataFrame(listresponsivesavings, columns=["URL", "Wasted Bytes", "Total Bytes"]))
#            st.info("Serving images in different sizes based on the user's device screen size can significantly reduce download times and improve performance.")
#        else:
#            st.write("No significant responsive image data found.")

    # 2.4.9.- Render Blocking Resources
    st.subheader("Render Blocking Resources")
    if 'render-blocking-resources' in data['lighthouseResult']['audits']:
        blocking_resources_score = data["lighthouseResult"]["audits"]["render-blocking-resources"]["score"]
        # Handle potential missing 'displayValue'
        blocking_resoures_savings = data["lighthouseResult"]["audits"]["render-blocking-resources"].get("displayValue", "N/A")
        st.write(f"Score: {blocking_resources_score}, Potential Savings: {blocking_resoures_savings}")
        listblockingresources = []
        for item in data["lighthouseResult"]["audits"]["render-blocking-resources"]["details"]["items"]:
            url = item.get("url", "N/A")
            totalbytes = item.get("totalBytes", "N/A")
            wastedbytes = item.get("wastedMs", "N/A")
            if url != "N/A":
                list1 = [url, totalbytes, wastedbytes]
                listblockingresources.append(list1)
        if listblockingresources:
            st.table(pd.DataFrame(listblockingresources, columns=["URL", "Total Bytes", "Wasted Milliseconds"]))
            st.info("Render-blocking resources can delay the initial rendering of your page, making it appear slow to users.  Consider optimizing the loading of critical resources and deferring non-critical ones.")
        else:
            st.write("No significant render-blocking resource data found.")

    # 2.4.10.- Use of Rel Preload
    st.subheader("Use of Rel Preload")
    if 'uses-rel-preload' in data['lighthouseResult']['audits']:
        rel_preload_score = data["lighthouseResult"]["audits"]["uses-rel-preload"]["score"]
        rel_preload_savings = data["lighthouseResult"]["audits"]["uses-rel-preload"]["displayValue"]
        st.write(f"Score: {rel_preload_score}, Potential Savings: {rel_preload_savings}")
        listrelpreload = []
        for item in data["lighthouseResult"]["audits"]["uses-rel-preload"]["details"]["items"]:
            url = item.get("url", "N/A")
            wastedms = item.get("wastedMs", "N/A")
            if url != "N/A":
                list1 = [url, wastedms]
                listrelpreload.append(list1)
        if listrelpreload:
            st.table(pd.DataFrame(listrelpreload, columns=["URL", "Wasted Milliseconds"]))
            st.info("The `rel=preload` attribute can be used to prioritize loading essential resources, improving initial page load times.")
        else:
            st.write("No significant rel preload data found.")

    # 2.4.11.- Estimated Input Latency (DEPRECATED)
    st.subheader("Estimated Input Latency")
    if 'estimated-input-latency' in data['lighthouseResult']['audits']:
        eil_score = data["lighthouseResult"]["audits"]["estimated-input-latency"]["score"]
        eil_duration = data["lighthouseResult"]["audits"]["estimated-input-latency"]["displayValue"]
        st.write(f"Score: {eil_score}, Duration: {eil_duration}")

    # 2.4.12.- Redirects
    st.subheader("Redirects")
    if 'redirects' in data['lighthouseResult']['audits']:
        redirects_score = data["lighthouseResult"]["audits"]["redirects"]["score"]
        redirect_savings = data["lighthouseResult"]["audits"]["redirects"]["displayValue"]
        st.write(f"Score: {redirects_score}, Potential Savings: {redirect_savings}")
        listredirects = []
        for item in data["lighthouseResult"]["audits"]["redirects"]["details"]["items"]:
            url = item.get("url", "N/A")
            wastedms = item.get("wastedMs", "N/A")
            list1 = [url,wastedms]
            listredirects.append(list1)
        st.table(pd.DataFrame(listredirects, columns=["URL", "Wasted Milliseconds"]))

    # 2.4.13.- Unused JavaScript
    st.subheader("Unused JavaScript")
    if 'unused-javascript' in data['lighthouseResult']['audits']:
        unused_js_score = data["lighthouseResult"]["audits"]["unused-javascript"]["score"]
        unused_js_savings = data["lighthouseResult"]["audits"]["unused-javascript"]["displayValue"]
        st.write(f"Score: {unused_js_score}, Potential Savings: {unused_js_savings}")
        listunusedjavascript = []
        for item in data["lighthouseResult"]["audits"]["unused-javascript"]["details"]["items"]:
            url = item.get("url", "N/A")
            totalbytes = item.get("totalBytes", "N/A")
            wastedbytes = item.get("wastedBytes", "N/A")
            wastedpercentage= item.get("wastedPercent", "N/A")
            list1 = [url, totalbytes, wastedbytes, wastedpercentage]
            listunusedjavascript.append(list1)
        st.table(pd.DataFrame(listunusedjavascript, columns=["URL", "Total Bytes", "Wasted Bytes", "Wasted Percentage"]))

    # 2.4.14.- Total Blocking Time
    st.subheader("Total Blocking Time")
    if 'total-blocking-time' in data['lighthouseResult']['audits']:
        blocking_time_score = data["lighthouseResult"]["audits"]["total-blocking-time"]["score"]
        blocking_time_duration = data["lighthouseResult"]["audits"]["total-blocking-time"]["displayValue"]
        st.write(f"Score: {blocking_time_score}, Duration: {blocking_time_duration}")

    # 2.4.15.- First Meaningful Paint
    st.subheader("First Meaningful Paint")
    if 'first-meaningful-paint' in data['lighthouseResult']['audits']:
        fmp_score = data["lighthouseResult"]["audits"]["first-meaningful-paint"]["score"]
        fmp = data["lighthouseResult"]["audits"]["first-meaningful-paint"]["displayValue"]
        st.write(f"Score: {fmp_score}, Time: {fmp}")

    # 2.4.16.- Cumulative Layout Shift
    st.subheader("Cumulative Layout Shift")
    if 'cumulative-layout-shift' in data['lighthouseResult']['audits']:
        cls_score = data["lighthouseResult"]["audits"]["cumulative-layout-shift"]["score"]
        cls = data["lighthouseResult"]["audits"]["cumulative-layout-shift"]["displayValue"]
        st.write(f"Score: {cls_score}, Value: {cls}")

    # 2.4.17.- Network RTT
    st.subheader("Network RTT")
    if 'network-rtt' in data['lighthouseResult']['audits']:
        network_rtt = data["lighthouseResult"]["audits"]["network-rtt"]["displayValue"]
        st.write(f"Network RTT: {network_rtt}")

    # 2.4.18.- Speed Index
    st.subheader("Speed Index")
    if 'speed-index' in data['lighthouseResult']['audits']:
        speed_index_score = data["lighthouseResult"]["audits"]["speed-index"]["score"]
        speed_index = data["lighthouseResult"]["audits"]["speed-index"]["displayValue"]
        st.write(f"Score: {speed_index_score}, Speed Index: {speed_index}")

    # 2.4.19.- Use of Rel Preconnect
    st.subheader("Use of Rel Preconnect")
    if 'uses-rel-preconnect' in data['lighthouseResult']['audits']:
        rel_preconnect_score = data["lighthouseResult"]["audits"]["uses-rel-preconnect"]["score"]
        rel_preconnect_warning = data["lighthouseResult"]["audits"]["uses-rel-preconnect"]["warnings"]
        st.write(f"Score: {rel_preconnect_score}, Warnings: {rel_preconnect_warning}")

#    # 2.4.20.- Use of Optimized Images
#    st.subheader("Use of Optimized Images")
#    if 'uses-optimized-images' in data['lighthouseResult']['audits']:
#        optimized_images_score = data["lighthouseResult"]["audits"]["uses-optimized-images"]["score"]
#        optimized_images = data["lighthouseResult"]["audits"]["uses-optimized-images"]["displayValue"]
#        st.write(f"Score: {optimized_images_score}, Potential Savings: {optimized_images}")
#        listoptimisedimages = []
#        for item in data["lighthouseResult"]["audits"]["uses-optimized-images"]["details"]["items"]:
#            url = item.get("url", "N/A")
#            wastedbytes = item.get("wastedBytes", "N/A")
#            totalbytes = item.get("totalBytes", "N/A")
#            list1 = [url, wastedbytes, totalbytes]
#            listoptimisedimages.append(list1)
#        st.table(pd.DataFrame(listoptimisedimages, columns=["URL", "Wasted Bytes", "Total Bytes"]))

    


def google_pagespeed_insights():

    st.markdown("<h1 style='text-align: center; color: #1565C0;'>PageSpeed Insights Analyzer</h1>", unsafe_allow_html=True)
    st.markdown(
        "<h3 style='text-align: center;'>Get detailed insights into your website's performance! Powered by Google PageSpeed Insights <a href='https://developer.chrome.com/docs/lighthouse/overview/'>[Learn More]</a></h3>",
        unsafe_allow_html=True
    )

    # User Input
    with st.form("pagespeed_form"):
        url = st.text_input("Enter Website URL", placeholder="https://www.example.com")
        api_key = st.text_input("Enter Google API Key (Optional)", placeholder="Your API Key", help="Get your API key here: [https://developers.google.com/speed/docs/insights/v5/get-started#key](https://developers.google.com/speed/docs/insights/v5/get-started#key)")
        device = st.selectbox("Choose Device", ["Mobile", "Desktop"])
        locale = st.selectbox("Choose Locale", ["en", "fr", "es", "de", "ja"])
        categories = st.multiselect(
            "Select Categories to Analyze",
            ['PERFORMANCE', 'ACCESSIBILITY', 'BEST_PRACTICES', 'SEO'],
            default=['PERFORMANCE', 'ACCESSIBILITY', 'BEST_PRACTICES', 'SEO']
        )

        submitted = st.form_submit_button("Analyze")

    if submitted:
        if not url:
            st.error("Please provide the website URL.")
        else:
            # Fetch and process PageSpeed Insights data
            strategy = 'mobile' if device == "Mobile" else 'desktop'
            data = run_pagespeed(url, api_key, strategy=strategy, locale=locale)

            # Display results in a user-friendly format
            if data:
                display_results(data)
            else:
                st.error("Failed to retrieve PageSpeed Insights data.")
