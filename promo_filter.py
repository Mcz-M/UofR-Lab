import ujson
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from collections import Counter  
import csv
import re
from pandas import DataFrame


class promoFiltering:

    keywords = ["dealer", "deal", "supply", "e-cig", "e-cigs", "ecig", "ecigs", "electroniccigarette", "vapin" ,"vape", "vapers", "vaping", "vapes", "vapor", "e-liquid", "ejuice", "eliquid", "e-juice", "vapercon", "vapeon", "vapefam", "vapenation", "juul", "store", "promo", "promotion"]
    #promotion keywords for username and user screen name
    keywords2 = ["dealer", "deal", "customer", "promotion", "promo", "promos", "discount", "sale", "free shipping", "sell", "$", "%", "dollar", "offer", "percent off", "store", "save", "price", "wholesale"]
    #promotion keywords for Twitter content

    def main(self):
        self.filter_promo()

    def contains1(self, line):  #detect whether the username contains promotion keywords
        string = ""
        if "user" in line:
            if "name" in line["user"]:
                string = line["user"]["name"]
        string = string.lower()

        for s in self.keywords:
            if (s in string):
                return True
        return False   

    def contains2(self, line):  #detect whether the user screen name contains promotion keywords
        string = ""
        if "user" in line:
            if "screen_name" in line["user"]:
                string = line["user"]["screen_name"]
        string = string.lower()

        for s in self.keywords:
            if (s in string):
                return True
        return False  

    def contains3(self, line):   #detect whether the username being retweeted by others contains promotion keywords
        string = ""
        if "delete" not in line:
            is_retweet = True if (line["text"].startswith("RT @")) else False
            if "retweeted_status" in line:
                if is_retweet:
                    if "user" in line["retweeted_status"]:
                        string = line["retweeted_status"]["user"]["name"]
        string = string.lower()

        for s in self.keywords:
            if (s in string):
                return True
        return False

    def contains4(self, line):   #detect whether the twitter content contains promotion keywords
        string = ""
        if "delete" not in line:
            is_retweet = True if (line["text"].startswith("RT @")) else False
            if "retweeted_status" in line:
                if is_retweet:
                    if "extended_tweet" in line["retweeted_status"]:
                        string = line["retweeted_status"]["extended_tweet"]["full_text"]
                    else:
                        string = line["retweeted_status"]["text"]
                else:
                    string = line["extended_tweet"]["full_text"] if "extended_tweet" in line else line["text"]
            else:
                string = line["extended_tweet"]["full_text"] if "extended_tweet" in line else line["text"]
        
        string = string.lower()
        for s in self.keywords2:
            if (s in string):
                return True
        return False   

    def filter_promo(self):
        with open("filtered_ecig_promo.json", 'w') as output:  #output file
            with open("filtered_ecig.json", 'rb') as src:   #input file
                for line in src:
                    parsedJsonRecord = ujson.decode(line)
                    if (self.contains1(parsedJsonRecord) is False) and (self.contains2(parsedJsonRecord) is False) and (self.contains3(parsedJsonRecord) is False) and (self.contains4(parsedJsonRecord) is False): 
                        #if all four conditions are not included in the json entry, then we count that entry as a non-promotion tweets
                        output.write(ujson.dumps(parsedJsonRecord) + '\n')
        output.close()
        src.close()


if __name__ == '__main__':
    promoFiltering().main()