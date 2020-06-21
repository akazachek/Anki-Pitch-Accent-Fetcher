from anki import Collection
from aqt import mw
import json

col = Collection("collectionCopy.anki2")
deckName = "Core 2k/6k Optimized Japanese Vocabulary"

decks = col.db.scalar("SELECT decks FROM col")
cards = col.db.all("SELECT nid,did FROM cards")
notes = col.db.all("SELECT id,sfld FROM notes")
fetchedNoteIDs = []
fetchedCards = []
decksJSON = json.loads(decks)
deckID = -1

# multidim dict navigation
for deck in decksJSON:
    deckInfo = decksJSON[deck]
    if deckInfo["name"] == deckName:
        deckID = deckInfo["id"]      
        
# creates list of relevant note IDs
for i in range(len(cards)):
        if cards[i][1] == deckID:
            fetchedNoteIDs.append(cards[i][0])

# creates list of cards corresponding to each note ID, as well as their search field
# in this case, search field is the word
for ID in fetchedNoteIDs:
    cardID = col.findCards("nid:" + str(ID))[0]
    noteSFLD = -1
    for i in range(len(notes)):
        if notes[i][0] == ID:
            noteSFLD = notes[i][1]
    fetchedCards.append([cardID, noteSFLD])

print(fetchedCards)

