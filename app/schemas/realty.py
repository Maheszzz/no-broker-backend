from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from enum import Enum


# Enums
class ContactStatus(str, Enum):
    new = "new"
    contacted = "contacted"
    closed = "closed"


class PropertyType(str, Enum):
    PG = "PG"
    ONE_RK = "1RK"
    ONE_BHK = "1BHK"
    TWO_BHK = "2BHK"


class Furnishing(str, Enum):
    fully_furnished = "fully_furnished"
    semi_furnished = "semi_furnished"
    unfurnished = "unfurnished"


class ListingType(str, Enum):
    buy = "buy"
    rent = "rent"


# Contact Schemas
class ContactBase(BaseModel):
    name_: str = Field(..., min_length=1, max_length=100, alias="name")
    phone: str = Field(..., min_length=10, max_length=15)
    email: EmailStr = Field(..., min_length=5, max_length=150)
    message: str = Field(..., max_length=250)
    status: Optional[ContactStatus] = ContactStatus.new


class ContactCreate(ContactBase):
    pass


class ContactUpdate(BaseModel):
    name_: Optional[str] = Field(None, min_length=1, max_length=100, alias="name")
    phone: Optional[str] = Field(None, min_length=10, max_length=15)
    email: Optional[EmailStr] = Field(None, min_length=5, max_length=150)
    message: Optional[str] = Field(None, max_length=250)
    status: Optional[ContactStatus] = None


class ContactResponse(ContactBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        populate_by_name = True


# Property Image Schemas
class PropertyImageBase(BaseModel):
    image_url: str = Field(..., max_length=500)
    is_primary: bool = False
    sort_order: int = 0


class PropertyImageCreate(PropertyImageBase):
    pass


class PropertyImageUpdate(BaseModel):
    image_url: Optional[str] = Field(None, max_length=500)
    is_primary: Optional[bool] = None
    sort_order: Optional[int] = None


class PropertyImageResponse(PropertyImageBase):
    id: int
    property_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Property Schemas
class PropertyBase(BaseModel):
    property_name: str = Field(..., max_length=150)
    location: str = Field(..., max_length=150)
    map_link: Optional[str] = Field(None, max_length=500)
    description: Optional[str] = None
    property_type: PropertyType
    furnishing: Optional[Furnishing] = Furnishing.unfurnished
    private_price: Optional[int] = None
    single_price: Optional[int] = None
    double_price: Optional[int] = None
    triple_price: Optional[int] = None
    listing_type: ListingType = ListingType.rent
    is_available: Optional[bool] = True


class PropertyCreate(PropertyBase):
    pass


class PropertyUpdate(BaseModel):
    property_name: Optional[str] = Field(None, max_length=150)
    location: Optional[str] = Field(None, max_length=150)
    map_link: Optional[str] = Field(None, max_length=500)
    description: Optional[str] = None
    property_type: Optional[PropertyType] = None
    furnishing: Optional[Furnishing] = None
    private_price: Optional[int] = None
    single_price: Optional[int] = None
    double_price: Optional[int] = None
    triple_price: Optional[int] = None
    listing_type: Optional[ListingType] = None
    is_available: Optional[bool] = None


class PropertyResponse(PropertyBase):
    id: int
    created_at: datetime
    updated_at: datetime
    images: List[PropertyImageResponse] = []
    
    class Config:
        from_attributes = True
