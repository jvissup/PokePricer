# API Reference

Complete API documentation for Pokemon Card Pricing Tool developers.

## Main Classes

### PokemonCardPricer

Main class for aggregating prices from multiple sources.

#### Constructor

```python
PokemonCardPricer()
```

Initializes the pricer with all available sources. Automatically loads eBay credentials from `.env` file.

**Example:**
```python
pricer = PokemonCardPricer()
```

#### Methods

##### get_price()

```python
get_price(card_name: str, language: str = "English", condition: str = "Near Mint") -> Dict
```

Get pricing information from all available sources.

**Parameters:**
- `card_name` (str): Name of the Pokemon card to price
- `language` (str, optional): Language of the card. Default: "English"
- `condition` (str, optional): Condition of the card. Default: "Near Mint"

**Returns:**
- `Dict`: Dictionary containing:
  - `card_name` (str): Name of the card searched
  - `language` (str): Language searched
  - `condition` (str): Condition searched
  - `sources` (List[Dict]): List of results from each source
  - `average_price` (float): Overall average price
  - `currency` (str): Currency code (usually "USD")
  - `price_range` (Dict): Min and max prices

**Example:**
```python
results = pricer.get_price("Charizard VMAX", "English", "Near Mint")
print(f"Average: ${results['average_price']}")
```

##### display_results()

```python
display_results(results: Dict) -> None
```

Display pricing results in a formatted way.

**Parameters:**
- `results` (Dict): Results dictionary from `get_price()`

**Example:**
```python
results = pricer.get_price("Pikachu V", "English", "Mint")
pricer.display_results(results)
```

---

### EbayPricer

Handles eBay API calls to fetch Pokemon card prices.

#### Constructor

```python
EbayPricer(app_id: str)
```

**Parameters:**
- `app_id` (str): eBay App ID (will be hashed for security)

**Example:**
```python
ebay = EbayPricer("your_app_id_here")
```

#### Methods

##### search_sold_items()

```python
search_sold_items(card_name: str, language: str = "English", condition: str = "Used") -> List[Dict]
```

Search for sold Pokemon cards on eBay.

**Parameters:**
- `card_name` (str): Name of the Pokemon card
- `language` (str, optional): Language of the card. Default: "English"
- `condition` (str, optional): Condition of the card. Default: "Used"

**Returns:**
- `List[Dict]`: List of sold items, each containing:
  - `title` (str): Item title
  - `price` (float): Sale price
  - `currency` (str): Currency code

**Example:**
```python
items = ebay.search_sold_items("Charizard", "English", "Mint")
for item in items:
    print(f"{item['title']}: ${item['price']}")
```

##### get_average_price()

```python
get_average_price(card_name: str, language: str = "English", condition: str = "Used") -> Optional[Dict]
```

Get average price from top 5 sold items.

**Parameters:**
- `card_name` (str): Name of the Pokemon card
- `language` (str, optional): Language of the card. Default: "English"
- `condition` (str, optional): Condition of the card. Default: "Used"

**Returns:**
- `Dict` or `None`: Dictionary containing:
  - `source` (str): "eBay"
  - `average_price` (float): Average price
  - `currency` (str): Currency code
  - `sample_size` (int): Number of items used for average
  - `items` (List[Dict]): Individual items

**Example:**
```python
result = ebay.get_average_price("Pikachu V", "English", "Near Mint")
if result:
    print(f"Average: ${result['average_price']} (from {result['sample_size']} items)")
```

---

### TCGPlayerPricer

Handles web scraping of TCGPlayer for Pokemon card prices.

#### Constructor

```python
TCGPlayerPricer()
```

**Example:**
```python
tcg = TCGPlayerPricer()
```

#### Methods

##### search_card()

```python
search_card(card_name: str, language: str = "English", condition: str = "Near Mint") -> Optional[Dict]
```

Search for a Pokemon card on TCGPlayer and extract pricing.

**Parameters:**
- `card_name` (str): Name of the Pokemon card
- `language` (str, optional): Language of the card. Default: "English"
- `condition` (str, optional): Condition of the card. Default: "Near Mint"

**Returns:**
- `Dict` or `None`: Dictionary containing:
  - `source` (str): "TCGPlayer"
  - `market_price` (float): Market price
  - `low_price` (float): Lowest price
  - `mid_price` (float): Mid-range price
  - `high_price` (float): Highest price
  - `currency` (str): Currency code
  - `condition` (str): Card condition

**Example:**
```python
result = tcg.search_card("Charizard VMAX", "English", "Near Mint")
if result:
    print(f"Market: ${result['market_price']}")
```

##### get_average_price()

```python
get_average_price(card_name: str, language: str = "English", condition: str = "Near Mint") -> Optional[Dict]
```

Get average/market price from TCGPlayer.

**Parameters:**
- `card_name` (str): Name of the Pokemon card
- `language` (str, optional): Language of the card. Default: "English"
- `condition` (str, optional): Condition of the card. Default: "Near Mint"

**Returns:**
- `Dict` or `None`: Dictionary containing:
  - `source` (str): "TCGPlayer"
  - `average_price` (float): Average/market price
  - `currency` (str): Currency code
  - `details` (Dict): Full pricing details

**Example:**
```python
result = tcg.get_average_price("Mewtwo VSTAR", "English", "Mint")
if result:
    print(f"TCGPlayer: ${result['average_price']}")
```

---

## Data Structures

### Price Result Dictionary

Structure of the dictionary returned by `PokemonCardPricer.get_price()`:

```python
{
    'card_name': str,           # Name of the card
    'language': str,            # Language searched
    'condition': str,           # Condition searched
    'sources': [                # List of source results
        {
            'source': str,      # Source name (e.g., "eBay", "TCGPlayer")
            'average_price': float,
            'currency': str,
            # Source-specific fields...
        }
    ],
    'average_price': float,     # Overall average
    'currency': str,            # Currency code
    'price_range': {            # Price range
        'min': float,
        'max': float
    }
}
```

### eBay Item Dictionary

Structure of individual eBay items:

```python
{
    'title': str,               # Item title
    'price': float,             # Sale price
    'currency': str             # Currency code
}
```

## Constants

### Supported Conditions

```python
CONDITIONS = [
    "Mint",
    "New", 
    "Near Mint",
    "Excellent",
    "Good",
    "Used",
    "Light Played",
    "Played",
    "Poor"
]
```

### eBay Condition Codes

Internal mapping used by `EbayPricer`:

```python
CONDITION_MAP = {
    'new': '1000',
    'mint': '1000',
    'near mint': '1500',
    'excellent': '2000',
    'good': '3000',
    'used': '3000',
    'light played': '4000',
    'played': '5000',
    'poor': '6000'
}
```

## Error Handling

All methods handle errors gracefully:

- Network errors: Return `None` or empty list, print error message
- API errors: Return `None` or empty list, print error message
- Parse errors: Skip problematic items, continue with valid ones
- Missing credentials: Print warning, skip that source

**Example:**
```python
try:
    results = pricer.get_price("Card Name", "English", "Mint")
    if not results['sources']:
        print("No data found")
    else:
        pricer.display_results(results)
except Exception as e:
    print(f"Error: {e}")
```

## Environment Variables

Required environment variables (in `.env` file):

```bash
EBAY_APP_ID=your_ebay_app_id      # Required for eBay pricing
EBAY_CERT_ID=your_ebay_cert_id    # Optional, for production use
```

## Rate Limits

- **eBay API**: 5,000 calls/day (default)
- **TCGPlayer**: No official limit, but be respectful

## Thread Safety

- `EbayPricer`: Thread-safe for read operations
- `TCGPlayerPricer`: Thread-safe for read operations
- `PokemonCardPricer`: Thread-safe for read operations

## Performance

Typical response times:
- eBay API: 1-3 seconds
- TCGPlayer scraping: 2-5 seconds
- Combined search: 3-8 seconds

## Examples

### Basic Usage

```python
from pokepicer import PokemonCardPricer

pricer = PokemonCardPricer()
results = pricer.get_price("Charizard VMAX", "English", "Near Mint")
pricer.display_results(results)
```

### Advanced Usage

```python
from pokepicer import PokemonCardPricer

pricer = PokemonCardPricer()

# Get results
results = pricer.get_price("Pikachu V", "Japanese", "Mint")

# Process programmatically
if results['average_price']:
    avg = results['average_price']
    min_price = results['price_range']['min']
    max_price = results['price_range']['max']
    
    print(f"Average: ${avg:.2f}")
    print(f"Range: ${min_price:.2f} - ${max_price:.2f}")
    
    # Analyze by source
    for source in results['sources']:
        print(f"{source['source']}: ${source['average_price']:.2f}")
```

### Error Handling

```python
from pokepicer import PokemonCardPricer

pricer = PokemonCardPricer()

try:
    results = pricer.get_price("Unknown Card", "English", "Mint")
    
    if not results['sources']:
        print("No pricing data available")
    elif results['average_price']:
        print(f"Found price: ${results['average_price']}")
    else:
        print("Unexpected result format")
        
except KeyError as e:
    print(f"Missing expected key: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

---

## Web API Endpoints

### GET /ebay/verification-token

Returns the eBay verification token for Marketplace Account Deletion notifications.

**Response:**
```json
{
    "verificationToken": "your-verification-token"
}
```

**Status Codes:**
- 200: Success
- 500: Verification token not configured

**Example:**
```bash
curl http://localhost:5000/ebay/verification-token
```

### POST /ebay/marketplace-account-deletion

Receives eBay Marketplace Account Deletion notifications.

**Request Body:**
```json
{
    "metadata": {
        "topic": "MARKETPLACE_ACCOUNT_DELETION",
        "schemaVersion": "1.0",
        "deprecated": false
    },
    "notification": {
        "notificationId": "unique-id",
        "eventDate": "2026-02-04T12:00:00.000Z",
        "publishDate": "2026-02-04T12:00:01.000Z",
        "publishAttemptCount": 1,
        "data": {
            "username": "ebay_user",
            "userId": "12345",
            "eiasToken": "token"
        }
    }
}
```

**Response:**
```json
{
    "status": "success",
    "message": "Account deletion notification received"
}
```

**Status Codes:**
- 200: Success
- 400: Invalid request data
- 500: Server error

**Example:**
```bash
curl -X POST http://localhost:5000/ebay/marketplace-account-deletion \
  -H "Content-Type: application/json" \
  -d '{
    "notification": {
      "data": {
        "username": "test_user",
        "userId": "12345"
      },
      "eventDate": "2026-02-04T12:00:00.000Z"
    }
  }'
```

---

For more examples, see [examples.py](examples.py) in the repository.
