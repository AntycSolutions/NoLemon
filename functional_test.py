from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):
    
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        
    def tearDown(self):
        self.browser.quit()
        
    def test_can_post_new_car_inspection_video(self):
        self.browser.get('http://localhost:8080')
        
        self.assertIn('No Lemon', self.browser.title)
        self.fail('Finish the test!')
        
    
if __name__ == '__main__':
    unittest.main(warnings='ignore')