import requests
from bs4 import BeautifulSoup


LINK = "https://www.producthunt.com/leaderboard/daily/2024/1/26"

PRODUCT_SECTION__CLASS = "styles_item__Dk_nz"
PRODUCT_TITLE__CLASS = "styles_titleContainer__qZRNa"
PRODUCT_EXTRAS__CLASS = "styles_extraInfo__Xs_5Y"
PRODUCT_VOTE_BUTTON__DATA_CLASS = "vote-button"
PRODUCT_VOTE_BUTTON_CLASS = "styles_voteCountItem__zwuqk"



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

        d["link"] = title_tag.a["href"]
        title_content = list(title_tag.stripped_strings)
        d["name"] = title_content[0]
        d["description"] = title_content[-1]

        extras_content = list(extras_tag.stripped_strings)
        if "Solo maker" in extras_content:
            d["is_solo_maker"] = True
            extras_content.remove("Solo maker")
        else:
            d["is_solo_maker"] = False
        
        if "Bootstrapped" in extras_content:
            d["is_bootstrapped"] = True
            extras_content.remove("Bootstrapped")
        else:
            d["is_bootstrapped"] = False
        
        topics = [i for i in extras_content if i != "•"]

        d["topics"] = topics

        a.append(d)

    return a
    
        

if __name__ == "__main__":
    soup = get_ph_soup()
    
    # print(soup.main)

    ts = get_top_products(soup.main)
    # print(ts)

