from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class NewsThumbnailResolution(BaseModel):
    """News thumbnail resolution"""
    url: Optional[str] = Field(None, description="Image URL")
    width: Optional[int] = Field(None, description="Width in pixels")
    height: Optional[int] = Field(None, description="Height in pixels")
    tag: Optional[str] = Field(None, description="Tag identifier")


class NewsThumbnail(BaseModel):
    """News thumbnail"""
    original_url: Optional[str] = Field(None, description="Original image URL")
    original_width: Optional[int] = Field(None, description="Original image width")
    original_height: Optional[int] = Field(None, description="Original image height")
    caption: Optional[str] = Field(None, description="Image caption")
    resolutions: Optional[List[NewsThumbnailResolution]] = Field(None, description="List of resolutions")


class NewsProvider(BaseModel):
    """News provider"""
    display_name: Optional[str] = Field(None, description="Display name")
    url: Optional[str] = Field(None, description="Provider URL")


class NewsCanonicalUrl(BaseModel):
    """News canonical URL"""
    url: Optional[str] = Field(None, description="Canonical URL")
    site: Optional[str] = Field(None, description="Site name")
    region: Optional[str] = Field(None, description="Region")
    lang: Optional[str] = Field(None, description="Language")


class NewsClickThroughUrl(BaseModel):
    """News click-through URL"""
    url: Optional[str] = Field(None, description="Click-through URL")
    site: Optional[str] = Field(None, description="Site name")
    region: Optional[str] = Field(None, description="Region")
    lang: Optional[str] = Field(None, description="Language")


class NewsMetadata(BaseModel):
    """News metadata"""
    editors_pick: Optional[bool] = Field(None, description="Editor's pick flag")


class NewsPremiumFinance(BaseModel):
    """News premium finance information"""
    is_premium_news: Optional[bool] = Field(None, description="Whether this is premium news")
    is_premium_free_news: Optional[bool] = Field(None, description="Whether this is free premium news")


class NewsFinance(BaseModel):
    """News finance information"""
    premium_finance: Optional[NewsPremiumFinance] = Field(None, description="Premium finance information")


class StorylineContent(BaseModel):
    """Storyline content"""
    id: Optional[str] = Field(None, description="Content ID")
    content_type: Optional[str] = Field(None, description="Content type")
    is_hosted: Optional[bool] = Field(None, description="Whether content is hosted")
    title: Optional[str] = Field(None, description="Content title")
    thumbnail: Optional[NewsThumbnail] = Field(None, description="Content thumbnail")
    provider: Optional[NewsProvider] = Field(None, description="Content provider")
    preview_url: Optional[str] = Field(None, description="Preview URL")
    provider_content_url: Optional[str] = Field(None, description="Provider content URL")
    canonical_url: Optional[NewsCanonicalUrl] = Field(None, description="Canonical URL")
    click_through_url: Optional[NewsClickThroughUrl] = Field(None, description="Click-through URL")


class StorylineItem(BaseModel):
    """Storyline item"""
    content: Optional[StorylineContent] = Field(None, description="Storyline content")


class NewsItem(BaseModel):
    """Single news item"""
    id: Optional[str] = Field(None, description="News ID")
    content_type: Optional[str] = Field(None, description="Content type")
    title: Optional[str] = Field(None, description="News title")
    description: Optional[str] = Field(None, description="News description")
    summary: Optional[str] = Field(None, description="News summary")
    pub_date: Optional[str] = Field(None, description="Publication date")
    display_time: Optional[str] = Field(None, description="Display time")
    is_hosted: Optional[bool] = Field(None, description="Whether news is hosted")
    bypass_modal: Optional[bool] = Field(None, description="Whether to bypass modal")
    preview_url: Optional[str] = Field(None, description="Preview URL")
    thumbnail: Optional[NewsThumbnail] = Field(None, description="News thumbnail")
    provider: Optional[NewsProvider] = Field(None, description="News provider")
    canonical_url: Optional[NewsCanonicalUrl] = Field(None, description="Canonical URL")
    click_through_url: Optional[NewsClickThroughUrl] = Field(None, description="Click-through URL")
    metadata: Optional[NewsMetadata] = Field(None, description="News metadata")
    finance: Optional[NewsFinance] = Field(None, description="Finance information")
    storyline: Optional[dict] = Field(None, description="Storyline information")

