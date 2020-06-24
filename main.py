import navCollection
from navOJAD import searchWord
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

colPath = "C:\\Users\\Alex\\AppData\\Roaming\\Anki2\\User 1\\collection.anki2"
deckName = "Core 2k/6k Optimized Japanese Vocabulary"
searchKey = "Vocabulary-Kanji"
modKey = "Vocabulary-Kana"

def getBinaryInput(question):
    while(True):
        inp = input(question + " (Y/N) ")
        if inp == "Y" or inp == "y":
            return False
        elif inp == "N" or inp == "n":
            return True
        else:
            print("Input not recognized.")
            
def progressBar(current, total, charLength):
    prcnt = float(current) * 100 / total
    arrow = "-" * int(prcnt/100 * charLength - 1) + ">"
    spaces = " " * (charLength - len(arrow))
    print("\r[%s%s] %d %% (%d/%d)" % (arrow, spaces, prcnt, current, total), end="")
            
print("Please ensure you have a backup. No changes made here are reversible.")
print("------")
debug = False
if not getBinaryInput("Would you like to see debug output?"):
    debug = True
print()

print("Default Collection Path: " + colPath)
if not getBinaryInput("Does the path need to be changed?"):
    colPath = input("Enter a new collection path: ")
col = navCollection.openCollection(colPath)
print()

print("Default Deck Name: " + deckName)
if not getBinaryInput("Does the deck need to be changed?"):
    deckName = input("Enter a deck name: ")
deckID = navCollection.getDeckID(col, deckName)
print()

print("Default Search Field Name: " + searchKey)
if not getBinaryInput("Does this field need to be changed?"):
    searchKey = input("Enter a field name: ")

# format -- list of [anki card ID, associated word]
while(True):
    try:
        print("Loading collection...")
        cards = navCollection.getCards(col, deckID, searchKey)
        break
    except KeyError:
        searchKey = input("Invalid field name given. Please enter a new one: ")
print()

inp = input("How many cards would you like to search? Enter 'All' to search all cards. ")
if inp == "All" or inp == "all":
    numCards = len(cards)
else:
    numCards = int(inp)

if debug:
    keyEWords = []
    indEWords = []

print("Starting browser...")
chromeOpts = Options()
chromeOpts.headless = True
browser = Chrome(executable_path="C:\\Program Files (x86)\\Google\\ChromeDriver\\chromedriver.exe", options=chromeOpts)
print("Searching words...")
for wordInd in range(numCards):
    try:
        pitchAccent = searchWord(browser, cards[wordInd][1])
        cards[wordInd].append(pitchAccent)
        progressBar(wordInd, numCards, 20)
    except IndexError as e:
        cards[wordInd].append(str(e))
        if debug:
            print("\n" + cards[wordInd][1] + " threw an exception:")
            print(str(e))
            indEWords.append(cards[wordInd][1])
    except KeyError as e:
        cards[wordInd].append(str(e))
        if debug:
            print("\n" + cards[wordInd][1] + " threw an exception:")
            print(str(e))
            keyEWords.append(cards[wordInd][1])
    except OverflowError:
        print("Could not search that many cards. Last card found was number " + wordInd + ".")
        numCards = wordInd
        break
print("\nPitch accent data compiled.")
if debug:
    print("Number of KeyErrors: " + str(len(keyEWords)) + ".")
    print(keyEWords)
    print("Number of IndexErrors: " + str(len(indEWords)) + ".")
    print(indEWords)

browser.close()
print()

done = False
print("Default Modifying Field Name: " + modKey)
if not getBinaryInput("Does this field need to be changed?"):
    modKey = input("Enter a field name: ")
while(done == False):
    for cardInd in range(numCards):
        try:
            navCollection.modifyNote(col.getCard(cards[cardInd][0]), modKey, cards[cardInd][2])
            if debug: print(cards[cardInd][1] + " assigned value of " + str(cards[cardInd][2]))
        except KeyError:
            print("Field not found for card with word " + cards[cardInd][1] + ".")
    print("Cards modified.")
    if not getBinaryInput("Would you like to try again with a different field name? "):
        modKey = input("Enter a field name: ")
    else:
        done = True

col.close()
print("Collection saved.")
print("Please ensure you hold 'Shift' next time you open Anki, and then force a one-way upload to AnkiWeb to preserve the changes.")
quit()