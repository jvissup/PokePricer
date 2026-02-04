"""
Pokemon Card Pricing Tool - Web Application
Flask-based web interface for searching Pokemon card prices
"""
from flask import Flask, render_template, request, jsonify
import os
from pokepicer import PokemonCardPricer

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# Initialize the pricer
pricer = PokemonCardPricer()


@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    """Handle search requests and return pricing data."""
    try:
        data = request.get_json()
        
        card_name = data.get('card_name', '').strip()
        language = data.get('language', 'English').strip() or 'English'
        condition = data.get('condition', 'Near Mint').strip() or 'Near Mint'
        
        if not card_name:
            return jsonify({
                'success': False,
                'error': 'Please enter a card name'
            }), 400
        
        # Get pricing data
        results = pricer.get_price(card_name, language, condition)
        
        # Format the response
        response = {
            'success': True,
            'card_name': results['card_name'],
            'language': results['language'],
            'condition': results['condition'],
            'sources': results['sources'],
            'average_price': results.get('average_price'),
            'currency': results.get('currency', 'USD'),
            'price_range': results.get('price_range')
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({'status': 'ok'})


@app.route('/ebay/verification-token', methods=['GET'])
def ebay_verification_token():
    """
    eBay verification token endpoint.
    Required for eBay Marketplace Account Deletion/Closure notifications.
    Returns the verification token from environment variables.
    """
    verification_token = os.getenv('EBAY_VERIFICATION_TOKEN', '')
    
    if not verification_token:
        return jsonify({
            'error': 'Verification token not configured'
        }), 500
    
    return jsonify({
        'verificationToken': verification_token
    })


@app.route('/ebay/marketplace-account-deletion', methods=['POST'])
def ebay_marketplace_account_deletion():
    """
    eBay Marketplace Account Deletion notification endpoint.
    Receives notifications when an eBay user deletes their marketplace account.
    Required for production eBay API access.
    
    Expected payload from eBay:
    {
        "metadata": {
            "topic": "MARKETPLACE_ACCOUNT_DELETION",
            "schemaVersion": "1.0",
            "deprecated": false
        },
        "notification": {
            "notificationId": "...",
            "eventDate": "...",
            "publishDate": "...",
            "publishAttemptCount": 1,
            "data": {
                "username": "...",
                "userId": "...",
                "eiasToken": "..."
            }
        }
    }
    """
    try:
        # Get the notification data
        data = request.get_json(silent=True)
        
        if not data:
            return jsonify({
                'error': 'No data provided'
            }), 400
        
        # Log the notification (in production, you would handle this appropriately)
        # For example, mark the user's data for deletion, remove their information, etc.
        notification = data.get('notification', {})
        user_data = notification.get('data', {})
        
        # Extract user information
        username = user_data.get('username')
        user_id = user_data.get('userId')
        
        # Log the deletion request
        print(f"eBay Marketplace Account Deletion notification received:")
        print(f"  Username: {username}")
        print(f"  User ID: {user_id}")
        print(f"  Event Date: {notification.get('eventDate')}")
        
        # In a production application, you would:
        # 1. Validate the notification authenticity
        # 2. Process the user data deletion
        # 3. Store the notification for compliance
        # 4. Remove or anonymize user data as required
        
        # Return success response
        return jsonify({
            'status': 'success',
            'message': 'Account deletion notification received'
        }), 200
        
    except Exception as e:
        print(f"Error processing marketplace account deletion: {e}")
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500


if __name__ == '__main__':
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║          POKEMON CARD PRICING TOOL - WEB APP           ║
    ║                                                        ║
    ║  Starting web server...                                ║
    ║  Open your browser to: http://localhost:5000           ║
    ╚════════════════════════════════════════════════════════╝
    """)
    
    # Get debug mode from environment (default: False for production)
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Run the Flask app
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
