from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

def searchWords(words):
    chromeOpts = Options()
    chromeOpts.headless = True
    browser = Chrome(executable_path="C:\\Program Files (x86)\\Google\\ChromeDriver\\chromedriver.exe", options=chromeOpts)
    
    for word in words:
        browser.get("http://www.gavo.t.u-tokyo.ac.jp/ojad/search")
        searchBox = browser.find_element_by_id("search_word")
        searchBox.send_keys(word)
        searchBox.submit()
        # first time this class occurs is for the normal pitch accent (i.e. not declined or conjugated)
        accentField = browser.find_elements_by_class_name("accented_word")[0]
    
def parseAccent(word):
    return True