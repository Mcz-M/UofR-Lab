import ujson
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize


class ecigFiltering:

    keywords = ["e-cig", "e-cigs", "ecig", "ecigs", "electroniccigarette", "vape", "vapers", "vaping", "vapes", "e-liquid", "ejuice", "eliquid", "e-juice", "vapercon", "vapeon", "vapefam", "vapenation", "juul"]


    def main(self):
        self.filter_ecig()

    def contains(self, line):  #detect whether those ecig-related keywords are in the Twitter contenct
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
        
        string = string.lower()   #make the tweets in lower case
        string = word_tokenize(string)   #tokienize the tweets by space
        
        if any(s == string[i] for s in self.keywords for i in range(len(string))):
            return True
        return False   


    def filter_ecig(self):
        with open("filtered_ecig.json", 'w') as output: #output filename
            with open("merged_file.json", 'rb') as src: #input filename
                for line in src:
                    parsedJsonRecord = ujson.decode(line)
                    if self.contains(parsedJsonRecord):
                        output.write(ujson.dumps(parsedJsonRecord) + '\n')

        output.close()
        src.close()


if __name__ == '__main__':
    ecigFiltering().main()