"""
Cryptocurrency data models
"""
from typing import Dict, Optional, List
from pydantic import BaseModel, Field


class CryptoPriceRequest(BaseModel):
    """Request model for cryptocurrency price lookup"""
    symbol: str = Field(..., description="Symbol of the cryptocurrency (e.g., BTC)")
    base_currency: Optional[str] = Field("USD", description="Base currency for price conversion")


class CryptoPrice(BaseModel):
    """Model for cryptocurrency price data"""
    symbol: str = Field(..., description="Symbol of the cryptocurrency")
    price: float = Field(..., description="Current price in the base currency")
    base_currency: str = Field(..., description="Base currency of the price")
    timestamp: int = Field(..., description="Timestamp of the price data")


class ExchangeRatesResponse(BaseModel):
    """Response model for Coinbase exchange rates API"""
    class Data(BaseModel):
        currency: str
        rates: Dict[str, str]

    data: Data


class CryptoPriceListResponse(BaseModel):
    """Response model for listing multiple cryptocurrency prices"""
    prices: List[CryptoPrice] = Field(..., description="List of cryptocurrency prices")
    count: int = Field(..., description="Number of prices returned")
    timestamp: int = Field(..., description="Timestamp of the response") 