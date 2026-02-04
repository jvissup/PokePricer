# Configuration Guide for Pokemon Card Pricing Tool

## eBay API Setup

### Step 1: Create an eBay Developer Account
1. Go to [eBay Developers Program](https://developer.ebay.com/)
2. Click "Register" and create an account
3. Complete the registration process

### Step 2: Create an Application
1. Log in to your eBay Developer account
2. Navigate to "My Account" → "Application Keys"
3. Click "Create a new application"
4. Fill in the application details:
   - Application Title: "Pokemon Card Pricer" (or your preferred name)
   - Application Description: "Tool to compare Pokemon card prices"
5. Submit the application

### Step 3: Get Your API Credentials
1. Once created, you'll see your Application Keys page
2. Copy your **App ID** (Client ID) - this is what you need
3. For production use, you'll also need the **Cert ID** (Client Secret)

### Step 4: Configure the Tool
1. Copy the `.env.example` file to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file and add your credentials:
   ```
   EBAY_APP_ID=YourActualAppIDHere
   EBAY_CERT_ID=YourActualCertIDHere
   ```

3. Save the file

**IMPORTANT**: Never commit the `.env` file to version control! It's already in `.gitignore`.

## API Key Security

The tool implements several security measures:

1. **Environment Variables**: API keys are stored in `.env` file, not in code
2. **Hashing**: API keys are hashed using SHA256 for internal reference
3. **Git Ignore**: The `.env` file is excluded from version control
4. **No Exposure**: Keys are never printed or logged in plain text

## Testing Without eBay API

The tool works even without eBay credentials:
- TCGPlayer scraping will still function
- You'll see a warning that eBay is not configured
- Results will show TCGPlayer data only

## API Rate Limits

### eBay Finding API Limits
- Sandbox: 5,000 calls per day
- Production: 5,000 calls per day (default)
- Can be increased by contacting eBay

### TCGPlayer
- No official API used (web scraping)
- Be respectful: add delays between requests
- Don't overload their servers

## Troubleshooting

### "eBay: API credentials not configured"
- Check that `.env` file exists
- Verify `EBAY_APP_ID` is set correctly
- Ensure there are no extra spaces or quotes

### "Error fetching eBay data"
- Verify your API credentials are valid
- Check your internet connection
- Ensure you haven't exceeded rate limits
- Try the eBay sandbox first before production keys

### "No results found"
- Check the card name spelling
- Try different search terms
- Some cards may not have recent sales data

## Advanced Configuration

### Using Different Endpoints
Edit `ebay_pricer.py` to use sandbox or different regions:

```python
# Sandbox endpoint
self.base_url = "https://svcs.sandbox.ebay.com/services/search/FindingService/v1"

# Global site (default is US)
# Add siteId parameter in search_sold_items()
```

### Customizing Search Parameters
Modify the `search_sold_items()` method in `ebay_pricer.py`:
- Change `entriesPerPage` to get more/fewer results
- Adjust `sortOrder` for different sorting
- Add additional filters for better results

## Privacy and Data Usage

- This tool only reads public pricing data
- No personal data is collected or stored
- API keys are kept local and never transmitted elsewhere
- All data is fetched in real-time, nothing is cached

## Support

For eBay API issues:
- [eBay Developer Documentation](https://developer.ebay.com/docs)
- [eBay Developer Forums](https://community.ebay.com/t5/Developer-Forums/ct-p/developer-forums)

For tool issues:
- Check the GitHub Issues page
- Review the README.md for common problems
- Verify all dependencies are installed correctly
