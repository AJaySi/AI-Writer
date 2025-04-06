"""
This Python script analyzes Google search keywords by fetching auto-suggestions, performing keyword clustering, and visualizing Google Trends data. It uses various libraries such as pytrends, requests_html, tqdm, and more.

Features:
- Fetches auto-suggestions for a given search keyword from Google.
- Performs keyword clustering using K-means algorithm based on TF-IDF vectors.
- Visualizes Google Trends data, including interest over time and interest by region.
- Retrieves related queries and topics for a set of search keywords.
- Utilizes visualization libraries such as Matplotlib, Plotly, and Rich for displaying results.
- Incorporates logger.for error handling and informative messages.

Usage:
- Provide a search term or a list of search terms for analysis.
- Run the script to fetch auto-suggestions, perform clustering, and visualize Google Trends data.
- Explore the displayed results, including top keywords in each cluster and related topics.

Modifications:
- Customize the search terms in the 'do_google_trends_analysis' function.
- Adjust the number of clusters for keyword clustering and other parameters as needed.
- Explore further visualizations and analyses based on the generated data.

Note: Ensure that the required libraries are installed using 'pip install pytrends requests_html tqdm tabulate plotly rich'.
"""

import os
import time # I wish
import random
import requests
import numpy as np
import sys
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score, silhouette_samples
from rich.console import Console
from rich.progress import Progress
import urllib
import json
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio
from requests_html import HTML, HTMLSession
from urllib.parse import quote_plus
from tqdm import tqdm
from tabulate import tabulate
from pytrends.request import TrendReq
from loguru import logger

# Configure logger
logger.remove()
logger.add(sys.stdout,
           colorize=True,
           format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
           )


def fetch_google_trends_interest_overtime(keyword):
    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        pytrends.build_payload([keyword], timeframe='today 1-y', geo='US')
        
        # 1. Interest Over Time
        data = pytrends.interest_over_time()
        data = data.reset_index()

        # Visualization using Matplotlib
        plt.figure(figsize=(10, 6))
        plt.plot(data['date'], data[keyword], label=keyword)
        plt.title(f'Interest Over Time for "{keyword}"')
        plt.xlabel('Date')
        plt.ylabel('Interest')
        plt.legend()
        plt.show()

        return data
    except Exception as e:
        logger.error(f"Error in fetch_google_trends_data: {e}")
        return pd.DataFrame()


def plot_interest_by_region(kw_list):
    try:
        from pytrends.request import TrendReq
        import matplotlib.pyplot as plt
        trends = TrendReq()
        trends.build_payload(kw_list=kw_list)
        kw_list = ' '.join(kw_list)
        data = trends.interest_by_region() #sorting by region
        data = data.sort_values(by=f"{kw_list}", ascending=False)
        print("\n📢❗🚨 ")
        print(f"Top 10 regions with highest interest for keyword: {kw_list}")
        data = data.head(10) #Top 10
        print(data)
        data.reset_index().plot(x="geoName", y=f"{kw_list}",
                        figsize=(20,15), kind="bar")
        plt.style.use('fivethirtyeight')
        plt.show()
        # FIXME: Send this image to vision GPT for analysis.

    except Exception as e:
        print(f"Error plotting interest by region: {e}")
        return None




def get_related_topics_and_save_csv(search_keywords):
    search_keywords = [f"{search_keywords}"]
    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        pytrends.build_payload(kw_list=search_keywords, timeframe='today 12-m')
        
        # Get related topics - this returns a dictionary
        topics_data = pytrends.related_topics()
        
        # Extract data for the first keyword
        if topics_data and search_keywords[0] in topics_data:
            keyword_data = topics_data[search_keywords[0]]
            
            # Create two separate dataframes for top and rising
            top_df = keyword_data.get('top', pd.DataFrame())
            rising_df = keyword_data.get('rising', pd.DataFrame())
            
            return {
                'top': top_df[['topic_title', 'value']] if not top_df.empty else pd.DataFrame(),
                'rising': rising_df[['topic_title', 'value']] if not rising_df.empty else pd.DataFrame()
            }
    except Exception as e:
        logger.error(f"Error in related topics: {e}")
        return {'top': pd.DataFrame(), 'rising': pd.DataFrame()}

def get_related_queries_and_save_csv(search_keywords):
    search_keywords = [f"{search_keywords}"]
    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        pytrends.build_payload(kw_list=search_keywords, timeframe='today 12-m')
        
        # Get related queries - this returns a dictionary
        queries_data = pytrends.related_queries()
        
        # Extract data for the first keyword
        if queries_data and search_keywords[0] in queries_data:
            keyword_data = queries_data[search_keywords[0]]
            
            # Create two separate dataframes for top and rising
            top_df = keyword_data.get('top', pd.DataFrame())
            rising_df = keyword_data.get('rising', pd.DataFrame())
            
            return {
                'top': top_df if not top_df.empty else pd.DataFrame(),
                'rising': rising_df if not rising_df.empty else pd.DataFrame()
            }
    except Exception as e:
        logger.error(f"Error in related queries: {e}")
        return {'top': pd.DataFrame(), 'rising': pd.DataFrame()}


def get_source(url):
    try:
        session = HTMLSession()
        response = session.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response
    except requests.exceptions.RequestException as e:
        logger.error(f"Error during HTTP request: {e}")
        return None



def get_results(query):
    try:
        query = urllib.parse.quote_plus(query)
        response = get_source(f"https://suggestqueries.google.com/complete/search?output=chrome&hl=en&q={query}")
        time.sleep(random.uniform(0.1, 0.6))

        if response:
            response.raise_for_status()
            results = json.loads(response.text)
            return results
        else:
            return None
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON response: {e}")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Error during HTTP request: {e}")
        return None



def format_results(results):
    try:
        suggestions = []
        for index, value in enumerate(results[1]):
            suggestion = {'term': value, 'relevance': results[4]['google:suggestrelevance'][index]}
            suggestions.append(suggestion)
        return suggestions
    except (KeyError, IndexError) as e:
        logger.error(f"Error parsing search results: {e}")
        return []



def get_expanded_term_suffixes():
    return ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm','n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']



def get_expanded_term_prefixes():
    # For shopping, review type blogs.
    #return ['discount *', 'pricing *', 'cheap', 'best price *', 'lowest price', 'best value', 'sale', 'affordable', 'promo', 'budget''what *', 'where *', 'how to *', 'why *', 'buy*', 'how much*','best *', 'worse *', 'rent*', 'sale*', 'offer*','vs*','or*']
    return ['what *', 'where *', 'how to *', 'why *','best *', 'vs*', 'or*']



def get_expanded_terms(query):
    try:
        expanded_term_prefixes = get_expanded_term_prefixes()
        expanded_term_suffixes = get_expanded_term_suffixes()

        terms = [query]

        for term in expanded_term_prefixes:
            terms.append(f"{term} {query}")

        for term in expanded_term_suffixes:
            terms.append(f"{query} {term}")

        return terms
    except Exception as e:
        logger.error(f"Error in get_expanded_terms: {e}")
        return []



def get_expanded_suggestions(query):
    try:
        all_results = []

        expanded_terms = get_expanded_terms(query)
        for term in tqdm(expanded_terms, desc="📢❗🚨 Fetching Google AutoSuggestions", unit="term"):
            results = get_results(term)
            if results:
                formatted_results = format_results(results)
                all_results += formatted_results
                all_results = sorted(all_results, key=lambda k: k.get('relevance', 0), reverse=True)

        return all_results
    except Exception as e:
        logger.error(f"Error in get_expanded_suggestions: {e}")
        return []



def get_suggestions_for_keyword(search_term):
    """ """
    try:
        expanded_results = get_expanded_suggestions(search_term)
        expanded_results_df = pd.DataFrame(expanded_results)
        expanded_results_df.columns = ['Keywords', 'Relevance']
        #expanded_results_df.to_csv('results.csv', index=False)
        pd.set_option('display.max_rows', expanded_results_df.shape[0]+1)
        expanded_results_df.drop_duplicates('Keywords', inplace=True)
        table = tabulate(expanded_results_df, headers=['Keywords', 'Relevance'], tablefmt='fancy_grid')
        # FIXME: Too much data for LLM context window. We will need to embed it.
        #try:
        #    save_in_file(table)
        #except Exception as save_results_err:
        #    logger.error(f"Failed to save search results: {save_results_err}")
        return expanded_results_df
    except Exception as e:
        logger.error(f"get_suggestions_for_keyword: Error in main: {e}")



def perform_keyword_clustering(expanded_results_df, num_clusters=5):
    try:
        # Preprocessing: Convert the keywords to lowercase
        expanded_results_df['Keywords'] = expanded_results_df['Keywords'].str.lower()

        # Vectorization: Create a TF-IDF vectorizer
        vectorizer = TfidfVectorizer()

        # Fit the vectorizer to the keywords
        tfidf_vectors = vectorizer.fit_transform(expanded_results_df['Keywords'])

        # Applying K-means clustering
        kmeans = KMeans(n_clusters=num_clusters, random_state=42)
        cluster_labels = kmeans.fit_predict(tfidf_vectors)

        # Add cluster labels to the DataFrame
        expanded_results_df['cluster_label'] = cluster_labels

        # Assessing cluster quality through silhouette score
        silhouette_avg = silhouette_score(tfidf_vectors, cluster_labels)
        print(f"Silhouette Score: {silhouette_avg}")

        # Visualize cluster quality using a silhouette plot
        #visualize_silhouette(tfidf_vectors, cluster_labels)

        return expanded_results_df
    except Exception as e:
        logger.error(f"Error in perform_keyword_clustering: {e}")
        return pd.DataFrame()



def visualize_silhouette(X, labels):
    try:
        silhouette_avg = silhouette_score(X, labels)
        print(f"Silhouette Score: {silhouette_avg}")

        # Create a subplot with 1 row and 2 columns
        fig, ax1 = plt.subplots(1, 1, figsize=(8, 6))

        # The 1st subplot is the silhouette plot
        ax1.set_xlim([-0.1, 1])
        ax1.set_ylim([0, X.shape[0] + (len(set(labels)) + 1) * 10])

        # Compute the silhouette scores for each sample
        sample_silhouette_values = silhouette_samples(X, labels)

        y_lower = 10
        for i in set(labels):
            # Aggregate the silhouette scores for samples belonging to the cluster
            ith_cluster_silhouette_values = sample_silhouette_values[labels == i]
            ith_cluster_silhouette_values.sort()

            size_cluster_i = ith_cluster_silhouette_values.shape[0]
            y_upper = y_lower + size_cluster_i

            color = plt.cm.nipy_spectral(float(i) / len(set(labels)))
            ax1.fill_betweenx(np.arange(y_lower, y_upper),
                              0, ith_cluster_silhouette_values,
                              facecolor=color, edgecolor=color, alpha=0.7)

            # Label the silhouette plots with their cluster numbers at the middle
            ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))

            # Compute the new y_lower for the next plot
            y_lower = y_upper + 10  # 10 for the 0 samples

        ax1.set_title("Silhouette plot for KMeans clustering")
        ax1.set_xlabel("Silhouette coefficient values")
        ax1.set_ylabel("Cluster label")

        # The vertical line for the average silhouette score of all the values
        ax1.axvline(x=silhouette_avg, color="red", linestyle="--")

        plt.show()
    except Exception as e:
        logger.error(f"Error in visualize_silhouette: {e}")



def print_and_return_top_keywords(expanded_results_df, num_clusters=5):
    """
    Display and return top keywords in each cluster.

    Args:
        expanded_results_df (pd.DataFrame): DataFrame containing expanded keywords, relevance, and cluster labels.
        num_clusters (int or str): Number of clusters or 'all'.

    Returns:
        pd.DataFrame: DataFrame with top keywords for each cluster.
    """
    top_keywords_df = pd.DataFrame()

    if num_clusters == 'all':
        unique_clusters = expanded_results_df['cluster_label'].unique()
    else:
        unique_clusters = range(int(num_clusters))

    for i in unique_clusters:
        cluster_df = expanded_results_df[expanded_results_df['cluster_label'] == i]
        top_keywords = cluster_df.sort_values(by='Relevance', ascending=False).head(5)
        top_keywords_df = pd.concat([top_keywords_df, top_keywords])

    print(f"\n📢❗🚨 GTop Keywords for All Clusters:")
    table = tabulate(top_keywords_df, headers='keys', tablefmt='fancy_grid')
    # Save the combined table to a file
    try:
        save_in_file(table)
    except Exception as save_results_err:
        logger.error(f"🚨 Failed to save search results: {save_results_err}")
    print(table)
    return top_keywords_df


def generate_wordcloud(keywords):
    """
    Generate and display a word cloud from a list of keywords.

    Args:
        keywords (list): List of keywords.
    """
    # Convert the list of keywords to a string
    text = ' '.join(keywords)

    # Generate word cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

    # Display the word cloud using matplotlib
    plt.figure(figsize=(600, 200))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()



def save_in_file(table_content):
    """ Helper function to save search analysis in a file. """
    file_path = os.environ.get('SEARCH_SAVE_FILE')
    try:
        # Save the content to the file
        with open(file_path, "a+", encoding="utf-8") as file:
            file.write(table_content)
            file.write("\n" * 3)  # Add three newlines at the end
        logger.info(f"Search content saved to {file_path}")
    except Exception as e:
        logger.error(f"Error occurred while writing to the file: {e}")


def do_google_trends_analysis(search_term):
    """ Get a google search keywords, get its stats."""
    search_term = [f"{search_term}"]
    all_the_keywords = []
    try:
        for asearch_term in search_term:
            #FIXME: Lets work with a single root keyword.
            suggestions_df = get_suggestions_for_keyword(asearch_term)
            if len(suggestions_df['Keywords']) > 10:
                result_df = perform_keyword_clustering(suggestions_df)
                # Display top keywords in each cluster
                top_keywords = print_and_return_top_keywords(result_df)
                all_the_keywords.append(top_keywords['Keywords'].tolist())
            else:
                all_the_keywords.append(suggestions_df['Keywords'].tolist())
            all_the_keywords = ','.join([', '.join(filter(None, map(str, sublist))) for sublist in all_the_keywords])
            
            # Generate a random sleep time between 2 and 3 seconds 
            time.sleep(random.uniform(2, 3))
        
        # Display additional information
        try:
            result_df = get_related_topics_and_save_csv(search_term)
            logger.info(f"Related topics:: result_df: {result_df}")
            # Extract 'Top' topic_title
            if result_df:
                top_topic_title = result_df['top']['topic_title'].values.tolist()
                # Join each sublist into one string separated by comma
                #top_topic_title = [','.join(filter(None, map(str, sublist))) for sublist in top_topic_title]
                top_topic_title = ','.join([', '.join(filter(None, map(str, sublist))) for sublist in top_topic_title])
        except Exception as err:
            logger.error(f"Failed to get results from google trends related topics: {err}")

        # TBD: Not getting great results OR unable to understand them.
        #all_the_keywords += top_topic_title
        all_the_keywords = all_the_keywords.split(',')
        # Split the list into chunks of 5 keywords
        chunk_size = 4
        chunks = [all_the_keywords[i:i + chunk_size] for i in range(0, len(all_the_keywords), chunk_size)]
        # Create a DataFrame with columns named 'Keyword 1', 'Keyword 2', etc.
        combined_df = pd.DataFrame(chunks, columns=[f'K📢eyword Col{i + 1}' for i in range(chunk_size)])
        
        # Print the table
        table = tabulate(combined_df, headers='keys', tablefmt='fancy_grid')
        # Save the combined table to a file
        try:
            save_in_file(table)
        except Exception as save_results_err:                 
            logger.error(f"Failed to save search results: {save_results_err}")
        print(table)
        
        #generate_wordcloud(all_the_keywords)
        return(all_the_keywords)
    except Exception as e:
        logger.error(f"Error in Google Trends Analysis: {e}")


def get_trending_searches(country='united_states'):
    """Get trending searches for a specific country."""
    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        trending_searches = pytrends.trending_searches(pn=country)
        return trending_searches
    except Exception as e:
        logger.error(f"Error getting trending searches: {e}")
        return pd.DataFrame()

def get_realtime_trends(country='US'):
    """Get realtime trending searches for a specific country."""
    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        realtime_trends = pytrends.realtime_trending_searches(pn=country)
        return realtime_trends
    except Exception as e:
        logger.error(f"Error getting realtime trends: {e}")
        return pd.DataFrame()