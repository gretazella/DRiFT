# DRiFT: Debate on Reddit Involving Food Transition
or DAIReS: Dairy Alternatives in Reddit Subs

Repository for the paper: "Dairy Milk" or "Plant-based Milk”? Language Shifts as a Thermometer of Social Change.

## Data

The folder "data" contains the initial list of keywords retreived from policy documents and the selected subreddits.

1.
```
data/policy_documents_keyowrds.csv
```
2. 
```
data/selected_subreddits.csv
```

It also contains the list of unwatned keywords, extracted from the _noise_ random sample (see paper), as well as neonyms and retronyms with relative pmw frequencies on which the bigram analysis was performed.

## Data Collection

Data collection was performed based on the code taken and adapted from: https://github.com/Watchful1/PushshiftDumps/blob/master/scripts/combine_folder_multiprocess.py.

```
data_collection/parallel_process.py
```

## Preprocessing

Emojis are converted to text, usernames, subreddits, urls and emails are replaced with placeholders. 
Tab and html characters, as well as numbers, extra white space and other characters outside letters from a to z are removed.
Comments containing "i am a bot" or shorter than three words are also removed.

```
preprocessing/cleaning_comments.py
```

3. Lexical Semantic Change Detection Experiments:

The experiments on Lexical Semantic Change Detections are based on the code from: https://github.com/SanneHoeken/LSVD/tree/main.

4. Connotation Experiments:

The experiments on connotation are based on the code from: https://github.com/valeriobasile/connhyp/tree/main.o
