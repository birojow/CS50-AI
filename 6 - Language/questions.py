from math import log
import nltk
import operator
import os
import string
import sys

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
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

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
    path = os.path.abspath(directory)

    # read files
    files = {}
    for file in os.listdir(path):
        with open(os.path.join(path, file), 'r') as text:
            files[file] = text.read()

    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    # tokenizing
    words = nltk.word_tokenize(document)

    #lowercasing
    for i in range(len(words)):
        words[i] = words[i].lower()

    # filtering
    copy_of_words = words[:]
    for word in copy_of_words:
        if word in nltk.corpus.stopwords.words("english"):
            words.remove(word)
        else:
            punct = []
            for letter in word:
                if letter in string.punctuation:
                    punct.append(True)
                else:
                    punct.append(False)
            if all(punct):
                words.remove(word)

    return words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    # list all words from all documents
    words = set()
    for key in documents:
        for word in documents[key]:
            words.add(word)

    # create idf_dict
    words_idf = {
        word: 0
        for word in words
    }

    # calculate idf
    for word in words_idf:
        occurrences = 0
        for key in documents:
            if word in documents[key]:
                occurrences += 1
        words_idf[word] = log(len(documents) / occurrences)

    return words_idf


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    # dict to map each file to it's rank
    top = {
        filename: 0
        for filename in files
    }

    # calculate ranks
    for file in files:
        for word in query:
            if word in files[file]:
                top[file] += files[file].count(word) * idfs[word]

    # sort files by tf-idf
    top = dict(sorted(top.items(), key=lambda x: x[1], reverse=True))

    # return a list of n top files
    return list(top)[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    # dict to track matching word measure of each sentence
    mwm = {
        sentence: 0
        for sentence in sentences
    }

    # dict to track query term density of each sentence
    qtd = {
        sentence: 0
        for sentence in sentences
    }

    # calculate matching word measure and query term density
    for sentence in sentences:
        occurrences = 0
        for word in query:
            if word in sentences[sentence]:
                mwm[sentence] += idfs[word]
                occurrences += 1
        qtd[sentence] = occurrences / len(sentences[sentence])

    # sort sentences by matching word measure, than by query term density
    top_sent = []
    for sentence in sentences:
        top_sent.append((sentence, mwm[sentence], qtd[sentence]))

    top_sent = sorted(top_sent, key=lambda x: (1-x[1], 1-x[2]))
    for i in range(len(top_sent)):
        top_sent[i] = top_sent[i][0]

    # return the desired number of sentences
    return top_sent[:n]


if __name__ == "__main__":
    main()
