import requests
from bs4 import BeautifulSoup, Tag


LINK = "https://www.producthunt.com/leaderboard/daily/2024/1/26"
PARSER = 'html.parser'

PRODUCT_SECTION__CLASS          = "styles_item__Dk_nz"
PRODUCT_TITLE__CLASS            = "styles_titleContainer__qZRNa"
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

        title_tag  = product_tag.find(class_=PRODUCT_TITLE__CLASS)
        extras_tag = product_tag.find(class_=PRODUCT_EXTRAS__CLASS)
        title_content = list(title_tag.stripped_strings)
        extras_links = [a_tag["href"] for a_tag in extras_tag.find_all('a')]

        product_info["name"] = title_content[0]
        product_info["description"] = title_content[-1]
        product_info["link"] = title_tag.a["href"]
        product_info["is_solo_maker"] = check_filter(extras_links, "soloMaker")
        product_info["is_bootstrapped"] = check_filter(extras_links, "bootstrapped")
        product_info["topics"] = get_topics(extras_links)

        products.append(product_info)
    return products


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
    topics = [link.split("/")[-1] for link in extras if link.startswith("/topics")]
    return topics


if __name__ == "__main__":
    soup = get_ph_soup()
    ts = get_top_products(soup.main)
