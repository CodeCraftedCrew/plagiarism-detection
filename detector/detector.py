import numpy as np
from numpy.linalg import norm
from sklearn.metrics.pairwise import cosine_similarity


def get_vectors(model, ngrams):
    """
        Obtiene vectores de palabras para cada n-grama en la lista de n-gramas utilizando el modelo de vectores de palabras.

        Parameters:
            model: El modelo de vectores de palabras.
            ngrams (list): Una lista de listas de palabras representando los n-gramas.

        Returns:
            list: Una lista de tuplas donde cada tupla contiene un vector de palabras promedio
                  para un n-grama y el n-grama en forma de cadena.
    """
    words_ngrams = [[word.text for word in ngram] for ngram in ngrams]
    return [(np.mean([model[word] if word in model else [0] * 300 for word in ngram], axis=0), " ".join(ngram)) for ngram in words_ngrams]


def get_similarity(model, suspicious, references, similarity_threshold):
    """
        Calcula la similitud entre las frases sospechosas y las frases de referencia utilizando el modelo de vectores de palabras.

        Parameters:
            model: El modelo de vectores de palabras.
            suspicious (list): Una lista de listas de palabras representando las frases sospechosas.
            references (list): Una lista de listas de palabras representando las frases de referencia.
            similarity_threshold (float): Umbral de similitud coseno que determina cuándo considerar que dos frases son similares.

        Returns:
            dict: Un diccionario donde las claves son las frases sospechosas y los valores son listas de frases de referencia
                  que tienen una similitud coseno de al menos 0.8 con la frase sospechosa correspondiente.
    """
    suspicious_vectors = get_vectors(model, suspicious)
    references_vectors = get_vectors(model, references)

    matches = {}

    for suspicious_vector, suspicious_phrase in suspicious_vectors:
        for references_vector, reference_phrase in references_vectors:
            if np.dot(suspicious_vector, references_vector)/(norm(suspicious_vector)*norm(references_vector)) > similarity_threshold:
                match = matches.get(suspicious_phrase, [])
                match.append(reference_phrase)
                matches[suspicious_phrase] = match

    return matches
