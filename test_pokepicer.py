"""
Unit tests for Pokemon Card Pricing Tool
Tests the core functionality without requiring external API calls
"""
import unittest
from unittest.mock import Mock, patch
import os
from ebay_pricer import EbayPricer
from tcgplayer_pricer import TCGPlayerPricer
from pokepicer import PokemonCardPricer
from app import app as flask_app


class TestEbayPricer(unittest.TestCase):
    """Test eBay pricing functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.pricer = EbayPricer("test_app_id")
    
    def test_initialization(self):
        """Test eBay pricer initialization."""
        self.assertIsNotNone(self.pricer)
        self.assertEqual(self.pricer.base_url, 
                        "https://svcs.ebay.com/services/search/FindingService/v1")
    
    def test_condition_mapping(self):
        """Test condition to eBay code mapping."""
        self.assertEqual(self.pricer._map_condition("new"), "1000")
        self.assertEqual(self.pricer._map_condition("Near Mint"), "1500")
        self.assertEqual(self.pricer._map_condition("Used"), "3000")
        self.assertEqual(self.pricer._map_condition("unknown"), "3000")
    
    @patch('ebay_pricer.requests.get')
    def test_search_sold_items_success(self, mock_get):
        """Test successful eBay API call."""
        # Mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            'findCompletedItemsResponse': [{
                'searchResult': [{
                    'item': [
                        {
                            'title': ['Charizard Card'],
                            'sellingStatus': [{
                                'currentPrice': [{
                                    '__value__': '45.99',
                                    '@currencyId': 'USD'
                                }]
                            }]
                        }
                    ]
                }]
            }]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        items = self.pricer.search_sold_items("Charizard", "English", "Mint")
        
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]['title'], 'Charizard Card')
        self.assertEqual(items[0]['price'], 45.99)
    
    @patch('ebay_pricer.requests.get')
    def test_search_sold_items_no_results(self, mock_get):
        """Test eBay API call with no results."""
        mock_response = Mock()
        mock_response.json.return_value = {
            'findCompletedItemsResponse': [{
                'searchResult': [{}]
            }]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        items = self.pricer.search_sold_items("NonExistentCard", "English", "Mint")
        
        self.assertEqual(len(items), 0)
    
    @patch('ebay_pricer.requests.get')
    def test_get_average_price(self, mock_get):
        """Test average price calculation."""
        mock_response = Mock()
        mock_response.json.return_value = {
            'findCompletedItemsResponse': [{
                'searchResult': [{
                    'item': [
                        {
                            'title': ['Card 1'],
                            'sellingStatus': [{
                                'currentPrice': [{
                                    '__value__': '10.00',
                                    '@currencyId': 'USD'
                                }]
                            }]
                        },
                        {
                            'title': ['Card 2'],
                            'sellingStatus': [{
                                'currentPrice': [{
                                    '__value__': '20.00',
                                    '@currencyId': 'USD'
                                }]
                            }]
                        }
                    ]
                }]
            }]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        result = self.pricer.get_average_price("Test Card", "English", "Mint")
        
        self.assertIsNotNone(result)
        self.assertEqual(result['average_price'], 15.00)
        self.assertEqual(result['sample_size'], 2)


class TestTCGPlayerPricer(unittest.TestCase):
    """Test TCGPlayer pricing functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.pricer = TCGPlayerPricer()
    
    def test_initialization(self):
        """Test TCGPlayer pricer initialization."""
        self.assertIsNotNone(self.pricer)
        self.assertEqual(self.pricer.base_url, "https://www.tcgplayer.com")
    
    def test_extract_prices_from_patterns(self):
        """Test price extraction from HTML."""
        from bs4 import BeautifulSoup
        
        html = """
        <div>
            <span class="market-price">Market Price: $45.99</span>
            <span class="low-price">Low: $40.00</span>
            <span class="high-price">High: $50.00</span>
        </div>
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        prices = self.pricer._extract_prices(soup, "Near Mint")
        
        # Should extract some price information
        self.assertIsNotNone(prices)


class TestPokemonCardPricer(unittest.TestCase):
    """Test main Pokemon Card Pricer functionality."""
    
    @patch.dict('os.environ', {'EBAY_APP_ID': 'test_app_id'})
    def test_initialization_with_ebay(self):
        """Test pricer initialization with eBay credentials."""
        pricer = PokemonCardPricer()
        
        self.assertIsNotNone(pricer.ebay_pricer)
        self.assertIsNotNone(pricer.tcgplayer_pricer)
    
    @patch.dict('os.environ', {}, clear=True)
    def test_initialization_without_ebay(self):
        """Test pricer initialization without eBay credentials."""
        pricer = PokemonCardPricer()
        
        self.assertIsNone(pricer.ebay_pricer)
        self.assertIsNotNone(pricer.tcgplayer_pricer)
    
    @patch('pokepicer.EbayPricer')
    @patch('pokepicer.TCGPlayerPricer')
    def test_get_price_aggregation(self, mock_tcg, mock_ebay):
        """Test price aggregation from multiple sources."""
        # Mock eBay results
        mock_ebay_instance = Mock()
        mock_ebay_instance.get_average_price.return_value = {
            'source': 'eBay',
            'average_price': 45.00,
            'currency': 'USD',
            'sample_size': 5
        }
        mock_ebay.return_value = mock_ebay_instance
        
        # Mock TCGPlayer results
        mock_tcg_instance = Mock()
        mock_tcg_instance.get_average_price.return_value = {
            'source': 'TCGPlayer',
            'average_price': 50.00,
            'currency': 'USD'
        }
        mock_tcg.return_value = mock_tcg_instance
        
        # Test
        pricer = PokemonCardPricer()
        pricer.ebay_pricer = mock_ebay_instance
        pricer.tcgplayer_pricer = mock_tcg_instance
        
        results = pricer.get_price("Charizard", "English", "Near Mint")
        
        self.assertEqual(len(results['sources']), 2)
        self.assertEqual(results['average_price'], 47.50)  # Average of 45 and 50
        self.assertEqual(results['price_range']['min'], 45.00)
        self.assertEqual(results['price_range']['max'], 50.00)


class TestFlaskEndpoints(unittest.TestCase):
    """Test Flask web application endpoints."""
    
    def setUp(self):
        """Set up test fixtures."""
        flask_app.config['TESTING'] = True
        self.client = flask_app.test_client()
    
    def test_health_endpoint(self):
        """Test health check endpoint."""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'ok')
    
    @patch.dict('os.environ', {'EBAY_VERIFICATION_TOKEN': 'test-token-12345'})
    def test_verification_token_endpoint_with_token(self):
        """Test verification token endpoint with configured token."""
        response = self.client.get('/ebay/verification-token')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['verificationToken'], 'test-token-12345')
    
    @patch.dict('os.environ', {}, clear=True)
    def test_verification_token_endpoint_without_token(self):
        """Test verification token endpoint without configured token."""
        response = self.client.get('/ebay/verification-token')
        self.assertEqual(response.status_code, 500)
        data = response.get_json()
        self.assertIn('error', data)
    
    def test_marketplace_account_deletion_success(self):
        """Test marketplace account deletion endpoint with valid data."""
        test_data = {
            'metadata': {
                'topic': 'MARKETPLACE_ACCOUNT_DELETION',
                'schemaVersion': '1.0',
                'deprecated': False
            },
            'notification': {
                'notificationId': 'test-notification-id',
                'eventDate': '2026-02-04T12:00:00.000Z',
                'publishDate': '2026-02-04T12:00:01.000Z',
                'publishAttemptCount': 1,
                'data': {
                    'username': 'test_user',
                    'userId': '12345',
                    'eiasToken': 'test-token'
                }
            }
        }
        
        response = self.client.post(
            '/ebay/marketplace-account-deletion',
            json=test_data,
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('message', data)
    
    def test_marketplace_account_deletion_no_data(self):
        """Test marketplace account deletion endpoint with no data."""
        response = self.client.post(
            '/ebay/marketplace-account-deletion',
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)
    
    def test_marketplace_account_deletion_minimal_data(self):
        """Test marketplace account deletion endpoint with minimal data."""
        test_data = {
            'notification': {
                'data': {
                    'username': 'test_user',
                    'userId': '12345'
                }
            }
        }
        
        response = self.client.post(
            '/ebay/marketplace-account-deletion',
            json=test_data,
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'success')


def run_tests():
    """Run all tests."""
    unittest.main(argv=[''], verbosity=2, exit=False)


if __name__ == '__main__':
    print("="*60)
    print("Running Pokemon Card Pricing Tool Tests")
    print("="*60)
    run_tests()
