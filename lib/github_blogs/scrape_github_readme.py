import os
import sys
import datetime
import pandas as pd

import json
import requests
from bs4 import BeautifulSoup
from loguru import logger
logger.remove()
logger.add(sys.stdout,
        colorize=True,
        format="<level>{level}</level>|<green>{file}:{line}:{function}</green>| {message}"
    )


from .take_url_screenshot import take_screenshot
from .gpt_providers.gemini_image_details import gemini_get_img_info



def get_readme_content(url):
    try:
        # Fetch the README content directly from the URL
        response = requests.get(url)
        print(response.status_code)
        if response.status_code == 200:
            logger.debug("Successfully fetched the README.md")
            readme_content = response.text
        else:
            readme_content = None
        return readme_content
    except Exception as err:
        logger.error(f"Failed to fetch raw readme from {url}: {err}: {response.status_code}")
        sys.exit(1)


def get_gh_repo_metadata(github_url):
    """ Function to get the repo details like stars, commits, forks etc """
    logger.info("Scraping github with BS4 and requests.")
    # download the target page
    page = requests.get(github_url)
    # parse the HTML document returned by the server
    soup = BeautifulSoup(page.text, 'html.parser')

    # initialize the object that will contain the scraped data
    repo = {}

    # repo scraping logic
    name_html_element = soup.select_one('[itemprop="name"]')
    name = name_html_element.get_text().strip()

    git_branch_icon_html_element = soup.select_one('.octicon-git-branch')
    main_branch_html_element = git_branch_icon_html_element.find_next_sibling('span')
    main_branch = main_branch_html_element.get_text().strip()

    # scrape the repo history data
    boxheader_html_element = soup.select_one('.Box .Box-header')

    # scrape the repo details in the right box
    bordergrid_html_element = soup.select_one('.BorderGrid')

    about_html_element = bordergrid_html_element.select_one('h2')
    description_html_element = about_html_element.find_next_sibling('p')
    description = description_html_element.get_text().strip()

    star_icon_html_element = bordergrid_html_element.select_one('.octicon-star')
    stars_html_element = star_icon_html_element.find_next_sibling('strong')
    stars = stars_html_element.get_text().strip().replace(',', '')

    eye_icon_html_element = bordergrid_html_element.select_one('.octicon-eye')
    watchers_html_element = eye_icon_html_element.find_next_sibling('strong')
    watchers = watchers_html_element.get_text().strip().replace(',', '')

    fork_icon_html_element = bordergrid_html_element.select_one('.octicon-repo-forked')
    forks_html_element = fork_icon_html_element.find_next_sibling('strong')
    forks = forks_html_element.get_text().strip().replace(',', '')

    # Find the div with class "f6" containing topic links
    topic_div = soup.find('div', class_='f6')
    if topic_div:
        # Find all the topic links within the div
        topic_links = topic_div.find_all('a', class_='topic-tag-link')
        # Extract and print the topics
        repo['topics'] = [link.text.strip() for link in topic_links]

    # FIXME: Unable to scrape branch name.
    repo['branch_name'] = None
    # store the scraped data
    repo['name'] = name
    repo['about'] = description
    repo['stars'] = stars
    repo['watchers'] = watchers
    repo['forks'] = forks
    #repo['readme'] = readme
    logger.info(f"Github Repo Details: {repo}") 
    return(repo)


def get_gh_details_vision(github_url, generated_image_filepath):
    """ Take a screenshot of the url and feed to vision models for scraping details. """
    logger.info(f"Take screenshot and pass it to gemini for repo details of {github_url}")

    generated_image_filepath = take_screenshot(github_url, generated_image_filepath)
    prompt = """From the given image of a github page, find out the number of stars, about, forks, last commit days, link url, topics and branch name. Return the result as json."""
    
    try:
        gh_details = gemini_get_img_info(prompt, generated_image_filepath)
        logger.info(f"Github Repo details, from vision model: {gh_details}")
        #gh_details = get_gh_repo_metadata(github_url)
    except Exception as err:
        logger.error(f"Failed to get gh images details: {err}")
        gh_details = get_gh_repo_metadata(github_url)
        return gh_details

    # Convert string to dictionary Split the string into lines
    lines = gh_details.split('\n')
    # Remove the first and last line
    modified_lines = lines[1:-1]
    # Join the modified lines back into a string
    gh_details = '\n'.join(modified_lines)
    gh_details = json.loads(gh_details)

    return(gh_details)


def research_github_topics(topics):
    """ Scrape github topics of interest for top repos to write on """
    # https://www.kaggle.com/code/subhaskumarray/scraping-github-topics-with-their-repositories
    # We are going to scrape https://github.com/topics
    # We will get a list of topics. For each topic, we will extract topic name, topic description and topic url.
    # For each topic, we will get top 30 repositories with repo name, repo username, stars and repo url.
    # Finally we are going to create csv file for each topic with respective repo details.

    #github_topics = "https://github.com/topics/"
    #response = requests.get(github_topics)
    #if response.status_code != 200:
    #    logger.error(f'There is something wrong with {url}')
    #response_contents = response.text
    # Now we will parse the contents using BeautifulSoup:
    #parsed_contents = BeautifulSoup(response_contents,'html.parser')
    #logger.info("Get all topics, Titles and their urls from github.")
    #topic_titles = get_topic_titles(parsed_contents)
    #topic_desc = get_topic_desc(parsed_contents)
    #topic_urls = get_topic_url(parsed_contents)
    #topic_df = pd.DataFrame(list(zip(topic_titles, topic_desc,topic_urls)),\
    #           columns =['title', 'description', 'url'])
    #logger.info(f"Scraped data from github: {topic_df}")

    gh_topics = ['ai', 'ai-tools', 'ai-assistant', 'ai-agents-framework', 'llm', 'multi-agent', 'fine-tuning', 'rag', 'generative', 'prompt-engineering', 'generative-ai', 'text-to-image-generation', 'llm-ops', 'retrieval-augmented-generation', 'langchain', 'gemini-api', 'vertex-ai', 'huggingface', 'auto-gpt', 'llmops', 'ai-toolkit', 'chatbot', 'chatgpt', 'code-assistant', 'text-to-video', 'llms', 'gpt-4']

    repo_info_dict = {
        'username':[],
        'repo_name': [],
        'stars': [],
        'repo_url': []
    }
    for agh_topic in gh_topics:
        topic_url = f"https://github.com/topics/{agh_topic}"
        first_topic_repo_page = download_repo_page(topic_url)
        logger.info(f"Get details on github topic: {topic_url}")
        repo_tags = first_topic_repo_page.find_all('h3', {'class': 'f3 color-fg-muted text-normal lh-condensed'})
        star_tags = first_topic_repo_page.find_all('span', {'class': 'Counter js-social-count'})
    
        for i in range(len(repo_tags)):
            repo_details = get_repo_info(repo_tags[i], star_tags[i])
        
            # Check if the repo URL is not already present in the dictionary
            if repo_details[3] not in repo_info_dict['repo_url']:
                # Store repos with more than 5000 stars.
                if repo_details[2] > 5000:
                    repo_info_dict['username'].append(repo_details[0])
                    repo_info_dict['repo_name'].append(repo_details[1])
                    repo_info_dict['stars'].append(repo_details[2])
                    repo_info_dict['repo_url'].append(repo_details[3])

    # Create a DataFrame from repo_info_dict
    df_repo_info = pd.DataFrame(repo_info_dict['repo_url'])

    # Check if the file already exists
    csv_filename = 'github_url_to_write.csv'
    if os.path.isfile(csv_filename):
        # Append to the existing file
        df_repo_info.to_csv(csv_filename, mode='a', header=False, index=False)
        logger.info(f"Data appended to existing file: {csv_filename}")
    else:
        # Create a new file
        df_repo_info.to_csv(csv_filename, index=False)


def get_topic_titles(parsed_content):
    try:
        selected_class = 'f3 lh-condensed mb-0 mt-1 Link--primary'
        topic_title_tags = parsed_content.find_all('p',{'class':selected_class})
        # We can make a list of topics
        topic_titles = []
        for tags in topic_title_tags:
            topic_titles.append(tags.text)
        return topic_titles
    except Exception as err:
        logger.error(f"Failed to get github topic titles: {err}")


def get_topic_desc(parsed_contents):
    try:
        desc_selector = 'f5 color-fg-muted mb-0 mt-1'
        topic_desc_tags = parsed_contents.find_all('p',{'class': desc_selector})
        print(f"{topic_desc_tags}")
        topic_desc = []
        for desc in topic_desc_tags:
            print("dsfsfs")
            topic_desc.append(desc.text.strip())  # strip() is used for trimming all extra spaces in description.
        return topic_desc
    except Exception as err:
        logger.error(f"Failed to get github topic desc: {err}")


def get_topic_url(parsed_contents):
    try:
        topic_link_tag = parsed_contents.find_all('a',{'class':'no-underline flex-1 d-flex flex-column'})
        topic_urls = []
        base_url = 'http://github.com'
        for urls in topic_link_tag:
            topic_urls.append(base_url + urls['href'])
        return topic_urls
    except Exception as err:
        logger.error(f"Failed to get github topic urls: {err}")


def download_repo_page(topic_url):
    response = requests.get(topic_url)
    if response.status_code != 200:
        print('There is some error in {}'.format(topic_url))
    response_contents = response.text
    
    parsed_contents = BeautifulSoup(response_contents,'html.parser')
    return parsed_contents


def get_repo_info(repo_tags,star_tags):
    # returns all info for a repo
    a_tags = repo_tags.find_all('a')
    username = a_tags[0].text.strip()
    repo_name = a_tags[1].text.strip()
    base_url = 'http://github.com/'
    repo_url = base_url + a_tags[1]['href'].strip()
    
    # Defining a function so that it will convert our star count to integer
    def star_counts_converter(stars):
        stars = stars.strip()
        if stars[-1] == 'k':
            return int(float(stars[:-1]) * 1000)
        return int(stars)
    star_counts = star_counts_converter(star_tags.text.strip())
    return username,repo_name,star_counts,repo_url


def save_to_csv(topic_url,topic_name):
    file_name = topic_name + '.csv'
    if os.path.exists(file_name):
        logger.debug(f"The file {file_name} already exists. Skipping.")
    topics_df = topic_repo_details(topic_url)
    topics_df.to_csv(file_name,index=None)
    logger.info(f"Successfully scraped topic {topic_name}")


def check_if_already_written(github_url, file_path='papers_already_written_on.txt'):
    """
    Check if a GitHub URL is an exact match in each line of a file.

    Args:
        github_url (str): GitHub URL string to check.
        file_path (str): Path to the file containing lines to check against. Default is 'papers_already_written_on.txt'.

    Returns:
        bool: True if an exact match is found, False otherwise.
    """
    try:
        with open(file_path, 'r', encoding="utf-8") as file:
            # Read each line in the file
            for line in file:
                # Check for an exact match
                if github_url.strip() == line.strip():
                    return True
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    return False








