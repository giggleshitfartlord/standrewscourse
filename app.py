from flask import Flask, render_template, url_for, send_from_directory, redirect
from datetime import datetime
import os
import stripe
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, static_folder='static', static_url_path='/static')

# Get Stripe API key from environment variable
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

# Validate Stripe configuration
if not stripe.api_key:
    print("Warning: Stripe API key not found in environment variables")

@app.context_processor
def inject_year():
    return {'year': datetime.now().year}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/hole/<int:hole_number>')
def hole(hole_number):
    if 1 <= hole_number <= 18:
        return render_template(f'holes/hole_{hole_number}.html')
    return "Hole not found", 404

@app.route('/history')
def history():
    return render_template('history.html')

@app.route('/tips')
def tips():
    return render_template('tips.html')

@app.route('/resources')
def resources():
    return render_template('resources.html')

@app.route('/ads.txt')
def ads_txt():
    return send_from_directory('static', 'ads.txt')

@app.route('/donate')
def donate():
    stripe_public_key = os.getenv('STRIPE_PUBLISHABLE_KEY')
    return render_template('donate.html', stripe_public_key=stripe_public_key)

@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    if not stripe.api_key:
        return "Stripe is not configured. Donations are temporarily unavailable.", 503
    
    try:
        checkout_session = stripe.checkout.Session.create(            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': 800,  # $8.00
                        'product_data': {
                            'name': 'Coffee & Snack Donation',
                            'description': 'Your kind support helps keep Old Course Caddie free for golfers worldwide. While entirely voluntary, your generosity means the world! ⛳️',
                        },
                    },
                    'quantity': 1,
                },
            ],            mode='payment',
            success_url=url_for('thank_you', _external=True),
            cancel_url=url_for('donate', _external=True),
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)

if __name__ == '__main__':
    app.run(debug=True)