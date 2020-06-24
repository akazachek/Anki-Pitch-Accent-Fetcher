import json
from anki import Collection
from anki.rsbackend import DBError
from contextlib import suppress

def openCollection(colPath):
    while(True):
        try: 
            col = Collection(colPath)
            return col
        except DBError:
            print("Collection could not be read. Is Anki running?")
            inp = input("Enter a new collection path, or leave blank to try again.")
            if inp:
                colPath = inp
        except AssertionError:
            colPath = input("Invalid collection file. Please input a new path: ")
                
def getDeckID(col, deckName):
    decks = col.db.scalar("SELECT decks FROM col")
    decksDict = json.loads(decks)
    while(True):
        for deck in decksDict:
            deckInfo = decksDict[deck]
            if deckInfo["name"] == deckName: return deckInfo["id"] 
        deckName = input("Deck name not found. Please enter a new deck name: ")
        
def getCards(col, deckID, searchKey):
    
    cards = col.db.all("SELECT nid,did FROM cards")

    fetchedNoteIDs = []
    fetchedCards = []
    
    for i in range(len(cards)):
        if cards[i][1] == deckID:
            fetchedNoteIDs.append(cards[i][0])
            
    for ID in fetchedNoteIDs:
        # overflow suppressed in case no card is found
        with suppress(OverflowError):
            # should be exactly one matching card
            cardID = col.findCards("nid:" + str(ID))[0]
            note = col.getCard(cardID).note()
            note.load()
            noteWord = note.__getitem__(searchKey)
            fetchedCards.append([cardID, noteWord])
        
    return fetchedCards

def modifyNote(card, key, pitch):
    note = card.note()
    note.load()
    newData = note.__getitem__(key) + " (" + str(pitch) + ")"
    note.__setitem__(key, newData)
    note.flush()
