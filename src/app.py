import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Creamos la familia
jackson_family = FamilyStructure("Jackson")

# Metemos miembros iniciales (como pide el ejercicio)
try:
    jackson_family.add_member({"first_name": "John", "age": 33, "lucky_numbers": [7, 13, 22]})
    jackson_family.add_member({"first_name": "Jane", "age": 35, "lucky_numbers": [10, 14, 3]})
    jackson_family.add_member({"first_name": "Jimmy", "age": 5, "lucky_numbers": [1]})
except Exception:
    # por si el server se recarga y ya estaban
    pass


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.route('/')
def sitemap():
    return generate_sitemap(app)


# 1) GET /members -> devuelve lista de miembros
@app.route('/members', methods=['GET'])
def get_all_members():
    try:
        return jsonify(jackson_family.get_all_members()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 2) GET /members/<id> -> devuelve un miembro
@app.route('/members/<int:member_id>', methods=['GET'])
def get_one_member(member_id):
    try:
        member = jackson_family.get_member(member_id)
        if member is None:
            return jsonify({"error": "Member not found"}), 404
        return jsonify(member), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 3) POST /members -> crea un miembro
@app.route('/members', methods=['POST'])
def create_member():
    try:
        body = request.get_json(silent=True)
        if body is None:
            return jsonify({"error": "Request body must be JSON"}), 400

        # Validación mínima de campos
        if "first_name" not in body or "age" not in body or "lucky_numbers" not in body:
            return jsonify({"error": "Missing fields: first_name, age, lucky_numbers"}), 400

        new_member = jackson_family.add_member(body)
        return jsonify(new_member), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 4) DELETE /members/<id> -> borra un miembro
@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    try:
        deleted = jackson_family.delete_member(member_id)
        if not deleted:
            return jsonify({"error": "Member not found"}), 404
        return jsonify({"done": True}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)