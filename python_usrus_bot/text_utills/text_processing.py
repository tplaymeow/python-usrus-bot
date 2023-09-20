from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import download


def download_res() -> None:
    download('punkt')
    download('stopwords')


def text_tokenize(text: str) -> [str]:
    return word_tokenize(text, language="russian")


def text_preprocessing(text: str) -> [str]:
    download_res()

    text_tokens = text_tokenize(text)
    stop_words = set(stopwords.words())
    result: [str] = []
    for string in text_tokens:
        if string not in stop_words and len(string) > 2:
            result.append(string)

    return result
