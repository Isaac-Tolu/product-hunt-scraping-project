import unittest
from startup import startup
from app import (get_title_section, get_extras_section, 
    get_votes_section, get_company, check_filter, get_topics
)
from constants import PRODUCT_SECTION__CLASS

soup = startup()
tags = soup.find_all(class_=PRODUCT_SECTION__CLASS)
# tags = [0, 1, 2]

class TestGetTitleSection(unittest.TestCase):

    def test_one(self):
        self.assertEqual(get_title_section(tags[0]),
                          ("OpenArt", "App store for AI image apps", "/posts/openart-2"))

    def test_two(self):
        self.assertEqual(get_title_section(tags[1]),
                          ("Share GPT", "Share your GPTs with anyone, no OpenAI subscription needed", "/posts/share-gpt"))
        
    def test_three(self):
        self.assertEqual(get_title_section(tags[2]),
                          ("Translatespace", "Auto-localization for busy people - don't miss out on SEO", "/posts/translatespace"))
        
class TestGetExtrasSection(unittest.TestCase):

    def test_one(self):
        self.assertEqual(get_extras_section(tags[0]),
                          ("OpenArt.ai", False, False, ['Design Tools', 'SaaS', 'Artificial Intelligence']))
        
    def test_two(self):
        self.assertEqual(get_extras_section(tags[1]),
                          (None, False, True, ['SaaS', 'Artificial Intelligence', 'No-Code']))
        
    def test_three(self):
        self.assertEqual(get_extras_section(tags[2]),
                          (None, True, True, ['Languages', 'SEO']))
        
class TestGetCompany(unittest.TestCase):

    def test_one(self):
        self.assertEqual(get_company(("/products/openart", "OpenArt.ai")),
                         "OpenArt.ai")
        
    def test_two(self):
        self.assertIsNone(get_company(('/?filters=bootstrapped', 'Bootstrapped')))

    def test_three(self):
        self.assertIsNone(get_company(('/?filters=soloMaker', 'Solo maker')))       

class TestCheckFilter(unittest.TestCase):

    def test_one_a(self):
        self.assertFalse(check_filter([('/products/openart', 'OpenArt.ai'),
                            ('/topics/design-tools', 'Design Tools'),
                            ('/topics/saas', 'SaaS'),
                            ('/topics/artificial-intelligence', 'Artificial Intelligence')
                        ], "soloMaker"))
        
    def test_one_b(self):
        self.assertFalse(check_filter([('/products/openart', 'OpenArt.ai'),
                            ('/topics/design-tools', 'Design Tools'),
                            ('/topics/saas', 'SaaS'),
                            ('/topics/artificial-intelligence', 'Artificial Intelligence')],
                        "bootstrapped"))
        
    def test_two_a(self):
        self.assertFalse(check_filter([('/?filters=bootstrapped', 'Bootstrapped'),
                            ('/topics/saas', 'SaaS'),
                            ('/topics/artificial-intelligence', 'Artificial Intelligence'),
                            ('/topics/no-code', 'No-Code')],
                        "soloMaker"))
        
    def test_two_b(self):
        self.assertTrue(check_filter([('/?filters=bootstrapped', 'Bootstrapped'),
                            ('/topics/saas', 'SaaS'),
                            ('/topics/artificial-intelligence', 'Artificial Intelligence'),
                            ('/topics/no-code', 'No-Code')],
                        "bootstrapped"))
        
    def test_three_a(self):
        self.assertTrue(check_filter([('/?filters=soloMaker', 'Solo maker'),
                            ('/?filters=bootstrapped', 'Bootstrapped'),
                            ('/topics/languages', 'Languages'),
                            ('/topics/seo', 'SEO')],
                        "soloMaker"))
        
    def test_three_b(self):
        self.assertTrue(check_filter([('/?filters=soloMaker', 'Solo maker'),
                            ('/?filters=bootstrapped', 'Bootstrapped'),
                            ('/topics/languages', 'Languages'),
                            ('/topics/seo', 'SEO')],
                        "bootstrapped"))
        
class TestGetTopics(unittest.TestCase):

    def test_one(self):
        self.assertEqual(get_topics([('/products/openart', 'OpenArt.ai'),
                            ('/topics/design-tools', 'Design Tools'),
                            ('/topics/saas', 'SaaS'),
                            ('/topics/artificial-intelligence', 'Artificial Intelligence')]),
                        ["Design Tools", "SaaS", "Artificial Intelligence"])
        
    def test_two(self):
        self.assertEqual(get_topics([('/?filters=bootstrapped', 'Bootstrapped'),
                            ('/topics/saas', 'SaaS'),
                            ('/topics/artificial-intelligence', 'Artificial Intelligence'),
                            ('/topics/no-code', 'No-Code')]),
                        ["SaaS", "Artificial Intelligence", "No-Code"])
        
    def test_three(self):
        self.assertEqual(get_topics([('/?filters=soloMaker', 'Solo maker'),
                            ('/?filters=bootstrapped', 'Bootstrapped'),
                            ('/topics/languages', 'Languages'),
                            ('/topics/seo', 'SEO')]),
                        ["Languages", "SEO"])   
        
class TestGetVotesSection(unittest.TestCase):

    def test_one(self):
        self.assertEqual(get_votes_section(tags[0]),
                          ("845",))
        
    def test_two(self):
        self.assertEqual(get_votes_section(tags[1]),
                          ("356",))
        
    def test_three(self):
        self.assertEqual(get_votes_section(tags[2]),
                          ("112",))


if __name__ == "__main__":
    unittest.main()