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


if __name__ == '__main__':
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║          POKEMON CARD PRICING TOOL - WEB APP           ║
    ║                                                        ║
    ║  Starting web server...                                ║
    ║  Open your browser to: http://localhost:5000           ║
    ╚════════════════════════════════════════════════════════╝
    """)
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
