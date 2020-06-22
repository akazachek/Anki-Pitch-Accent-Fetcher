from anki import Collection
import json

def getCards(colName, deckName):
    
    col = Collection(colName)
    decks = col.db.scalar("SELECT decks FROM col")
    cards = col.db.all("SELECT nid,did FROM cards")
    notes = col.db.all("SELECT id,sfld FROM notes")

    fetchedNoteIDs = []
    fetchedCards = []
    
    decksDict = json.loads(decks)
    deckID = ""
    for deck in decksDict:
        deckInfo = decksDict[deck]
        if deckInfo["name"] == deckName: deckID = deckInfo["id"] 
    if deckID == "": raise KeyError("Err: No such deck exists.")
    
    for i in range(len(cards)):
        if cards[i][1] == deckID:
            fetchedNoteIDs.append(cards[i][0])
            
    for ID in fetchedNoteIDs:
        try:
            # should be exactly one matching card
            cardID = col.findCards("nid:" + str(ID))[0]
            noteSFLD = "N/A"
            for i in range(len(notes)):
                if notes[i][0] == ID:
                    noteSFLD = notes[i][1]
                    fetchedCards.append([cardID, noteSFLD])
        except OverflowError:
            pass
        
    return fetchedCards
