import glob
import itertools
import collections

from functools import partial

import numpy as np  # math
import random       # probabilty
import pandas as pd # handling table data
import calendar     # for generating random dates

# statistics
import scipy
import scipy.stats as scis

# astrology part
import flatlib
from flatlib.geopos import GeoPos
from flatlib.datetime import Datetime
from flatlib.chart import Chart


def generate_aspects_mapping_dict():
    """Genete dict where keys are all possible values of aspects combinations. We need
    this to build a vector for each profession. If for some professions some aspects are
    not presented then it will be equal to 0.
    """
    
    # get dict of all possibile combinations planets with aspects
    planets = flatlib.const.LIST_OBJECTS
    aspect_names = list(ANGLE_2_ASPECT.keys())
    planet_combinations = list(itertools.product(planets, planets, aspect_names))
    # remove cases aspects of the same planet, e.g. Sun Sun
    possible_combintaions = list(filter(lambda x: x[0]!=x[1], planet_combinations))
    # change structure to `planetX-planetY-aspect`
    possible_combintaions = list(map(lambda x: ''.join((x[0]+'-'+x[1]+'-'+x[2])), 
                                     possible_combintaions))
    # generate dict to map unique key with unique index
    IND2KEY = {k:v for k, v in enumerate(possible_combintaions)}
    KEY2IND = {v:k for k, v in IND2KEY.items()}    
    return IND2KEY, KEY2IND


ANGLE_2_ASPECT = {'CONJUNCTION': 0, 'SEXTILE': 60, 'SQUARE': 90, 'TRINE': 120, 
                'OPPOSITION': 180}
ASPECT_2_ANGLE = {v:k for k, v in ANGLE_2_ASPECT.items()}
MIN_COLUMNS = ['name',  'date',  'category',  'sign_code',  'east_horo', 'astro_format', 
               'sign',  'day',  'month',  'year']
SIGNS_LIST = ['Kozerog', 'Vodoley', 'Ryby', 'Oven', 'Telec', 'Bliznecy', 'Rak', 'Lev', 
             'Deva',  'Vecy', 'Scorpion', 'Strelec']
IND2KEY, KEY2IND = generate_aspects_mapping_dict()


def create_df_from_all_files_in_folder(folder):
    """Concat all file from folder to one dataframe."""
    all_files = glob.glob('folder/' + "/*.csv")
    dummy = []
    for file_ in all_files:
        data = pd.read_csv(dummy, header=0)
        dummy.append(data)
    data = pd.concat(dummy)
    del data['Unnamed: 0']
    return data


################################################################################
########################## ASTROLOGICAL'S HELPERS ##############################
################################################################################

def calculate_chart(date, time='17:00', utcoffset='+00:00', lat='55n45', lon='37e36'):
    """Calculates astrological chart based on a person's birth date, time and location. 
    Using flatlib library. 
    
    Args:
        bdate (str): with format `2015/03/13`
        time  (str): with format `17:00`
        utcoffset (str):  UTC Offset with format `+00:00`
        lat (str): latitude of birth location
        lon (str): longtitude of birth location
     
    Returns:
        chart (flatlib.chart.Chart): chart object with astrological information 
            such as plantes positions and so on.
    """
    
    # create flatlib.datetime object 
    date = Datetime(date, time, utcoffset)
    # create flatlib.geopos object
    location = GeoPos('55n45', '37e36')
    # calculate chart 
    chart = Chart(date, location, IDs=flatlib.const.LIST_OBJECTS)
    return chart


def calculate_aspects(chart: flatlib.chart.Chart):
    """Calculate all existing aspects (angles between planets) based on a chart.
    
    Returns:
        aspects (list): list where elements are flatlib.aspects.Aspect object. So 
            each element in the list is an aspect. To see aspect `print(aspects[0])`.
            
    Example:
        aspects[0].__dict__ - returns all properties
        aspects[0].active.id, aspects[0].passive.id - derive planets from aspect. 
        real_aspects[0].orb - to derive orbis of the aspect. This is deviation from 
            theoretical angle to form an aspect.
    """  
    
    # get planets from chart
    planets = [i for i in chart.objects]    
    # calculate aspects each with each planets, if aspect doen't exist element in 
    # list will equal -1
    aspects = [flatlib.aspects.getAspect(*pair, aspList=flatlib.const.MAJOR_ASPECTS) \
              for pair in itertools.product(planets, planets)] 
    # filter existing aspetcs from -1 (i.e. aspect doesn't exist)
    aspects = [angle for angle in aspects if angle.type != -1]
    return aspects


def flatlib_aspetcs_to_string(aspect: flatlib.aspects.Aspect):
    """Derives info from a flatlib.aspects.Aspect."""
    
    data = {'active': aspect.active.id, 
            'passive': aspect.passive.id, 
            'aspect': ASPECT_2_ANGLE[aspect.type], 
            'orbise': aspect.orb}
    string = data['active']+'-'+data['passive']+'-'+data['aspect']
    return string


def calculate_aspects_in_profession(data: pd.core.frame.DataFrame, professtion: str): 
    """Returns list with all aspects for each sample in profession. So we just loop 
    over each sample in profession and add all aspects from this sample to common 
    list of aspects for this profession. 
    """
    
    data = data.loc[data.category==professtion].copy()              # filter profession from df
    data.loc[:, 'chart'] = data.astro_format.apply(calculate_chart) # add chart to df
    data.loc[:, 'aspects'] = data.chart.apply(calculate_aspects)    # add aspects to df
    # add sample aspects to list with aspects from all
    profession_aspects = []
    for row in data.iterrows():
        person_aspects = row[1]['aspects']
        profession_aspects.extend(person_aspects)        
    return profession_aspects


def calculate_aspects_from_dates(dates: list): 
    """ 
    """
    
    data = pd.DataFrame(dates, columns=['date'])           # generate dataframe
    data['chart'] = data.date.apply(calculate_chart)       # add chart to df
    data['aspects'] = data.chart.apply(calculate_aspects)  # add aspects to df
    
    # add sample aspects to list with aspects from all
    flatlib_aspects = []
    for row in data.iterrows():
        person_aspects = row[1]['aspects']
        flatlib_aspects.extend(person_aspects)      
    
    # convert to string
    aspects_string = list(map(flatlib_aspetcs_to_string, flatlib_aspects))
    sum_of_aspects = collections.Counter(aspects_string)
    return sum_of_aspects


def calculate_sum_of_aspects_for_profession(
    data: pd.core.frame.DataFrame, profession: str) -> collections.Counter:
    """Take a dataframe, filter for profession, calculate aspects for each sample in 
    profession and append to common list of aspects for profession. Then just count 
    each aspect and returns a dict (collections.Counter) where keys are existing in 
    profession aspects and values are number of each aspect in profession.
    """
    
    # calculate aspects in flatlib format for each sample in profession
    flatlib_aspects = calculate_aspects_in_profession(data, profession)
    # convert flatliub aspects to string
    aspects_string = list(map(flatlib_aspetcs_to_string, flatlib_aspects))
    # count among of each aspect in profession
    sum_of_aspects = collections.Counter(aspects_string)
    return sum_of_aspects


def create_profession_vector(sum_of_aspects: collections.Counter) -> dict:
    """Function takes a dict where keys are aspects for profession, values 
    are number of aspect in profession and returns dict with all possible 
    aspects and if aspects is present then show number of this aspect. So simply 
    saying it's a vector for profession in a space of all possible aspects.
    
    Args:
        sum_of_aspects: this is receiver threough collections.Counter(), i.e.
            it's a dict which inform about how many and what aspects occurs in 
            all sample in profession.
    Returns a dict will number of aspects for a profession. Number of all aspects.
        It's some aspects not presented then aspect equal to 0.
    """
    
    # init dummy dict with all aspects combinations as keys as 0 values 
    dict_vector = dict.fromkeys(list(KEY2IND.keys()), 0)
    # fill dict with presented in profession aspects and they numebers
    for aspect in sum_of_aspects.items():
        dict_vector[aspect[0]] = aspect[1]  # 0 means key, 1 means value         
    return dict_vector


def generate_random_bdates(year_min: int, year_max: int, n_samples: int) -> list: 
    """Generates random birth dates from defined years range and returns a list. 
    Generated outputs should have the followint structure: year/month/day e.g. 1988/2/29."""
    
    years  = np.random.randint(year_min, year_max, size=n_samples)
    months = np.random.randint(1, 13, size=n_samples)
    
    # get max days in month dependent from year and month
    days_range  = list(map(calendar.monthrange, years, months)) # monthrange -> (1, 31) i.e. days range
    max_day_in_month = [i[1]+1 for i in days_range]  # +1 for np.random.randint function
    random_day = partial(np.random.randint, 1)       # means for low in randint always use 1
    days = list(map(random_day, max_day_in_month))   # random from day 1 to max day + 1   
    # combine all together in required sctructure: `year/month/day`
    date = [''.join((str(y), '/', str(m), '/', str(d))) for y, m, d in zip(years, months, days)]    
    return date


def calculate_each_person_vector_in_profession(data: pd.core.frame.DataFrame, professtion: str): 
    """Returns list with dict for each person in profession. Dict keys already 
    strings, i.e. not flatlib aspects. If aspects is present for person that the
    key with this aspect equal to 1, other equal to 0.
    """
    
    data = data.loc[data.category==professtion].copy()                    # filter profession from df
    data.loc[:, 'chart'] = data.astro_format.apply(utils.calculate_chart) # add chart to df
    data.loc[:, 'aspects'] = data.chart.apply(utils.calculate_aspects)    # add aspects to df    
    # add sample aspects to list with aspects from all
    profession_aspects = []
    for row in data.iterrows():
        flatlib_aspects = row[1]['aspects']      
        # convert flatlib aspects to string
        aspects_string = list(map(utils.flatlib_aspetcs_to_string, flatlib_aspects))     
        # init full dummy vector for sample (person) with 0 values for each aspect
        person_vector = dict.fromkeys(list(utils.KEY2IND.keys()), 0)        
        # assign 1 to aspects which present for sample 
        for row in person_vector.items():
            if row[0] in aspects_string:
                person_vector[row[0]] = 1        
        # add persons vector to category list
        profession_aspects.append(person_vector)       
    df = pd.DataFrame(profession_aspects)
    df['category'] = professtion
    return df




################################################################################
############################### REWORK THESE SHIT ##############################
################################################################################
def get_sign(month, day):
    # add zero before day 
    day_month = {'month' : month, 'day' : day}
    if day_month['day'] <= 9:
        day_month['month'] *= 10
    # convert to one value
    l = [str(v) for k, v in day_month.items()]
    converted_date = int(l[0] + l[1])
    # convert date to sign
    global sign_list
    sign_list = ['Kozerog', 'Vodoley', 'Ryby', 'Oven', 'Telec', 'Bliznecy', 'Rak', 
                 'Lev', 'Deva',  'Vecy', 'Scorpion', 'Strelec']
    zodiacs_list = [(120, 'Kozerog'), (218, 'Vodoley'), (320, 'Ryby'), (420, 'Oven'), 
                    (521, 'Telec'), (621, 'Bliznecy'), (722, 'Rak'), (823, 'Lev'), 
                    (923, 'Deva'), (1023, 'Vecy'), (1122, 'Scorpion'), (1222, 'Strelec'), 
                    (1231, 'Kozerog')]
    for z in zodiacs_list:
        if converted_date <= z[0]:
            return z[1]
        
        
def get_animal(year):
    global animals_list
    animals_list = ['Krysa', 'Buk', 'Tigr', 'Krolik', 'Drakon', 'Zmeya', 'Loshad', 
                    'Koza', 'Obezyana', 'Petuh', 'Sobaka', 'Svinya']
    years_to_animal = dict(zip((np.arange(12) + 1960), animals_list))
    if year > (11 + 1960):
        while year not in years_to_animal.keys():
            year -= 12
        return years_to_animal[year]
    elif year < 1960:
        while year not in years_to_animal.keys():
            year += 12
        return years_to_animal[year]
    
    
def bar_by_sign(dataframe, customer):
    data = dataframe[dataframe['Sign Name'] == customer['sign']]
    num_range = range(len(data))
    plt.bar(num_range, data['Name'].values)
    plt.xticks(num_range, data['Category'], rotation=90)

    
def search_by_sign(dataframe, day, month, plot=True):
    # define sign
    sign = get_sign(month, day)
    data_per_customer_sign = dataframe[dataframe['Sign Name'] == sign]['Category'].value_counts().sort_index()
    num_per_cat = dataframe['Category'].value_counts().sort_index()
    # convert to % related to category
    data_per_customer_sign__norm = (data_per_customer_sign.values / num_per_cat.values) * 100
    # convert to dataframe
    data_per_customer_sign__norm = pd.DataFrame(list(zip(num_per_cat.index, data_per_customer_sign__norm)),
                                           columns=['Category', '%'])
    # plot results
    if plot:
        fig, ax = plt.subplots(figsize=(15, 6))
        bins = ax.bar(range(len(num_per_cat)), data_per_customer_sign__norm['%'].values, facecolor='green', edgecolor='gray', 
                      alpha=0.5, width=0.9)
        plt.xticks(range(len(num_per_cat)), data_per_customer_sign__norm['Category'].values, rotation=90)
        plt.xlabel('Профессии')
        plt.ylabel('% от общего приходящийся на знак')
        plt.plot([-1, 50], [(1/12) * 100, (1/12) * 100], '--')
        plt.legend()
        plt.rcParams['xtick.labelsize'] = 14
        plt.show()
    return data_per_customer_sign__norm.sort_values(by=['%'])


################################################################################
############################ STATISTIC'S HELPERS ###############################
################################################################################
def chi_square_goodness_of_fit(observed_freqs=None, expected_freqs=None, accuracy=0.95, verbose=1):
    """Function returns - True when null hypothesis rejected.
    
    Args:
        observed_freqs (list): list with num of sample for each column
        expected_freqs (list): the same len list with expected freqs
    """
    
    n = sum(observed_freqs)
    assert n > 5, 'With less that 5 sample test is invalid.'
    df = len(observed_freqs) - 1
    chi_square = sum((observed_freqs - expected_freqs)**2 / expected_freqs)
    # critical value of chi for defined by user accuracy 
    crit = scipy.stats.chi2.ppf(q = accuracy, df = df)
    
    if verbose:
        print(f'Degree of freedom - {df}') 
        print(f'Critical value - {crit}')
        print(f'Calculated Chi-square value - {chi_square}')       
        print('Null hypothesis is refected!') if chi_square > crit else print('Null hypothesis is confirmed!')
    return True if chi_square > crit else False


def cramers_stat(confusion_matrix):
    chi2 = scis.chi2_contingency(confusion_matrix)[0]
    n = confusion_matrix.sum()
    return np.sqrt(chi2 / (n*(min(confusion_matrix.shape)-1)))


