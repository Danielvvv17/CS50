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
    a set of all other pages in the corpus that are linked to by the page.
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
    prob_dist = {}
    total_pages = len(corpus)

    if corpus[page]:  # Page has outgoing links
        for linked_page in corpus:
            prob_dist[linked_page] = (1 - damping_factor) / total_pages
        for linked_page in corpus[page]:
            prob_dist[linked_page] += damping_factor / len(corpus[page])
    else:  # Page has no outgoing links
        for linked_page in corpus:
            prob_dist[linked_page] = 1 / total_pages

    return prob_dist


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = {page: 0 for page in corpus}
    current_page = random.choice(list(corpus.keys()))

    for _ in range(n):
        pagerank[current_page] += 1
        model = transition_model(corpus, current_page, damping_factor)
        current_page = random.choices(
            list(model.keys()), weights=model.values(), k=1
        )[0]

    # Normalize the PageRank values
    total_samples = sum(pagerank.values())
    for page in pagerank:
        pagerank[page] /= total_samples

    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    total_pages = len(corpus)
    pagerank = {page: 1 / total_pages for page in corpus}
    new_pagerank = pagerank.copy()

    while True:
        for page in corpus:
            total = 0
            for potential_linker in corpus:
                if page in corpus[potential_linker]:
                    total += pagerank[potential_linker] / len(corpus[potential_linker])
                if not corpus[potential_linker]:  # Treat no links as linking to all
                    total += pagerank[potential_linker] / total_pages
            new_pagerank[page] = (1 - damping_factor) / total_pages + damping_factor * total

        # Check for convergence
        if all(
            abs(new_pagerank[page] - pagerank[page]) < 0.001
            for page in pagerank
        ):
            break

        pagerank = new_pagerank.copy()

    # Normalize the PageRank values
    total_rank = sum(new_pagerank.values())
    for page in new_pagerank:
        new_pagerank[page] /= total_rank

    return new_pagerank


if __name__ == "__main__":
    main()
