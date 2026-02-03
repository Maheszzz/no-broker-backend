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
    