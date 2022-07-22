import numpy as np
import pandas as pd
import json

import nltk
import re
import unicodedata

#### TOC ####
# 1) basic_clean
# 2) remove_stopwords
# 3) tokenize
# 4) lemmatize
# 5) get_json_data
# 6) prep_data


def basic_clean(words):
    '''
    Takes a space delimited string and returns a space delimited string that is:
      1) Converted to lowercase
      2) Normalize the unicode string (NFKD)
      3) Encode to ASCII (bytes) and decode to UTF-8 (string)
      NOT YET: 4) Strip any characters that aren't a-z, 0-9, a space or apostrophe
    '''
    #Lowercase
    words = words.lower()
    #Normalize unicode
    words = unicodedata.normalize('NFKD',words).encode('ascii','ignore').decode('utf-8','ignore')
    #remove special characters
    #Replace markdown carriage returns or new line with a space
    words = re.sub(r"[\r|\n]",' ',words)
    #Remove '(http' words
    words = re.sub(r"\(http[^\s]*",'',words)
    #Remove any words with just # signs - not perfect, but should remove most
    words = re.sub(r"\s#+\s",'',words)
    #Remove these characters
    #words = re.sub(r"[\'|\"|\-")
    words = re.sub(r"[^a-z0-9'\s#]",'',words)

    #return stripped string
    return words.strip()

def remove_stopwords(words,extra_words=None,exclude_words=None,language='english'):
    '''
    Takes a space delimited string and returns a space delimited string with the stopwords removed.
    By default it utilizes the nltk english stopword corpus.  

    Parameters:
            (R) words: String - space delimited
      (O) extra_words: List of any additional stopwords to be removed
    (O) exclude_words: List of nltk stopwords you do not want removed (that would be in the )
         (O) language: String - stopword language (must be present in nltk stopword corpus). Default: English
    '''
    #list
    stopwords_list = nltk.corpus.stopwords.words(language)
    #convert to set
    stopwords_set = set(stopwords_list)
    #add any extra words
    if extra_words: stopwords_set.update(extra_words)
    #remove any unwanted words
    if exclude_words: stopwords_set - set(extra_words)
    filtered = [word for word in words.split() if word not in stopwords_set]
    return ' '.join(filtered)

def tokenize(words):
    toktok = nltk.tokenize.toktok.ToktokTokenizer()
    return toktok.tokenize(words, return_str=True)

def lemmatize(words):
    #lemmatize
    wnl = nltk.stem.WordNetLemmatizer()
    #apply to individual 
    lemmas = [wnl.lemmatize(word) for word in words.split()]
    return ' '.join(lemmas)

def get_json_data():
    '''
    Retrieves json data.  Returns List of Dictionaries
    '''
    #open json file
    f = open('data2.json')
    #get data
    data = json.loads(f.read())
    #close json file
    f.close()
    return data

def prep_data():
    '''
    Prepares the Github Readme data for exploration and modeling.
    
    Outputs: Pandas DataFrame
    '''
    #retrieve stored data
    data = get_json_data()
    #Convert to DataFrame
    df = pd.DataFrame(data)
    #rename readme_contents column
    df.rename(columns={'readme_contents':'content'},inplace=True)
    #drop rows with nulls
    df.dropna(axis=0,inplace=True)
    
    #Do a Basic Clean - lowercase, unicode, ascii, some special character removal
    df.content = df.content.apply(basic_clean)
    #tokenize
    df.content = df.content.apply(tokenize)
    #remove stopwords
    df.content = df.content.apply(remove_stopwords)
    #lemmatize
    df.content = df.content.apply(lemmatize)
    
    return df
    
    
    