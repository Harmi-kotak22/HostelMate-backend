from flask import Flask, request
import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# 🔹 Initialize Firebase Admin SDK using env variable
firebase_json = os.environ.get("FIREBASE_KEY")
if not firebase_json:
    raise Exception("FIREBASE_KEY environment variable not set!")

cred = credentials.Certificate(json.loads(firebase_json))
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route("/")
def home():
    return "✅ Gatepass Approval Server is running!"

@app.route("/approve")
def approve():
    gatepass_id = request.args.get("gatepassId")
    if not gatepass_id:
        return "❌ Missing gatepassId", 400

    try:
        db.collection("Gatepass").document(gatepass_id).update({"parentApproval": "Approved"})
        return f"✅ Gatepass {gatepass_id} approved successfully!"
    except Exception as e:
        return f"❌ Error updating Firestore: {str(e)}", 500

@app.route("/decline")
def decline():
    gatepass_id = request.args.get("gatepassId")
    if not gatepass_id:
        return "❌ Missing gatepassId", 400

    try:
        db.collection("Gatepass").document(gatepass_id).update({"parentApproval": "Declined"})
        return f"❌ Gatepass {gatepass_id} declined successfully!"
    except Exception as e:
        return f"❌ Error updating Firestore: {str(e)}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
