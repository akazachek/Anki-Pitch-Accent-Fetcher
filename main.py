from anki import Collection
import navCollection
from navOJAD import searchWord
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

colName = "collectionCopy.anki2"
deckName = "Core 2k/6k Optimized Japanese Vocabulary"
col = Collection(colName)

# format -- list of [anki card ID, associated word]
cards = navCollection.getCards(col, deckName)
        
numCards = 20

chromeOpts = Options()
chromeOpts.headless = True
browser = Chrome(executable_path="C:\\Program Files (x86)\\Google\\ChromeDriver\\chromedriver.exe", options=chromeOpts)

for wordInd in range(numCards):
    try:
        pitchAccent = searchWord(browser, cards[wordInd][1])
        cards[wordInd].append(pitchAccent)
    except (KeyError, IndexError) as e:
        cards[wordInd].append(str(e))
        print(cards[wordInd][1] + " threw an exception:")
        print(str(e))
        
for cardInd in range(numCards):
    note = col.getCard(cards[cardInd][0]).note()
    note.load()
    # hardcoded for my deck, can be found by looking at note.keys()
    key = "Vocabulary-Kana"
    kanaVocab = note.__getitem__(key) + " (" + str(cards[cardInd][2]) + ")"
    ### will permanently override the current db entry
    # note.__setitem__(key, kanaVocab)
    
        
