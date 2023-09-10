import pandas as pd
from collections import Counter, OrderedDict
import operator
import ujson
from nltk.tokenize import word_tokenize
import glob

class FrequencyStat_flavor():
    keyword_file = "Copy_of_e-cig_brand_list_3.xlsx"
    keywords = []
    list = []

    def extract_keywords(self):
        input_keyword_file = pd.read_excel(self.keyword_file)   #read keyword file
        self.keywords = input_keyword_file.iloc[:, 1].tolist()  #make flavor names in excel column 1 as keywords
        self.keywords = list(set(self.keywords))


    def contains(self, line):
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
        for s in self.keywords:
            if s in string:
                self.list.append(s)   #if flavor names mentioned in the tweets, add the flavor name to the list


    def name_file(self, inputFile, outputFile):
        f = open(outputFile, "a")
        src = open(inputFile, "r")
        for line in src:
            self.contains(ujson.loads(line))
        dic = Counter(self.list)  #count flavor name mentioned frequency
        dic = OrderedDict(sorted(dic.items(), key=operator.itemgetter(1), reverse=True))  #reserved order by frequency

        with open(outputFile, 'w') as f:
            for key in dic.keys():
                f.write("%s,%s\n" % (key, dic[key]))  #write csv file with flavor name and its frequency stats
        f.close()
        src.close()
        self.list.clear()

    def __init__(self):
        self.extract_keywords()
        for f in glob.glob('filtered_ecig_promo_flavor.json'): #read input file
            self.name_file(f, (f[:-5] +".csv"))  #set the output filename same as the input filename, just change the file type from .json to .csv


if __name__ == '__main__':
    stat = FrequencyStat_flavor()