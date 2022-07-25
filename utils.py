#Basics
import numpy as np
import pandas as pd
#Viz
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(palette='colorblind')

#nlp
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from wordcloud import WordCloud

#as a function
def plot_target_distro(tr):
    '''
    Plots the distribution of the target variable (language)
    '''
    ax = sns.countplot(data=tr,x='language',order=tr.language.value_counts().index); 
    #show count
    for bar in ax.patches:
        #calculate middle x of bar
        x_pt = bar.get_x() + (bar.get_width() / 2)
        #Add small buffer to height of bar (y)
        y_pt = bar.get_height() + .5
        #plot values - note that the height in this case is the value we want to plot
        ax.text(x = x_pt, y = y_pt, s = bar.get_height(),horizontalalignment='center')

    plt.title('Distribution of Readme Languages',size=14)
    plt.ylabel('Count',size=14)
    plt.xlabel('Language',size=14)
    plt.ylim((0,55))
    plt.tight_layout()
    return None

def create_aggregated_tfidf(tr):
    '''
    Creates a TF-IDF score for each word by language. 
    Languages are aggregated into a single 'document'
    
    Returns: Pandas DataFrame (columns are words, index is language, cell is tf-idf score for that word/language)
    '''
    #GROUP content by language
    grouped = pd.DataFrame(tr.groupby(by='language')['content'].transform(lambda x: ' '.join(x)).drop_duplicates())
    #get names for the indices
    names = [tr.loc[115,'language'], tr.loc[395,'language'],
             tr.loc[166,'language'], tr.loc[348,'language'],
             tr.loc[124,'language'], tr.loc[248,'language'],
             tr.loc[385,'language'], tr.loc[19,'language']]
    #set index labels
    grouped.set_axis(names,inplace=True)
    
    #CREATE TF-IDF Vectorizer for grouped content
    #initialize vectorizer
    tfidf = TfidfVectorizer() 
    #create sparse matrix
    tfidfs = tfidf.fit_transform(grouped.content) 
    #convert to DataFrame
    tr_tfidf = pd.DataFrame(tfidfs.todense(), columns=tfidf.get_feature_names()) 
    #Set human friendly index names
    tr_tfidf.set_index(grouped.index, inplace=True)
    return tr_tfidf

def generate_plots_and_cloud(lang,tr,tr_tfidf):
    '''
    Generates plots and bigram word cloud for a given language. 
    Parameters:
        (R) lang: the language to plot (string must exactly match what the github readme api produces)
        (R)   tr: train dataframe
    (R) tr_tfidf: DataFrame of tf-idf values.  Created using 'create_aggregated_tfidf' function
    '''
    #GET DATA SUBSETS
    #get top 10 tf-idf
    top10 = tr_tfidf.sort_values(by=lang,axis=1,ascending=False).loc[lang,:].head(10)
    #get top 10 words
    txt = ' '.join(tr[tr.language == lang].content)
    freq = pd.Series(str(txt).split()).value_counts().head(10)
    #get bigrams
    bigrams = pd.Series(nltk.ngrams(txt.split(), 2)).value_counts().head(15)

    #INITIALIZE FIGURE
    plt.figure(figsize=(12,8))
    plt.suptitle(f'Language: {lang}')

    #FIRST PLOT - Top Left - top 10 words
    plt.subplot(2,2,1)
    plt.barh(y=freq.index,width=freq);
    plt.title(f'Top 10 Words by Count',size=14);
    plt.xlabel(f'Count');
    plt.gca().invert_yaxis();

    #SECOND PLOT - Top Right - top 10 tf-idf words
    plt.subplot(2,2,2)
    plt.barh(y=top10.index,width=top10);
    plt.title(f'Top 10 Words by TF-IDF',size=14);
    plt.xlabel(f'TF-IDF');
    plt.gca().invert_yaxis();

    #THIRD PLOT - Bottom - Bigram word cloud
    plt.subplot(2,2,(3,4))
    data = {k[0] + ' ' + k[1]: v for k, v in bigrams.to_dict().items()}
    bigramc = WordCloud(background_color='white', width=1400, height=400).generate_from_frequencies(data)
    plt.imshow(bigramc)
    plt.title('Top Bigrams',size=14)
    plt.axis('off')

    plt.tight_layout()
    
    return None