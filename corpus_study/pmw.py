# coding: latin1

from nltk.collocations import *
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk.corpus import stopwords
import pandas as pd
import os.path
import csv
from collections import Counter
import time
import re

all_files = os.listdir(input_folder)
filtered_files.sort()

def pmw(input_folder, output_folder):
    for f in all_files:
        with open(output_folder+f.split('.')[0] +'_keywords_frequency.csv', 'w') as csv_outfile:
            writer = csv.writer(csv_outfile)
            writer.writerow(["content word", "pmw", "raw frequency"])
            
            df = pd.read_csv(input_folder+f)        
            words = []
            
            for index, row in df.iterrows():
                
                comment = re.sub(r'[^\w\s_-]|(?<!\w)[_-]|[_-](?!\w)'," ",row['comment'])
                tokens = word_tokenize(comment.lower())
                for tok in tokens:
                    words.append(tok)
            
            occurrences = Counter(words)
            
            for key,value in occurrences.items():
                writer.writerow([key, ((value/len(words))*1000000), value])
input_folder=""
output_folder=""
pmw(input_folder, output_folder)
