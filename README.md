## Structure of the code
```
├── data                            <- folder for datasets (dataset downloading in statistics.ipynb)
├── notebooks               
│   ├── raw_data_processing.ipynb   <- preprocessing raw data, DRAFT notebook 
│   └── data_analysis.ipynb         <- main notebook with all statistical analysis 
├── images                          <- images for README.md file
└── utils.py                        <- supporter funcs
```

## Table of contents
1. [Introcudction](#introduction)
2. [Data](#data)
3. [Statistical Analysis](#statistical-analysis)
    * [Pearson's chi-squared test (Goodness of Fit)](#pearson's-chi-squared-test-(goodness-of-fit))
    * [Pearson's chi-squared test (Independence)](#pearson's-chi-squared-test-(independence))
    * [Cramer's V](#cramer's-v)
4. [Aspects](#aspects )
6. [Data. Aspects generation](#data-aspects-generation)
7. [Professions representation in aspects vector space](#Professions-representation-in-aspects-vector-space)


## Introduction
The purspose of the project is to determine possibility to predict person's atitude for best suitible profession based on day and month of birth (astrological sign). I was inspired by work of researchers at Columbia University Department of Medicine whos found 55 diseases that were significantly dependent on birth month - [Birth month affects lifetime disease risk:a phenome-wide method](shorturl.at/DUW09).</br>

Also interesing [Shawn Carlson’s “A Double-blind Test of Astrology”](https://www.nature.com/articles/318419a0), published in the journal Nature, in 1985. Full-PDF coule be found [here](http://muller.lbl.gov/papers/Astrology-Carlson.pdf) link. Based on the experiment clear that among other people are not able to make unbised self-estimation in terms of personal trails.</br>

Main problem here is that it's not possible to performe fully controlled double-blind test. Anyway this research is more like funny pet-project that fundamental research project. __So formaly speaking any correlation and hypothesis testing resulys don't mean causation. Double blint test should be held.__</br>

A main purpose of this project is to discover possibility to recommend `best suitible profession based on date of birth`. In terms of current research `best suitible` - means that person can fulfill himself in a profession with less efforts and more easily comparing to others professions. In case of achive statisticaly significant results I will build recomendational system.</br> 

Since I'm not a professional astrologist and don't have enought domain knowledge I will start from simple astological sign (which utilizes day and month information). I don't considering time of birth because I don't have enought data to do such detalied separation. Dividing samples by time I will not receive event one sample in each possible combination. Also based on same assumption and to simplify research I don't use location of birth.

__Main purpose of this research is to build a recomendational system which can recommend appropriate profession for customer.__ The systme should output sorted list of scores where each score is a measure of how easly user can be fullfiled in this profession. Here is my attemp to analys and build a classifier for predicting success in profession based on degrees between planets in time and location of birth. Results should be a score for each profession. Very importany that it should not be single label classifier since more often people has several profession instead on clear one. It's obvious that if man success in sport it doesn't mean he cann't discover potential in some other area. So while building recomendation system I take to account this.</br>

## Data
To prerform this research data from wikipedia.org were used. I wrote a [parser](https://github.com/linkyeu/wikipedia_parser) to parse data from wikipedia. The parser could be used to parse different type of data. More than 100k profiles from 46 profession were parsed and preprocessed to be applicable for further analysis.

Very rare people have one profession. More often it's at least several. Also people were more outstanding that now. Outstanding people in same time did math, physics, write novels, politics. 

![samples distribution](https://github.com/linkyeu/astrology-research-1/blob/master/images/samples_distribution_per_profession.png)</br>
_Figure 1_ - Few professions have more number of samples that 5k and only one 30k. Number of samples already have meaning. At least could be interpreted as profession popularity. Also time range for profession's samples could be interpreted as profession popularity in that specific time.

![year of birth distribution](https://github.com/linkyeu/astrology-research-1/blob/master/images/disribution_year_of_birth.png)
</br>
_Figure 2_ - Plot is also very interesting probably it could be interpreted as profession popularity in very coarse approximation. Some professions are became out of date, e.g. `botanic`. 

__Assumptions about data__</br>
- People in profession's category are fulfilled themselves (achive some success) as professionals because they are presented on wikipedia. There definetly exceptions but I assume they not so much and these exceptions are going to be an noise for regularization. 
- Persons from category is really randomly sampled from population of professionals in specific profession. Simply saying that persons are random sample from population of people fulfilled themselves in own profession.</br>
__These assumptions is main risk for all research.__


## Statistical Analysis
For further analysis I heavily applied - [Pearson's chi-squared test](https://en.wikipedia.org/wiki/Pearson%27s_chi-squared_test) to determine any correlations between month/day birth and professions. 

#### Pearson's chi-squared test (Goodness of Fit)
A test of goodness of fit establishes whether an observed frequency distribution differs from a theoretical distribution*.</br> 
Null hypothesis declares __"Astrological signs within profession have discrete uniform distribution."__</br> 
Alternative hypothesis declares that distribution is not uniform and success in specific profession depends on astrological sign. Test was performed for each profession separately with 95% confidence interval.</br>
![chi_square_goodness_of_fit](https://github.com/linkyeu/astrology-research-1/blob/master/images/chi_square_goodness_of_fit.png)</br>
_Figure 3_ - Pearson's chi-squared test (Goodness of Fit) for each profession.</br>

__Conclution #1:__
Null hypothesis was rejected for some professions with weak trend that it depends on a number of samples. __It means actual astrological signs distribution has statistical significant deviation from theoretical (discrete uniform) distribution for some professions__. Even if null hypotheses rejected it doesn't directly mean that root cause is astrological sign since we declare it in alternative hypothesis. Also I take in account that there some professions which really don't depend from astrological sign (i.e. professions which don't require specefic personal traits).</br>


#### Pearson's chi-squared test (Independence)
A test of independence assesses whether observations consisting of measures on two variables, expressed in a contingency table, are independent of each other (e.g. polling responses from people of different nationalities to see if one's nationality is related to the response)*.</br>
Null hypothesis declares __"Success in profession doesn't depend on astrological sign."__(e.g. there is no relation between profession variable and astrological sign variable)</br> 
Alternative hypothesis declares that success in a profession depends on an astrological sign. Test was held for all professions with same 95% confidence interval.</br>

__Test's results:__
```
Degree of freedom - 495
P_value - 4.4927518254293616e-07
Critical value - 547.8659538616452
Calculated Chi-square value - 665.2745568207469
Null hypothesis is refected!
```
__Conclution #2:__</br>
__TODO: This should beworked. Instead of taking profession pair beter to add eastern animal to astrological sign and test against one profession.__</br>
Degree of freedom is very hight in case when I used all professions (high cardinality). To understand approximatly individual weight of each profession I tested all profession pairs (each with each).</br>
![chi_square_each_with_each](https://github.com/linkyeu/astrology-research-1/blob/master/images/chi_square_each_with_each.png)</br>
_Figure 4_ - Pearson's chi-squared test (Independence) for each professions pairs. _Black cells mean that null hypothesis rejected_</br></br>

 Null hypothesis rejection clearly depends on profession pairs. At least four professions have stong influence (e.g. NH rejected almost no matter on what pair is). __Success in some professions depends from astrological sign and this dependence has statistical significance.__.</br>


#### Cramer's V
In statistics, [Cramér's V]((https://en.wikipedia.org/wiki/Cramér%27s_V)) (sometimes referred to as Cramér's phi and denoted as φc) is a measure of association between two nominal variables, giving a value between 0 and +1 (inclusive). Test help for each pair of profession and also for all professions.</br>

__Test results:__
```
Cramer's V value for all professions: 0.02

Statisctics of Cramer's V value for pairs of professions:
min / max - 0.0/0.15
median - 0.06
```

__Conclutions #3:__
Cramer's V test showed weak relation between astrological sign and success in profession. In same time we conclude that dependency between sign and success in professions is different for profession. It clearly confirm my assumption that some professions don't require specific personal trails or they too weak.</br>

We have relationship between profession and birth date but also clear that it's not enought only astrological sign for profession recommendation. To fix this we need to decompose a birth date to more number of features and these features should be informative. Googling this question I found that all astrological predictions and recomendations are based on angles between planets in birht time and location. So I took this as hypotethis.
