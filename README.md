# Autobookwork, a tool to automatically log SPARX Bookwork codes

## How to install:
#### Chapter 1: Installing all dependencies
1. Clone [the autobookwork repo](https://github.com/acquitelol/autobookwork).
2. `cd` into the directory, then run the following commands:
```sh
pip3 install -U selenium
pip3 install webdriver-manager
```
3. Enter into the `Local/info.json`, and:
- Either Add the path to your ChromeDriver executable binary into the path if you've already installed it,
- Otherwise Install Chrome Driver from [here](https://chromedriver.chromium.org/downloads).
#### Chapter 2: Setting up your Sparx.
1. Open a new tab, and:
- Either Navigate to `https://auth.sparxmaths.uk/oauth2/auth?client_id=sparx-maths-xxxxx`, which should be a link that requires your Username and Password for Sparx.
- Otherwise go to `https://sparxmaths.uk/` and add your school name, then you should get a link similar to `https://auth.sparxmaths.uk/oauth2/auth?client_id=sparx-maths-xxxxx`
2. Once you get this link, paste it into `Local/info.json`
3. Run the script with the following command:
```py
python3 ./main.py
```
4. On the first setup, you will be greeted with inputs for your Sparx Username and Password, and also settings like auto continue or auto bookwork.
For the questions with optional answers, you can answer with the following prompts:
```
y
yes
true
```
5. If you want your settings to be re-entered every time you run the script, then make sure to disable saving settings.
- (Quick FAQ: The password input is still typing, even though it may not look like it. It just flushes the buffer (empties the char) to make it invisible. Once you are done entering your password, and press enter, you will see a ✓ to determine that your input was recorded.
#### Chapter 3: Using the Script:
Any Sparx answers will be both logged to the console and logged to a .log file with the date for when it was created. <br>
If you type a different answer, the answer will be logged again.

It will automatically press the "Continue" or "Second Chance" button if it detects it.

## **Have Fun with Faster SPARX!!!**
#### Made with <3 By Acquite :)
#### Version 1.0.0
