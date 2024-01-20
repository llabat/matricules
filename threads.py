import time
from crawling import Crawling_Spider
from utils import divide_chunks
from concurrent.futures import ThreadPoolExecutor

from const import SEARCH_COMBINATIONS

class Parallelizer():
    
    def __init__(self, nworkers, combination_list):
        
        self.start_time = time.time()
        self.nworkers = nworkers
        self.combination_list = combination_list
        self.no_results, self.too_many_results = [], []
        
        self.main()
        
    def main(self):

        files = list(divide_chunks(self.combination_list, int(len(self.combination_list)/self.nworkers)) )
        
        with ThreadPoolExecutor(max_workers=self.nworkers) as executor:
            dead_spiders = executor.map(Crawling_Spider, files)
            
        for deads in dead_spiders:
            self.no_results += deads.no_results
            self.too_many_results += deads.too_many_results
        
        addnr(self.no_results)
        addtmr(self.too_many_results) 
        
        print(f'{len(self.combination_list)} combinations were processed in {round((time.time() - self.start_time))} seconds.')

def __main__():

    Parallelizer(14, SEARCH_COMBINATIONS)