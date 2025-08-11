from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class TickerPriceItem(BaseModel):
    """Single price data item"""
    date: Optional[datetime] = Field(None, description="Date and time")
    open: Optional[float] = Field(None, description="Opening price")
    high: Optional[float] = Field(None, description="Highest price")
    low: Optional[float] = Field(None, description="Lowest price")
    close: Optional[float] = Field(None, description="Closing price")
    volume: Optional[int] = Field(None, description="Trading volume")
    dividends: Optional[float] = Field(None, description="Dividends")
    stock_splits: Optional[float] = Field(None, description="Stock splits")
