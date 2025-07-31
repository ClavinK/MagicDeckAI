import requests

def search_cards(card):
    url = f"https://api.scryfall.com/cards/search?q={card.replace(' ', '+')}"
    response = requests.get(url)
    data = response.json()
    # JSON data is in a dictionary so call on data key first
    card_data = data['data']
    if response.status_code == 500:
        print("Ooops")
        return None
    else:
        # first bracket is the specific card, second bracket is the a specific detail for that card
        display = {}
        for i in range(len(card_data)):
            try:
                image = card_data[i]["image_uris"]["small"]
            except KeyError:
                image = card_data[i]["card_faces"][0]["image_uris"]["small"]
                # image2 = card_data[i]["card_faces"][1]["image_uris"]["normal"]
            display[card_data[i]["id"]] = {"name": card_data[i]["name"], "image_url": image}
        return display
    
def get_info(card_id):
    print(card_id)
    url = f"https://api.scryfall.com/cards/{card_id.replace(' ', '+')}"
    response = requests.get(url)
    data = response.json()
    return data
    
def get_card_name(card_id):
    url = f"https://api.scryfall.com/cards/{card_id.replace(' ', '+')}"
    response = requests.get(url)
    data = response.json()
    return data["name"]


def search_decks():
    pass
