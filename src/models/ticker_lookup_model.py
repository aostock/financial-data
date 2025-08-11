from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class LookupItem(BaseModel):
    """Lookup item"""
    symbol: Optional[str] = Field(None, description="Stock symbol")
    exchange: Optional[str] = Field(None, description="Exchange code")
    industry_link: Optional[str] = Field(None, description="Industry link")
    industry_name: Optional[str] = Field(None, description="Industry name")
    quote_type: Optional[str] = Field(None, description="Quote type")
    rank: Optional[float] = Field(None, description="Ranking")
    regular_market_change: Optional[float] = Field(None, description="Regular market change")
    regular_market_percent_change: Optional[float] = Field(None, description="Regular market percentage change")
    regular_market_price: Optional[float] = Field(None, description="Regular market price")
    short_name: Optional[str] = Field(None, description="Short name")
    time: Optional[str] = Field(None, description="Timestamp")
