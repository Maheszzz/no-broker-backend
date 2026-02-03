
    """Schema for updating an existing contact (all fields optional)."""
    name_: Optional[str] = Field(None, min_length=1, max_length=100, alias="name")
    phone: Optional[str] = Field(None, min_length=10, max_length=15)
    email: Optional[EmailStr] = Field(None, max_length=150)
    message: Optional[str] = Field(None, max_length=250)
    status: Optional[ContactStatus] = None

    model_config = {"populate_by_name": True}




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