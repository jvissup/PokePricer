"""
TCGPlayer web scraper for Pokemon card pricing.
Uses manual crawl algorithm to extract pricing data.
"""
import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict
import time
import re


class TCGPlayerPricer:
    """Handles web scraping of TCGPlayer for Pokemon card prices."""
    
    def __init__(self):
        """Initialize TCGPlayer scraper."""
        self.base_url = "https://www.tcgplayer.com"
        self.search_url = f"{self.base_url}/search/pokemon/product"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def search_card(self, card_name: str, language: str = "English",
                   condition: str = "Near Mint") -> Optional[Dict]:
        """
        Search for a Pokemon card on TCGPlayer and extract pricing.
        
        Args:
            card_name: Name of the Pokemon card
            language: Language of the card (default: English)
            condition: Condition of the card (default: Near Mint)
            
        Returns:
            Dictionary with pricing information
        """
        # Note: TCGPlayer's structure may change; this is a basic implementation
        search_params = {
            'q': card_name,
            'language': language
        }
        
        try:
            # Step 1: Search for the card
            response = requests.get(
                self.search_url, 
                params=search_params,
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Step 2: Extract price information
            # TCGPlayer typically shows Market Price, Low Price, Mid Price
            prices = self._extract_prices(soup, condition)
            
            if prices:
                return {
                    'source': 'TCGPlayer',
                    'market_price': prices.get('market_price'),
                    'low_price': prices.get('low_price'),
                    'mid_price': prices.get('mid_price'),
                    'high_price': prices.get('high_price'),
                    'currency': 'USD',
                    'condition': condition
                }
            
            return None
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching TCGPlayer data: {e}")
            return None
    
    def _extract_prices(self, soup: BeautifulSoup, condition: str) -> Optional[Dict]:
        """
        Extract price information from the page HTML.
        
        Args:
            soup: BeautifulSoup object of the page
            condition: Card condition to look for
            
        Returns:
            Dictionary with extracted prices
        """
        prices = {}
        
        # Try to find price elements (structure may vary)
        # Look for common TCGPlayer price classes/patterns
        price_patterns = [
            r'market[_\s-]?price["\s:>]+\$?([\d,.]+)',
            r'low[_\s-]?price["\s:>]+\$?([\d,.]+)',
            r'mid[_\s-]?price["\s:>]+\$?([\d,.]+)',
            r'high[_\s-]?price["\s:>]+\$?([\d,.]+)'
        ]
        
        page_text = soup.get_text()
        
        for pattern in price_patterns:
            match = re.search(pattern, page_text, re.IGNORECASE)
            if match:
                price_type = pattern.split('[')[0].lower().replace('_', ' ').strip()
                try:
                    price_value = float(match.group(1).replace(',', ''))
                    prices[f"{price_type.replace(' ', '_')}"] = price_value
                except (ValueError, IndexError):
                    continue
        
        # If we couldn't find structured prices, try to find any price listings
        if not prices:
            price_elements = soup.find_all(text=re.compile(r'\$[\d,.]+'))
            if price_elements:
                extracted_prices = []
                for elem in price_elements[:5]:  # Get first 5 prices found
                    price_match = re.search(r'\$([\d,.]+)', elem)
                    if price_match:
                        try:
                            extracted_prices.append(float(price_match.group(1).replace(',', '')))
                        except ValueError:
                            continue
                
                if extracted_prices:
                    prices = {
                        'market_price': sum(extracted_prices) / len(extracted_prices),
                        'low_price': min(extracted_prices),
                        'high_price': max(extracted_prices)
                    }
        
        return prices if prices else None
    
    def get_average_price(self, card_name: str, language: str = "English",
                         condition: str = "Near Mint") -> Optional[Dict]:
        """
        Get average/market price from TCGPlayer.
        
        Args:
            card_name: Name of the Pokemon card
            language: Language of the card
            condition: Condition of the card
            
        Returns:
            Dictionary with average price
        """
        result = self.search_card(card_name, language, condition)
        
        if result and result.get('market_price'):
            return {
                'source': 'TCGPlayer',
                'average_price': round(result['market_price'], 2),
                'currency': 'USD',
                'details': result
            }
        elif result:
            # Calculate average from available prices
            available_prices = [
                v for k, v in result.items() 
                if k in ['low_price', 'mid_price', 'high_price', 'market_price'] 
                and v is not None
            ]
            if available_prices:
                avg = sum(available_prices) / len(available_prices)
                return {
                    'source': 'TCGPlayer',
                    'average_price': round(avg, 2),
                    'currency': 'USD',
                    'details': result
                }
        
        return None
