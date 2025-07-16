from flask import Flask, request, jsonify
from RandomDataGenerator import (
    load_schemas,
    save_schema,
    generate_data,
    data_fields
)

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"Message": "Random Data Generator API is running."})

## ENDPOINT 1 - POST /schemas - Create a new Schema ##
#app.route("/schemas", methods=["POST"])
#def create_schema():
#    data = request.get_json()
#    name = data.get("name")
#    fields = data.get("fields")
#    count = data.get("count")

#    if name and isinstance(fields, list) and isinstance(count, int):
#        save_schema(name, fields, count)
#        return jsonify({"Message": f"Schema '{name}' has been created successfully!"})
#    return jsonify({"Error": "Invalid request format."}), 400

## ENDPOINT 2 - GET /schemas/<name>/data - Generates and returns fake data from the chosen schema ##
@app.route("/schemas/<name>/data", methods=["GET"])
def get_schema_data(name):
    schemas = load_schemas()
    schema = schemas.get(name)
    if not schema:
        return jsonify({"Error": f"Schema '{name}' can't be found!"}), 404

    data = generate_data(schema["fields"], schema["count"])
    return jsonify(data)

## ENDPOINT 3 - GET /schemas - List all schemas ##
@app.route("/schemas", methods=["GET"])
def list_schemas():
    return jsonify(load_schemas())

if __name__ == "__main__":
    app.run()
