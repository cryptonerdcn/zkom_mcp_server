"""
Service for interacting with Coinbase API
"""
import os
import time
import logging
import httpx
from typing import Dict, Optional, List, Union, Any
from pydantic import ValidationError

from app.models.crypto import ExchangeRatesResponse, CryptoPrice

logger = logging.getLogger(__name__)

COINBASE_API_URL = os.getenv("COINBASE_API_URL", "https://api.coinbase.com/v2/exchange-rates")
CACHE_TTL = int(os.getenv("CACHE_TTL", "60"))  # Cache time-to-live in seconds


class CoinbaseClient:
    """Client for interacting with the Coinbase API"""
    
    def __init__(self):
        self._cache = {}
        self._last_update = {}
    
    async def get_exchange_rates(self, base_currency: str = "USD") -> Dict[str, float]:
        """
        Get exchange rates from Coinbase API
        
        Args:
            base_currency: Base currency for the exchange rates
            
        Returns:
            Dictionary of exchange rates
        """
        # Check cache first
        current_time = time.time()
        if (
            base_currency in self._cache 
            and current_time - self._last_update.get(base_currency, 0) < CACHE_TTL
        ):
            logger.debug(f"Using cached exchange rates for {base_currency}")
            return self._cache[base_currency]
            
        # Make API request
        url = f"{COINBASE_API_URL}?currency={base_currency}"
        logger.info(f"Fetching exchange rates from Coinbase API: {url}")
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                response.raise_for_status()
                
                # Parse response
                data = response.json()
                exchange_rates = ExchangeRatesResponse(**data)
                
                # Convert string rates to float
                rates = {
                    symbol: float(rate) 
                    for symbol, rate in exchange_rates.data.rates.items()
                }
                
                # Update cache
                self._cache[base_currency] = rates
                self._last_update[base_currency] = current_time
                
                return rates
                
        except httpx.RequestError as e:
            logger.error(f"Error fetching exchange rates: {e}")
            raise
        except ValidationError as e:
            logger.error(f"Error parsing exchange rates response: {e}")
            raise
    
    async def get_crypto_price(self, symbol: str, base_currency: str = "USD") -> Optional[CryptoPrice]:
        """
        Get price of a cryptocurrency in the specified base currency
        
        Args:
            symbol: Symbol of the cryptocurrency (e.g., BTC)
            base_currency: Base currency for the price (e.g., USD)
            
        Returns:
            CryptoPrice object with the price information
        """
        try:
            # For Coinbase, we need to get the rates in terms of the crypto
            # then calculate the inverse for the real price
            base_rates = await self.get_exchange_rates(symbol)
            
            if base_currency not in base_rates:
                logger.warning(f"Currency {base_currency} not found in exchange rates")
                return None
                
            # The rate is how many base_currency units you get for 1 unit of symbol
            rate = base_rates[base_currency]
            
            # Calculate the price (inverse of the rate)
            price = 1.0 / float(rate) if float(rate) != 0 else 0
            
            return CryptoPrice(
                symbol=symbol,
                price=price,
                base_currency=base_currency,
                timestamp=int(time.time() * 1000)
            )
            
        except Exception as e:
            logger.error(f"Error getting price for {symbol}/{base_currency}: {e}")
            return None
    
    async def get_multiple_prices(
        self, symbols: List[str], base_currency: str = "USD"
    ) -> List[CryptoPrice]:
        """
        Get prices for multiple cryptocurrencies
        
        Args:
            symbols: List of cryptocurrency symbols
            base_currency: Base currency for the prices
            
        Returns:
            List of CryptoPrice objects
        """
        results = []
        for symbol in symbols:
            price = await self.get_crypto_price(symbol, base_currency)
            if price:
                results.append(price)
        
        return results


# Create singleton instance
coinbase_client = CoinbaseClient() 