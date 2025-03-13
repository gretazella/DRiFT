#coding: latin-1

from pandas import *
import random
import pandas as pd
import math
import os
import csv
from nltk import word_tokenize
from nltk import sent_tokenize
import re

all_files = os.listdir(input_folder)
filtered_files.sort()

noise_file = "../data/noise.csv"
noisy_kw =[]

with open(noise_file, 'r', newline='') as noise_file:
    df = pd.read_csv(noise_file)
    dict_noisy_kw = df.groupby('noise').groups
    for key in dict_noisy_kw.keys():
        noisy_kw.append(key)

def remove_noise(input_folder, output_folder):
  for f in filtered_files:
      print(f)
      
      name_file = f.split('.')[0]
          
      with open(output_folder + name_file + '_no_noise' + '.csv', 'w') as csv_file:
          writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
          writer.writerow(['comment', 'id'])
          
          comment_id = 0 
          
          df = pd.read_json(input_folder+f,lines=True)  
          
          for index, row in df.iterrows():
              
              present = False
              for kw in noisy_kw:
                  if kw in comment.lower():
                      present = True
              
              if present == True:
                  pass
              else:
                  comment_without_punctuation = re.sub(r"[^a-zA-Z\u00C0-\u00FF-_]," ",comment)
                  if len([tok for tok in word_tokenize(comment_without_punctuation)]) >=3:
                      writer.writerow([comment, comment_id])
                      comment_id+=1
input_folder=""
output_folder=""
remove_noise(input_folder, output_folder)
