from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class InsiderRosterHolderItem(BaseModel):
    """Insider roster holder item"""
    name: Optional[str] = Field(None, description="Name of the insider")
    position: Optional[str] = Field(None, description="Position of the insider")
    url: Optional[str] = Field(None, description="URL to the insider's profile")
    most_recent_transaction: Optional[str] = Field(None, description="Most recent transaction type")
    latest_transaction_date: Optional[datetime] = Field(None, description="Latest transaction date")
    shares_owned_directly: Optional[int] = Field(None, description="Number of shares owned directly")
    position_direct_date: Optional[datetime] = Field(None, description="Date of direct position")

