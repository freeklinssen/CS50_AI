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
    random = 1 - damping_factor
    result = {}
    
    pages = 0
    for items in corpus:
        pages += 1
    
    links = 0
    for item in corpus[page]:
        links += 1 
    
    for item in corpus:
        result[item] = (random / pages)
        
        if item in corpus[page]:
            result[item] += (damping_factor / links)
            
    return result
        

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    result = {}
    helper = []
    for item in corpus:
        result[item] = 0
        helper.append(item) 
        
    pages = 0
    for items in corpus:
        pages += 1
        
    first = random.randint(0, (pages-1))
    
    result[helper[first]] = 1
    
    current_page = helper[first]
    
    for i in range(n-1):
            
        distribution = transition_model(corpus, current_page, damping_factor)
        
        sites = []
        weights = []
        
        for item in distribution:
            sites.append(item)
            weights.append(distribution[item])
            
        Next = random.choices(sites, weights=weights, k=1)
        
        result[Next[0]] += 1
        current_page = Next[0]

    for item in result:
        result[item] = result[item] / n 
    
    return result 
    

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    #print('corpus: ', corpus)
    total_pages = 0
    numlinks = {}
    incoming_pages = {}
    for item in corpus:
        total_pages += 1
        numlinks[item] = 0
        incoming_pages[item] = set()
        
    result = {}
    for item in corpus:
        result[item] = 1/total_pages
        
    for item in corpus:
        for item2 in corpus:
            if item in corpus[item2]:
                incoming_pages[item].add(item2)
                
    for item in corpus:
        for page in corpus[item]:
            numlinks[item] += 1
                
    # print("result ", result)
    # print("numlinks ", numlinks)
    # print("incoming_pages ", incoming_pages)
            
    count = 0
    while count != total_pages:
        count = 0
        for item in result:
            copy_result = result[item]

            second_condition = 0 
            for page in incoming_pages[item]:
                second_condition += (result[page]/numlinks[page])
                
            result[item] = ((1 - damping_factor)/total_pages) + (damping_factor * second_condition)
            
            if -0.001 < (copy_result-result[item]) < 0.001:
                count += 1
                
    sum_result = 0
    for item in result:
        sum_result += result[item]
    
    for item in result:
        result[item] = result[item] / sum_result
        
    return result
    

if __name__ == "__main__":
    main()
