# coding: latin1
import gzip
import os
import json
import re
from nltk.tokenize import sent_tokenize
from nltk import word_tokenize
from emoji import demojize

list_of_files = [filename for filename in os.listdir(input_dir)]

list_of_files.sort()

os.makedirs(output_dir, exist_ok=True)

# Iterate over input files with progressive numbers
file_num = 0

def cleaning(input_folder, output_folder):
    for f in list_of_files:
        print(f)
        outfile = f'cleaned_file.{file_num:06d}.jsonl.gz'
    
        # Clean the JSONL.gz file
        with gzip.open(input_dir+f, 'rt', encoding='utf-8') as input_file, gzip.open(output_dir+outfile, 'wt', encoding='utf-8') as output_file:
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
                            output_file.write(json.dumps(json_obj) + '\n')
              
    
        # Progressing files
        file_num += 1

input_dir = ""
output_dir = ""
cleaning(input_folder, output_folder)

    
