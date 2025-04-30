from collections import Counter
from nltk.collocations import *
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk.corpus import stopwords
import os
from tqdm import tqdm
from nltk.probability import FreqDist
import pandas as pd
import csv
import re

punctuation = r'[^\w\s_-]|(?<!\w)[_-]|[_-](?!\w)'
stop_words = set(stopwords.words('english'))
stop_words.update(["also", "even", "often"])

def detect_bigrams_frequencies(input_path,output_path,chunk_size=10000):

    all_files =os.listdir(input_path)
    all_files.sort()
    for f in all_files:

        # Instantiate global freq and corpus length
        global_bigram_freq = FreqDist()
        corpus_length = 0

        # number of lines for tqdm
        total_lines = sum(1 for _ in open(input_path + f)) - 1  # -1 for header

        # Read the CSV file in chunks
        for chunk in tqdm(pd.read_csv(input_path + f, chunksize=chunk_size), 
            desc=f"Chunks in {f}", 
            total=total_lines // chunk_size + 1):

            words = []

            for index, row in chunk.iterrows():
                
                # Exclude empty comments if any
                if type(row['comment']) != str:
                    print('not a string')
                    print(row['comment'])
                    pass

                else:

                    # Remove charachters that are not words. Leave dashes.
                    comment = re.sub(punctuation," ",row['comment'])

                    # Tokenize comments
                    tokens = word_tokenize(comment.lower())

                    # Remove punctuation inside tokens
                    tokens = [re.sub(punctuation, '', i) for i in tokens if re.sub(punctuation, '', i)] 
                    for tok in tokens:
                        if tok != "":
                            words.append(tok)
        
            # Considers all sequences of bigrams in the text as collocations by default
            finder = BigramCollocationFinder.from_words(words)
        
            # Filters out bigrams containing stopwords
            finder.apply_word_filter(lambda w: w in (stop_words))

            # Gets raw counts of bigrams
            bigram_freq = finder.ngram_fd

            # Update global count
            global_bigram_freq.update(bigram_freq)

            # Update corpus length for pmw calculation
            corpus_length += len(words)

        # Sorting bigrams from the most frequent to the least
        sorted_bigrams = sorted(global_bigram_freq.items(), key=lambda x: x[1], reverse=True)

        with open(output_path+f.split('.')[0]+"_bigrams.csv", 'w') as csv_outfile:
            writer = csv.writer(csv_outfile)
            writer.writerow(["bigram", "pmw", "raw frequency"])

            for item in sorted_bigrams:

                # # Filters out bigrams with a frequency less than 10
                if item[1]<10:
                    pass
                else:
                    writer.writerow([item[0], ((item[1]/corpus_length)*1000000), item[1]])

input_path = [directory where csv file with corpora are stored]
output_path = [directory where csvc file with bigrams and pmw frequencies are stored]

detect_bigrams_frequencies(input_path,output_path)
