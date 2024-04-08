import re


def find_quoted_text(document):
    """
        Encuentra y devuelve todas las frases citadas entre comillas en un documento de texto.

        Parameters:
            document (str): El documento de texto en el que buscar frases citadas.

        Returns:
            list: Una lista de tuplas donde cada tupla contiene la frase citada, su índice de inicio y su índice de fin en el documento.
    """
    results = []
    for matched in re.finditer(r'"([^"]*)"(  *)(\(([^,]+)(,([^,^\)]+))\)|\[\d+\])', document):
        phrase = matched.group()
        results.append((phrase, matched.start(), matched.end()))
    return results


def remove_quoted_references(document):
    """
        Elimina las referencias citadas entre paréntesis o corchetes del documento de texto.

        Parameters:
            document (str): El documento de texto del cual eliminar las referencias citadas.

        Returns:
            str: El documento de texto sin las referencias citadas.
    """
    last_end = 0
    result = ""
    for (_, start, end) in find_quoted_text(document):
        result += document[last_end:start]
        last_end = end

    result += document[last_end:]
    return result


def remove_referenced_sentences(sentences):
    """
        Elimina las oraciones que contienen referencias citadas de una lista.

        Parameters:
            sentences (iterable): iterable de oraciones.

        Returns:
            list: Una lista de oraciones sin las que contienen referencias citadas.
    """
    reference = r'(\(([^,]+)(,([^,^\)]+))\)|\[\d+\])'

    pattern = f".(  *){reference}|{reference}(  *)."

    clean_sentences = [sentence for sentence in sentences if not re.search(pattern, sentence.text)]

    return clean_sentences
