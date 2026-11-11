from flask import Flask, jsonify
from flask_cors import CORS
import uuid
app = Flask(__name__)
CORS(app, origins="*")
def uid(): return str(uuid.uuid4())
transactions = [
 {"id": uid(), "date": "2026-11-10", "desc": "Demo reset", "merchant": "System", "amount": 10, "type": "Income", "method": "Demo", "sim": False},
 {"id": uid(), "date": "2026-11-09", "desc": "Upwork", "merchant": "Upwork", "amount": 150, "type": "Income", "method": "PayPal", "sim": False},
 {"id": uid(), "date": "2026-11-10", "desc": "Naivas", "merchant": "Naivas", "amount": -28, "type": "Expense", "method": "M-Pesa", "sim": True},
 {"id": uid(), "date": "2026-11-10", "desc": "Airtime", "merchant": "Safaricom", "amount": -5, "type": "Expense", "method": "M-Pesa", "sim": True},
 {"id": uid(), "date": "2026-11-09", "desc": "Airtime", "merchant": "Safaricom", "amount": -5, "type": "Expense", "method": "M-Pesa", "sim": True},
 {"id": uid(), "date": "2026-11-08", "desc": "Bolt", "merchant": "Bolt", "amount": -6.7, "type": "Expense", "method": "M-Pesa", "sim": True},
 {"id": uid(), "date": "2026-11-07", "desc": "Airtime", "merchant": "Safaricom", "amount": -5, "type": "Expense", "method": "M-Pesa", "sim": True},
]
@app.route("/api/transactions", methods=["GET"])
def get_tx():
 inc = sum(t["amount"] for t in transactions if t["amount"]>0)
 spent = abs(sum(t["amount"] for t in transactions if t["amount"]<0))
 return jsonify({"transactions": transactions, "summary": {"income": inc, "spent": spent, "net": inc-spent}})
@app.route("/api/reset", methods=["POST"])
def reset():
 global transactions
 transactions = transactions[:]
 return jsonify({"message": "Reset OK 160"})
@app.route("/", methods=["GET"])
def home(): return jsonify({"message": "PesaAI Running", "count": len(transactions)})
@app.route("/health", methods=["GET"])
def health(): return jsonify({"status": "ok"})