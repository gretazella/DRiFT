# DRIFT: Debate on Reddit Involving Food Transition
or DAIReS: Dairy Alternatives in Reddit Subs

Repository for the paper: "Dairy Milk" or "Plant-based Milk”? Language Shifts as a Thermometer of Social Change.

## Data

The "data" folder contains a sample of raw data collected from reddit, the initial list of keywords retreived from policy documents, the selected subreddits, and a list of noisy keywords/phrases that were removed. It also contains neonyms and retronyms with relative pmw frequencies on which the bigram analysis was performed.

## Scripts

For each of the following scripts, set the parameters inside of the code first. 

Data collection was performed based on the code taken and adapted from: https://github.com/Watchful1/PushshiftDumps/blob/master/scripts/combine_folder_multiprocess.py.
The code creates a new zst. file every 100.000 lines, numbering them progressively. 

```
1. scripts/data_collection.py
```

Comments are pre-processed and grouped by same subreddit and year. 

```
2. scripts/preprocessing.py
```

Corpora for diachronic (to and t1) and diastratic analyses are created.

```
3. scripts/create_corpora.py
```

## Corpus Study: Bigram Analysis

Per million word (pmw) frequency distributions are calculated for our keywords in each corpus.

```
1. corpus_sutyd/pmw.py
```
The data is merged to allow diachronic and diastratic comparisons.

```
2. corpus_sutyd/merge_pmw.py
```
For each of the two diachronic and one diastratic analyses, we detect words that have undergone a frequency increase of above 2 Standard Deviations above the mean.

```
3. corpus_sutyd/candidate_words_detection.py
```
Bigrams are retrieved based on raw frequency.

```
4. corpus_sutyd/bigrams.py
```

## Lexical Semantic Change Detection Experiments:

The experiments on Lexical Semantic Change Detections are based on the code from: https://github.com/SanneHoeken/LSVD/tree/main.

## Connotation Experiments:

to be added: script to replace neonyms and retronyms with placeholders.

The experiments on connotation are based on the code from: https://github.com/valeriobasile/connhyp/tree/main.o
