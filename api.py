## API By Rajeen Kaleerathan  ##

## Imported ##
from flask import Flask, request, jsonify, Response
from RandomDataGenerator import generate_data
import json

####################

app = Flask(__name__)

## In-memory schema storage ##
schemas = {}

####################

@app.route("/")
def home():
    return jsonify({"message": "Random Data Generator API is running."})

####################

## POST /schemas - Create and store a schema in memory ##
@app.route("/schemas", methods=["POST"])
def create_schema():
    data = request.get_json()
    name = data.get("name")
    fields = data.get("fields")
    count = data.get("count")

    if not all([name, isinstance(fields, dict), isinstance(count, int)]):
        return jsonify({
            "error": "Invalid input. Must include 'name', 'fields' (dict), and 'count' (int)."
        }), 400

    schemas[name] = {
        "fields": fields,
        "count": count
    }

    return jsonify({
        "message": f"Schema '{name}' created successfully."
    }), 201

####################

## GET /schemas/<name>/data - Generate data using saved schema ##
@app.route("/schemas/<name>/data", methods=["GET"])
def get_schema_data(name):
    schema = schemas.get(name)

    if not schema:
        return jsonify({"error": f"Schema '{name}' not found."}), 404

    ## Pass raw fields (which map field → data_type) to the generator
    data = generate_data(schema["fields"], schema["count"])

    accept_header = request.headers.get("Accept", "application/json").lower()

    if "application/x-ndjson" in accept_header:
        ndjson_output = "\n".join(json.dumps(record) for record in data)
        return Response(ndjson_output, mimetype="application/x-ndjson")

    return jsonify(data)

####################

## GET /schemas - List all schema names ##
@app.route("/schemas", methods=["GET"])
def list_schemas():
    return jsonify(list(schemas.keys()))

####################

if __name__ == "__main__":
    app.run(debug=True)
