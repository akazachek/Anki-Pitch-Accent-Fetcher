from selenium.webdriver import Chrome
from selenium.common.exceptions import NoSuchElementException

classNames = ["mola_-", " accent_top mola_-", " accent_plain mola_-"]

def searchWord(browser, word):

    browser.get("http://www.gavo.t.u-tokyo.ac.jp/ojad/search")
    searchBox = browser.find_element_by_id("search_word")
    searchBox.send_keys(word)
    searchBox.submit()
    
    # handling synonyms
    wordPos = -1
    foundWords = browser.find_elements_by_class_name("midashi_word")
    for wordInd in range(len(foundWords)):
        if foundWords[wordInd].text == word:
            wordPos = wordInd
            break
    # means word cannot be found on OJAD
    if wordPos == -1: raise KeyError("Err: Not found in OJAD.")
    
    # (ugly) hardcoded navigation to the correct element in OJAD's table where every mora's pitch is stored
    OJADMoraSpan = browser.find_elements_by_xpath('//*[@id="word_table"]/tbody/tr[' + str(wordPos + 1) + ']/td[3]')[0].find_element_by_class_name("accented_word")
    
    wordPitch = []
    # words will never be longer than 6 mora in length (at least i hope)
    for moraInd in range(6, 0, -1):
        try:
            wordPitch.append(moraPitch(OJADMoraSpan, moraInd))
        except IndexError:
            pass

    return wordPitchType(wordPitch)
    
# return of 0 means pitch is low
# return of 1 means pitch is high and drops
# return of 2 means pitch is high and stays high
def moraPitch(OJADMoraSpan, moraInd):
    for nameInd in range(3):
        try:
            # classCond = "span[class='" + classNames[nameInd] + str(moraInd) + "']"
            # OJADMoraSpan.find_element_by_css_selector(classCond)
            # looking for exact class match
            classCond = ".//span[@class='" + classNames[nameInd] + str(moraInd) + "']"
            OJADMoraSpan.find_element_by_xpath(classCond)
            return(nameInd)
        except NoSuchElementException:
            pass
    raise IndexError("Err: Mora index " + str(moraInd) + " invalid.")

# returns pitch accent type based on standard dictionary defn
def wordPitchType(wordPitch):
    try:
        return wordPitch.index(1) + 1
    except ValueError:
        if wordPitch[-1] == 2 and wordPitch[0] == 0:
            return 0
        elif wordPitch[0] == 0 and len(wordPitch) == 1:
            return 0
    raise IndexError("Err: Invalid pitch accent parsed.")
        