# coding: latin1
import zipfile
import os
from nltk.collocations import *
from nltk import word_tokenize
import pandas as pd
import csv
from collections import Counter
import time
import re
from tqdm import tqdm
import string

def calculate_pmw(input_path, output_path):

    zipped_files = os.listdir(input_path)

    for zf in zipped_files:
        with zipfile.ZipFile(zf, 'r') as zipped_file:
            csv_f = zipped_file.namelist()[0]
            print(csv_f)

            base_name = os.path.basename(csv_f)
        
            with open(base_name.split('.')[0] +'_words_frequency.csv', 'w', newline='', encoding='utf-8') as csv_outfile:
                writer = csv.writer(csv_outfile)
                if '2010' in base_name:
                    timeframe = 't0'
                else:
                    timeframe = 't1'
                writer.writerow(["word", timeframe, "raw frequency"])

                with zipped_file.open(csv_f) as f:
                    
                    df = pd.read_csv(f)
                    time.sleep(10)
                    words = []

                    print("Listing words")
                    
                    for index, row in tqdm(df.iterrows()):
                        
                        comment = re.sub(r'[^\w\s_-]|(?<!\w)[_-]|[_-](?!\w)'," ",row['comment'])
                        tokens = word_tokenize(comment.lower())
                        for tok in tokens:
                            if tok not in string.punctuation:
                                words.append(tok)

                    print("Counting occurrences")
                    
                    occurrences = Counter(words)
                    for key,value in tqdm(occurrences.items()):

                        # Calculate pmw for each word
                        writer.writerow([key, ((value/len(words))*1000000), value])

input_path = '[path to directory containing jsonl.gz files with one comment per line]'
output_path = '[path to directory where csv files with per million word frequencies for each corpus are stored]'

calculate_pmw(input_path, output_path)
