# coding: latin1

from collections import Counter
import nltk
from nltk.collocations import *
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk.corpus import stopwords
import os.path
import pandas as pd
import csv
from nltk.probability import FreqDist
import re

list_punct = [",", "\n", ".", ";", '"', "'", "''",  "?", "!", ":", "(", ")", "#", "$", "%", "&", "*", "+", "/", ">", "<", "[", "^", "{", "|", "}", "~", "]", "=", "\\", "@", "...", "``", "..", "---", "--", "__", "___", "....", ".....", "......", ".......", "........", ".........", "..........", "�", "_", "�", "�", "�", "�", "�", "�", "�", "�", "�", "�", "�", "�", "�", "�", "�", "�", "�", "�", "�", "�", "�", "�", "�", "�", "�", "�", "�", "�", "�", "�", "�", "�", "�", "�", "�", "�", "�", "�", "�", "�", "�", "�", "�", "�", "�", "�", "�", "�", "�", "�", "�", "�", "�", "�", "�", "�", "�"]

stopwords = ['i', 'myself', 'does', 'further', 'both', 'y', 'aren', 'won', 'me', 'above', 'do', 'had', 'between', 'no', "wouldn't", 'if', 'off', 'hadn', 'for', 'yourself', 'to', 'ours', "she's", 'own', 'who', 'an', 'under', "aren't", 'which', 'few', 'weren', 'yourselves', 'couldn', 'theirs', 'where', 'why', 'was', 'more', 'am', 'against', 'yours', "couldn't", 'wasn', 'after', 'being', 'what', 'very', 'into', 'his', 'her', 'and', "weren't", 'needn', 'about', 'up', 'you', 'nor', 'itself', "you'd", 'again', 'over', 'there', 'your', 'each', "shouldn't", 'whom', "doesn't", 'because', 'other', 'm', 'when', 'mustn', 'hers', 'while', 'than', "isn't", "won't", 'by', 'from', 'most', 'in', "didn't", 'those', 'be', 'before', "hadn't", 'we', 'all', 'he', 'below', 's', "shan't", 'during', 'out', 'were', 'too', 'they', 'll', 'them', 'doing', 'she', 'here', 'how', 'once', "don't", 'ain', 'didn', 'themselves', 'shan', 'as', 'did', 'have', 'this', "should've", 'at', 'on', "that'll", 'is', 're', 'can', 'him', "wasn't", 'so', 'that', 'a', 'ourselves', 'having', 'but', 'wouldn', 'd', "it's", "you've", "needn't", 'then', 'mightn', 'isn', 'through', 't', 'some', 'himself', 'same', 'my', 'of', 'don', 'these', 'has', 'down', 'any', "haven't", "mustn't", "hasn't", 'or', 'with', 'its', "you'll", 'the', 'our', 'it', "you're", 'such', 'ma', 'are', 'doesn', 'just', 'should', 'shouldn', 'hasn', 'will', 'haven', 'now', 'their', 'herself', "mightn't", 'o', 'until', 've', 'been', 'only', "not", "also", "even", "often"]

def count_bigrams_from_csv_with_sentences(file_path, chunk_size=10000):
    corpus_length = 0
    chunk_number = 0
    
    global_bigram_freq = FreqDist()

    # Read the CSV file in chunks
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
    
        chunk_number += 1
        
        print("Chunk number " + str(chunk_number))
            
        words = []
        
        for index, row in chunk.iterrows():
            
            if type(row['comment']) != str:
                print('not a string')
                print(row['comment'])
                pass
                
            else:
                comment = re.sub(r'[^\w\s_-]|(?<!\w)[_-]|[_-](?!\w)'," ",row['comment'])
                tokens = word_tokenize(comment.lower())
                tokens_1 = [i for i in tokens if i not in list_punct] # exclude tokens that are punct
                tokens_2 = [i.strip("".join(list_punct)) for i in tokens_1 if i not in list_punct] # remove punct from inside tokens
                for tok in tokens_2:
                    if tok != "":
                        words.append(tok)
        
        # Considers all sequences of bigrams in the text as collocations by default
        finder = BigramCollocationFinder.from_words(words)
        
        # Filters out bigrams with a frequency less than 10
        #finder.apply_freq_filter(10)
        
        # Filters out bigrams containing stopwords
        finder.apply_word_filter(lambda w: w in (stopwords))
        
        # Gets raw counts of bigrams
        bigram_freq = finder.ngram_fd
        
        # Update global count
        global_bigram_freq.update(bigram_freq)
        
        # Update corpus length for pmw calculation
        corpus_length += len(words)
    
    sorted_bigrams = sorted(global_bigram_freq.items(), key=lambda x: x[1], reverse=True)
    
    with open(output_dir + 'generic_bigrams.csv', 'w') as csv_outfile: #cambia
        writer = csv.writer(csv_outfile)
        writer.writerow(["bigram", "frequency per million", "raw frequency"])
        for item in sorted_bigrams:
            if item[1]<10:
                pass
            else:
                writer.writerow([item[0], ((item[1]/corpus_length)*1000000), item[1]])

all_files = os.listdir(input_folder)
filtered_files.sort()

for f in all_files:
  count_bigrams_from_csv_with_sentences(f)
