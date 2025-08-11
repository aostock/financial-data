from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class InsiderTransactionItem(BaseModel):
    """Insider transaction item"""
    shares: Optional[int] = Field(None, description="Number of shares")
    value: Optional[float] = Field(None, description="Transaction value")
    url: Optional[str] = Field(None, description="URL to transaction details")
    text: Optional[str] = Field(None, description="Transaction description text")
    insider: Optional[str] = Field(None, description="Name of the insider")
    position: Optional[str] = Field(None, description="Position of the insider")
    transaction: Optional[str] = Field(None, description="Type of transaction")
    start_date: Optional[datetime] = Field(None, description="Transaction start date")
    ownership: Optional[str] = Field(None, description="Ownership type")
