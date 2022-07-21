import numpy as np
import pandas as pd

import os
import json
from typing import Dict, List, Optional, Union, cast
import requests
import time
from bs4 import BeautifulSoup as BSoup

from env import github_token, github_username

#### TOC ######
# 1) get_repo_links() >> used by get_oceanography_repos to pull repo links for 1 search results page
# 2) get_oceanography_repos >> used by create_REPOS to get new list of oceanography repos
# 3) create_REPOs >> Returns a list of all repos for other acquire functions - from csv or new copy
# 4) series of functions provided by Codeup
# 5) acuire_data >> wrapper for merging list of repos with codeup acquisition functions


#Define Header
headers = {"Authorization": f"token {github_token}", "User-Agent": github_username}

def get_repo_links(soup):
    '''
    Given the soup of a repo search page, get a list urls for all the repos in the results
    
    Output: Returns LIST of partial URLs
    Parameters: (R) soup: Beautiful Soup object of the page contents
    '''
    pg_repos = []
    #loop over all our 'a' tags
    for a in soup.find_all('a',{'class':'v-align-middle'}):
        #grab the href and strip first character >> append to repo list
        pg_repos.append(a['href'][1:])
    #return the list 
    return pg_repos

def get_oceanography_repos():
    '''
    Gets a list of oceanography repos from Github.  
    Must have your own github token and username in a local env file. 
    Output: Returns LIST of strings - with section of URL in format 'user/repo'
    '''
    #set starting point
    #we know there are multiple pages, so including query parameter 'p'
    p=1
    url = f'https://github.com/search?p={p}&q=games&type=Repositories'
    
    #FIRST PAGE
    #get page info
    response = requests.get(url, headers=headers)
    #SOUP, there it is!
    soup = BSoup(response.text, 'html.parser')
    
    #grab links for first page
    repo_list = get_repo_links(soup)
    
    #NEXT PAGE - 
    #set domain
    domain = 'https://github.com'
    #get first next page
    np_tag = soup.find('a',{'class':'next_page'})
    #IF that element exists, go to and repeat!
    while np_tag:
        #create url for next page
        url = domain + np_tag['href']
        
        #get new soup
        response = requests.get(url, headers=headers)
        soup = BSoup(response.text, 'html.parser')
        
        #add new links to our list
        repo_list += get_repo_links(soup)
        
        #break loop if we have > X links
        if len(repo_list) >= 250: break
        
        #grab next page
        np_tag = soup.find('a',{'class':'next_page'})
        time.sleep(7)
        
    return repo_list

def create_REPOS():
    filename = 'repos.csv'
    #see if file exists
    if os.path.isfile(filename):
        df = pd.read_csv(filename,header=None)
        return df.iloc[:,0].tolist()
    else:
        #get new list of repos
        mylist = get_oceanography_repos()
        #save to CSV
        pd.DataFrame(mylist).to_csv(filename,header=False,index=False)
        return mylist


######## CODEUP'S GITHUB CODE #########
if headers["Authorization"] == "token " or headers["User-Agent"] == "":
    raise Exception(
        "You need to follow the instructions marked TODO in this script before trying to use it"
    )


def github_api_request(url: str) -> Union[List, Dict]:
    response = requests.get(url, headers=headers)
    response_data = response.json()
    if response.status_code != 200:
        return None #CAYT - plus uncommenting below
        # raise Exception(
        #     f"Error response from github api! status code: {response.status_code}, "
        #     f"response: {json.dumps(response_data)}"
        # )
    return response_data


def get_repo_language(repo: str) -> str:
    url = f"https://api.github.com/repos/{repo}"
    repo_info = github_api_request(url)
    if not repo_info: return None #CAYT
    if type(repo_info) is dict:
        repo_info = cast(Dict, repo_info)
        return repo_info.get("language", None)
    raise Exception(
        f"Expecting a dictionary response from {url}, instead got {json.dumps(repo_info)}"
    )


def get_repo_contents(repo: str) -> List[Dict[str, str]]:
    url = f"https://api.github.com/repos/{repo}/contents/"
    contents = github_api_request(url)
    if not contents: return None #CAYT
    if type(contents) is list:
        contents = cast(List, contents)
        return contents
    raise Exception(
        f"Expecting a list response from {url}, instead got {json.dumps(contents)}"
    )


def get_readme_download_url(files: List[Dict[str, str]]) -> str:
    """
    Takes in a response from the github api that lists the files in a repo and
    returns the url that can be used to download the repo's README file.
    """
    for file in files:
        if file["name"].lower().startswith("readme"):
            return file["download_url"]
    return ""


def process_repo(repo: str) -> Dict[str, str]:
    """
    Takes a repo name like "gocodeup/codeup-setup-script" and returns a
    dictionary with the language of the repo and the readme contents.
    """
    contents = get_repo_contents(repo)
    if not contents: return None #CAYT
    #get readme URL
    rm_url = get_readme_download_url(contents)
    #if url exists
    if rm_url == '': return None #CAYT
    readme_contents = requests.get(rm_url).text
    return {
        "repo": repo,
        "language": get_repo_language(repo),
        "readme_contents": readme_contents,
    }


def scrape_github_data(REPOS) -> List[Dict[str, str]]:
    """
    Loop through all of the repos and process them. Returns the processed data.
    """
    return [process_repo(repo) for repo in REPOS]

###########################

#WRAPPER FUNCTION
def acquire_data():
    #create repo list
    REPOS = create_REPOS()
    #Pass Repo list to codeup functions
    mylist = scrape_github_data(REPOS)

    #remove any Nones, then return list
    return [i for i in mylist if i]

if __name__ == "__main__":
    data = acquire_data()
    json.dump(data, open("data2.json", "w"), indent=1)