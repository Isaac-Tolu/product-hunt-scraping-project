import bs4

from constants import PARSER

def startup() -> bs4.BeautifulSoup:
    """Returns the BeautifulSoup HTML tree of the test html file"""

    with open("test_file.html", 'r') as f:
        content = f.read()

    soup = bs4.BeautifulSoup(content, PARSER)

    return soup