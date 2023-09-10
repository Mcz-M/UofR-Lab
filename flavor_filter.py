import ujson
import pandas as pd



class FlavorFiltering:

    keyword_file = "Copy_of_e-cig_brand_list_3.xlsx" #favor list excel file
    keywords = []


    def extract_keywords(self):
        input_keyword_file = pd.read_excel(self.keyword_file) #read excel file
        self.keywords = input_keyword_file.iloc[:, 1].tolist() #take flavor names as keywords, which is the column with index 1

    def main(self):
        self.extract_keywords() 
        print(self.keywords)
        self.filter_flavor()

    def contains(self,line):
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
        
        for s in self.keywords:
            if (s in string.lower()):
                return True
        return False

    def filter_flavor(self):
        with open("filtered_ecig_promo_flavor.json", 'w') as output: #output filename
            with open("filtered_ecig_promo.json", 'rb') as src:  #input filename
                for line in src:
                    parsedJsonRecord = ujson.decode(line)
                    if self.contains(parsedJsonRecord):
                        output.write(ujson.dumps(parsedJsonRecord) + '\n')

        output.close()
        src.close()


if __name__ == '__main__':
    flt = FlavorFiltering()
    flt.main()