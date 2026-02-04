// Pokemon Card Pricing Tool - Frontend JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('searchForm');
    const searchBtn = document.getElementById('searchBtn');
    const btnText = document.getElementById('btnText');
    const btnLoader = document.getElementById('btnLoader');
    const resultsSection = document.getElementById('results');
    const errorSection = document.getElementById('error');
    const noResultsSection = document.getElementById('noResults');
    
    searchForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Get form data
        const cardName = document.getElementById('cardName').value.trim();
        const language = document.getElementById('language').value;
        const condition = document.getElementById('condition').value;
        
        if (!cardName) {
            showError('Please enter a card name');
            return;
        }
        
        // Show loading state
        setLoading(true);
        hideAllSections();
        
        try {
            // Make API request
            const response = await fetch('/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    card_name: cardName,
                    language: language,
                    condition: condition
                })
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'Search failed');
            }
            
            if (data.success) {
                displayResults(data);
            } else {
                throw new Error(data.error || 'Unknown error occurred');
            }
            
        } catch (error) {
            console.error('Search error:', error);
            showError(error.message || 'An error occurred while searching');
        } finally {
            setLoading(false);
        }
    });
    
    function setLoading(isLoading) {
        searchBtn.disabled = isLoading;
        if (isLoading) {
            btnText.classList.add('hidden');
            btnLoader.classList.remove('hidden');
        } else {
            btnText.classList.remove('hidden');
            btnLoader.classList.add('hidden');
        }
    }
    
    function hideAllSections() {
        resultsSection.classList.add('hidden');
        errorSection.classList.add('hidden');
        noResultsSection.classList.add('hidden');
    }
    
    function showError(message) {
        hideAllSections();
        errorSection.textContent = '❌ Error: ' + message;
        errorSection.classList.remove('hidden');
    }
    
    function displayResults(data) {
        hideAllSections();
        
        // Check if we have any sources
        if (!data.sources || data.sources.length === 0) {
            noResultsSection.classList.remove('hidden');
            return;
        }
        
        // Display card info
        const cardInfo = document.getElementById('cardInfo');
        cardInfo.innerHTML = `
            <p><strong>Card:</strong> ${escapeHtml(data.card_name)}</p>
            <p><strong>Language:</strong> ${escapeHtml(data.language)}</p>
            <p><strong>Condition:</strong> ${escapeHtml(data.condition)}</p>
        `;
        
        // Display average price
        const averageBox = document.getElementById('averagePrice');
        if (data.average_price) {
            averageBox.innerHTML = `
                <div class="label">Overall Average Price</div>
                <div class="price">$${data.average_price.toFixed(2)} ${data.currency || 'USD'}</div>
                ${data.price_range ? `
                    <div class="range">
                        Range: $${data.price_range.min.toFixed(2)} - $${data.price_range.max.toFixed(2)}
                    </div>
                ` : ''}
            `;
        } else {
            averageBox.innerHTML = `
                <div class="label">No average price available</div>
            `;
        }
        
        // Display source results
        const sourceResults = document.getElementById('sourceResults');
        sourceResults.innerHTML = '';
        
        data.sources.forEach(source => {
            const sourceCard = document.createElement('div');
            sourceCard.className = 'source-card';
            
            let detailsHtml = '';
            if (source.source === 'eBay' && source.sample_size) {
                detailsHtml = `<div class="source-details">Based on ${source.sample_size} sold items</div>`;
            } else if (source.details) {
                const details = [];
                if (source.details.market_price) {
                    details.push(`Market: $${source.details.market_price.toFixed(2)}`);
                }
                if (source.details.low_price) {
                    details.push(`Low: $${source.details.low_price.toFixed(2)}`);
                }
                if (source.details.high_price) {
                    details.push(`High: $${source.details.high_price.toFixed(2)}`);
                }
                if (details.length > 0) {
                    detailsHtml = `<div class="source-details">${details.join(' • ')}</div>`;
                }
            }
            
            sourceCard.innerHTML = `
                <div class="source-name">${escapeHtml(source.source)}</div>
                <div class="source-price">$${source.average_price.toFixed(2)} ${source.currency || 'USD'}</div>
                ${detailsHtml}
            `;
            
            sourceResults.appendChild(sourceCard);
        });
        
        // Show results
        resultsSection.classList.remove('hidden');
        
        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
    
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
});
