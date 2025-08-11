from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class InsiderPurchaseItem(BaseModel):
    """Insider purchase item"""
    insider_purchases_last6m: Optional[str] = Field(None, description="Insider purchases in the last 6 months")
    shares: Optional[float] = Field(None, description="Number of shares")
    trans: Optional[float] = Field(None, description="Number of transactions")

