import bs4

from constants import PRODUCT_TITLE__CLASS


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

def get_extras_section(tag:bs4.Tag) -> tuple[str|None, str, str, list[str]]:
    """
    Extract the:
        - company (if there is),
        - whether is the product was done solo (is_solo_maker),
        - whether the product was bootstrapped (is_bootstrapped),
        - all the topics (tags) associated with the product
    """
    return ()

def get_votes_section(tag:bs4.Tag) -> tuple[str]:
    """Extract the number of current votes at the time of extraction"""
    return ()