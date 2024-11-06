from flask import Flask, jsonify, request
from repositories.mtg_repository import MTGRepository
from repositories.collection_repository import CollectionRepository
from models.card import Card

app = Flask(__name__)

mtg_repo = MTGRepository()
collection_repo = CollectionRepository()

@app.route("/card/list", methods=['GET'], strict_slashes=False)
@app.route("/card/list/<page>", methods=['GET'], strict_slashes=False)
def get_all_cards(page=1):
    cards = mtg_repo.get_cards(page)
    return jsonify([{
        "id": card.id,
        "name": card.name,
        "imageUrl": card.image_url,
        "set": card.set
    } for card in cards])

@app.route("/card/search/<name>", methods=['GET'], strict_slashes=False)
def search_by_name(name):
    """
    Search for a Magic: The Gathering card by its name.

    Args:
        name (str): The name of the card to search for.

    Returns:
        Response: A JSON response containing the card details if found,
                  or an error message if the card is not found. The response
                  includes the card's id, name, imageUrl, and set.
    """
    card = mtg_repo.get_card_by_name(name)
    if card is not None:
        return jsonify({
            "id": card.id,
            "name": card.name,
            "imageUrl": card.image_url,
            "set": card.set
        })
    else:
        return jsonify({"error": "Card not found"}), 404

@app.route("/card/add", methods=['POST'], strict_slashes=False)
def add_card_to_collection():
    """
    Adds a card to the collection.

    This function retrieves card data from the JSON request body, creates a Card object,
    and adds it to the collection repository. It returns a JSON response indicating
    that the card has been successfully added to the collection.

    example request body:
    {
        "id": 1,
        "name": "Black Lotus",
        "imageUrl": "http://example.com/black_lotus.jpg",
        "set": "Alpha"
    }

    Returns:
        Response: A JSON response with a message indicating the card was added and
                  an HTTP status code 201 (Created).
    """
    card = Card(**request.json)
    collection_repo.add_card(card)
    return jsonify({"message": "Card added to collection"}), 201

@app.route("/card/collection", methods=['GET'], strict_slashes=False)
def list_collection():
    cards = collection_repo.get_cards()
    return jsonify([{
        "id": card.id,
        "name": card.name,
        "imageUrl": card.image_url,
        "set": card.set
    } for card in cards])

@app.route("/card/delete/<id>", methods=['DELETE'], strict_slashes=False)
def delete_card_from_collection(id):
    """

    Deletes a card from the collection

    Args:
        id (str): the id of the card to delete
    """
    try:
        collection_repo.delete_card(id)
        return jsonify({"message": "Card with ID '{}' deleted successfully".format(id)}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(port=5000)
