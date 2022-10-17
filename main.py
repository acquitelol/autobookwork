# main imports from modules and dependencies
from enum import auto
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from datetime import datetime
from Acqu_Dependencies.acqu_pass import input_password
from Acqu_Dependencies.acqu_format import formatted_log
import time, json, re, os

# used globally around the script for different items, set in the "local" class
class info:
    USERNAME = ""
    PASSWORD = ""
    PATH = ""
    VERSION = ""
    URL = ""

    FILE_NAME = datetime.now().strftime("%d-%m-%Y-%H-%M-%S") # the current date formatted
    FILE_DIR = f'Logs/{FILE_NAME}'
    FILE_PARAM = f"{FILE_DIR}/{FILE_NAME}.log" # the output location
    LAST_MESSAGE = ""
    IS_OPEN = True
    AUTO_CONTINUE = False
    AUTO_BOOKWORK = False

# bash color codes used for pretty terminal
class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    OKPINK = '\033[95m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class logging:
    def __init__(self, typeOf, message, fp):
        self.type = typeOf # used for logging
        self.message = message # the message to write/print
        self.fp = fp # the file path / file parameter

    def log(self):
        if info.LAST_MESSAGE == self.message or len(self.message) < 34:
            return # returns early if the message didnt change
        else:
            final_message = re.sub("\\033\[(.*?)m", "", str(self.message)) # removes any color codes to write it to log file with a simple regex

            current_time = time.strftime("%H:%M:%S", time.localtime()) # formats the time
            log_file = open(self.fp, "a") # append to a file
            log_file.write(f"[{str(current_time)}] {final_message} \n") # write the new contents with the reformatted message
            log_file.close() #close the file

            print(f"{colors.WARNING}{colors.BOLD}[{current_time}] {colors.ENDC}{colors.OKCYAN}{self.message}") # also print the original message with color codes to terminal
            info.LAST_MESSAGE = self.message # sets the message to the last message
            return

    def create_log(self):
        try:
            os.mkdir(info.FILE_DIR)
            log_file = open(self.fp, "a") # appends to a file
            log_file.write(formatted_log( 
                info.FILE_NAME, 
                info.USERNAME, 
                info.PASSWORD, 
                info.AUTO_CONTINUE, 
                info.AUTO_BOOKWORK, 
                info.VERSION)
            ) # uses a dependency which just prints a multiline string interpolation, moved it to a seperate function because it looks ugly
            log_file.close()
            logging(
                None,
                f"{colors.HEADER}{colors.BOLD}[{self.type}] {colors.ENDC}{colors.OKCYAN}Creating New Log File...",
                self.fp
            ).log()
                
            logging(
                None,
                f"{colors.HEADER}{colors.BOLD}[{self.type}] {colors.ENDC}{colors.OKCYAN}New Log Made: {colors.OKBLUE}{info.FILE_NAME}",
                self.fp
            ).log()
            return
        except:
            return onError(main, f"{colors.WARNING}Failed to create a new log file")

class local:
    def __init__(self, typeOf, fp):
        self.type = typeOf
        self.fp = fp

    def saveSettings(self):
        info.USERNAME = input(f"{colors.HEADER}{colors.BOLD}[{self.type}] {colors.ENDC}{colors.OKCYAN}Sparx Username: {colors.OKBLUE}")
        info.PASSWORD = input_password(f"{colors.HEADER}{colors.BOLD}[{self.type}] {colors.ENDC}{colors.OKCYAN}Sparx Password: {colors.OKBLUE}")
        print("✓") # print a tick once the user pressed enter to signify that the password has been recorded
        CONTINUE = input(f"{colors.HEADER}{colors.BOLD}[{self.type}] {colors.ENDC}{colors.OKCYAN}Auto Continue: {colors.OKBLUE}").casefold()
        BOOKWORK = input(f"{colors.HEADER}{colors.BOLD}[{self.type}] {colors.ENDC}{colors.OKCYAN}Auto Bookwork: {colors.OKBLUE}").casefold()
        SAVE = input(f"{colors.HEADER}{colors.BOLD}[{self.type}] {colors.ENDC}{colors.OKCYAN}Save Settings: {colors.OKBLUE}").casefold()

        if CONTINUE == "true" or CONTINUE == "yes" or CONTINUE == "y":
            info.AUTO_CONTINUE = True
            print(f"\n{colors.HEADER}{colors.BOLD}[{self.type}] {colors.ENDC}{colors.OKCYAN}Auto Continue enabled.")
        if BOOKWORK == "true" or BOOKWORK == "yes" or BOOKWORK == "y":
            info.AUTO_BOOKWORK = True
            print(f"{colors.HEADER}{colors.BOLD}[{self.type}] {colors.ENDC}{colors.OKCYAN}Auto Bookwork enabled.")
        if SAVE == "true" or SAVE == "yes" or SAVE == "y":
            print(f"{colors.HEADER}{colors.BOLD}[{self.type}] {colors.ENDC}{colors.OKCYAN}Saving settings to \"{colors.WARNING}{self.fp}{colors.OKCYAN}\". {colors.OKBLUE}This may take some time... \n")

            data = {'settings': [
                    {
                        'USERNAME': info.USERNAME, 
                        'PASSWORD': info.PASSWORD, 
                        'AUTO_CONTINUE': info.AUTO_CONTINUE, 
                        'AUTO_BOOKWORK': info.AUTO_BOOKWORK
                    }
                ]
            }
            with open(self.fp, 'w') as outfile:
                json.dump(data, outfile)
            return
        else:
            return onError(main, f"{colors.WARNING}Invalid argument provided")

    def loadSettings(self):
        try:
            with open(self.fp) as json_file:
                data = json.load(json_file)
                print(f"{colors.HEADER}{colors.BOLD}[{self.type}] {colors.ENDC}{colors.OKCYAN}Loading setting configurations. {colors.OKGREEN}This may take some time...")
                info.USERNAME = data['settings'][0]['USERNAME']
                info.PASSWORD = data['settings'][0]['PASSWORD']
                info.AUTO_CONTINUE = data['settings'][0]['AUTO_CONTINUE']
                info.AUTO_BOOKWORK = data['settings'][0]['AUTO_BOOKWORK']
                return True
        except:
            return False

    def loadDriverLink(self):
        try:
            with open('Local/personal.json') as json_file:
                data = json.load(json_file)
                print(f"{colors.HEADER}{colors.BOLD}[{self.type}] {colors.ENDC}{colors.OKCYAN}Loading local configurations. {colors.OKGREEN}This may take some time...")
                info.URL = data['config'][0]['URL']
                info.VERSION = data['config'][0]['VERSION']
                info.PATH = data['config'][0]['PATH']
                return True
        except:
            return False

def onError(function, errorMessage):
    print(f"{colors.FAIL}{colors.BOLD}[Error] {colors.ENDC}{colors.OKBLUE}Autobookwork has failed to start. {errorMessage}{colors.OKBLUE}, Trying again...")
    function() # start the script again

def main():
    if not local("Local", None).loadDriverLink():
        return onError(main, f"{colors.WARNING}Failed loading local info")

    time.sleep(1)
    print(f"\n{colors.OKCYAN}[Made By {colors.OKPINK}{colors.BOLD}Acquite {colors.ENDC}{colors.OKCYAN}<3]")
    print(f"{colors.OKCYAN}{colors.BOLD}[Autobookwork] {colors.HEADER}[Version] {colors.ENDC}{colors.OKBLUE}{info.VERSION}\n")
    time.sleep(1)

    filePath = 'Local/settings.json'
    if not local("Settings", filePath).loadSettings():  # if loadsettings returns false then savesettings for next time.
        local("Settings", filePath).saveSettings()

    logging("Log", None, info.FILE_PARAM).create_log()

    DRIVER = webdriver.Chrome(service=Service(info.PATH))
    DRIVER.maximize_window()
    size = DRIVER.get_window_size() # window size at full screen
    DRIVER.set_window_size(size['width'], size['height']*0.77) # full screen with 77% height to see console
    DRIVER.get(info.URL)
    USERNAME_ELEMENT = DRIVER.find_element(By.ID, "username")
    PASSWORD_ELEMENT = DRIVER.find_element(By.ID, "password")

    USERNAME_ELEMENT.send_keys(info.USERNAME)
    PASSWORD_ELEMENT.send_keys(info.PASSWORD)
    PASSWORD_ELEMENT.send_keys(Keys.RETURN)

    logging(
        None,
        f"{colors.HEADER}{colors.BOLD}[Main] {colors.ENDC}{colors.OKCYAN}Chrome Version: {colors.OKBLUE}{str(DRIVER.capabilities['browserVersion'])}",
        info.FILE_PARAM
    ).log()
    
    try:
        mainLoop(DRIVER)
    except:
        logging(
            None,
            f"{colors.HEADER}{colors.BOLD}[Main] {colors.ENDC}{colors.OKBLUE}Chrome's Custom Process has been terminated. Exiting script...", 
            info.FILE_PARAM
        ).log()
        info.IS_OPEN = False
        exit()

def mainLoop(driver):
    while info.IS_OPEN:
        if "Sparx" in driver.title:
            try:
                BOOKWORK = driver.find_element(By.CLASS_NAME, 'bookwork-code')
                SUBMIT_ELEM = driver.find_element(By.ID, "skill-delivery-submit-button")

                def autoContinue(if_continue):
                    if if_continue:
                        driver.execute_script("""
                            let both = document.getElementsByClassName('button-text')

                            for (var i = 0; i < both.length; i++) {
                                if (both.item(i).innerText=="Continue" || both.item(i).innerText=="Second chance") {
                                    both.item(i).parentElement.parentElement.click()
                                }
                            }
                        """)

                driver.execute_script("""
                    var ele = arguments[0]; 
                    ele.addEventListener('click', () => {
                        ele.setAttribute('automationTrack','true');
                    });
                    document.addEventListener('keydown', (event) => {
                        if (event.key === "Enter") {
                            ele.setAttribute('automationTrack','true');
                        }
                    });
                """, SUBMIT_ELEM)
                    
                try:  
                    if SUBMIT_ELEM.get_attribute("automationTrack"):
                        answer = driver.find_element(By.CLASS_NAME, "skill-delivery-view")
                        bookwork = BOOKWORK.text.split(': ', 1)[1]
                        answer.screenshot(f'./Logs/{info.FILE_NAME}/{bookwork}.png')
                        logging(
                            None,
                            f"{colors.HEADER}{colors.BOLD}[Bookwork] {colors.ENDC}{colors.HEADER}{bookwork} {colors.OKBLUE}Saved Successfully at {colors.OKCYAN}./Logs/{bookwork}", 
                            info.FILE_PARAM
                        ).log()
                        time.sleep(1)
                except:
                    autoContinue(info.AUTO_CONTINUE)
                
            except:
                "acquite is a girl"


if __name__ == '__main__':
    main()