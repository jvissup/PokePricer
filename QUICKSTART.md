# Quick Start Guide

## Installation (5 minutes)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/jvissup/PokePricer.git
   cd PokePricer
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure eBay API (Optional but recommended):**
   ```bash
   cp .env.example .env
   # Edit .env and add your eBay App ID
   ```
   
   See [CONFIGURATION.md](CONFIGURATION.md) for detailed setup instructions.

## Usage

### Interactive Mode (Recommended for beginners)

```bash
python pokepicer.py
```

You'll be prompted to enter:
- Pokemon card name
- Language (default: English)
- Condition (default: Near Mint)

### Demo Mode (No user input required)

```bash
python demo.py
```

### Programmatic Usage

```python
from pokepicer import PokemonCardPricer

pricer = PokemonCardPricer()
results = pricer.get_price("Charizard VMAX", "English", "Near Mint")
pricer.display_results(results)
```

See [examples.py](examples.py) for more usage examples.

## Testing

Run the test suite:
```bash
python test_pokepicer.py
```

## Features at a Glance

| Feature | Description |
|---------|-------------|
| **eBay Integration** | ✓ Fetches top 5 sold items for accurate pricing |
| **TCGPlayer Scraping** | ✓ Manual crawl algorithm for web scraping |
| **Secure API Keys** | ✓ Hashed keys, never exposed publicly |
| **Multi-language** | ✓ Search cards in any language |
| **Condition-based** | ✓ Accurate pricing by card condition |
| **Price Aggregation** | ✓ Average from multiple sources |

## Common Card Conditions

- **Mint/New**: Perfect condition, never played
- **Near Mint**: Minimal wear, looks new
- **Excellent**: Light play, slight edge wear
- **Good/Used**: Moderate wear
- **Played**: Heavy wear, still playable

## Need Help?

- **Setup issues**: Check [CONFIGURATION.md](CONFIGURATION.md)
- **API problems**: See [CONFIGURATION.md](CONFIGURATION.md) troubleshooting
- **Usage examples**: Review [examples.py](examples.py)
- **Full documentation**: Read [README.md](README.md)

## Quick Examples

### Search for a specific card
```bash
python pokepicer.py
> Charizard VMAX
> English
> Near Mint
```

### Compare different conditions
Run [examples.py](examples.py) and uncomment `example_different_conditions()`

### Batch search multiple cards
Run [examples.py](examples.py) and uncomment `example_multiple_cards()`

## What if eBay API is not configured?

The tool still works! It will:
- Show a warning about eBay
- Use TCGPlayer pricing only
- Provide accurate results from available sources

## Tips for Best Results

1. **Use exact card names**: "Charizard VMAX" not "charizard"
2. **Specify set if needed**: "Charizard VMAX Darkness Ablaze"
3. **Be patient**: Web scraping can take a few seconds
4. **Check spelling**: Incorrect names return no results
5. **Try variations**: Some cards have multiple versions

## Next Steps

1. ✓ Install and run the tool
2. ✓ Get eBay API key for better results
3. ✓ Try the examples
4. ✓ Integrate into your own projects

---

**Ready to start?** Run `python pokepicer.py` now!
