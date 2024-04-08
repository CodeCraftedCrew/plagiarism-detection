import argparse
from pathlib import Path
from gensim.models import KeyedVectors
from tabulate import tabulate

from corpus.corpus import MRParaphraseCorpus
from detector.detector import get_similarity
from helpers import metrics
from helpers.documents import process_document, get_n_grams


def handle_args():
    parser = argparse.ArgumentParser(description="Plagiarism detection between two documents")
    parser.add_argument("suspicious_path", type=str, help="Path to suspicious file", default="", nargs='?')
    parser.add_argument("reference_path", type=str, help="Path to reference file", default="", nargs='?')
    parser.add_argument("similarity_threshold", type=float, help="Threshold for document similarity",
                        default=0.8, nargs='?')

    args = parser.parse_args()
    return args.suspicious_path, args.reference_path, args.similarity_threshold


if __name__ == '__main__':
    suspicious_path, reference_path, similarity_threshold = handle_args()

    if not Path(suspicious_path).exists() or not Path(reference_path).exists():
        corpus = MRParaphraseCorpus()

        model_file_name = 'C:/Users/Nahomi/gensim-data/word2vec-google-news-300/word2vec-google-news-300.gz'
        model = KeyedVectors.load_word2vec_format(model_file_name, binary=True)

        detected = []

        max_iterations = 5801
        iterations = 0

        for test in corpus.tests:
            sentence1 = process_document(3, corpus.sentences[test.sentence1].sentence)
            sentence2 = process_document(3, corpus.sentences[test.sentence2].sentence)

            matches = get_similarity(model, sentence1, sentence2, similarity_threshold)
            reference_matches = set([value for values in matches.values() for value in values])

            similarity = max(len(matches.keys()) / len(sentence1),
                             len(reference_matches) / len(sentence2))

            iterations += 1

            if similarity > similarity_threshold:
                detected.append(test)

            if iterations >= max_iterations:
                break

        results = metrics.get_evaluation(corpus.tests[:max_iterations],
                                         [test for test in corpus.tests if test.result][:max_iterations], detected)

        rows = [[key, results[key]] for key in results.keys()]

        print(tabulate(rows, headers=["Metric", "Value"], tablefmt="grid"))

    else:

        with open(suspicious_path, 'r', encoding='utf-8') as file:
            suspicious_string = file.read()

        suspicious_ngrams = process_document(3, suspicious_string, True)

        with open(reference_path, 'r', encoding='utf-8') as file:
            reference_string = file.read()

        reference_ngrams = process_document(3, suspicious_string)

        # load the Google Word2Vec
        model_file_name = 'C:/Users/Nahomi/gensim-data/word2vec-google-news-300/word2vec-google-news-300.gz'
        model = KeyedVectors.load_word2vec_format(model_file_name, binary=True)

        matches = get_similarity(model, suspicious_ngrams, reference_ngrams, similarity_threshold)
        reference_matches = set([value for values in matches.values() for value in values])

        similarity = max(len(matches.keys()) / len(suspicious_ngrams), len(reference_matches) / len(reference_ngrams))

        print(f"Plagiarism percentage is {similarity * 100}%")
