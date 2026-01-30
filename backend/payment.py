import razorpay
from config import RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET
from database.models import Order, db

client = razorpay.Client(
    auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET)
)

def create_deposit(user_id, amount):
    order = client.order.create({
        "amount": int(amount * 100),
        "currency": "INR",
        "payment_capture": 1
    })

    new_order = Order(
        user_id=user_id,
        amount=amount,
        status="PENDING"
    )
    db.add(new_order)
    db.commit()

    return order
