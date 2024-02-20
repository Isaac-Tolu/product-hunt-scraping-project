import bs4

from constants import PRODUCT_TITLE__CLASS, PRODUCT_EXTRAS__CLASS


"""
I divided the page structure into three:
    - title
        - name
        - description
    - extras
        - company
        - filters
        - topics
    - votes
        - current_votes
"""
def get_title_section(tag:bs4.Tag) -> tuple[str, str, str]:
    """
     Extract the name, description, and link of the product
        (name, description, link)
    """

    title_tag = tag.find(class_=PRODUCT_TITLE__CLASS)
    a_tag = title_tag.find('a')
    content = list(a_tag.stripped_strings)

    return (content[0], content[-1], a_tag['href'])

def get_extras_section(tag:bs4.Tag) -> tuple[str|None, bool, bool, list[str]]:
    """
    Extract the:
        - company (if there is),
        - whether is the product was done solo (is_solo_maker),
        - whether the product was bootstrapped (is_bootstrapped),
        - all the topics (tags) associated with the product

        (company, is_solo_maker, is_bootstrapped, topics)
    """

    extras_tag = tag.find(class_=PRODUCT_EXTRAS__CLASS)
    a_tags = extras_tag.find_all('a')
    links_and_text = [(a_tag['href'], a_tag.text) for a_tag in a_tags]

    return (get_company(links_and_text[0]),
            check_filter(links_and_text, "soloMaker"),
            check_filter(links_and_text, "bootstrapped"),
            get_topics(links_and_text))

# wishlists
def get_company(extra:tuple[str, str]) -> str|None:
    """Extract the company (if there is)"""
    return None

def check_filter(extras:list[tuple[str, str]], filter:str) -> bool:
    """
    Return True if `filter` exists in extras
    otherwise, False.
    """
    return False

def get_topics(extras:list[tuple[str, str]]) -> list[str]:
    """Extract topics from extras, if any"""
    return []

def get_votes_section(tag:bs4.Tag) -> tuple[str]:
    """Extract the number of current votes at the time of extraction"""
    return ()