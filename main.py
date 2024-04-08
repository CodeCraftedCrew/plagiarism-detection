import argparse
import concurrent.futures
from pathlib import Path
from gensim.models import KeyedVectors
from tabulate import tabulate

from corpus.corpus import MRParaphraseCorpus
from detector.detector import process_similarity, get_similarity
from helpers import metrics
from helpers.documents import process_document


def handle_args():
    parser = argparse.ArgumentParser(description="Plagiarism detection between two documents")
    parser.add_argument("suspicious_path", type=str, help="Path to suspicious file", default="", nargs='?')
    parser.add_argument("reference_path", type=str, help="Path to reference file", default="", nargs='?')
    parser.add_argument("similarity_threshold", type=float, help="Threshold for document similarity",
                        default=0.6, nargs='?')

    args = parser.parse_args()
    return args.suspicious_path, args.reference_path, args.similarity_threshold


def print_matches(matches_found, string, ngram_lala):
    string = string.replace("\n", "")

    previews_index = -1
    first = -1
    last = -1

    for _, index in sorted(matches_found, key=lambda x: x[1]):
        ngram = ngram_lala[index]

        if previews_index == -1:
            first = ngram[0].idx
        elif previews_index != index - 1:
            print(f"{string[first:last]}\n")
            first = ngram[0].idx

        previews_index = index
        last = ngram[-1].idx + len(ngram[-1].text)

        if index == len(suspicious_ngrams) - 1:
            print(f"{string[first:last]}\n")


if __name__ == '__main__':
    suspicious_path, reference_path, similarity_threshold = handle_args()

    if not Path(suspicious_path).exists() or not Path(reference_path).exists():
        corpus = MRParaphraseCorpus()

        model_file_name = 'C:/Users/Nahomi/gensim-data/word2vec-google-news-300/word2vec-google-news-300.gz'
        model = KeyedVectors.load_word2vec_format(model_file_name, binary=True)

        detected = []
        max_iterations = 5801

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_results = [executor.submit(process_similarity, test, corpus, model, similarity_threshold) for
                              test in corpus.tests[:min(max_iterations, len(corpus.tests))]]

            for future in concurrent.futures.as_completed(future_results):
                similarity, test = future.result()

                if similarity > similarity_threshold:
                    detected.append(test)

        results = metrics.get_evaluation(corpus.tests[:max_iterations],
                                         [test for test in corpus.tests[:max_iterations] if test.result], detected)

        rows = [[key, results[key]] for key in results.keys()]

        print(tabulate(rows, headers=["Metric", "Value"], tablefmt="grid"))

    else:

        with open(suspicious_path, 'r', encoding='utf-8') as file:
            suspicious_string = file.read()

        suspicious_ngrams = process_document(3, suspicious_string, True)

        with open(reference_path, 'r', encoding='utf-8') as file:
            reference_string = file.read()

        reference_ngrams = process_document(3, reference_string)

        # load the Google Word2Vec
        model_file_name = 'C:/Users/Nahomi/gensim-data/word2vec-google-news-300/word2vec-google-news-300.gz'
        model = KeyedVectors.load_word2vec_format(model_file_name, binary=True)

        matches = get_similarity(model, suspicious_ngrams, reference_ngrams, similarity_threshold)
        reference_matches = set([value for values in matches.values() for value in values])

        similarity = max(len(matches.keys()) / len(suspicious_ngrams), len(reference_matches) / len(reference_ngrams))

        print(f"Plagiarism percentage is {similarity * 100}%")

        print(f"Plagiarism detected in the following sections:")

        print_matches(matches.keys(), suspicious_string, suspicious_ngrams)

        print(f"In the following sections of the reference document:")

        print_matches(reference_matches, reference_string, reference_ngrams)
