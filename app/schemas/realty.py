"""Pydantic schemas for Realty models with validation."""
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, field_validator
from enum import Enum


# ==================== ENUMS ====================

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


# ==================== CONTACT SCHEMAS ====================

class ContactBase(BaseModel):
    """Base schema for Contact with validation."""
    name_: str = Field(..., min_length=1, max_length=100, alias="name")
    phone: str = Field(..., min_length=10, max_length=15)
    email: EmailStr = Field(..., max_length=150)
    message: str = Field(..., max_length=250)
    status: Optional[ContactStatus] = ContactStatus.new

    model_config = {"populate_by_name": True}


class ContactCreate(ContactBase):
    """Schema for creating a new contact."""
    pass


class ContactUpdate(BaseModel):
    """Schema for updating an existing contact (all fields optional)."""
    name_: Optional[str] = Field(None, min_length=1, max_length=100, alias="name")
    phone: Optional[str] = Field(None, min_length=10, max_length=15)
    email: Optional[EmailStr] = Field(None, max_length=150)
    message: Optional[str] = Field(None, max_length=250)
    status: Optional[ContactStatus] = None

    model_config = {"populate_by_name": True}


class ContactResponse(ContactBase):
    """Schema for contact response with ID and timestamps."""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True, "populate_by_name": True}


# ==================== PROPERTY IMAGE SCHEMAS ====================

class PropertyImageBase(BaseModel):
    """Base schema for PropertyImage."""
    image_url: str = Field(..., max_length=500)
    is_primary: bool = False
    sort_order: int = Field(default=0, ge=0)


class PropertyImageCreate(PropertyImageBase):
    """Schema for creating a new property image."""
    pass


class PropertyImageUpdate(BaseModel):
    """Schema for updating an existing property image."""
    image_url: Optional[str] = Field(None, max_length=500)
    is_primary: Optional[bool] = None
    sort_order: Optional[int] = Field(None, ge=0)


class PropertyImageResponse(PropertyImageBase):
    """Schema for property image response with ID and timestamps."""
    id: int
    property_id: int
    created_at: datetime

    model_config = {"from_attributes": True}


# ==================== PROPERTY SCHEMAS ====================

class PropertyBase(BaseModel):
    """Base schema for Property with validation."""
    property_name: str = Field(..., min_length=1, max_length=150)
    location: str = Field(..., min_length=1, max_length=150)
    phone: str = Field(..., min_length=10, max_length=15)
    map_link: Optional[str] = Field(None, max_length=500)
    description: Optional[str] = None
    property_type: PropertyType
    furnishing: Optional[Furnishing] = Furnishing.unfurnished
    private_price: Optional[float] = Field(None, ge=0)
    single_price: Optional[float] = Field(None, ge=0)
    double_price: Optional[float] = Field(None, ge=0)
    triple_price: Optional[float] = Field(None, ge=0)
    listing_type: ListingType = ListingType.rent
    is_available: Optional[bool] = True

    @field_validator('map_link')
    @classmethod
    def validate_map_link(cls, v: Optional[str]) -> Optional[str]:
        """Validate that map_link is a valid URL if provided."""
        if v is not None and not v.startswith(('http://', 'https://')):
            raise ValueError('map_link must be a valid URL starting with http:// or https://')
        return v


class PropertyCreate(PropertyBase):
    """Schema for creating a new property."""
    pass


class PropertyUpdate(BaseModel):
    """Schema for updating an existing property (all fields optional)."""
    property_name: Optional[str] = Field(None, min_length=1, max_length=150)
    location: Optional[str] = Field(None, min_length=1, max_length=150)
    phone: Optional[str] = Field(None, min_length=10, max_length=15)
    map_link: Optional[str] = Field(None, max_length=500)
    description: Optional[str] = None
    property_type: Optional[PropertyType] = None
    furnishing: Optional[Furnishing] = None
    private_price: Optional[float] = Field(None, ge=0)
    single_price: Optional[float] = Field(None, ge=0)
    double_price: Optional[float] = Field(None, ge=0)
    triple_price: Optional[float] = Field(None, ge=0)
    listing_type: Optional[ListingType] = None
    is_available: Optional[bool] = None

    @field_validator('map_link')
    @classmethod
    def validate_map_link(cls, v: Optional[str]) -> Optional[str]:
        """Validate that map_link is a valid URL if provided."""
        if v is not None and not v.startswith(('http://', 'https://')):
            raise ValueError('map_link must be a valid URL starting with http:// or https://')
        return v


class PropertyResponse(PropertyBase):
    """Schema for property response with ID, timestamps, and images."""
    id: int
    created_at: datetime
    updated_at: datetime
    images: List[PropertyImageResponse] = []

    model_config = {"from_attributes": True}
