def create_sentence(raw_sentence):
    """
        Crea una instancia de Sentence a partir de una cadena de texto en formato crudo.

        Parameters:
            raw_sentence (str): La cadena de texto en formato crudo que contiene información sobre la oración.

        Returns:
            Sentence or None: La instancia de Sentence creada a partir de la cadena de texto.
                             Retorna None si la cadena de texto no tiene el formato esperado.
    """
    split = raw_sentence.split("\t")

    if len(split) < 7:
        return None

    sentence_id = int(split[0])
    sentence = split[1]
    author = split[2]
    url = split[3]
    agency = split[4]
    date = split[5]
    web_date = split[6]

    return Sentence(sentence_id, sentence, author, url, agency, date, web_date)


def create_test(raw_test):
    """
        Crea una instancia de TestResult a partir de una cadena de texto en formato crudo.

        Parameters:
            raw_test (str): La cadena de texto en formato crudo que contiene información sobre el resultado de la prueba.

        Returns:
            TestResult or None: La instancia de TestResult creada a partir de la cadena de texto.
                                Retorna None si la cadena de texto no tiene el formato esperado.
    """
    split_by_result = raw_test.split("\t")
    if len(split_by_result) < 3:
        return None
    return TestResult(split_by_result[0], int(split_by_result[1]), int(split_by_result[2]))


class TestResult:
    def __init__(self, result, sentence1, sentence2):
        self.result = result
        self.sentence1 = sentence1
        self.sentence2 = sentence2


class Sentence:
    def __init__(self, sentence_id, sentence, author, url, agency, date, web_date):
        self.id = sentence_id
        self.sentence = sentence
        self.author = author
        self.date = date
        self.url = url
        self.agency = agency
        self.web_date = web_date


class MRParaphraseCorpus:
    """
       Clase para manejar el corpus de MSR Paraphrase
    """

    def __init__(self):
        """
                Inicializa una instancia de la clase MRParaphraseCorpus.

                Lee los datos del corpus de entrenamiento y de prueba desde archivos de texto,
                crea instancias de las sentencias y pruebas correspondientes, y las almacena
                en los atributos 'sentences' y 'tests' respectivamente.
        """
        with open("C:/MSRParaphraseCorpus/msr_paraphrase_data.txt", 'r', encoding='utf-8') as file:
            corpus_data_string = file.read()

        raw_sentences = corpus_data_string.split('\n')[1:]

        sentences_instances = [create_sentence(item) for item in raw_sentences]

        self.sentences = {sentence.id: sentence for sentence in sentences_instances if sentence}

        with open("C:/MSRParaphraseCorpus/msr_paraphrase_test.txt", 'r', encoding='utf-8') as file:
            corpus_test_string = file.read()

        raw_tests = corpus_test_string.split('\n')[1:]

        tests_instances = [create_test(item) for item in raw_tests]

        with open("C:/MSRParaphraseCorpus/msr_paraphrase_train.txt", 'r', encoding='utf-8') as file:
            corpus_train_string = file.read()

        raw_tests = corpus_train_string.split('\n')[1:]

        tests_instances.extend([create_test(item) for item in raw_tests])

        self.tests = [test for test in tests_instances if test]
