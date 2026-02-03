"""Realty API endpoints for Contacts, Properties, and Property Images."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional

from app.configs.db_config import get_mysql_db
from app.dto.realty import (
    ContactCreate, ContactUpdate, ContactResponse,
    PropertyCreate, PropertyUpdate, PropertyResponse,
    PropertyImageCreate, PropertyImageUpdate, PropertyImageResponse,
    PropertyType, ListingType, ContactStatus
)
from app.repo import realty as realty_repo
from app.core.exceptions import NotFoundException, DatabaseError

realty_router = APIRouter(tags=["Realty"])


# ==================== CONTACT ENDPOINTS ====================

@realty_router.get("/realty/contacts", response_model=List[ContactResponse])
def list_contacts(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of records to return"),
    status: Optional[ContactStatus] = Query(None, description="Filter by contact status"),
    db: Session = Depends(get_mysql_db)
):
    """
    List all contacts with pagination and optional status filter.
    
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum records to return (default: 100, max: 100)
    - **status**: Filter by status (new, contacted, closed)
    """
    contacts = realty_repo.get_contacts(
        db, skip=skip, limit=limit, 
        status=status.value if status else None
    )
    return contacts


@realty_router.get("/realty/contacts/{contact_id}", response_model=ContactResponse)
def get_contact(contact_id: int, db: Session = Depends(get_mysql_db)):
    """
    Get a specific contact by ID.
    
    - **contact_id**: The unique identifier of the contact
    """
    contact = realty_repo.get_contact_by_id(db, contact_id)
    if not contact:
        raise NotFoundException("Contact", contact_id)
    return contact


@realty_router.post("/realty/contacts", response_model=ContactResponse, status_code=201)
def create_contact(contact: ContactCreate, db: Session = Depends(get_mysql_db)):
    """
    Create a new contact.
    
    - **name**: Contact name (required, 1-100 chars)
    - **phone**: Phone number (required, 10-15 chars)
    - **email**: Email address (required, valid email format)
    - **message**: Message content (required, max 250 chars)
    - **status**: Contact status (optional, defaults to 'new')
    """
    try:
        return realty_repo.create_contact(db, contact.model_dump(by_alias=False))
    except SQLAlchemyError as e:
        raise DatabaseError(f"Failed to create contact: {str(e)}")


@realty_router.put("/realty/contacts/{contact_id}", response_model=ContactResponse)
def update_contact(
    contact_id: int,
    contact: ContactUpdate,
    db: Session = Depends(get_mysql_db)
):
    """
    Update an existing contact.
    
    - **contact_id**: The unique identifier of the contact
    - Only provided fields will be updated
    """
    db_contact = realty_repo.get_contact_by_id(db, contact_id)
    if not db_contact:
        raise NotFoundException("Contact", contact_id)
    
    try:
        return realty_repo.update_contact(
            db, db_contact, 
            contact.model_dump(exclude_unset=True, by_alias=False)
        )
    except SQLAlchemyError as e:
        raise DatabaseError(f"Failed to update contact: {str(e)}")


@realty_router.delete("/realty/contacts/{contact_id}", status_code=204)
def delete_contact(contact_id: int, db: Session = Depends(get_mysql_db)):
    """
    Delete a contact.
    
    - **contact_id**: The unique identifier of the contact
    """
    db_contact = realty_repo.get_contact_by_id(db, contact_id)
    if not db_contact:
        raise NotFoundException("Contact", contact_id)
    
    try:
        realty_repo.delete_contact(db, db_contact)
    except SQLAlchemyError as e:
        raise DatabaseError(f"Failed to delete contact: {str(e)}")
    return None


# ==================== PROPERTY ENDPOINTS ====================

@realty_router.get("/realty/properties", response_model=List[PropertyResponse])
def list_properties(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of records to return"),
    property_type: Optional[PropertyType] = Query(None, description="Filter by property type"),
    listing_type: Optional[ListingType] = Query(None, description="Filter by listing type"),
    is_available: Optional[bool] = Query(None, description="Filter by availability"),
    db: Session = Depends(get_mysql_db)
):
    """
    List all properties with pagination and filters.
    
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum records to return (default: 100, max: 100)
    - **property_type**: Filter by type (PG, 1RK, 1BHK, 2BHK)
    - **listing_type**: Filter by listing (buy, rent)
    - **is_available**: Filter by availability (true/false)
    """
    properties = realty_repo.get_properties(
        db, skip=skip, limit=limit,
        property_type=property_type.value if property_type else None,
        listing_type=listing_type.value if listing_type else None,
        is_available=is_available
    )
    return properties


@realty_router.get("/realty/properties/{property_id}", response_model=PropertyResponse)
def get_property(property_id: int, db: Session = Depends(get_mysql_db)):
    """
    Get a specific property by ID with its images.
    
    - **property_id**: The unique identifier of the property
    """
    property_obj = realty_repo.get_property_by_id(db, property_id)
    if not property_obj:
        raise NotFoundException("Property", property_id)
    return property_obj


@realty_router.post("/realty/properties", response_model=PropertyResponse, status_code=201)
def create_property(property_data: PropertyCreate, db: Session = Depends(get_mysql_db)):
    """
    Create a new property.
    
    - **property_name**: Property name (required)
    - **location**: Location (required)
    - **property_type**: Type (PG, 1RK, 1BHK, 2BHK - required)
    - **listing_type**: Listing type (buy, rent - defaults to rent)
    """
    try:
        return realty_repo.create_property(db, property_data.model_dump())
    except SQLAlchemyError as e:
        raise DatabaseError(f"Failed to create property: {str(e)}")


@realty_router.put("/realty/properties/{property_id}", response_model=PropertyResponse)
def update_property(
    property_id: int,
    property_data: PropertyUpdate,
    db: Session = Depends(get_mysql_db)
):
    """
    Update an existing property.
    
    - **property_id**: The unique identifier of the property
    - Only provided fields will be updated
    """
    db_property = realty_repo.get_property_by_id(db, property_id)
    if not db_property:
        raise NotFoundException("Property", property_id)
    
    try:
        return realty_repo.update_property(
            db, db_property,
            property_data.model_dump(exclude_unset=True)
        )
    except SQLAlchemyError as e:
        raise DatabaseError(f"Failed to update property: {str(e)}")


@realty_router.delete("/realty/properties/{property_id}", status_code=204)
def delete_property(property_id: int, db: Session = Depends(get_mysql_db)):
    """
    Delete a property and its associated images.
    
    - **property_id**: The unique identifier of the property
    """
    db_property = realty_repo.get_property_by_id(db, property_id)
    if not db_property:
        raise NotFoundException("Property", property_id)
    
    try:
        realty_repo.delete_property(db, db_property)
    except SQLAlchemyError as e:
        raise DatabaseError(f"Failed to delete property: {str(e)}")
    return None


# ==================== PROPERTY IMAGE ENDPOINTS ====================

@realty_router.get("/realty/properties/{property_id}/images", response_model=List[PropertyImageResponse])
def list_property_images(property_id: int, db: Session = Depends(get_mysql_db)):
    """
    List all images for a specific property.
    
    - **property_id**: The unique identifier of the property
    """
    # Verify property exists
    property_obj = realty_repo.get_property_by_id(db, property_id)
    if not property_obj:
        raise NotFoundException("Property", property_id)
    
    return realty_repo.get_property_images(db, property_id)


@realty_router.post("/realty/properties/{property_id}/images", response_model=PropertyImageResponse, status_code=201)
def add_property_image(
    property_id: int,
    image: PropertyImageCreate,
    db: Session = Depends(get_mysql_db)
):
    """
    Add a new image to a property.
    
    - **property_id**: The unique identifier of the property
    - **image_url**: URL of the image (required)
    - **is_primary**: Whether this is the primary image (default: false)
    - **sort_order**: Display order (default: 0)
    """
    # Verify property exists
    property_obj = realty_repo.get_property_by_id(db, property_id)
    if not property_obj:
        raise NotFoundException("Property", property_id)
    
    try:
        return realty_repo.create_property_image(db, image.model_dump(), property_id)
    except SQLAlchemyError as e:
        raise DatabaseError(f"Failed to add property image: {str(e)}")


@realty_router.put("/realty/images/{image_id}", response_model=PropertyImageResponse)
def update_property_image(
    image_id: int,
    image: PropertyImageUpdate,
    db: Session = Depends(get_mysql_db)
):
    """
    Update a property image.
    
    - **image_id**: The unique identifier of the image
    - Only provided fields will be updated
    """
    db_image = realty_repo.get_property_image_by_id(db, image_id)
    if not db_image:
        raise NotFoundException("Image", image_id)
    
    try:
        return realty_repo.update_property_image(
            db, db_image,
            image.model_dump(exclude_unset=True)
        )
    except SQLAlchemyError as e:
        raise DatabaseError(f"Failed to update property image: {str(e)}")


@realty_router.delete("/realty/images/{image_id}", status_code=204)
def delete_property_image(image_id: int, db: Session = Depends(get_mysql_db)):
    """
    Delete a property image.
    
    - **image_id**: The unique identifier of the image
    """
    db_image = realty_repo.get_property_image_by_id(db, image_id)
    if not db_image:
        raise NotFoundException("Image", image_id)
    
    try:
        realty_repo.delete_property_image(db, db_image)
    except SQLAlchemyError as e:
        raise DatabaseError(f"Failed to delete property image: {str(e)}")
    return None
