import requests
from bs4 import BeautifulSoup, Tag
from datetime import datetime, timedelta


URL = "https://www.producthunt.com/"
PARSER = 'html.parser'

PRODUCT_SECTION__CLASS    = "styles_item__Dk_nz"
PRODUCT_TITLE__CLASS      = "styles_titleContainer__qZRNa"
PRODUCT_BY__CLASS         = "styles_container__br9Sy"
PRODUCT_EXTRAS__CLASS     = "styles_extraInfo__Xs_5Y"
PRODUCT_VOTE_BUTTON__CLASS = "styles_voteCountItem__zwuqk"


def get_ph_soup() -> BeautifulSoup:
    """
    Gets the Product Hunt page and returns the HTML soup.
    """
    yesterday = get_yesterday()
    year, month, day = yesterday.year, yesterday.month, yesterday.day
    url = URL + f"leaderboard/daily/{year}/{month}/{day}"

    print(f"Getting {url}\n")

    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, PARSER)
    return soup

def get_top_products(tag:Tag) -> list[dict]:
    """
    Extract these data from each product on the page:
      {
        name: str, description: str, link: str, "by": str,
        is_solo_maker: bool, is_bootstrapped: bool,
        topics: list[str]
      }
    Returns the result as a list of dictionaries.
    """
    products = []

    for product_tag in tag.find_all(class_=PRODUCT_SECTION__CLASS):
        product_info = {}

        title_tag = product_tag.find(class_=PRODUCT_TITLE__CLASS)
        by_tag = product_tag.find(class_=PRODUCT_BY__CLASS)
        extras_tag = product_tag.find(class_=PRODUCT_EXTRAS__CLASS)
        upvote_count_tag = product_tag.find(class_=PRODUCT_VOTE_BUTTON__CLASS)

        title_content = get_title_contents(title_tag)
        if by_tag is None:
            by_content = (None,)
        else:
            by_content = get_by_contents(by_tag)
        extras_content = get_extras_content(extras_tag)
        vote_count = get_current_vote_count(upvote_count_tag)

        product_info["name"] = title_content[0]
        product_info["description"] = title_content[1]
        product_info["link"] = title_content[2]
        product_info["by"] = by_content[0]
        product_info["is_solo_maker"] = extras_content[0]
        product_info["is_bootstrapped"] = extras_content[1]
        product_info["topics"] = extras_content[2]
        product_info["current_votes"] = vote_count[0]

        products.append(product_info)
    return products

def get_title_contents(tag:Tag):
    """Extract the title section of the page"""
    a_tag = tag.find('a')
    content = list(a_tag.stripped_strings)
    return (content[0],
            content[-1],
            a_tag['href'])

def get_by_contents(tag:Tag):
    """Extract the product owner section of the page"""
    a_tag = tag.find('a')
    return (a_tag['href'],)


def get_extras_content(tag:Tag):
    """Extract the extras section of the page"""
    links = [a_tag["href"] for a_tag in tag.find_all('a')]
    solo_maker_filter   = check_filter(links, "soloMaker")
    bootstrapped_filter = check_filter(links, "bootstrapped")
    topics = get_topics(links)

    return (solo_maker_filter,
            bootstrapped_filter,
            topics)

def get_current_vote_count(tag:Tag):
    """Extract the current vote count number from page"""
    return (tag.text,)

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

def get_topics(extras:list[str]) -> list[str]:
    """Extract topics from extras"""
    topics = [link for link in extras if link.startswith("/topics")]
    return topics

def get_yesterday() -> datetime:
    """Returns the datetime object for yesterday"""
    return datetime.today() - timedelta(days=1)


if __name__ == "__main__":
    soup = get_ph_soup()
    ts = get_top_products(soup.main)
