# Predicting Coding Language in 'Games' Readmes
### By: Arsene Boundaone, Cayt Schlichting, Paige Rackley


Target audience for our project is the Codeup Data Science cohort and instructors.


<hr style="background-color:silver;height:3px;" />

## Project Summary
<hr style="background-color:silver;height:3px;" />


### Project Deliverables
> - <b> google slides that: </b>

    - summarize results from exploration and modeling
    - visuals that help describe our findings
    
> - <b> a github repository containing: </b>

    - final notebook containing steps, analysis and findings
    - a README.md that contains description and steps to reproduce
    - README.md should also contain hyperlink to google slides
    
> - <b> a 5-6 minute presentation of findings </b>
    
### Initial questions on the data
> - What are the top 5 programming languages when searching for 'Game' repos in github?
> - What are the most common words for some of these languages?
> - How do the most common words for a language compare to the highest TF-IDF scores for that language?
> - What are common bigrams for some of these languages? Are they significant to the kind of programming language?

### Project Plan 

- [ ] **Acquire** Web scrapping of Github search results. The first 500 repos with the keyword of 'games' on the search date of July 22, 2022 were used.
- [ ] Clean and **prepare** data for the explore phase. 
- [ ] Create wrangle.py to store functions I created to automate the cleaning and preparation process. 
- [ ] Separate train, validate, test subsets and scaled data.
- [ ] **Explore** the data through visualization using natural language processing methods.
    - [ ] Clearly define our hypotheses and questions.
    - [ ] Document findings and takeaways.
- [ ] Perform **modeling**:
   - [ ] Identify model evaluation criteria (what is our baseline?)
   - [ ] Create at least three different classification models.
   - [ ] Evaluate models on appropriate data subsets.
- [ ] Create **Final Report** notebook with a curtailed version of the above steps.
- [ ] Create and review README. Ensure it contains:
   - [ ] Data dictionary
   - [ ] Project summary and goals
   - [ ] Initial Hypothesis
   - [ ] Executive Summary
---

<hr style="background-color:silver;height:3px;" />

## Executive Summary
<hr style="background-color:silver;height:3px;" />
Through classification models, we were able to beat our baseline of 25.38% accuracy with a K-Nearest Neighbor model that had 33.8% accuracy. This is a small win, but I do believe there is room for improvement to have an even more accurate model. 
</p>
</p>
<b>Project Goal:</b>
The goal of this project was to use natural language processing and classification models to identify terms for predicting a readme's primary language on Github.
</p>
</p>
<b>Discoveries and Recommendations:</b>


<hr style="background-color:silver;height:3px;" />

## Data Dictionary
<hr style="background-color:silver;height:3px;" />

|Target|Definition|
|:-------|:----------|
| Language | The primary coding language identified in the GitHub repository|

|Feature|Definition|
|:-------|:----------|
| content       | Content's of the repository's readme.md (String) |
| repo        | partial repo URL |

<hr style="background-color:silver;height:3px;" />

## Reproducing this project
<hr style="background-color:silver;height:3px;" />

You can reproduce this project with the following steps:
> - Read this README
> - Clone the repository. Alternatively, you can download the .py, .json and Final_Report from the main folder.
> - Run the Final_Report notebook or explore the other notebooks for greater insight into the project.

If you want to recreate this with your own list of repos:
> - Clone the repository
> - Remove the repos.csv and data2.json files.
> - Read through the acquire.py functions and update the search URL with any keyword changes or increase the number of results.
> - run "python acquire.py" from your terminal to generate the csv and json files.
> - Step through the Final Report and other notebooks.  You may want to modify which languages are viewed.


