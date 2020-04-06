# Career Guidance 
Small descrption here

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

![samples distribution](https://github.com/linkyeu/career_guidance/blob/master/images/samples_distribution_per_profession.png)</br>
_Figure 1_ - Few professions have more number of samples that 5k and only one 30k. Number of samples already have meaning. At least could be interpreted as profession popularity. Also time range for profession's samples could be interpreted as profession popularity in that specific time.

![year of birth distribution](https://github.com/linkyeu/career_guidance/blob/master/images/disribution_year_of_birth.png)
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
![chi_square_goodness_of_fit](https://github.com/linkyeu/career_guidance/blob/master/images/chi_square_goodness_of_fit.png)</br>
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
![chi_square_each_with_each](https://github.com/linkyeu/career_guidance/blob/master/images/chi_square_each_with_each.png)</br>
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


# Aspects 
First question is what are hell is that?) Add brief and clear review waht is that and why we are using it here. 
For aspects calculation we definetly needs birth location at least approximate and need to convert location to coordinats.I have several assumption about how to predict proffesion based on aspects.  First assumption is to build a general profession representation in aspects space. I mean that totaly exist 1050 of aspects but each person have some aspects, it could be any arbitrary number of aspects. 

__Main assumptions__
- People with similar aspects will be successful in similar professions
- Aspects have relationship with personal trails and profession

__Show plot where mean number of aspects per each proffession__

Person's professions list should be predicted based on one with each profession classifier. Probably I can build method which compare similarity between two one how vectors. Or even use cosine similarity. Or if estimate compare to each it will be necessery to save value of aspect insted of 1 or -1. COnvert to 10 or 100. </br> In previous research I analysed only astrologica sign, but when we analys aspects we decompose astrological sign to partial variables. In such way we can derive more detailed information because astrological sign is combined all this information.

##  Aspects dataset
In this research I represent persons in terms of aspects. In same way from wikipedia were parsed data with bdate, location of birth, image and profession. Need to be clear that very few people has only one profession, mostly people were succed in several profession. Actors oftern do movie_ making, scenrio, write books. Mathematics or engineers often works at universities and learn students and so on. So while preprocessing of data we should not remove samples with several labels (profession). 

`Here is a plot which describe samples with several professions`</br>

Aspects calculation required a geographic position on Earth given by a latitude and longitude in birth location, i.e. `(latitude='38n32', longititude='8w54')`. Northern latitudes and eastern longitudes have positive values, while southern latitudes and western longitudes have negative values. Location of birth parsed from wikipedia is in a string format: 'Kiev', 'USA', 'Moscow'. Wikipedia also contains coorinates of places. So it's better to parse these coordinates directly from wikipedia. 

Aspects for each person in dataset were calculated using [flatlib](https://flatlib.readthedocs.io/en/latest/) python library. First we calculate astrological chart (position of the planets at the time of birth).

### Professions representation in aspects vector space
Sparse one hot vectors were build for each profession to represent profession in aspect's vector space. Vectors were calculated in the following way:

We take birth dates of people who fulfilled themselves in different professions. Let's analys how ofter (or rare) the same aspects occur in groups of people with similar professions. To do this we need to calculate number of repeated aspects in they birth dates and if we find matches will test it statisticaly. 

- Take one profession
- Calculate aspects for people from this profession

## Model 1 - Cosine similarity
Here I made attemt to predict profession based on similarity between user and existing users with profession. Cosine similarity calculated between user row aspects vector and matrix with row users aspects. In result we derive similarity between user and users with professions. Then just take top n users with highest similarity and see they profession. Issue here that some professions has a lot of samples and they everywhere in vector space, since signal (aspects) contains noise. 

__Solution 1:__ take more N samples to avoid noise like football players and other sportsmens.</br>
__Solution 1.1:__ Use PCA to reduce noise. But how many variance PCA should describe? take more N samples to avoid noise like football players and other sportsmens.</br>
__Solution 2:__ build vector per each profession instead of vector for each sample. Take the same cosine similarity. How to build profession vector? Filter noise with randomly calculated aspects. How many sigmas to use?
__Solution 3:__ make PCA reduction. use collaborative filtering  with several layers.





## Model 2 - Collaborative filtering
In this approach I built a recommendational system based on cosine similarity between user vector and profession vectors. Data processing held in the following way:
- Aspects were calculated for all persons within each profession
- All same aspects within professions were summed 
- Random date generated and aspects calculated within each profession 
- Professions vectors with actual and randomly generated are substracted
- Resulting vectors for each profession are filtered so all values less than 3* stddev = 0, other 1



## Use Fast.ai to build recomendational system 



### Usefull links:
https://towardsdatascience.com/paper-review-neural-collaborative-filtering-explanation-implementation-ea3e031b7f96

https://www.excavating.ai/
https://towardsdatascience.com/various-implementations-of-collaborative-filtering-100385c6dfe0
http://axon.cs.byu.edu/~martinez/classes/778/Papers/GP.pdf
https://hackernoon.com/introduction-to-recommender-system-part-1-collaborative-filtering-singular-value-decomposition-44c9659c5e75




### TODO
- I should train multiclass classifier or recomenrdation system since one person could be in different professions. If person good in sport it doesn't mean he good only in sport!



 


`*` - wikipedia.org

__TODO:__
- Add `magic` with degrees between planets (ascpects) in date and approx. location of birth. 
- Builde a recommendation system (classifier) based on hypothesis testing results for frequency of specific aspects/they combinations for specific profession
- BIG5/ MBTI for determining personal traits and required traits for success in profession (Exploratory Factor Analysis)
- Predict astrological sing/personal traits with image (face). Face should be cropped and 3D face reconstruction should be performed to align face
- Analys possibility of predicted face areas responding for `serial killer` patterns 
- Build 3D plot with embeded professions and astrological signs. Analys how they distributed in space.
- (optional) Reparse wiki with images and locations of birth
- (optional) convert locations to coordinates
- (optional) remove all peoples with several professions or merge them in separate group


#### Conclutions

