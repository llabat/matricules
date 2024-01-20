import os
import time
import pandas as pd
import numpy as np

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import WebDriverException, NoSuchElementException

from utils import TooManyResults, NoResults
from const import COMPLEMENT, BUREAUX, PARIS_WEBSITE

class Crawling_Spider(object):

    def __init__(self, comblist, webdriverpath, mainsite):
        
        # comblist : (ngram : str, clas : int) List
        # webdriverpath : str
        self.comblist = comblist
        self.webdriverpath = webdriverpath
        self.mainsite = mainsite
        
        # store pandas-parsed html in a list
        self.data = []
        self.df = []
        self.collected = False
        
        # save unsuccessful combinations
        self.no_results, self.too_many_results, self.trifails = [], [], []
        
        # sets up and stores the chrome webdriver
        self.driver = webdriver.Chrome(self.webdriverpath)
        
        # launches the spider on the comblist
        self.main()

    def parse(self, page_source):
        # page_source : html (str)

        # use the pandas function to parse html tables
        tables = pd.read_html(page_source,extract_links='body')
        # collect the table
        table = tables[0]
        # format the table to keep relevant info
        for col in table.columns[:-1]:
            table[col] = pd.DataFrame([table[col][r][1] for r in range(len(table[col]))],columns=[col]) if col in {"details","Unnamed: 5"} else pd.DataFrame([table[col][r][0] for r in range(len(table[col]))],columns=[col]) 
        # remove the htmlese to have the link as value
        table["link"] = pd.DataFrame([COMPLEMENT+table["Unnamed: 5"][r][1].replace('javascript:ArkVisuImage(\'','').replace("' );","") for r in range(len(table))])
        table["details"] = COMPLEMENT+table["details"]
        # remove used col
        table = table.drop(["Unnamed: 5"],axis=1)
        
        return table
    
    def send_parameters(self, ngram, clas, bureau = None):
        # send parameters to the search engine
        # ngram : str
        # clas : str
        
        self.driver.get(self.mainsite)
        time.sleep(3)

        search_bar = self.driver.find_element("css selector","#form_rech_230")
        search_bar.send_keys(ngram)

        search_bar = self.driver.find_element("css selector",".champ_formulaire~ h4+ .champ_formulaire input")
        search_bar.send_keys(clas)
        
        if bureau:
            select = Select(self.driver.find_element('id','form_rech_237'))
            select.select_by_value(bureau)

        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        self.driver.find_element("css selector",".rechercher").click()
        time.sleep(3)
        
    def test_results(self):
            
        try:
            # pay attention to possible alert messages
            alert = self.driver.find_element('css selector',".alerte span")
            if alert.text == "Aucun résultat pour cette recherche":
                raise NoResults
            if alert.text == "500 résultats maximum, merci d'affiner votre recherche":
                raise TooManyResults
                
        except NoSuchElementException:
            print("Successful combination (less than 500 results)")
        
        return True
        
    def exhaust_combination(self):
        
        # iterates over all pages available for the search parameter combination
        while True :
            try:
                page_source = self.driver.page_source
                self.data.append(self.parse(page_source))
                self.driver.maximize_window()
                self.driver.find_element("link text",">").click()
                time.sleep(2)
                
            except NoSuchElementException :
                print("All pages were scraped.")
                self.df = pd.concat(self.data) if self.data else None
                self.collected = True if self.data else False
                break
    
    def process(self, ngram, clas):
        
        self.send_parameters(ngram, clas)
        try :
            self.test_results()
        except NoResults :
            self.no_results.append((ngram, clas))
            print(ngram + ":" + clas+ " est une combinaison infructueuse")
            return
        except TooManyResults :
            for bureau in BUREAUX:
                try:
                    self.send_parameters(ngram, clas,bureau=bureau)
                    self.test_results()
                    self.exhaust_combination()
                    continue
                except NoResults :
                    print(ngram + ":" + clas+ ":"+ str(BUREAUX.index(bureau)) + " est une combinaison infructueuse")
                    continue
                except TooManyResults :
                    self.trifails.append((ngram,clas,str(BUREAUX.index(bureau))))
                    print(ngram + ":" + clas+ ":"+ str(BUREAUX.index(bureau)) + " est une combinaison à affiner")
                    continue
            return
        self.exhaust_combination()
    
    def clear(self):
        self.df = pd.DataFrame([])
        self.data = []

    def main(self):
        for comb in self.comblist:
            self.process(comb[0], comb[1])
            filename = "/Users/leolabat/Desktop/triparam/" + comb[0]+ "_" + comb[1] + ".csv"
            if self.collected : self.df.to_csv(filename)
            self.clear()
            
        self.driver.quit()