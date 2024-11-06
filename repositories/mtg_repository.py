import requests
from models.card import Card

class MTGRepository:
    BaseURL = "https://api.magicthegathering.io/v1/cards"

    def get_cards(self, page=1) -> list[Card]:
        url = f"{self.BaseURL}?page={page}"
        response = requests.get(url)
        if response.status_code == 200:
            cards = [Card(**card) for card in response.json()["cards"]]
            return cards

    def get_card_by_name(self, name):
        url = f"{self.BaseURL}?name={name}"
        response = requests.get(url)
        if response.status_code == 200:
            card = Card(**response.json()["cards"][0])
            return card
        return None

    def delete_card(self, id):
        query = "DELETE FROM cards WHERE id =?"
        self.cursor.execute(query, (id,))
        affected_rows = self.cursor.rowcount
        if affected_rows == 0:
            raise ValueError("No card found with ID '{}'".format(id))
        self.conn.commit()
