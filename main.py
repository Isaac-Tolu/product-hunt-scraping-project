import requests
from bs4 import BeautifulSoup


LINK = "https://www.producthunt.com/leaderboard/daily/2024/1/26"
IMPORTANT_ATTRS = {
    "product_section_class": "styles_item__Dk_nz",
    "product_title_class": "styles_titleContainer__qZRNa",
    "product_extras_class": "styles_extraInfo__Xs_5Y",
    "product_vote_button_dt": "vote-button",
    "product_vote-button_class": "styles_voteCountItem__zwuqk",
}


def get_ph_soup() -> BeautifulSoup:
    """
    Returns the HTML soup for Product Hunt
    """
    
    response = requests.get(LINK)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def get_top_products(tag):
    a = []

    for product_tag in tag.find_all(class_=IMPORTANT_ATTRS["product_section_class"]):
        d = {}

        title_tag  = product_tag.find(class_=IMPORTANT_ATTRS["product_title_class"])
        extras_tag = product_tag.find(class_=IMPORTANT_ATTRS["product_extras_class"])

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
    #print(ts)

