"""
Database Schemas for Geo Transect CMS

Each Pydantic model represents a MongoDB collection. The collection name is the lowercase of the class name.
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

class Service(BaseModel):
    title: str = Field(..., description="Service title")
    slug: str = Field(..., description="URL-friendly slug")
    summary: str = Field(..., description="Short summary")
    description: Optional[str] = Field(None, description="Detailed description")
    icon: Optional[str] = Field(None, description="Icon name or URL")
    cover_image: Optional[str] = Field(None, description="Cover image URL")

class Project(BaseModel):
    title: str = Field(...)
    slug: str = Field(...)
    sector: Optional[str] = Field(None, description="Sector or category")
    summary: str = Field(...)
    body: Optional[str] = Field(None)
    location: Optional[str] = Field(None)
    images: Optional[List[str]] = Field(default_factory=list)
    services: Optional[List[str]] = Field(default_factory=list, description="Related service slugs")
    map_embed: Optional[str] = Field(None, description="Optional map iframe embed HTML")

class TeamMember(BaseModel):
    name: str
    role: str
    expertise: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    photo_url: Optional[str] = None

class Inquiry(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    subject: str
    message: str

# Example retained for reference of collection naming convention
class User(BaseModel):
    name: str
    email: EmailStr
    is_active: bool = True

class Product(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    category: str
    in_stock: bool = True
