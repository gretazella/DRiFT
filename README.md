# DRiFT: Debate on Reddit Involving Food Transition
or DAIReS: Dairy Alternatives in Reddit Subs

Repository for the paper: "Dairy Milk" or "Plant-based Milk”? Language Shifts as a Thermometer of Social Change.

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
