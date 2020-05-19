from time import sleep
from selenium import webdriver
from instapy import InstaPy, smart_run

'''
This GUI instagram application mimics modern instagram bot services by providing services such as 'organically' 
growing a bot account, and automating a set of bot accounts to like a posts by a series of users, must have 
fireFox installed in order to run this

To fix errors caused from InstaPy's instagram status checks, comment out the following lines in login_util.py:
# Hotfix - this check crashes more often than not -- plus in not necessary, I can verify my own connection
if want_check_browser:
    if not check_browser(browser, logfolder, logger, proxy_address):
        return False
'''
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget


from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QDialogButtonBox

from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QFormLayout


from functools import partial


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
        session.join_pods(topic='general', engagement_mode='no_comments')


def like_user_posts(users, session):
    with smart_run(session):
        # like 50% of posts
        session.set_do_follow(enabled=False, percentage=50)
        # put the given comments 80% of the time upon interaction
        session.set_comments(photo_comments)
        session.set_do_comment(enabled=True, percentage=80)
        # like 70% of interacted posts
        session.set_do_like(True, percentage=70)
        session.interact_by_users(users, amount=5, randomize=True, media='Photo')


class IgBotUi(QMainWindow):
    """PyCalc's View (GUI)."""
    def __init__(self):
        """View initializer."""
        super().__init__()
        # Set some main window's properties
        self.setWindowTitle('Instagram Bot')
        self.setFixedSize(250, 200)

        # Set the central widget
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)        
        self.setCentralWidget(self._centralWidget)

        self._centralWidget.setLayout(self.generalLayout)
        self._credentials()
        self._buttons()

    def _credentials(self):
        layout = QFormLayout()
        username = QLineEdit()
        password = QLineEdit()
        password.setEchoMode(2)
        numAccounts = QLineEdit()
        numAccounts.setMaximumWidth(25)
        username.setPlaceholderText("username")
        password.setPlaceholderText("password")
        self.username = username
        self.password = password
        self.numAccounts = numAccounts
        # self.generalLayout.addWidget(username)
        layout.addRow('Username:', username)
        layout.addRow('Password:', password)
        layout.addRow('# of Accounts:', numAccounts)

        # # Add the display to the general layout
        self.generalLayout.addLayout(layout)

    '''
    Launches instagram using the provided log in and automates the account to 
    like posts and follow other accounts
    '''
    def grow(self):
        session = InstaPy(username=self.username.text(), password=self.password.text())
        organically_grow_account(session)

    '''
    Launches the dialog box to get the list of usernames to interact with
    '''
    def interact(self):
        dlg = Dialog(numAccounts = self.numAccounts.text(), view = self)
        dlg.exec_()

    '''
    Given the provided usernames will create a new instagram session and 
    interact with the users on the list
    '''
    def interactWithUsers(self, usernames):
        session = InstaPy(username=self.username.text(), password=self.password.text())
        like_user_posts(usernames, session)

    '''
    Initializes the buttons on the main window
    '''
    def _buttons(self):
        self.pushButtons = {}

        self.pushButtons["organicallyGrow"] = QPushButton("Organically Grow Account")
        self.pushButtons["likeUserPosts"] = QPushButton("Designate Account to interact with Users")

        self.generalLayout.addWidget(self.pushButtons["organicallyGrow"])
        self.generalLayout.addWidget(self.pushButtons["likeUserPosts"])


class Dialog(QDialog):
    """Dialog."""
    def __init__(self, parent=None, numAccounts = "3", view=None):
        """Initializer."""
        super().__init__(parent)
        self.view = view
        self.setWindowTitle('QDialog')
        dlgLayout = QVBoxLayout()
        formLayout = QFormLayout()

        # Retreiving the number of accounts interact with
        try: 
            numAccount = int(numAccounts)
        except Exception:
            numAccount = 3
        if (numAccount > 20 or numAccount < 1):
            numAccount = 3

        # Adding all the QlineEdits to a collective array that's used to
        # amass all the usernames entries
        self.usernames = []
        for i in range(numAccount):
            self.usernames.append(QLineEdit())
        for username in self.usernames:
            formLayout.addRow('username:', username)

        # Ok/Cancel Buttons    
        dlgLayout.addLayout(formLayout)
        btns = QDialogButtonBox()
        btns.setStandardButtons(
            QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
             
        # Actions depending on whether OK or Cancel are clicked on
        btns.accepted.connect(self.addAccounts)

        dlgLayout.addWidget(btns)
        self.setLayout(dlgLayout)

    def addAccounts(self):
        usernamesStr = []
        for username in self.usernames:
            usernamesStr.append(username.text())
        self.close()
        self.view.interactWithUsers(usernamesStr)


class IgBotCtrl:
    """IgBot Controller class."""
    def __init__(self, view):
        """Controller initializer."""
        self._view = view
        # Connect signals and slots
        self._connectSignals()
  
    def _connectSignals(self):
        self._view.pushButtons["organicallyGrow"].clicked.connect(self._view.grow)
        self._view.pushButtons["likeUserPosts"].clicked.connect(self._view.interact)
        # self._view.display.returnPressed.connect(self._growAccount)

# Client code
def main():
    """Main function."""
    # Create an instance of QApplication
    igBot = QApplication(sys.argv)
    
    # Show the calculator's GUI
    view = IgBotUi()
    view.show()

    # Create instances of the model and the controller
    IgBotCtrl(view=view)
    # print("controller exected")

    # Execute the calculator's main loop
    sys.exit(igBot.exec_())

if __name__ == '__main__':
    main()

'''
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

'''