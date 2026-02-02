from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.configs.db_config import get_mysql_db
from app.models.realty import Contact, Property, PropertyImage
from app.schemas.realty import (
    ContactCreate, ContactUpdate, ContactResponse,
    PropertyCreate, PropertyUpdate, PropertyResponse,
    PropertyImageCreate, PropertyImageUpdate, PropertyImageResponse
)
from app.repo import realty as realty_repo
from app.dependencies.auth import get_current_user
from app.models.user import User

realty_router = APIRouter(tags=["Realty"])


# ==================== CONTACT ENDPOINTS ====================

@realty_router.get("/realty/contacts", response_model=List[ContactResponse])
def list_contacts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    status: Optional[str] = None,
    db: Session = Depends(get_mysql_db)
):
    """List all contacts with pagination and optional status filter"""
    contacts = realty_repo.get_contacts(db, skip=skip, limit=limit, status=status)
    return contacts


@realty_router.get("/realty/contacts/{contact_id}", response_model=ContactResponse)
def get_contact(contact_id: int, db: Session = Depends(get_mysql_db)):
    """Get a specific contact by ID"""
    contact = realty_repo.get_contact_by_id(db, contact_id)
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contact with ID {contact_id} not found"
        )
    return contact


@realty_router.post("/realty/contacts", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
def create_contact(
    contact: ContactCreate, 
    db: Session = Depends(get_mysql_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new contact"""
    return realty_repo.create_contact(db, contact.model_dump())


@realty_router.put("/realty/contacts/{contact_id}", response_model=ContactResponse)
def update_contact(
    contact_id: int, 
    contact: ContactUpdate, 
    db: Session = Depends(get_mysql_db),
    current_user: User = Depends(get_current_user)
):
    """Update an existing contact"""
    db_contact = realty_repo.get_contact_by_id(db, contact_id)
    if not db_contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contact with ID {contact_id} not found"
        )
    
    return realty_repo.update_contact(db, db_contact, contact.model_dump(exclude_unset=True))


@realty_router.delete("/realty/contacts/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(
    contact_id: int, 
    db: Session = Depends(get_mysql_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a contact"""
    db_contact = realty_repo.get_contact_by_id(db, contact_id)
    if not db_contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contact with ID {contact_id} not found"
        )
    
    realty_repo.delete_contact(db, db_contact)
    return None


# ==================== PROPERTY ENDPOINTS ====================

@realty_router.get("/realty/properties", response_model=List[PropertyResponse])
def list_properties(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    property_type: Optional[str] = None,
    listing_type: Optional[str] = None,
    is_available: Optional[bool] = None,
    db: Session = Depends(get_mysql_db)
):
    """List all properties with pagination and filters"""
    properties = realty_repo.get_properties(
        db, skip=skip, limit=limit, 
        property_type=property_type, 
        listing_type=listing_type, 
        is_available=is_available
    )
    return properties


@realty_router.get("/realty/properties/{property_id}", response_model=PropertyResponse)
def get_property(property_id: int, db: Session = Depends(get_mysql_db)):
    """Get a specific property by ID with its images"""
    property = realty_repo.get_property_by_id(db, property_id)
    if not property:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Property with ID {property_id} not found"
        )
    return property


@realty_router.post("/realty/properties", response_model=PropertyResponse, status_code=status.HTTP_201_CREATED)
def create_property(
    property: PropertyCreate, 
    db: Session = Depends(get_mysql_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new property"""
    return realty_repo.create_property(db, property.model_dump())


@realty_router.put("/realty/properties/{property_id}", response_model=PropertyResponse)
def update_property(
    property_id: int, 
    property: PropertyUpdate, 
    db: Session = Depends(get_mysql_db),
    current_user: User = Depends(get_current_user)
):
    """Update an existing property"""
    db_property = realty_repo.get_property_by_id(db, property_id)
    if not db_property:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Property with ID {property_id} not found"
        )
    
    return realty_repo.update_property(db, db_property, property.model_dump(exclude_unset=True))


@realty_router.delete("/realty/properties/{property_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_property(
    property_id: int, 
    db: Session = Depends(get_mysql_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a property and its associated images"""
    db_property = realty_repo.get_property_by_id(db, property_id)
    if not db_property:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Property with ID {property_id} not found"
        )
    
    realty_repo.delete_property(db, db_property)
    return None


# ==================== PROPERTY IMAGE ENDPOINTS ====================

@realty_router.get("/realty/properties/{property_id}/images", response_model=List[PropertyImageResponse])
def list_property_images(property_id: int, db: Session = Depends(get_mysql_db)):
    """List all images for a specific property"""
    # Verify property exists
    property = realty_repo.get_property_by_id(db, property_id)
    if not property:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Property with ID {property_id} not found"
        )
    
    return realty_repo.get_property_images(db, property_id)


@realty_router.post("/realty/properties/{property_id}/images", response_model=PropertyImageResponse, status_code=status.HTTP_201_CREATED)
def add_property_image(
    property_id: int, 
    image: PropertyImageCreate, 
    db: Session = Depends(get_mysql_db),
    current_user: User = Depends(get_current_user)
):
    """Add a new image to a property"""
    # Verify property exists
    property = realty_repo.get_property_by_id(db, property_id)
    if not property:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Property with ID {property_id} not found"
        )
    
    return realty_repo.create_property_image(db, image.model_dump(), property_id)


@realty_router.put("/realty/images/{image_id}", response_model=PropertyImageResponse)
def update_property_image(
    image_id: int, 
    image: PropertyImageUpdate, 
    db: Session = Depends(get_mysql_db),
    current_user: User = Depends(get_current_user)
):
    """Update a property image"""
    db_image = realty_repo.get_property_image_by_id(db, image_id)
    if not db_image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Image with ID {image_id} not found"
        )
    
    return realty_repo.update_property_image(db, db_image, image.model_dump(exclude_unset=True))


@realty_router.delete("/realty/images/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_property_image(
    image_id: int, 
    db: Session = Depends(get_mysql_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a property image"""
    db_image = realty_repo.get_property_image_by_id(db, image_id)
    if not db_image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Image with ID {image_id} not found"
        )
    
    realty_repo.delete_property_image(db, db_image)
    return None
