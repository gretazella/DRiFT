import argparse
import gzip
import json
import logging
import multiprocessing
from multiprocessing import Pool
from pathlib import Path
from nltk import word_tokenize

import zstandard
from jsonlines import Writer
from tqdm import tqdm

SELECTED_SUBREDDITS = set(['food', 'Cooking','Baking', 'vegan', 'vegetarian', 'PlantBasedDiet', 'Showerthoughts', 'AskReddit', 'mildlyinfuriating', 'unpopularopinion', 'meat', 'burgers', 'steak', 'AntiVegan', 'zerocarb', 'carnivore', 'Cheese', 'Milk', 'carnivorediet', 'exvegans', 'tonightsdinner', '52weeksofcooking', 'AskCulinary', 'recipes', 'seriouseats', 'Old_Recipes', 'RecipeInspiration', 'vegancirclejerk', 'environment', 'greenhouse', 'Pescetarian', 'dairyfree', 'verticalfarming', 'veganuk', 'vegancheesemaking', 'Veganivore', 'recycling', 'todayilearned', 'mildlyinteresting', 'worldnews', 'politics', 'NoStupidQuestions', 'science', 'news', 'nutrition', 'interestingasfuck', 'explainlikeimfive', 'Futurology', 'Thatsactuallyverycool'])

filter_list_kw = ["milk", "meat", "beef", "pork", "chicken", "chickens", "soy", "dairy", "turkey", "turkeys", "egg", "eggs", "fish", "poultry", "burger", "burgers", "sausage", "sausages", "yogurt", "yoghurt", "yogurts", "yoghurts", "tofu", "veal", "lamb", "steak", "steaks", "cheese", "cheeses", "mutton"]

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())


def read_and_decode(
    reader, chunk_size, max_window_size, previous_chunk=None, bytes_read=0
):
    chunk = reader.read(chunk_size)
    bytes_read += chunk_size
    if previous_chunk is not None:
        chunk = previous_chunk + chunk
    try:
        return chunk.decode('utf-8', 'ignore') 
    except UnicodeDecodeError:
        if bytes_read > max_window_size:
            raise UnicodeError(
                f"Unable to decode frame after reading {bytes_read:,} bytes"
                )
        log.info(f"Decoding error with {bytes_read:,} bytes, reading another chunk")
        return read_and_decode(reader, chunk_size, max_window_size, chunk, bytes_read)


def read_lines_zst(file_name):
    with open(file_name, "rb") as file_handle:
        print(file_name)
        buffer = ""
        reader = zstandard.ZstdDecompressor(max_window_size=2**31).stream_reader(
            file_handle
        )
        while True:
            chunk = read_and_decode(reader, 2**27, (2**29) * 2)

            if not chunk:
                break
            lines = (buffer + chunk).split("\n")

            for line in lines[:-1]:
                yield line, file_handle.tell()

            buffer = lines[-1]

        reader.close()


def simple_line_generator(files):
    for file in tqdm(files):
        try:
            for line, _ in read_lines_zst(file):
                yield line
        except Exception as e:
            print(e)
            pass


def simple_filter(line):
    try:
        json_obj = json.loads(line)
    except Exception as e:
        print(e)
        return None
    if "subreddit" in json_obj and json_obj["subreddit"] in SELECTED_SUBREDDITS:
        if "created_utc" in json_obj and int(json_obj["created_utc"]) >= 1262304000:
            tokenized = word_tokenize(json_obj["body"].lower())
            if any(tok in filter_list_kw for tok in tokenized):
                return json_obj
            else:
                return None
        else:
            return None
    else:
        return None


def write_to_json(lines, filename):
    with gzip.open(filename, "wt") as zipfile:
        writer = Writer(zipfile)
        writer.write_all(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Use multiple processes to filter comments from pushshift dump files"
    )
    parser.add_argument("input", help="input folder")
    parser.add_argument("output", help="output folder")
    parser.add_argument(
        "--lines_per_output_file", help="line per output file", default=100000
    )
    parser.add_argument("--pool_size", help="number of parallel workers", default=None)

    args = parser.parse_args()

    input_files = sorted(Path(args.input).glob("*.zst"))
    output_folder = Path(args.output)
    output_folder.mkdir(exist_ok=True)

    pool_size = (
        multiprocessing.cpu_count() if args.pool_size is None else args.pool_size
    )
    n_filter_processes = pool_size - 1  # leave one worker for writing output files

    comments = []
    file_count = 0

    with Pool(processes=n_filter_processes) as filter_pool:
        for idx, json_obj in enumerate(
            filter_pool.imap_unordered(
                simple_filter, simple_line_generator(input_files), chunksize=1000
            )
        ):
            if json_obj is not None:
                comments.append(json_obj)
                if len(comments) == args.lines_per_output_file:
                    multiprocessing.Process(
                        target=write_to_json,
                        args=(
                            comments,
                            output_folder.joinpath(
                                f"reddit_comments.{file_count:0>6}.jsonl.gz"
                            ),
                        ),
                        daemon=True,
                    ).start()
                    file_count += 1
                    comments = []

    if len(comments):
        write_to_json(
            comments,
            output_folder.joinpath(f"reddit_comments.{file_count:0>6}.jsonl.gz"),
        )
