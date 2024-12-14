import os
import random
import re
import sys
import numpy as np


DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    print(transition_model(corpus,"3.html",DAMPING))
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    #print(ranks)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
       print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    #print(ranks)
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
    #Create a dictionary with keys but no values based off corpus
    #print("Initial Corpus: ", corpus)
    trans_model = {}
    for item in corpus.keys():
        trans_model.update({item: 0.0})

    #print("After Adding All Keys: ", trans_model)

    #get the number of links and
    num_links = len(corpus[page])
    if num_links > 0:
        #print("Number of Links on Page 2: ",num_links)
        chance = damping_factor/num_links
        #print("Chance of Selecting a page from Page 2",chance)
        for random_chance in corpus[page]:
            trans_model[random_chance] = chance

        #print("After First Round of Updates: ",trans_model)

        otherwise = (1-damping_factor)/len(corpus)
        for item in trans_model:
            trans_model[item] = trans_model[item] + otherwise

    else:
        for item in trans_model:
            trans_model[item] = trans_model[item] + 1/len(corpus)

    #print("Final Trans Model: ",trans_model)

    return trans_model

    raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    #Create a dictionary with keys but no values based off corpus
    trans_model = {}
    for item in corpus.keys():
        trans_model.update({item: 0})

    #Create a list of the pages
    arr_pages = []
    for item in corpus.keys():
        arr_pages.append(item)

    curr_page = ""
    for i in range(n):
        if i == 0:
            item = random.sample(list(trans_model.items()),1)
            actual_item = item[0][0]
            trans_model[actual_item] = trans_model[actual_item] + 1
            curr_page = actual_item

        else:
            probabilities = transition_model(corpus,curr_page,damping_factor)
            #get cumulative weights
            cum_weights = []
            for key in probabilities.keys():
                cum_weights.append(probabilities[key])
            #generate next page
            next_page = np.random.choice(arr_pages, 1, p=cum_weights)
            trans_model[next_page[0]] = trans_model[next_page[0]] + 1
            curr_page = next_page[0]

    for item in trans_model.keys():
        trans_model[item] = trans_model[item]/n

    return trans_model


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    page_ranks_previous = {}
    page_ranks = {}
    for key in corpus.keys():
        page_ranks.update({key: 0})

    #initially assign equal page rank to every page
    equal_chance = 1/len(page_ranks)
    for item in page_ranks.keys():
        page_ranks[item] = page_ranks[item] + equal_chance

    page_ranks_previous = page_ranks


    page_ranks,page_ranks_previous = helper_iterate_pagerank(corpus,damping_factor,page_ranks,page_ranks_previous)

    for i in range(1000):
        page_ranks,page_ranks_previous = helper_iterate_pagerank(corpus,damping_factor,page_ranks,page_ranks_previous)

    return page_ranks

def sum(page_rank):
    sum = 0
    for item in page_rank:
        sum = sum + page_rank[item]
    return sum

def findLinks(corpus,page):
    incoming_links = []
    for pages in corpus.keys():
        links = corpus[pages]
        if page in links:
            incoming_links.append(pages)
    if len(incoming_links) == 0:
        for pages in corpus.keys():
            incoming_links.append(pages)
    return incoming_links

def helper_iterate_pagerank(corpus, damping_factor, page_ranks, page_ranks_previous):

    #one iteration

    for page in page_ranks.keys():
        new_rank = 0
        #print("Current Page: ",page)
        for incoming in findLinks(corpus,page):
            new_rank = new_rank + page_ranks_previous[incoming]/len(corpus[incoming])
        new_rank = (1 - damping_factor)/len(corpus) + damping_factor*new_rank
        page_ranks[page] = new_rank

    return page_ranks,page_ranks_previous

if __name__ == "__main__":
   main()
