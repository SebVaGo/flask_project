from flask import Blueprint, jsonify
from app.config import db
from app.models.test_model import Test

test_bp = Blueprint("test", __name__)

@test_bp.route("/test-db", methods=["GET"])
def test_db():
    try:
        test_entry = Test(name="Prueba desde Flask")
        db.session.add(test_entry)
        db.session.commit()
        return jsonify({"message": "Conexión exitosa y datos insertados"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
