# PokePricer

Pokemon Card Price Comparison Tool that aggregates pricing from multiple sources including eBay, TCGPlayer, and more!

## Features

- **eBay Integration**: Fetches the top 5 last completed and sold items to calculate average price
- **TCGPlayer Web Scraping**: Uses manual crawl algorithm to extract pricing data
- **Secure API Key Handling**: eBay API keys are hashed and never exposed in public
- **Multi-language Support**: Search for cards in different languages (English, Japanese, French, etc.)
- **Condition-based Pricing**: Get accurate prices based on card condition (Mint, Near Mint, Played, etc.)
- **Price Aggregation**: Combines data from multiple sources for comprehensive pricing

## Installation

1. Clone the repository:
```bash
git clone https://github.com/jvissup/PokePricer.git
cd PokePricer
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your eBay API credentials:
   - Go to [eBay Developers Program](https://developer.ebay.com/)
   - Create an application to get your App ID and Cert ID
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` and add your credentials:
     ```
     EBAY_APP_ID=your_actual_app_id
     EBAY_CERT_ID=your_actual_cert_id
     ```

## Usage

Run the pricing tool:
```bash
python pokepicer.py
```

The tool will prompt you for:
1. **Pokemon Card Name**: e.g., "Charizard VMAX", "Pikachu V"
2. **Language**: The language of the card (default: English)
3. **Condition**: The condition of the card (default: Near Mint)

### Example Session

```
Enter Pokemon card name: Charizard VMAX
Enter card language (default: English): English
Enter card condition (default: Near Mint): Near Mint

============================================================
Searching for: Charizard VMAX
Language: English | Condition: Near Mint
============================================================

Fetching prices from eBay...
✓ eBay: $45.67 (based on 5 sold items)

Fetching prices from TCGPlayer...
✓ TCGPlayer: $48.99

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

The tool consists of three main modules:

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
