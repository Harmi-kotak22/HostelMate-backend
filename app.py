from flask import Flask, request, render_template_string
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

app = Flask(__name__)

# 🔹 Initialize Firebase Admin SDK using environment variable
firebase_json = os.environ.get("FIREBASE_KEY")  # set this in Render Environment Variables
if not firebase_json:
    raise Exception("FIREBASE_KEY environment variable not set!")

cred_dict = json.loads(firebase_json)
cred = credentials.Certificate(cred_dict)
firebase_admin.initialize_app(cred)
db = firestore.client()

# 🔹 HTML template for success/failure page
SUCCESS_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Gatepass Status</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f5f5f5; display: flex; justify-content: center; align-items: center; height: 100vh; }
        .container { text-align: center; background: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
        .approved { color: #4CAF50; font-size: 24px; font-weight: bold; }
        .declined { color: #F44336; font-size: 24px; font-weight: bold; }
        p { font-size: 16px; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="{{ status_class }}">{{ message }}</div>
        <p>Thank you for using HostelMate.</p>
    </div>
</body>
</html>
"""

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
        return render_template_string(SUCCESS_PAGE, message=f"Gatepass {gatepass_id} Approved ✅", status_class="approved")
    except Exception as e:
        return render_template_string(SUCCESS_PAGE, message=f"Error: {str(e)}", status_class="declined"), 500

@app.route("/decline")
def decline():
    gatepass_id = request.args.get("gatepassId")
    if not gatepass_id:
        return "❌ Missing gatepassId", 400

    try:
        db.collection("Gatepass").document(gatepass_id).update({"parentApproval": "Declined"})
        return render_template_string(SUCCESS_PAGE, message=f"Gatepass {gatepass_id} Declined ❌", status_class="declined")
    except Exception as e:
        return render_template_string(SUCCESS_PAGE, message=f"Error: {str(e)}", status_class="declined"), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
