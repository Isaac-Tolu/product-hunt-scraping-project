import unittest
from startup import startup
from app import (get_title_section, get_extras_section, get_votes_section)
from constants import PRODUCT_SECTION__CLASS

soup = startup()
tags = soup.find_all(class_=PRODUCT_SECTION__CLASS)
# tags = [0, 1, 2]

class TestGetTitleSection(unittest.TestCase):

    def test_one(self):
        self.assertEqual(get_title_section(tags[0]),
                          ("OpenArt", "App Store for AI Images", "/posts/openart-2"))

    def test_two(self):
        self.assertEqual(get_title_section(tags[1]),
                          ("ShareGPT", "Share your GPTs with anyone, no OpenAI subscription needed", "/posts/share-gpt"))
        
    def test_three(self):
        self.assertEqual(get_title_section(tags[2]),
                          ("Translatespace", "Auto-localization for busy people - don't miss out on SEO", "/posts/translatespace"))
        
class TestGetExtrasSection(unittest.TestCase):

    def test_one(self):
        self.assertEqual(get_extras_section(tags[0]),
                          ("OpenArt.ai", False, False, ['Design Tools', 'SaaS', 'Artificial Intelligence']))
        
    def test_two(self):
        self.assertEqual(get_extras_section(tags[1]),
                          (None, False, True, ['SaaS', '', 'Artificial Intelligence', 'No-Code']))
        
    def test_three(self):
        self.assertEqual(get_extras_section(tags[2]),
                          (None, True, True, ['Languages', 'SEO']))
        
class TestGetVotesSection(unittest.TestCase):

    def test_one(self):
        self.assertEqual(get_votes_section(tags[0]),
                          (845,))
        
    def test_two(self):
        self.assertEqual(get_votes_section(tags[0]),
                          (356,))
        
    def test_three(self):
        self.assertEqual(get_votes_section(tags[0]),
                          (112,))


if __name__ == "__main__":
    unittest.main()