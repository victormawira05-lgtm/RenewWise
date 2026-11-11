import re
import os
import json
import uuid as uuid_lib
from datetime import datetime, timezone
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import requests

load_dotenv()

app = Flask(__name__)
CORS(app, origins="*", allow_headers=["Content-Type", "Authorization"], methods=["GET", "POST", "OPTIONS"], supports_credentials=False)

@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
    return response

PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID")
PAYPAL_SECRET = os.getenv("PAYPAL_SECRET")
PAYPAL_BASE = "https://api-m.sandbox.paypal.com"

def uuid():
    return str(uuid_lib.uuid4())

# GLOBAL IN-MEMORY STORE - Fixed for Render
transactions = [
    {"id": uuid(), "date": "2026-11-10", "desc": "Demo balance reset", "merchant":"System", "amount": 10, "type":"Income", "method":"Demo", "sim": False},
    {"id": uuid(), "date": "2026-11-09", "desc": "Upwork Payment - Client John", "merchant":"Upwork", "amount": 150, "type":"Income", "method":"PayPal", "sim": False},
    {"id": uuid(), "date": "2026-11-10", "desc": "Naivas Supermarket", "merchant":"Naivas", "amount": -28, "type":"Expense", "method":"M-Pesa", "sim": True},
    {"id": uuid(), "date": "2026-11-10", "desc": "Safaricom Airtime $5 daily", "merchant":"Safaricom", "amount": -5, "type":"Expense", "method":"M-Pesa", "sim": True},
    {"id": uuid(), "date": "2026-11-09", "desc": "Safaricom Airtime $5 daily", "merchant":"Safaricom", "amount": -5, "type":"Expense", "method":"M-Pesa", "sim": True},
    {"id": uuid(), "date": "2026-11-08", "desc": "Bolt Ride - Westlands", "merchant":"Bolt", "amount": -6.7, "type":"Expense", "method":"M-Pesa", "sim": True},
    {"id": uuid(), "date": "2026-11-07", "desc": "Safaricom Airtime $5 daily", "merchant":"Safaricom", "amount": -5, "type":"Expense", "method":"