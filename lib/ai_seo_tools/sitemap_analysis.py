import streamlit as st
import advertools as adv
import pandas as pd
import plotly.graph_objects as go
from urllib.error import URLError
import xml.etree.ElementTree as ET
import requests

def main():
    st.title("📊 Sitemap Analyzer")
    st.write("""
        This tool analyzes a website's sitemap to understand its content structure and publishing trends. 
        Enter a sitemap URL to start your analysis.
    """)

    sitemap_url = st.text_input("Please enter the sitemap URL:", "https://www.example.com/sitemap.xml")

    if st.button("Analyze Sitemap"):
        try:
            sitemap_df = fetch_all_sitemaps(sitemap_url)
            if sitemap_df is not None and not sitemap_df.empty:
                sitemap_df = process_lastmod_column(sitemap_df)
                ppmonth = analyze_content_trends(sitemap_df)
                sitemap_df = categorize_and_shorten_sitemaps(sitemap_df)
                
                display_key_metrics(sitemap_df, ppmonth)
                plot_sitemap_content_distribution(sitemap_df)
                plot_content_trends(ppmonth)
                plot_content_type_breakdown(sitemap_df)
                plot_publishing_frequency(sitemap_df)

                st.success("🎉 Analysis complete!")
            else:
                st.error("No valid URLs found in the sitemap.")
        except URLError as e:
            st.error(f"Error fetching the sitemap: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

def fetch_all_sitemaps(sitemap_url):
    st.write(f"🚀 Fetching and analyzing the sitemap: {sitemap_url}...")

    try:
        sitemap_df = fetch_sitemap(sitemap_url)
        
        if sitemap_df is not None:
            all_sitemaps = sitemap_df.loc[sitemap_df['loc'].str.contains('sitemap'), 'loc'].tolist()
            
            if all_sitemaps:
                st.write(f"🔄 Found {len(all_sitemaps)} additional sitemaps. Fetching data from them...")
                all_urls_df = pd.DataFrame()

                for sitemap in all_sitemaps:
                    try:
                        st.write(f"Fetching URLs from {sitemap}...")
                        temp_df = fetch_sitemap(sitemap)
                        if temp_df is not None:
                            all_urls_df = pd.concat([all_urls_df, temp_df], ignore_index=True)
                    except Exception as e:
                        st.error(f"Error fetching {sitemap}: {e}")

                st.write(f"✅ Successfully fetched {len(all_urls_df)} URLs from all sitemaps.")
                return all_urls_df
            
            else:
                st.write(f"✅ Successfully fetched {len(sitemap_df)} URLs from the main sitemap.")
                return sitemap_df
        else:
            return None

    except Exception as e:
        st.error(f"⚠️ Error fetching the sitemap: {e}")
        return None

def fetch_sitemap(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        ET.fromstring(response.content)
        
        sitemap_df = adv.sitemap_to_df(url)
        return sitemap_df

    except requests.RequestException as e:
        st.error(f"⚠️ Request error: {e}")
        return None
    except ET.ParseError as e:
        st.error(f"⚠️ XML parsing error: {e}")
        return None

def process_lastmod_column(sitemap_df):
    st.write("📅 Converting 'lastmod' column to DateTime format and setting it as the index...")

    try:
        sitemap_df = sitemap_df.dropna(subset=['lastmod'])
        sitemap_df['lastmod'] = pd.to_datetime(sitemap_df['lastmod'])
        sitemap_df.set_index('lastmod', inplace=True)
        
        st.write("✅ 'lastmod' column successfully converted to DateTime format and set as the index.")
        return sitemap_df

    except Exception as e:
        st.error(f"⚠️ Error processing the 'lastmod' column: {e}")
        return None

def categorize_and_shorten_sitemaps(sitemap_df):
    st.write("🔍 Categorizing and shortening sitemap names...")

    try:
        sitemap_df['sitemap_name'] = sitemap_df['sitemap'].str.split('/').str[4]
        sitemap_df['sitemap_name'] = sitemap_df['sitemap_name'].replace({
            'sitemap-site-kasko-fiyatlari.xml': 'Kasko',
            'sitemap-site-bireysel.xml': 'Personal',
            'sitemap-site-kurumsal.xml': 'Cooperate',
            'sitemap-site-arac-sigortasi.xml': 'Car',
            'sitemap-site.xml': 'Others'
        })

        st.write("✅ Sitemap names categorized and shortened.")
        return sitemap_df

    except Exception as e:
        st.error(f"⚠️ Error categorizing sitemap names: {e}")
        return sitemap_df

def analyze_content_trends(sitemap_df):
    st.write("📅 Analyzing content publishing trends...")
    
    try:
        ppmonth = sitemap_df.resample('M').size()
        sitemap_df['monthly_count'] = sitemap_df.index.to_period('M').value_counts().sort_index()
        
        st.write("✅ Content trends analysis completed.")
        return ppmonth
    
    except Exception as e:
        st.error(f"⚠️ Error during content trends analysis: {e}")
        return pd.Series()

def display_key_metrics(sitemap_df, ppmonth):
    st.write("### Key Metrics")
    
    total_urls = len(sitemap_df)
    total_articles = ppmonth.sum()
    average_frequency = ppmonth.mean()
    
    st.write(f"**Total URLs Found:** {total_urls:,}")
    st.write(f"**Total Articles Published:** {total_articles:,}")
    st.write(f"**Average Monthly Publishing Frequency:** {average_frequency:.2f} articles/month")

def plot_sitemap_content_distribution(sitemap_df):
    st.write("📊 Visualizing content amount by sitemap categories...")

    try:
        if 'sitemap_name' in sitemap_df.columns:
            stmc = sitemap_df.groupby('sitemap_name').size()
            fig = go.Figure()
            fig.add_bar(x=stmc.index, y=stmc.values, name='Sitemap Categories')
            fig.update_layout(
                title='Content Amount by Sitemap Categories',
                xaxis_title='Sitemap Categories',
                yaxis_title='Number of Articles',
                paper_bgcolor='#E5ECF6'
            )
            st.plotly_chart(fig)
        else:
            st.warning("⚠️ The 'sitemap_name' column is missing in the data.")
    
    except Exception as e:
        st.error(f"⚠️ Error during sitemap content distribution plotting: {e}")

def plot_content_trends(ppmonth):
    st.write("📈 Plotting content publishing trends over time...")

    try:
        fig = go.Figure()
        fig.add_scatter(x=ppmonth.index, y=ppmonth.values, mode='lines+markers', name='Publishing Trends')
        fig.update_layout(
            title='Content Publishing Trends Over Time',
            xaxis_title='Month',
            yaxis_title='Number of Articles',
            paper_bgcolor='#E5ECF6'
        )
        st.plotly_chart(fig)
    
    except Exception as e:
        st.error(f"⚠️ Error during content trends plotting: {e}")

def plot_content_type_breakdown(sitemap_df):
    st.write("🔍 Plotting content type breakdown...")

    try:
        if 'sitemap_name' in sitemap_df.columns and not sitemap_df['sitemap_name'].empty:
            content_type_counts = sitemap_df['sitemap_name'].value_counts()
            st.write("Content Type Counts:", content_type_counts)  # Debug line
            
            if not content_type_counts.empty:
                fig = go.Figure(data=[go.Pie(labels=content_type_counts.index, values=content_type_counts.values)])
                fig.update_layout(
                    title='Content Type Breakdown',
                    paper_bgcolor='#E5ECF6'
                )
                st.plotly_chart(fig)
            else:
                st.warning("⚠️ No content types to display.")
        else:
            st.warning("⚠️ The 'sitemap_name' column is missing or empty.")
    
    except Exception as e:
        st.error(f"⚠️ Error during content type breakdown plotting: {e}")

def visualize_content_by_sitemap_category(sitemap_df):
    st.write("🔍 Visualizing content amount by sitemap categories...")

    try:
        # Check if the 'sitemap_name' column exists and is non-empty
        if 'sitemap_name' in sitemap_df.columns and not sitemap_df['sitemap_name'].empty:
            st.write("Sitemap Data Preview:", sitemap_df['sitemap_name'].head())  # Check the data

            # Group and count the number of entries per sitemap category
            sitemap_category_counts = sitemap_df['sitemap_name'].value_counts()

            # Display the grouped data
            st.write("Sitemap Category Counts:", sitemap_category_counts)  # Debug line

            # If we have valid data, plot it
            if not sitemap_category_counts.empty:
                fig = go.Figure()
                fig.add_bar(x=sitemap_category_counts.index, y=sitemap_category_counts.values, name='Sitemap Names')
                fig.update_layout(
                    title='Content Amount by Sitemap Categories',
                    paper_bgcolor='#E5ECF6',
                    yaxis_title='Article Amount',
                )
                st.plotly_chart(fig)
            else:
                st.warning("⚠️ No data to display for sitemap categories.")
        else:
            st.warning("⚠️ The 'sitemap_name' column is missing or empty.")
    
    except Exception as e:
        st.error(f"⚠️ Error during content amount visualization: {e}")

def plot_publishing_frequency(sitemap_df):
    st.write("📆 Plotting publishing frequency by month...")

    try:
        if not sitemap_df.empty:
            frequency_by_month = sitemap_df.index.to_period('M').value_counts().sort_index()
            frequency_by_month.index = frequency_by_month.index.astype(str)  # Convert Period to string for Plotly
            
            fig = go.Figure()
            fig.add_bar(x=frequency_by_month.index, y=frequency_by_month.values, name='Publishing Frequency')
            fig.update_layout(
                title='Publishing Frequency by Month',
                xaxis_title='Month',
                yaxis_title='Number of Articles',
                paper_bgcolor='#E5ECF6'
            )
            st.plotly_chart(fig)
        else:
            st.warning("⚠️ No data available to plot publishing frequency.")
    
    except Exception as e:
        st.error(f"⚠️ Error during publishing frequency plotting: {e}")

if __name__ == "__main__":
    main()

