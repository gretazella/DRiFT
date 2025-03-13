import csv
import pandas as pd
import numpy as np

stopwords = ['i', 'myself', 'does', 'further', 'both', 'y', 'aren', 'won', 'me', 'above', 'do', 'had', 'between', 'no', "wouldn't", 'if', 'off', 'hadn', 'for', 'yourself', 'to', 'ours', "she's", 'own', 'who', 'an', 'under', "aren't", 'which', 'few', 'weren', 'yourselves', 'couldn', 'theirs', 'where', 'why', 'was', 'more', 'am', 'against', 'yours', "couldn't", 'wasn', 'after', 'being', 'what', 'very', 'into', 'his', 'her', 'and', "weren't", 'needn', 'about', 'up', 'you', 'nor', 'itself', "you'd", 'again', 'over', 'there', 'your', 'each', "shouldn't", 'whom', "doesn't", 'because', 'other', 'm', 'when', 'mustn', 'hers', 'while', 'than', "isn't", "won't", 'by', 'from', 'most', 'in', "didn't", 'those', 'be', 'before', "hadn't", 'we', 'all', 'he', 'below', 's', "shan't", 'during', 'out', 'were', 'too', 'they', 'll', 'them', 'doing', 'she', 'here', 'how', 'once', "don't", 'ain', 'didn', 'themselves', 'shan', 'as', 'did', 'have', 'this', "should've", 'at', 'on', "that'll", 'is', 're', 'can', 'him', "wasn't", 'so', 'that', 'a', 'ourselves', 'having', 'but', 'wouldn', 'd', "it's", "you've", "needn't", 'then', 'mightn', 'isn', 'through', 't', 'some', 'himself', 'same', 'my', 'of', 'don', 'these', 'has', 'down', 'any', "haven't", "mustn't", "hasn't", 'or', 'with', 'its', "you'll", 'the', 'our', 'it', "you're", 'such', 'ma', 'are', 'doesn', 'just', 'should', 'shouldn', 'hasn', 'will', 'haven', 'now', 'their', 'herself', "mightn't", 'o', 'until', 've', 'been', 'only', "not", "also", "even", "often"]

all_files = os.listdir(input_folder)
filtered_files.sort()

for file in all_files:
    df = pd.read_csv(file_path)
    list_of_changes = []
    
    for index, row in df.iterrows():
        if row['word'] not in stopwords:
            list_of_changes.append(row['change'])   
    
    mean = np.mean(list_of_changes)
    print("Mean:", mean)
    
    std_dev = np.std(list_of_changes)
    print("Standard Deviation:", std_dev)
    
    threshold = mean+(std_dev*2)
    
    with open(file.split('.')[0].csv", 'w') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["candidate", "change"])
    
        for index, row in df.iterrows():
            if row['word'] not in stopwords:
                if row['change'] >= threshold:
                    writer.writerow([row['word'], row['change']])
