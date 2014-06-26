import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(unittest.TestCase):
    
    def setUp(self):
        self.browser = webdriver.Firefox()
        
    def tearDown(self):
        self.browser.quit()
        
    def test_can_register_as_a_seller_and_log_in(self):
        self.fail("Finish this test!")
        # Dot wants to sell her car, and her buyer wants to see
        # that she's listed it on NoLemon.ca. She goes there to
        # list it
        
        # Dot notices at the top of the page, there is text that
        # tells her she should register for an account to sell
        # her car
        
        # Dot clicks on the register link and it takes her to the
        # registration page
        
        # Dot inputs her name and her email address. The page
        # tells her that she will be sent a temporary password
        # to her email, and in the future she can use her email
        # address to log in to NoLemon.ca
        
        # After Dot checks her email and receives her temporary
        # password, she returns to NoLemon via the link in her email
        # where she is prompted to change her password.
        
        # She inputs her chosen password and hits save, where she is
        # then taken her account page. 
        
        # She wants to test that it worked so the logs out of NoLemon
        # and logs back in. 
        
        # When she logs in she notices she is taken back to the main
        # page, but in the top right corner she sees her name and a
        # link to her account page
        
        # satisfied, Dot logs out and closes her browser
        

    def test_seller_can_request_an_inspection(self):
        self.fail("Finish this test!")
        
        # Dot remembers she wanted to get an inspection done for
        # her vehicle, so she goes to NoLemon.ca, and logs in to
        # her account
        
        # She clicks on the link in the top right corner to go to
        # her account page
        
        # From her account page, she notices text that asks if she
        # has a car to sell. Beside it is a button that she can
        # click to request an inspection by a mechanic.
        
        # Dot clicks the button and is taken to a page that tells
        # her she needs to fill out a request form, and pay an
        # inspection fee.
        
        # She fills out the form with the vehicle's VIN, year, 
        # make, and model. At the bottom there's text that tells her
        # when she clicks okay, a pop-up will come up asking for
        # her credit card information.
        
        # Dot enters her information, and when the pop-up closes,
        # she is brought to a page with a thank you message. The 
        # page also tells her that a download will start soon
        # with the form that she will need to take to the mechanic
        
        # Dot notices the page lists the mechanics that are
        # registered on the site, with their contact information 
        # and location.
        
        # After she choses a mechanic, Dot closes her browser.
        
        
    def test_can_search_for_car_inspection_video(self):
        # Enzo browses to NoLemon.ca
        self.browser.get('http://localhost:8080')
        self.fail("Finish the test!")
        
        # Enzo notices the title is NoLemon, and at the top
        # of the page, there is a header that also says NoLemon
        
        # Enzo sees that there is a search bar that invites him
        # to search for a vehicle using it's VIN
        
        # Enzo types in the VIN for the car he's looking at, and
        # when he hits enter he sees a list of inspections done
        # on the car, the most recent inspection at the top
        
        # he clicks on what looks to be the most recent inspection
        # done and it takes him to the page that shows more detail
        # about the inspection done on the vehicle
        
        # Enzo notices the inspection page has comments about the
        # vehicle, the name of the person selling the vehicle, and
        # the name of the mechanic who did the inspection
        
        # Enzo clicks play on the video to watch it
        
        # satisfied by the inspection, he gives the seller a good
        # rating, and closes his browser
        
    
    def test_mechanic_can_upload_inspection(self):
        self.fail("Finish this test!")
        

if __name__ == '__main__':
    unittest.main(warnings='ignore')