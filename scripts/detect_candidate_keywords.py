import os
from nltk.collocations import *
from nltk.corpus import stopwords
from nltk import word_tokenize
import pandas as pd
import csv
from collections import Counter
import time
import re
from tqdm import tqdm
import string
import numpy as np

stop_words = set(stopwords.words('english'))
stop_words.update(["also", "even", "often"])

def detect_candidate_words(df1_2,initial_keywords,output_path):
    
    candidate_words = []
    freq_change = []

    for index, row in df1_2.iterrows():
        if row['word'] not in stop_words:
            freq_change.append(row['frequency change'])
    
    mean = np.mean(freq_change)
    print("Mean frequency change from t0 to t1:", mean)

    std_dev = np.std(freq_change)
    print("Standard Deviation:", std_dev)

    # Defininf threshold
    threshold = mean+(std_dev*2)   
    print("Threshold:", threshold)             
    
    # Writing all candidate words to csv
    with open(output_path+"candidates_for_semantic_change_sustainable.csv", 'w') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["candidate", "change"])

        for index, row in df1_2.iterrows():
            if row['word'] not in stop_words:
                if row['frequency change'] >= threshold:

                    # Finding candidate words among the manually selected keywords
                    if row['word'] in initial_keywords:
                        candidate_words.append(row['word'])
                        writer.writerow([row['word'], row['frequency change']])
    
    print(f"Candidate words for semantic change: {candidate_words}")
    #return f"Candidate words for semantic change: {candidate_words}"

def compare_frequencies(df1,df2):

    df1 = df1[df1['count'] >= 10]
    df2 = df2[df2['count'] >= 10]

    # Merge DataFrames on the 'word' column to get common words
    common_words_df = pd.merge(df1, df2, on='word', how='inner')

    # Extract columns 't0' and 't1' for the common words
    df1_2 = common_words_df[['word', 'pmw t0', 'pmw t1']]

    # Calculate difference in frequency between t1 and t0
    df1_2['frequency change'] = df1_2['pmw t1'] - df1_2['pmw t0']

    detect_candidate_words(df1_2,initial_keywords,output_path)

def calculate_pmw(input_path,community):

    files = os.listdir(input_path)
    files.sort()

    for f in files:

        if community in f:
            
            if '2010' in f or '2021' in f:
        
                if '2010' in f:
                    timeframe = 't0'
                elif '2021' in f:
                    timeframe = 't1'

                print(community,timeframe)
                    
                df = pd.read_csv(input_path+f, encoding='utf-8')
                time.sleep(10)
                words = []

                print("Listing words")
                
                for index, row in tqdm(df.iterrows(), total=len(df)):
                    
                    comment = re.sub(r'[^\w\s_-]|(?<!\w)[_-]|[_-](?!\w)'," ",row['comment'])
                    tokens = word_tokenize(comment.lower())
                    for tok in tokens:
                        if tok not in string.punctuation:
                            words.append(tok)

                print("Counting occurrences")
                
                occurrences = Counter(words)

                df = pd.DataFrame(list(occurrences.items()), columns=['word', 'count'])

                # Calculate PMW (per million word frequency)
                total_words = len(words)
                df['pmw'] = (df['count'] / total_words) * 1_000_000

                df = df[['word', 'pmw', 'count']]

                if timeframe == 't0':
                    df1 = df
                    df1 = df1.rename(columns={'pmw': 'pmw t0'})
                elif timeframe == 't1':
                    df2 = df
                    df2 = df2.rename(columns={'pmw': 'pmw t1'})
                    
    compare_frequencies(df1,df2)

community = 'sustainable' # Communities
initial_keywords = "../data/policy_documents_keywords.csv" # keywords to be tested for frequency increase

input_path = '[path to directory containing csv files with one comment per line]'
output_path = '[path to directory where csv files with final candidate words and pmw frequencies for each corpus are stored]'

calculate_pmw(input_path,community)
