"""
Example: Using Pokemon Card Pricing Tool Programmatically
This demonstrates how to integrate the pricing tool into your own Python code
"""
from pokepicer import PokemonCardPricer


def example_basic_search():
    """Basic example: Search for a single card."""
    print("="*60)
    print("Example 1: Basic Card Search")
    print("="*60)
    
    # Initialize the pricer
    pricer = PokemonCardPricer()
    
    # Search for a card
    results = pricer.get_price(
        card_name="Charizard VMAX",
        language="English",
        condition="Near Mint"
    )
    
    # Display results
    pricer.display_results(results)
    
    # Access results programmatically
    if results['average_price']:
        print(f"Found average price: ${results['average_price']}")
        print(f"Price range: ${results['price_range']['min']} - ${results['price_range']['max']}")


def example_multiple_cards():
    """Example: Compare prices for multiple cards."""
    print("\n" + "="*60)
    print("Example 2: Multiple Card Search")
    print("="*60)
    
    pricer = PokemonCardPricer()
    
    cards_to_check = [
        "Charizard VMAX",
        "Pikachu V",
        "Mewtwo VSTAR"
    ]
    
    all_results = []
    
    for card_name in cards_to_check:
        print(f"\nSearching for: {card_name}")
        results = pricer.get_price(card_name, "English", "Near Mint")
        all_results.append(results)
        
        if results['average_price']:
            print(f"  → Average: ${results['average_price']}")
        else:
            print(f"  → No pricing found")
    
    # Find most expensive card
    valid_results = [r for r in all_results if r['average_price']]
    if valid_results:
        most_expensive = max(valid_results, key=lambda x: x['average_price'])
        print(f"\nMost expensive card: {most_expensive['card_name']} "
              f"(${most_expensive['average_price']})")


def example_different_conditions():
    """Example: Compare prices across different conditions."""
    print("\n" + "="*60)
    print("Example 3: Same Card, Different Conditions")
    print("="*60)
    
    pricer = PokemonCardPricer()
    card_name = "Charizard VMAX"
    conditions = ["Mint", "Near Mint", "Played"]
    
    print(f"\nComparing prices for: {card_name}")
    print("-" * 60)
    
    for condition in conditions:
        results = pricer.get_price(card_name, "English", condition)
        
        if results['average_price']:
            print(f"{condition:15} ${results['average_price']:>8.2f}")
        else:
            print(f"{condition:15} No data")


def example_custom_processing():
    """Example: Custom processing of results."""
    print("\n" + "="*60)
    print("Example 4: Custom Result Processing")
    print("="*60)
    
    pricer = PokemonCardPricer()
    
    results = pricer.get_price("Pikachu V", "English", "Near Mint")
    
    # Custom analysis
    print(f"\nCard: {results['card_name']}")
    print(f"Sources checked: {len(results['sources'])}")
    
    for source in results['sources']:
        print(f"\n{source['source']}:")
        print(f"  Price: ${source['average_price']}")
        
        # eBay-specific details
        if source['source'] == 'eBay' and 'items' in source:
            print(f"  Sample items:")
            for item in source['items'][:3]:  # Show first 3
                print(f"    - {item['title'][:50]}: ${item['price']}")
    
    # Calculate price variance
    if len(results['sources']) > 1:
        prices = [s['average_price'] for s in results['sources']]
        variance = max(prices) - min(prices)
        variance_pct = (variance / min(prices)) * 100
        print(f"\nPrice variance: ${variance:.2f} ({variance_pct:.1f}%)")


def example_error_handling():
    """Example: Proper error handling."""
    print("\n" + "="*60)
    print("Example 5: Error Handling")
    print("="*60)
    
    pricer = PokemonCardPricer()
    
    # Try searching for a card that might not exist
    card_name = "NonExistentCard12345"
    
    try:
        results = pricer.get_price(card_name, "English", "Near Mint")
        
        if not results['sources']:
            print(f"⚠ No pricing data found for '{card_name}'")
            print("Suggestions:")
            print("  - Check the card name spelling")
            print("  - Try a more common card name")
            print("  - Verify your internet connection")
        else:
            pricer.display_results(results)
            
    except Exception as e:
        print(f"❌ Error occurred: {e}")
        print("The tool will continue to work with other cards")


if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║     POKEMON CARD PRICING TOOL - EXAMPLES               ║
    ║                                                        ║
    ║  These examples show how to use the tool               ║
    ║  programmatically in your own Python code              ║
    ╚════════════════════════════════════════════════════════╝
    """)
    
    # Run examples
    # Note: Uncomment the examples you want to run
    
    # example_basic_search()
    # example_multiple_cards()
    # example_different_conditions()
    # example_custom_processing()
    example_error_handling()
    
    print("\n" + "="*60)
    print("Examples complete!")
    print("="*60)
    print("\nTo use in your code, simply import and use:")
    print("  from pokepicer import PokemonCardPricer")
    print("  pricer = PokemonCardPricer()")
    print("  results = pricer.get_price('Charizard', 'English', 'Mint')")
