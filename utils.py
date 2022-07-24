#Basics
import numpy as np
import pandas as pd
#Viz
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(palette='colorblind')

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