# DRIFT: Debate on Reddit Involving Food Transition
or DAIReS: Dairy Alternatives in Reddit Subs

Repository for the paper: "Dairy Milk" or "Plant-based Milk”? Language Shifts as a Thermometer of Social Change.

## Data

The "data" folder contains a sample of raw data collected from reddit, the initial list of keywords retreived from policy documents, the selected subreddits, and a list of noisy keywords/phrases that were removed. It also contains neonyms and retronyms with relative pmw frequencies on which the bigram analysis was performed.

## Scripts

For each of the following scripts, set the parameters inside of the code first. 

Data collection was performed based on the code taken and adapted from: https://github.com/Watchful1/PushshiftDumps/blob/master/scripts/combine_folder_multiprocess.py.
The code creates a new jsonl.gz file every 100.000 lines, numbering them progressively. 

```
1. scripts/data_collection.py
```

Comments are pre-processed and grouped by same subreddit and year. 

```
2. scripts/preprocessing.py
```

Corpora for diachronic (t0 and t1) and diastratic analyses are created.

```
3. scripts/create_corpora.py
```

### Corpus Study

to be added: frequency distributions are calculated and candidate words are selected based on them.

to be added: bigrams statistics.

## Lexical Semantic Change Detection Experiments:

The experiments on Lexical Semantic Change Detections are based on the code from: https://github.com/SanneHoeken/LSVD/tree/main.

## Connotation Experiments:

to be added: neonyms and retronyms are replaced with placeholders.

The experiments on connotation are based on the code from: https://github.com/valeriobasile/connhyp/tree/main.o
