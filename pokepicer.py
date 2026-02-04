"""
Main Pokemon Card Pricing Tool
Aggregates pricing from multiple sources: eBay, TCGPlayer, and others.
"""
import os
from typing import Dict, List, Optional
from dotenv import load_dotenv
from ebay_pricer import EbayPricer
from tcgplayer_pricer import TCGPlayerPricer


class PokemonCardPricer:
    """Main class for aggregating Pokemon card prices from multiple sources."""
    
    def __init__(self):
        """Initialize the pricer with all available sources."""
        load_dotenv()
        
        # Initialize eBay pricer if credentials are available
        ebay_app_id = os.getenv('EBAY_APP_ID')
        self.ebay_pricer = EbayPricer(ebay_app_id) if ebay_app_id else None
        
        # Initialize TCGPlayer scraper
        self.tcgplayer_pricer = TCGPlayerPricer()
        
    def get_price(self, card_name: str, language: str = "English", 
                 condition: str = "Near Mint") -> Dict:
        """
        Get pricing information from all available sources.
        
        Args:
            card_name: Name of the Pokemon card to price
            language: Language of the card (default: English)
            condition: Condition of the card (default: Near Mint)
            
        Returns:
            Dictionary with pricing from all sources and aggregated data
        """
        results = {
            'card_name': card_name,
            'language': language,
            'condition': condition,
            'sources': [],
            'average_price': None,
            'currency': 'USD'
        }
        
        print(f"\n{'='*60}")
        print(f"Searching for: {card_name}")
        print(f"Language: {language} | Condition: {condition}")
        print(f"{'='*60}\n")
        
        # Fetch from eBay
        if self.ebay_pricer:
            print("Fetching prices from eBay...")
            ebay_result = self.ebay_pricer.get_average_price(card_name, language, condition)
            if ebay_result:
                results['sources'].append(ebay_result)
                print(f"✓ eBay: ${ebay_result['average_price']} "
                      f"(based on {ebay_result['sample_size']} sold items)")
            else:
                print("✗ eBay: No results found")
        else:
            print("⚠ eBay: API credentials not configured")
        
        # Fetch from TCGPlayer
        print("\nFetching prices from TCGPlayer...")
        tcgplayer_result = self.tcgplayer_pricer.get_average_price(card_name, language, condition)
        if tcgplayer_result:
            results['sources'].append(tcgplayer_result)
            print(f"✓ TCGPlayer: ${tcgplayer_result['average_price']}")
        else:
            print("✗ TCGPlayer: No results found")
        
        # Calculate overall average
        if results['sources']:
            prices = [source['average_price'] for source in results['sources']]
            results['average_price'] = round(sum(prices) / len(prices), 2)
            results['price_range'] = {
                'min': round(min(prices), 2),
                'max': round(max(prices), 2)
            }
        
        return results
    
    def display_results(self, results: Dict):
        """
        Display pricing results in a formatted way.
        
        Args:
            results: Results dictionary from get_price()
        """
        print(f"\n{'='*60}")
        print(f"PRICING SUMMARY")
        print(f"{'='*60}")
        print(f"Card: {results['card_name']}")
        print(f"Language: {results['language']}")
        print(f"Condition: {results['condition']}")
        print(f"{'='*60}\n")
        
        if not results['sources']:
            print("⚠ No pricing data found from any source.")
            print("Please check:")
            print("  - Card name spelling")
            print("  - Internet connection")
            print("  - API credentials (for eBay)")
            return
        
        print("SOURCE BREAKDOWN:")
        print("-" * 60)
        for source in results['sources']:
            source_name = source['source']
            price = source['average_price']
            currency = source.get('currency', 'USD')
            print(f"{source_name:20} ${price:>8.2f} {currency}")
            
            # Show additional details for eBay
            if source_name == 'eBay' and 'sample_size' in source:
                print(f"{'':20} (Based on {source['sample_size']} sold items)")
        
        print("-" * 60)
        
        if results['average_price']:
            print(f"\n{'OVERALL AVERAGE:':20} ${results['average_price']:>8.2f} USD")
            if 'price_range' in results:
                print(f"{'PRICE RANGE:':20} ${results['price_range']['min']:.2f} - "
                      f"${results['price_range']['max']:.2f}")
        
        print(f"\n{'='*60}\n")


def main():
    """Main function to run the Pokemon card pricer."""
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║          POKEMON CARD PRICING TOOL                     ║
    ║  Get prices from eBay, TCGPlayer & more!              ║
    ╚════════════════════════════════════════════════════════╝
    """)
    
    pricer = PokemonCardPricer()
    
    while True:
        print("\n" + "="*60)
        
        # Get user input
        card_name = input("Enter Pokemon card name (or 'quit' to exit): ").strip()
        
        if card_name.lower() in ['quit', 'exit', 'q']:
            print("\nThank you for using Pokemon Card Pricing Tool!")
            break
        
        if not card_name:
            print("⚠ Please enter a valid card name.")
            continue
        
        # Get language
        print("\nAvailable languages: English, Japanese, French, German, Spanish, Italian, etc.")
        language = input("Enter card language (default: English): ").strip()
        if not language:
            language = "English"
        
        # Get condition
        print("\nAvailable conditions:")
        print("  - Mint/New")
        print("  - Near Mint")
        print("  - Excellent")
        print("  - Good/Used")
        print("  - Light Played")
        print("  - Played")
        print("  - Poor")
        condition = input("Enter card condition (default: Near Mint): ").strip()
        if not condition:
            condition = "Near Mint"
        
        # Fetch and display prices
        results = pricer.get_price(card_name, language, condition)
        pricer.display_results(results)
        
        # Ask if user wants to continue
        continue_search = input("\nSearch for another card? (y/n): ").strip().lower()
        if continue_search not in ['y', 'yes', '']:
            print("\nThank you for using Pokemon Card Pricing Tool!")
            break


if __name__ == "__main__":
    main()
