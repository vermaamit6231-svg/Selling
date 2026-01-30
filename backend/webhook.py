from flask import Flask, request
import hmac, hashlib
from config import RAZORPAY_WEBHOOK_SECRET
from database.models import User, Order, db

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def razorpay_webhook():
    payload = request.data
    received_sig = request.headers.get("X-Razorpay-Signature")

    generated_sig = hmac.new(
        RAZORPAY_WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()

    if generated_sig == received_sig:
        data = request.json
        amount = data["payload"]["payment"]["entity"]["amount"] / 100

        order = db.query(Order).filter_by(status="PENDING").first()
        if order:
            order.status = "PAID"
            user = db.query(User).filter_by(user_id=order.user_id).first()
            user.balance += amount
            db.commit()

        return "OK", 200

    return "Invalid", 400

if __name__ == "__main__":
    app.run(port=5000)
