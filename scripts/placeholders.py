import csv
import ast
import os
import re

def extract_modifiers(modifiers_file):

    # Set to collect unique first words from bigrams
    modifiers = []

    with open(modifiers_file, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        
        for row in reader:
            
            bigram_str = row[0]
            
            # converting strings to tuples
            bigram = ast.literal_eval(bigram_str)
            if isinstance(bigram, tuple) and len(bigram) == 2:
                modifiers.append(bigram[0])
                  
    return modifiers

def placeholders(input_path):

    neonyms= extract_modifiers(neonyms_file)
    retronyms = extract_modifiers(retronyms_file)

    all_files = os.listdir(input_path)

    for f in all_files:
        print(f)

        with open(input_path+f, 'r') as infile:
            with open(output_path+f.split('.')[0]+'_placeholders.txt', 'w') as outfile:
            
                for line in infile:
                    
                    line = line.lower()
                    
                    for neonym in neonyms:
                    
                            pattern = r'\b{}\s+(milk|meat|cheese|burger|burgers)\b'.format(re.escape(neonym.strip())) #regex for neonyms
                            line = re.sub(pattern, r'plant_\1', line)       
                            
                    for retronym in retronyms:
                    
                        pattern = r'\b{}\s+(milk|meat|cheese|burger|burgers)\b'.format(re.escape(retronym.strip())) # regex for retronyms
                        line = re.sub(pattern, r'animal_\1', line)
                    
                    outfile.write(line)

input_path = [directory to where txt file of the corpora are stored] 
output_path = [directory where to store txt files of corpora with neonyms' and retronyms' placeholders]
neonyms_file = "../data/neonyms.csv" 
retronyms_file = "../data/retronyms.csv"

placeholders(input_path)
                                
    
    
