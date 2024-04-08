import math

import spacy

from helpers.references import remove_quoted_references, remove_referenced_sentences


def process_document(n, document, remove_references=False):
    """
       Procesa un documento de texto para generar n-gramas de palabras.

       Parameters:
           n (int): El tamaño del n-grama.
           document (str): El documento de texto a procesar.
           remove_references (bool, optional): Indica si se deben eliminar las referencias citadas del documento. Por defecto es False.

       Returns:
           list: Una lista de n-gramas de palabras generados a partir del documento de texto.
    """

    if remove_references:
        document = remove_quoted_references(document)

    nlp = spacy.load('en_core_web_sm')
    doc = nlp(document)

    sentences = remove_referenced_sentences(doc.sents) if remove_references else doc.sents
    stopwords = nlp.Defaults.stop_words

    return get_n_grams(n, [token for sentence in sentences for token in sentence if token.is_alpha
                           and token.text not in stopwords])


def get_n_grams(n, tokens):
    """
        Genera n-gramas de palabras a partir de una lista de tokens.

        Parameters:
            n (int): El tamaño del n-grama.
            tokens (list): Una lista de tokens de palabras.

        Returns:
            list: Una lista de n-gramas de palabras generados a partir de los tokens.
        """
    return [tokens[i*n:i*n+n] for i in range(math.ceil(len(tokens)/n))]

