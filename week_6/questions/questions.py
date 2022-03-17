import nltk
import sys
import os
import string
import math
nltk.download('stopwords')

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n = FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    result = {}
    for folder in os.listdir(directory):
        print(folder)
        path = os.path.join(directory, folder)
        with open(path) as f:
            lines = f.readlines()
            tmp = ""
            for line in lines:
                tmp += line
            result[folder] = tmp

    return result


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    stopwords = nltk.corpus.stopwords.words("english")
    punctuation = string.punctuation
    letters = string.ascii_letters

    result = []
    tmp = []
    document = document.lower()
    document = nltk.word_tokenize(document)
    for word in document:
        if word not in stopwords and word not in punctuation:
            tmp.append(word)

    for word in tmp:
        for letter in word:
            if letter in letters:
                result.append(word)
                break

    return result



def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    result = {}
    tot_docs = 0
    for document in documents:
        tot_docs += 1
        for word in documents[document]:
            if word in result:
                if document in result[word]["documents"]:
                    result[word]["count"] += 1
                else:
                    result[word]["documents"].append(document)
                    result[word]["doc_count"] += 1
                    result[word]["count"] += 1
            else:
                result[word] = {
                    "documents": [document],
                    "doc_count": 1,
                    "count": 1
                }

    result2 = {}
    for word in result:
        result2[word] = math.log(tot_docs / result[word]["doc_count"])

    return result2


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    result = []
    helper = {}
    tf = {}

    for file in files:
        helper[file] = 0
        tf[file] = {}

    for file in files:
        for word in files[file]:
            if word in tf[file]:
                tf[file][word] += 1
            else:
                tf[file][word] = 1

    for file in helper:
        for word in query:
            if word not in tf[file]:
                continue
            else:
                 helper[file] += tf[file][word] * idfs[word]

    #print("helper",helper)

    while len(result) <  n:
        tmp = 0
        tmp2 = None
        for file in helper:
            if helper[file] > tmp:
                tmp = helper[file]
                tmp2 = file

        helper.pop(tmp2, None)
        result.append(tmp2)

    #print(result)

    return result


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    print(query)
    helper = {}
    for sentence in sentences:
        helper[sentence] = {
             "IDF": 0,
            "density": 0
        }
    result = []

    for sentence in sentences:
        for word in query:
            if word in sentences[sentence]:
                helper[sentence]["IDF"] += idfs[word]

    for sentence in sentences:
        count_s = 0
        count_q = 0
        for word in sentences[sentence]:
            count_s += 1
            if word in query:
                count_q += 1
        helper[sentence]["density"] = count_q / count_s


    print(helper)

    while len(result) < n:
        tmp = 0
        tmp2 = 0
        tmp3 = None
        for sentence in helper:
            if helper[sentence]["IDF"] >= tmp:
                if helper[sentence]["IDF"] == tmp:
                    if helper[sentence]["density"] > tmp2:
                        tmp = helper[sentence]["IDF"]
                        tmp2 = helper[sentence]["density"]
                        tmp3 = sentence
                else:
                    tmp = helper[sentence]["IDF"]
                    tmp2 = helper[sentence]["density"]
                    tmp3 = sentence

        helper.pop(tmp3, None)
        result.append(tmp3)

    return result


if __name__ == "__main__":
    main()
