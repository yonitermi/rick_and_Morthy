import requests
import csv
from flask import Flask, jsonify

app = Flask(__name__)

def get_characters():
    url = "https://rickandmortyapi.com/api/character"
    params = {
        "species": "Human",
        "status": "Alive",
        "origin": "Earth"
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data["results"]

def write_to_csv(characters):
    fieldnames = ["Name", "Location", "Image"]
    filename = "rick_and_morty_characters.csv"
    with open(filename, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for character in characters:
            writer.writerow({
                "Name": character["name"],
                "Location": character["location"]["name"],
                "Image": character["image"]
            })
    return filename

@app.route("/characters", methods=["GET"])
def get_characters_endpoint():
    characters = get_characters()
    return jsonify(characters)

@app.route("/healthcheck", methods=["GET"])
def healthcheck():
    return "Service is healthy"

if __name__ == "__main__":
    characters = get_characters()
    write_to_csv(characters)
    app.run(debug=True, host="0.0.0.0", port=5000)

