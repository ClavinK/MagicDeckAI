import pyperclip
from flask import Flask, render_template, request, session
from services.scryfall_api import search_cards, get_info, get_card_name
from models.deck import Deck

app = Flask(__name__, template_folder='./templates')
# flask --app main run

app.secret_key = "30422eb857c6fed8e2f5199605763db507403262f591dc4c58768200fe8045f6"

# Interface
@app.route("/")
def index():
    session.clear()
    return render_template('index.html', deck={}, cards={}, info="", deck_build = False)

@app.route("/search-card", methods=["GET", "POST"])
def get_cards():
    card = request.form["card"]
    output = search_cards(card)
    session["cards"] = output
    print(session)
    if "deck_build" in session:
        # here session deck might not work in return statement if it doesnt already exist...
        return render_template('deck.html', deck=session["deck"], cards=output, info="", deck_build = True)
    else:
        return render_template('index.html', deck={}, cards=session["cards"], info="", deck_build = False)

@app.route("/card-info/<card_id>", methods=["GET", "POST"])
def card_info(card_id):
    info = get_info(card_id)
    return render_template('index.html', info=info, deck={}, cards={}, deck_build = False)

@app.route("/build-deck", methods=["POST"])
def build_deck():
    deck = Deck()
    session['deck'] = deck.deck
    session['deck_build'] = "Yes"
    return render_template('deck.html', info="", deck=deck.deck, cards={}, deck_build=True)

@app.route("/add_to_deck/<card_id>", methods=["GET","POST"])
def add_to_deck(card_id):
    deck = session['deck']
    card_name = get_card_name(card_id)
    if card_name not in deck:
        deck[card_name] = 0
    deck[card_name] += 1
    session['deck'] = deck
    print(session)
    return render_template('deck.html', info="", cards=session["cards"], deck=deck, deck_build = True)

@app.route("/export-deck", methods=["GET"])
def export_deck():
    deck = session['deck']
    deck_export = ""
    for card, count in deck.items():
        deck_export += (str(count) + " " + card + "\n")
    pyperclip.copy(deck_export)
    return render_template('deck.html', info="", cards=session['cards'], deck=deck, deck_build=True)

if __name__ == "__main__":
    app.debug() == True
    app.run()