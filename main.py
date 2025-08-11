import pyperclip
from flask import Flask, render_template, request, session
from services.scryfall_api import search_cards, get_info, get_card_name
from models.deck import Deck
from sqlalchemy import Integer, String, select
from sqlalchemy.dialects.postgresql import insert
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from dotenv import load_dotenv
import os

load_dotenv()

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__, template_folder='./templates')
app.secret_key = os.getenv("COOKIE_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
# flask --app main run
db.init_app(app)

class DeckDB(db.Model):
    __tablename__ = "deck_db"
    # will eventually be used to id decks in case of multiple saved decks under 1 account.
    # id: Mapped[int] = mapped_column(primary_key=True)
    card_name: Mapped[str] = mapped_column(primary_key=True)
    card_count: Mapped[int]
    
    def __repr__(self):
        return f"{self.card_name}|{self.card_count}"

with app.app_context():
    db.create_all()
    
def get_deck():
    deck = {}
    for row in db.session.execute(db.select(DeckDB)):
        str_count = 0
        c_name = ''
        string = str(row[0])
        for i in range(len(string)):
            if string[i] != '|':
                str_count += 1
            else:
                c_name = string[:str_count]
        c_count = string[str_count:]
        deck[c_name] = int(c_count)
    return deck

@app.route("/")
def index():
    session.clear()
    return render_template('index.html', deck={}, cards={}, info="", deck_build = False)

@app.route("/search-card", methods=["GET", "POST"])
def get_cards():
    card = request.form["card"]
    output = search_cards(card)
    session["cards"] = output
    if "deck_build" in session:
        deck = get_deck()
        return render_template('deck.html', deck=deck, cards=output, info="", deck_build = True)
    else:
        return render_template('index.html', deck={}, cards=output, info="", deck_build = False)

@app.route("/card-info/<card_id>", methods=["GET", "POST"])
def card_info(card_id):
    info = get_info(card_id)
    return render_template('index.html', deck={}, info=info, cards={}, deck_build = False)

@app.route("/build-deck", methods=["POST"])
def build_deck():
    deck = get_deck()
    session['deck_build'] = "Yes"
    return render_template('deck.html', deck=deck, info="", cards={}, deck_build=True)

@app.route("/add_to_deck/<card_id>", methods=["GET","POST"])
def add_to_deck(card_id):
    card_name = get_card_name(card_id)
    stmt = insert(DeckDB).values(card_name=card_name, card_count=1)
    stmt = stmt.on_conflict_do_update(
        index_elements=["card_name"],
        set_=dict(card_count=DeckDB.card_count + 1)
    )
    db.session.execute(stmt)
    db.session.commit()
    deck = get_deck()
    
    return render_template('deck.html', deck=deck, info="", cards=session["cards"], deck_build = True)

@app.route("/export-deck", methods=["GET"])
def export_deck():
    # deck = session['deck']
    deck = get_deck()
    deck_export = ""
    for card, count in deck.items():
        deck_export += (str(count) + " " + card + "\n")
    pyperclip.copy(deck_export)
    return render_template('deck.html', deck=deck, info="", cards=session['cards'], deck_build=True)

if __name__ == "__main__":
    app.debug() == True
    app.run()