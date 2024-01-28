import requests
from bs4 import BeautifulSoup


LINK = "https://www.producthunt.com/leaderboard/daily/2024/1/26"

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

    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def get_top_products(tag):
    a = []

    for product_tag in tag.find_all(class_=PRODUCT_SECTION__CLASS):
        d = {}

        title_tag  = product_tag.find(class_=PRODUCT_TITLE__CLASS)
        extras_tag = product_tag.find(class_=PRODUCT_EXTRAS__CLASS)
        title_content = list(title_tag.stripped_strings)
        filters_and_topics = [a["href"] for a in extras_tag.find_all('a')]
        # print(filters_and_topics)
        # filters = [i.split("=")[-1] for i in filters_and_topics if i.startswith("/?filters")]
        # print(filters)
        # topics = [i.split("/")[-1] for i in filters_and_topics if i.startswith("/topics")]
        # print(topics)
        # print("\n\n")

        d["name"] = title_content[0]
        d["description"] = title_content[-1]
        d["link"] = title_tag.a["href"]
        d["is_solo_maker"] = check_filter(filters_and_topics, "soloMaker")
        d["is_bootstrapped"] = check_filter(filters_and_topics, "bootstrapped")
        d["topics"] = get_topics(filters_and_topics)

        
        # if "Solo maker" in extras_content:
        #     d["is_solo_maker"] = True
        #     extras_content.remove("Solo maker")
        # else:
        #     d["is_solo_maker"] = False

        # if "Bootstrapped" in extras_content:
        #     d["is_bootstrapped"] = True
        #     extras_content.remove("Bootstrapped")
        # else:
        #     d["is_bootstrapped"] = False
        
        # topics = [i for i in extras_content if i != "•"]

        # d["topics"] = topics

        a.append(d)

    return a


def check_filter(l, filter):

    filters = [i.split("=")[-1] for i in l if i.startswith("/?filters")]
    if filter in filters:
        return True
    return False


# ## List -> Boolean
# ## return true if the soloMaker filter is one of the URLs, otherwise false
# def is_solo_maker(l):
#     if "soloMaker" in l:
#         return True
#     return False

# ## List -> Boolean
# ## return true if the bootstrapped filter is one of the URLs, otherwise false
# def is_bootstrapped(l):
#     if "bootstrapped" in l:
#         return True
#     return False

## List -> List
## Extract the topics from their URLs and return them
def get_topics(l):
    
    topics = [i.split("/")[-1] for i in l if i.startswith("/topics")]
    return topics


if __name__ == "__main__":
    soup = get_ph_soup()
    
    # print(soup.main)

    ts = get_top_products(soup.main)
    # print(ts)

