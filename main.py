######################################################################
##  Author: Nikolaos Markakis
##  Requires selenium, numpy, webdriver_manager and Google Chrome
##
##  Throughout the code random delays and random behaviours in general
##  are added to maintain human patterns and prevent the bot from
##  getting blocked.
##
##  Scrolling during the non-idle brake was not implemented because
##  running scripts might be considered suspicious and therefore get
##  the bot blocked.
##
##  All element classes can be found using the developer environment
##  of Chrome (F12).
##
##  The bot runs an infinite loop of liking sessions and breaks
##  press Ctrl+C to terminate.
######################################################################


from selenium import webdriver
from datetime import datetime  
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
import time

class InstagramBot():
    likes_made = 0     
    
    def __init__(self,email,password):
        self.browser = webdriver.Chrome(ChromeDriverManager().install())
        self.email = email
        self.password = password

    #signs in with credentials provided during object initialization
    def signIn(self):

        self.browser.get('https://www.instagram.com/accounts/login/')
        print('{} Logging in as: {}'.format(datetime.now(),self.email))
        time.sleep(np.random.randint(4,7))
        emailInput = self.browser.find_elements_by_css_selector('form input')[0]
        passwordInput = self.browser.find_elements_by_css_selector('form input')[1]

        emailInput.send_keys(self.email)
        passwordInput.send_keys(self.password)
        passwordInput.send_keys(Keys.ENTER )
        time.sleep(np.random.randint(4,7))
        notification_btn = WebDriverWait(self.browser, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//button[@class='aOOlW   HoLwm ']")
            )
        )
        notification_btn.click()
        

    #Uses the search bar to search for argument 'name' 
    def search(self,name,is_tag = False):
        print('{} Searching for: {}...'.format(datetime.now(),name))
        searchbox = WebDriverWait(self.browser, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//input[@placeholder='Search']")
            )
        )
        
        if(is_tag):
            name= '#'+name
            
        searchbox.send_keys(name)
        time.sleep(np.random.randint(4,7))
        searchbox.send_keys(Keys.ENTER)
        searchbox.send_keys(Keys.ENTER)
        time.sleep(np.random.randint(7,10))


    #Likes an already loaded post
    def like_media(self):
        like_btn = WebDriverWait(self.browser, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//button[@class='dCJp8 afkep _0mzm-']")
            )
        )
        like_btn.click()
        self.likes_made=self.likes_made+1
        print('{} Liked media: {}'.format(datetime.now(),self.likes_made))

    #Returns to the explore page/search rerults from a picture by pressing X
    def back_from_media(self):
        back_btn = WebDriverWait(self.browser, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//button[@class='ckWGn']")
            )
        )
        print('{} Exiting from media.'.format(datetime.now()))
        back_btn.click()

    #Proceeds to the next picture by pressing the right arrow
    #Element type is 'a' not 'button'
    def next_to_media(self):
        next_btn = WebDriverWait(self.browser, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//a[@class='HBoOv coreSpriteRightPaginationArrow']")
            )
        )
        print('{} Moving on to the Next.'.format(datetime.now()))
        next_btn.click()


    #Likes search result medias using search and next_to_media
    #Uses random delay and random behaviour when exiting and nexting media
    #Likes a percentage of media seen (0.0-1.0)
    def like_results(self,numberOfLikes,percentage=0.85):
        first_pic = WebDriverWait(self.browser, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//div[@class='_9AhH0']")
            )
        )
        first_pic.click()
        
        counter = 0
        while counter < numberOfLikes:
            time.sleep(np.random.randint(32,45))
            if(np.random.random_sample()<percentage):
                self.like_media()
                counter = counter + 1
            time.sleep(np.random.randint(50,75)) 
            self.next_to_media()

        time.sleep(np.random.randint(3,5))
        self.back_from_media() #should incorporate random exiting now and then 

    
    #Non-idle break
    #Simulates the behaviour of scrolling for no reason while waiting for the
    #next liking session 
    def nonidle_break(self,duration):        
        print("{} Entering non-idle brake..".format(datetime.now()))
        self.go_home()
        time.sleep(duration/2)
        search("meme",is_tag=True)        
        time.sleep(duration/2)
        self.go_home()
    ##  self.scroll(duration)
        

    
    #Run_bot method runs the bot for specified tags and credentials
    #and switches between liking and braking
    def run_bot(self,tag_list):
        while True:
            for tag in tag_list:
                try:
                    self.search(tag,is_tag = True)
                    self.like_results(np.random.randint(17,25))                    
                    self.nonidle_break(np.random.randtint(378,798))
                except:
                    self.go_home()
                    time.sleep(np.random.randint(4,7))
                    print("{} Exception caught during liking hashtag {}".format(datetime.now(),tag))
                    continue           
                            
            


    #presses the home button
    def go_home(self):        
        home_btn = WebDriverWait(self.browser, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//span[@class='glyphsSpriteApp_instagram__outline__24__grey_9 u-__7']")
            )
        )
        print("{} Going to Home page..".format(datetime.now()))
        home_btn.click()
        time.sleep(4)

##    #scrolls
##    #TO BE IMPLEMENTED
##    def scroll(self,duration):
##        
##        print("{} Scrolling..".format(datetime.now()))
##        while ((datetime.now()-start_time).seconds < duration):
##            for i in range (np.random.randint(2,4)):
##                #scroll a little bit 
##            time.sleep(np.random.randint(5,30))
        
            
        
bot = InstagramBot('username','password')
bot.signIn()
time.sleep(8)
bot.run_bot(['cars','cats','dogs'])









