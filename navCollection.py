import json

def getCards(col, deckName):
    
    decks = col.db.scalar("SELECT decks FROM col")
    cards = col.db.all("SELECT nid,did FROM cards")

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
            noteWord = "N/A"
            note = col.getCard(cardID).note()
            note.load()
            # hardcoded for my deck, will return the card's word in kanji
            key = "Vocabulary-Kanji"
            noteWord = note.__getitem__(key)
            fetchedCards.append([cardID, noteWord])
        except OverflowError:
            pass
        
    return fetchedCards
