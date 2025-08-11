import pyperclip

class Deck():
    
    def __init__(self):
        self.deck = {}
        # self.deck_type = deck_type
        
    # def create_deck(self, deck_name, deck_type):
    #     pass
    
    # def save_deck(self, deck, deck_type):
    #     pass
    
    def add_card(self, card):
        if card not in self.deck:
            self.deck[card] = 0
        self.deck[card] += 1
        return
    
    def remove_card(self, card):
        pass
    
    def export_deck_to_clipboard(self, curr_deck):
        deck_export = ""
        for card, count in curr_deck.items():
            deck_export += (str(count) + " " + card)
        pyperclip.copy(deck_export)
        return