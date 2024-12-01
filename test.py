from flask import Flask, jsonify, request

app = Flask(__name__)

# Mock database
data = {
    "items": []
}

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the API!"})

@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(data["items"])

@app.route('/items', methods=['POST'])
def add_item():
    item = request.json.get('item')
    if not item:
        return jsonify({"error": "Item is required"}), 400
    data["items"].append(item)
    return jsonify({"message": "Item added", "item": item}), 201

@app.route('/items/<int:index>', methods=['DELETE'])
def delete_item(index):
    try:
        removed_item = data["items"].pop(index)
        return jsonify({"message": "Item deleted", "item": removed_item})
    except IndexError:
        return jsonify({"error": "Index out of range"}), 404

if __name__ == '__main__':
    app.run(debug=True)
