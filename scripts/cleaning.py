# coding: latin1
import gzip
import os
import json
import re
from nltk.tokenize import sent_tokenize
from nltk import word_tokenize
from emoji import demojize
import io
import pandas as pd
from tqdm import tqdm

def merge_sub_years(intermediate_path,intermediate_file,output_path):
    print('Creating one file for each subreddit-year combination')
    # Extract subreddit and year from the filename
    subreddit, year = intermediate_file.split('_')[:2]
    
    # Name output filename
    output_filename = f"{subreddit}_{year}.json"
    
    # Check if the merged file already exists
    if os.path.isfile(output_path+output_filename):
        # File already exists, append data to the existing file
        with open(output_path+output_filename, 'a') as output_file:
            
            # Read and append data to the merged file
            try:
                df = pd.read_json(intermediate_path+intermediate_file, lines=True)
                df.to_json(output_file, orient='records', lines=True)
            except pd.errors.EmptyDataError:
                print(f"Warning: Empty file encountered: {intermediate_file}")
    else:
        # File doesn't exist, create a new file
        try:
            df = pd.read_json(intermediate_path+intermediate_file, lines = True)
            with open(output_path+output_filename, 'w') as output_file:
                df.to_json(output_file, orient='records', lines=True)
        except pd.errors.EmptyDataError:
            print(f"Warning: Empty file encountered: {intermediate_file}")

def create_sub_files(cleaned_file, intermediate_path):
    print('Combining subreddits and years')
    df = pd.read_json(cleaned_file, lines=True)
  
    # Convert 'created_utc' from epoch time to datetime
    df['created_utc'] = pd.to_datetime(df['created_utc'], unit='s')
    
    # Convert datetime to year
    df['year'] = df['created_utc'].dt.year
    
    # Group by subreddit and year
    grouped = df.groupby(['subreddit', 'year'])
    
    # Output each group to a separate jsonl file
    for (subreddit, year), group in grouped:
        # Increment file count for the category-year combination
        file_count[(subreddit, year)] = file_count.get((subreddit, year), 0) + 1
        
        # counter
        counter_str = str(file_count[(subreddit, year)]).zfill(3)
        
        # Naming intermediate file
        intermediate_filename = f"{subreddit}_{year}_{counter_str}.jsonl.gz"
        
        # Write group to jsonl file
        with gzip.open(intermediate_path+intermediate_filename, 'wt', encoding='utf-8') as intermediate_file:
            group.to_json(intermediate_file, orient='records', lines=True)

def cleaning(raw_file):
    temp_file = io.StringIO()
    
    # Clean the jsonl file
    with gzip.open(input_path+raw_file, 'rt', encoding='utf-8') as input_file:
        print('Cleaning file')
        for line in input_file:
            json_obj = json.loads(line)
            
            if type(json_obj["body"]) != str:
                pass
            else:                    
                if "i am a bot" not in json_obj["body"].lower():

                    # Converting emojis
                    json_obj["body"] = demojize(json_obj["body"])                        
    
                    # Replacing urls
                    json_obj["body"] = re.sub(r'(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:\'\".,<>?������])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))', 'url', json_obj["body"], flags=re.MULTILINE)
                        
                    # Replacing emails
                    json_obj["body"] = re.sub(r'^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$', "email", json_obj["body"])
                    
                    # Replacing usernames
                    json_obj["body"] = re.sub(r'(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9-_]+)', "user", json_obj["body"])
                    
                    # Replacing subreddits mentions
                    json_obj["body"] = re.sub(r'(?<=(^|\b))([rR]\/[^\s\W]{2,})', "subreddit", json_obj["body"])
                    
                    # Removing html characters
                    if "&gt;" in json_obj["body"]:
                        json_obj["body"] = json_obj["body"].replace("&gt;", " ")
                    if "&gl;" in json_obj["body"]:
                        json_obj["body"] = json_obj["body"].replace("&gl;", " ")
                    if "&amp;" in json_obj["body"]:
                        json_obj["body"] = json_obj["body"].replace("&amp;", " ")
                    if "#x200B;" in json_obj["body"]:
                        json_obj["body"] = json_obj["body"].replace("#x200B;", " ")
                    
                    # Removing \t
                    while '\t' in json_obj['body']:
                        json_obj["body"] = re.sub('\t', ' ', json_obj["body"])

                    # Removing every character that is not a letter (including numbers) 
                    comment_without_punctuation = re.sub(r"[^\w\s_-]|(?<!\w)[_-]|[_-](?!\w)"," ",json_obj['body'])
                    
                    # Counting number of tokens excluding punctiation                         
                    sent_tokens = sent_tokenize(comment_without_punctuation)
                    length_comment = 0
                    for sent in sent_tokens:
                        toks = word_tokenize(sent)
                        length_comment+=len(toks)
                    
                    # Excluding comments shorter than 3 words
                    if length_comment < 3:
                        pass
                    else:
                        temp_file.write(json.dumps(json_obj) + "\n")
    
    temp_file.seek(0)
    create_sub_files(temp_file, intermediate_path)

def main(input_path, intermediate_path, output_path):
    # Cleaning files and grouping subreddits and years
    list_of_raw_files = [raw_file for raw_file in os.listdir(input_path)]
    list_of_raw_files.sort()
    os.makedirs(intermediate_path, exist_ok=True)    
    for f in tqdm(list_of_raw_files):
        cleaning(f)

    # Merging subreddits
    list_of_cleaned_files = [raw_file for raw_file in os.listdir(intermediate_path)]
    os.makedirs(output_path, exist_ok=True)  
    for f in tqdm(list_of_cleaned_files):
        print(f)
        merge_sub_years(intermediate_path, f, output_path)
    

if __name__ == '__main__':   
    # Numbering files progressively
    file_num = 0
    
    # Dictionary to keep track of the number of files written for each subreddit-year combination
    file_count = {}

    input_path = '[path to directory containing jsonl.gz files with one comment per line]'
    intermediate_path = '[path to directory where progressively numbered, cleaned subreddit_year files are saved]'
    output_path = '[path to directory where one unique file for each subreddit-year combination is stored]'

    main(input_path, intermediate_path, output_path)
