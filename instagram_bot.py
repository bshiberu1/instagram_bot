from time import sleep
from selenium import webdriver
from instapy import InstaPy, smart_run

'''
This instagram mimics modern instagram bot services by providing services such as 'organically' growing a bot account, 
and automating a set of bot accounts to like a posts by a series of users 
'''

list_of_proxies = [("8.8.8.8", 8080)]
list_of_accounts = [("username1", "password1"), ("username2", "password2"), ("username3", "password3")]
list_of_users = ["username1", "username2", "username3"]

photo_comments = ['Nice shot! @{}',
    'I love your profile! @{}',
    'Your feed is an inspiration :thumbsup:',
    'Just incredible :heart_eyes:',
    'What camera did you use @{}?',
    'Love your posts @{}',
    'Looks awesome @{}',
    'Getting inspired by you @{}',
    ':raised_hands: Yes!',
    'I can feel your passion @{} :muscle:']

def organically_grow_account(session):  
    with smart_run(session):
        session.set_user_interact(amount=3, randomize=True, percentage=100,
                              media='Photo')
        session.set_relationship_bounds(enabled=True,
                                        potency_ratio=None,
                                        delimit_by_numbers=True,
                                        max_followers=1000,
                                        min_followers=100,
                                        min_following=100)
        session.set_simulation(enabled=False)
        session.set_do_like(enabled=True, percentage=80)
        session.set_do_comment(enabled=True, percentage=30)
        session.set_do_follow(enabled=True, percentage=25, times=1)
        session.set_comments(photo_comments)
        session.set_action_delays(enabled=True, like=40)
        session.set_do_story(enabled = True, percentage = 100, simulate = False)

        # activity
        session.interact_user_followers([], amount=340)
        session.join_pods(topic='gaming', engagement_mode='no_comments')

def like_user_posts(users, session):
    # like 50% of posts
    session.set_do_follow(enabled=False, percentage=50)
    # put the given comments 80% of the time upon interaction
    session.set_comments(photo_comments)
    session.set_do_comment(enabled=True, percentage=80)
    # like 70% of interacted posts
    session.set_do_like(True, percentage=70)
    session.interact_by_users(users, amount=5, randomize=True, media='Photo')

session = InstaPy(username=list_of_accounts[0][0], password=list_of_accounts[0][1])
session.login()

like_user_posts(list_of_users, session)
organically_grow_account(session)

# Initial use of Page Object Patterns to log into instagram (Deprecated)
class LaunchLogin:
    def __init__(self, browser):
        self.browser = browser    
        self.browser.get('https://www.instagram.com/')
    def login(self, username, password):
        sleep(2)

        username_input = self.browser.find_element_by_css_selector("input[name='username']")
        password_input = self.browser.find_element_by_css_selector("input[name='password']")

        username_input.send_keys(username)
        password_input.send_keys(password)

        login_button = self.browser.find_element_by_xpath("//button[@type='submit']")
        login_button.click()

        sleep(5)
        
def test_login_selenium():    
    browser = webdriver.Firefox()
    browser.implicitly_wait(5)
    login_page = LaunchLogin(browser)
    login_page.login("username", "password")