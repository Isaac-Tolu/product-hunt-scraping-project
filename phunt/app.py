import bs4


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
def get_title_section(tag:bs4.Tag, class_name:str) -> tuple[str, str]:
    """
     Extract the name and description of the product
        (name, description)
    """
    ...

def get_extras_section(tag:bs4.Tag, class_name:str) -> tuple[str|None, str, str, list[str]]:
    """
    Extract the:
        - company (if there is),
        - whether is the product was done solo (is_solo_maker),
        - whether the product was bootstrapped (is_bootstrapped),
        - all the topics (tags) associated with the product
    """
    ...

def get_votes_section(tag:bs4.Tag, class_name:str) -> tuple[str]:
    """Extract the number of current votes at the time of extraction"""
    ...