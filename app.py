from flask import Flask, request
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# 🔹 Initialize Firebase Admin SDK
cred = credentials.Certificate("serviceAccountKey.json")  # Make sure this file is in the same folder
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
        return f"❌ Error: {str(e)}", 500

@app.route("/decline")
def decline():
    gatepass_id = request.args.get("gatepassId")
    if not gatepass_id:
        return "❌ Missing gatepassId", 400

    try:
        db.collection("Gatepass").document(gatepass_id).update({"parentApproval": "Declined"})
        return f"❌ Gatepass {gatepass_id} declined successfully!"
    except Exception as e:
        return f"❌ Error: {str(e)}", 500

if __name__ == "__main__":
    # 🔹 Run server on all interfaces at port 5000
    app.run(host="0.0.0.0", port=5000)
