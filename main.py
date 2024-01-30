import requests
from bs4 import BeautifulSoup, Tag


LINK = "https://www.producthunt.com/leaderboard/daily/2024/1/26"
PARSER = 'html.parser'

PRODUCT_SECTION__CLASS          = "styles_item__Dk_nz"
PRODUCT_TITLE__CLASS            = "styles_titleContainer__qZRNa"
PRODUCT_BY__CLASS               = "styles_container__EoS8Q"
PRODUCT_EXTRAS__CLASS           = "styles_extraInfo__Xs_5Y"
PRODUCT_VOTE_BUTTON__DATA_CLASS = "vote-button"
PRODUCT_VOTE_BUTTON_CLASS       = "styles_voteCountItem__zwuqk"


def get_ph_soup() -> BeautifulSoup:
    """
    Gets the Product Hunt page and returns the HTML soup.
    """
    response = requests.get(LINK)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, PARSER)
    return soup

def get_top_products(tag:Tag) -> list[dict]:
    """
    Extract these information from each product on the page
      {
        name: str, description: str, link: str,
        is_solo_maker: bool, is_bootstrapped: bool,
        topics: list[str]
      }
    Returns these objects in a list
    """
    products = []

    for product_tag in tag.find_all(class_=PRODUCT_SECTION__CLASS):
        product_info = {}

        title_tag = product_tag.find(class_=PRODUCT_TITLE__CLASS)
        by_tag = product_tag.find(class_=PRODUCT_BY__CLASS)
        extras_tag = product_tag.find(class_=PRODUCT_EXTRAS__CLASS)

        title_content = get_title_contents(title_tag)
        if by_tag is None:
            by_content = (None,)
        else:
            by_content = get_by_contents(by_tag)
        extras_content = get_extras_content(extras_tag)

        product_info["name"] = title_content[0]
        product_info["description"] = title_content[1]
        product_info["link"] = title_content[2]
        product_info["by"] = by_content[0]
        product_info["is_solo_maker"] = extras_content[0]
        product_info["is_bootstrapped"] = extras_content[1]
        product_info["topics"] = extras_content[2]

        products.append(product_info)
    return products

def get_title_contents(tag:Tag):
    a_tag = tag.find('a')
    content = list(a_tag.stripped_strings)
    return (content[0],
            content[-1],
            a_tag['href'])

def get_by_contents(tag:Tag):
    a_tag = tag.find('a')
    return (a_tag['href'],)


def get_extras_content(tag:Tag):
    links = [a_tag["href"] for a_tag in tag.find_all('a')]
    solo_maker_filter   = check_filter(links, "soloMaker")
    bootstrapped_filter = check_filter(links, "bootstrapped")
    topics = get_topics(links)

    return (solo_maker_filter,
            bootstrapped_filter,
            topics)

def check_filter(extras:list[str], filter:str) -> bool:
    """
    Extract filters from extras and
    return True if `filter` exists in the result
    otherwise, False
    """
    filters = [link.split("=")[-1] for link in extras if link.startswith("/?filters")]
    if filter in filters:
        return True
    return False

def get_topics(extras:list[str]):
    """Extract topics from extras"""
    topics = [link for link in extras if link.startswith("/topics")]
    return topics


if __name__ == "__main__":
    soup = get_ph_soup()
    ts = get_top_products(soup.main)
