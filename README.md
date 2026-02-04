# PokePricer

Pokemon Card Price Comparison Tool - **Now with Web Interface!** 🌐

Get real-time pricing from multiple sources including eBay and TCGPlayer through an easy-to-use web interface or command-line tool.

## ✨ Features

- **🌐 Web Interface**: Beautiful, responsive web UI for easy searching
- **💻 CLI Version**: Command-line interface for power users
- **🛒 eBay Integration**: Fetches the top 5 last completed and sold items to calculate average price
- **🎯 TCGPlayer Web Scraping**: Uses manual crawl algorithm to extract pricing data
- **🔒 Secure API Key Handling**: eBay API keys are hashed and never exposed in public
- **🌍 Multi-language Support**: Search for cards in different languages (English, Japanese, French, etc.)
- **📊 Condition-based Pricing**: Get accurate prices based on card condition (Mint, Near Mint, Played, etc.)
- **📈 Price Aggregation**: Combines data from multiple sources for comprehensive pricing

## 🚀 Quick Start

### Web Version (Recommended)

1. **Clone and install:**
```bash
git clone https://github.com/jvissup/PokePricer.git
cd PokePricer
pip install -r requirements.txt
```

2. **Run the web server:**
```bash
python app.py
```

3. **Open your browser:**
```
http://localhost:5000
```

That's it! Start searching for Pokemon cards in your browser! 🎉

### Command-Line Version

```bash
python pokepicer.py
```

## 📸 Screenshots

The web interface features:
- Clean, modern design with Pokemon-themed colors
- Responsive layout that works on desktop and mobile
- Real-time search results with price breakdowns
- Source-by-source pricing comparison
- Average price calculation with price ranges

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/jvissup/PokePricer.git
cd PokePricer
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Set up your eBay API credentials:
   - Go to [eBay Developers Program](https://developer.ebay.com/)
   - Create an application to get your App ID
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` and add your credentials:
     ```
     EBAY_APP_ID=your_actual_app_id
     EBAY_CERT_ID=your_actual_cert_id
     ```

## 📖 Usage

### Web Interface

1. Start the server:
   ```bash
   python app.py
   ```

2. Open http://localhost:5000 in your browser

3. Enter your search:
   - **Pokemon Card Name**: e.g., "Charizard VMAX", "Pikachu V"
   - **Language**: Select from dropdown (default: English)
   - **Condition**: Select card condition (default: Near Mint)

4. Click "Search Prices" and view results!

### Command Line Interface

Run the CLI version:
```bash
python pokepicer.py
```

The tool will prompt you for:
1. **Pokemon Card Name**: e.g., "Charizard VMAX", "Pikachu V"
2. **Language**: The language of the card (default: English)
3. **Condition**: The condition of the card (default: Near Mint)

### Example Results

```
============================================================
PRICING SUMMARY
============================================================
Card: Charizard VMAX
Language: English
Condition: Near Mint
============================================================

SOURCE BREAKDOWN:
------------------------------------------------------------
eBay                 $   45.67 USD
                     (Based on 5 sold items)
TCGPlayer            $   48.99 USD
------------------------------------------------------------

OVERALL AVERAGE:     $   47.33 USD
PRICE RANGE:         $45.67 - $48.99
```

## Supported Conditions

- **Mint/New**: Brand new, never played
- **Near Mint**: Excellent condition with minimal wear
- **Excellent**: Light play with slight edge wear
- **Good/Used**: Moderate play, visible wear
- **Light Played**: Some play, noticeable wear
- **Played**: Heavy play, significant wear
- **Poor**: Damaged, heavy wear

## Supported Languages

- English
- Japanese
- French
- German
- Spanish
- Italian
- Portuguese
- And more...

## Architecture

The tool consists of multiple components:

### Web Application (`app.py`)
- Flask-based web server
- RESTful API endpoint for searching
- Serves static HTML/CSS/JS files
- **Run with:** `python app.py`
- **Access at:** http://localhost:5000

### Frontend (HTML/CSS/JS)
- Modern, responsive web interface
- Real-time search with loading states
- Beautiful Pokemon-themed design
- Mobile-friendly layout

### Backend Modules

### 1. `ebay_pricer.py`
- Connects to eBay Finding API
- Searches for completed and sold items
- Extracts prices from the top 5 sold listings
- Calculates average price
- **Security**: API keys are hashed using SHA256

### 2. `tcgplayer_pricer.py`
- Web scraping implementation for TCGPlayer
- Manual crawl algorithm to extract pricing
- Parses market price, low price, and high price
- Handles different page structures

### 3. `pokepicer.py`
- Main application entry point
- User interface for card search
- Aggregates data from all sources
- Displays formatted results

## Security Notes

- eBay API credentials are stored in `.env` file (not committed to repository)
- API keys are hashed using SHA256 for additional security
- Never commit your `.env` file or expose your API keys publicly
- The `.gitignore` file is configured to exclude sensitive files

## API Rate Limits

- **eBay**: Be aware of eBay's API rate limits for the Finding API
- **TCGPlayer**: Web scraping should be done responsibly with appropriate delays

## Troubleshooting

### No eBay results
- Check your API credentials in `.env`
- Ensure your eBay App ID is valid and active
- Check your internet connection
- Try a different card name or spelling

### No TCGPlayer results
- TCGPlayer's website structure may change
- Check your internet connection
- Try using the exact card name as shown on TCGPlayer

### Import errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Use Python 3.7 or higher

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Disclaimer

This tool is for educational and personal use only. Please respect the terms of service of eBay and TCGPlayer when using this tool. Web scraping should be done responsibly and in accordance with each website's robots.txt and terms of service.
