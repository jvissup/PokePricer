#!/usr/bin/env python3
"""
Demo script for Pokemon Card Pricing Tool
Demonstrates the functionality without requiring user input
"""
from pokepicer import PokemonCardPricer


def demo_without_ebay():
    """
    Demo the tool without eBay API (TCGPlayer only).
    This shows the tool working even without eBay credentials.
    """
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║      POKEMON CARD PRICING TOOL - DEMO MODE            ║
    ║                                                        ║
    ║  Note: This demo runs without eBay API credentials    ║
    ║  To enable eBay pricing:                              ║
    ║    1. Get API key from developer.ebay.com             ║
    ║    2. Add to .env file                                ║
    ╚════════════════════════════════════════════════════════╝
    """)
    
    pricer = PokemonCardPricer()
    
    # Demo searches
    demo_cards = [
        {"name": "Charizard VMAX", "language": "English", "condition": "Near Mint"},
        {"name": "Pikachu V", "language": "English", "condition": "Mint"},
    ]
    
    for card_info in demo_cards:
        print(f"\n{'#'*60}")
        print(f"Demo Search #{demo_cards.index(card_info) + 1}")
        print(f"{'#'*60}")
        
        results = pricer.get_price(
            card_info["name"],
            card_info["language"],
            card_info["condition"]
        )
        pricer.display_results(results)
        
        input("\nPress Enter to continue to next demo...")
    
    print("\n" + "="*60)
    print("Demo complete!")
    print("="*60)
    print("\nTo run the interactive version: python pokepicer.py")
    print("\nFeatures:")
    print("  ✓ eBay API integration (fetches top 5 sold items)")
    print("  ✓ TCGPlayer web scraping")
    print("  ✓ Multi-language support")
    print("  ✓ Condition-based pricing")
    print("  ✓ Price aggregation from multiple sources")
    print("  ✓ Secure API key handling (hashed)")


if __name__ == "__main__":
    demo_without_ebay()
