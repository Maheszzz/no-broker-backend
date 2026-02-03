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





    """Schema for contact response with ID and timestamps."""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True, "populate_by_name": True}



