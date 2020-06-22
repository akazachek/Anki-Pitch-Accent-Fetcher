from aqt import mw
import navCollection
from navOJAD import searchWord
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

colName = "collectionCopy.anki2"
deckName = "Core 2k/6k Optimized Japanese Vocabulary"

validDeck = False

while not validDeck:
    try:
        # format -- list of [anki card ID, associated word]
        cards = navCollection.getCards(colName, deckName)
        validDeck = True
    except KeyError as e:
        print(e)

chromeOpts = Options()
chromeOpts.headless = True
browser = Chrome(executable_path="C:\\Program Files (x86)\\Google\\ChromeDriver\\chromedriver.exe", options=chromeOpts)

for wordInd in range(len(cards)):
    try:
        pitchAccent = searchWord(browser, cards[wordInd][1])
        cards[wordInd].append(pitchAccent)
    except (KeyError, IndexError) as e:
        cards[wordInd].append(str(e))
        print(cards[wordInd][1] + " threw an exception:")
        print(str(e))