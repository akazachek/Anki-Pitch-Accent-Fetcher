from aqt import mw
import navCollection
from navOJAD import searchWords
import navOJAD

colName = "collectionCopy.anki2"
deckName = "Core 2k/6k Optimized Japanese Vocabulary"

def isolateWords(cards):
    words = []
    for i in range(len(cards)):
        words.append(cards[i][1])
    return words

validDeck = False

while not validDeck:
    try:
        cards = navCollection.getCards(colName, deckName)
        validDeck = True
    except KeyError as e:
        print(e)

navOJAD.searchWords(isolateWords(cards))
        