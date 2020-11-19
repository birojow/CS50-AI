import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    probabilities = {}

    # probability of all pages being selected at random
    for key in corpus.keys():
        probabilities[key] = (1 - damping_factor) * 1 / len(corpus.keys())

    # probability of pages linked to current page being selected
    # added to the random dumping probability
    links = corpus[page]
    for value in links:
        probabilities[value] += damping_factor * 1 / len(links)

    return probabilities


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # list to store each sample
    samples = []

    # selecting a random page to start
    samples.append(random.choice(list(corpus.keys())))
    n -= 1

    while n > 0:
        # calculate probabilities for the current state
        probabilities = transition_model(corpus, samples[-1], damping_factor)
        pages = list(probabilities.keys())
        weight = list(probabilities.values())

        # pick a page based on probabilities
        selected_page = random.choices(pages, weights=weight, k=1)
        samples.append(selected_page[0])
        n -= 1
    
    # calculate pageranks
    pagerank = {}
    for key in corpus.keys():
        pagerank[key] = samples.count(key) / len(samples)

    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = {}
    for page in corpus:
        # calculate initial pageranks
        pagerank[page] = 1 / len(corpus.keys())
        # pages with no outgoing links now links to all pages
        if len(corpus[page]) == 0:
            corpus[page] = corpus.keys()

    # iterate using formula
    stop_iterating = False
    while not stop_iterating:
        # stores pagerank from last iteration for comparison
        old_pagerank = dict(pagerank)

        # stores new pageranks to update all at once
        new_pagerank = {}

        for page in corpus:
            # list pages linking to current page
            links_to_page = []
            for key in corpus:
                if page in corpus[key]:
                    links_to_page.append(key)

            # get the number of links on each page linking to
            # the current page and their pagerank
            numlinks_i = []
            pr_i = []
            for i in range(len(links_to_page)):
                numlinks_i.append(len(corpus[links_to_page[i]]))
                pr_i.append(pagerank[links_to_page[i]])

            # sum all PR(i)/NumLinks(i)
            pri_to_numlinks = []
            for i in range(len(pr_i)):
                pri_to_numlinks.append(pr_i[i] / numlinks_i[i])
            
            # calculate pagerank using formula
            new_pagerank[page] = (1 - damping_factor) / len(corpus.keys()) + damping_factor * sum(pri_to_numlinks)

        # update all pages
        pagerank = dict(new_pagerank)
        
        # time to stop?
        for key in pagerank.keys():
            if abs(pagerank[key] - old_pagerank[key]) > 0.001:
                break
            stop_iterating = True

    return pagerank


if __name__ == "__main__":
    main()
