import os
from utils import SEARCH_COMBINATIONS, BUREAUX, COMPLEMENT

class TooManyResults(Exception):
    pass

class NoResults(Exception):
    pass

def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]

search_combinations = SEARCH_COMBINATIONS

def left_to_parse(filepath):
    
    with open(filepath) as f:
            for filename in os.listdir("/Users/leolabat/Desktop/scraping_csv"):
                if filename.endswith(".csv"):
                    bigram, clas = filename.replace(".csv","").split("_")
                    search_combinations.remove((bigram,clas))
    print(f'There are {len(search_combinations)} combinations left to parse')

    return search_combinations