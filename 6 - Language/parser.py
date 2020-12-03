from copy import copy
import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | S Conj NP VP | NP AdvP VP | S Conj VP NP
NP -> N | NP PP | AP NP | Det Nom | Det Nom PP | Det N | Conj N | Det N PP | Adj NP
AP -> Adj | Adj AP
AdvP -> Adv | Adv VP
Nom -> Adj Nom | N Nom | Adj Adj N | N
VP -> V | V NP | VP PP | V NP PP | VP Adv | V S | V PP | V Adj | NP V
PP -> P NP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    sentence = nltk.word_tokenize(sentence)
    copy_of_sentence = sentence[:]
    for word in copy_of_sentence:
        sentence[sentence.index(word)] = word.lower()
        if not sentence[sentence.index(word.lower())].islower():
            sentence.remove(word)

    return sentence


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """

    # find all NP positions
    nps = []
    positions = tree.treepositions()
    for position in positions:
        if not isinstance(tree[position], str):
            if tree[position].label() == 'NP':
                nps.append(position)

    # find np chunks
    npc = []
    for i in range(len(nps)):
        has_np = False
        for j in range(len(nps)):
            if i == j:
                continue
            if len(nps[i]) < len(nps[j]) and list(nps[i]) == list(nps[j])[:len(nps[i])]:
                has_np = True
                break
        if not has_np:
            npc.append(tree[nps[i]])

    return npc


if __name__ == "__main__":
    main()
