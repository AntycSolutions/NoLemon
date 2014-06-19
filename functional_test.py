import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(unittest.TestCase):
    
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        
    def tearDown(self):
        self.browser.quit()
        
    def test_can_search_for_car_inspection_video(self):
        self.browser.get('http://localhost:8080')
        
        self.assertIn('No Lemon', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('No Lemon', header_text)
        
        searchbox = self.browser.find_element_by_id('id_vin_search')
        self.assertEqual(searchbox.get_attribute('placeholder'),
                         'Search by VIN')
        
        # assume this VIN exists
        searchbox.send_keys('A1B2C3D4E5F6G7H8I')
        
        searchbox.send_keys(Keys.ENTER)
        
        results = self.browser.find_elements_by_class_name('search_result')
        self.assertIn('A1B2C3D4E5F6G7H8I',
                      any(result.id for result in results))
        
        self.fail('Finish the test!')
        
    
if __name__ == '__main__':
    unittest.main(warnings='ignore')