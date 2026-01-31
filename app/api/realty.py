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
    query = db.query(Contact)
    
    if status:
        query = query.filter(Contact.status == status)
    
    contacts = query.offset(skip).limit(limit).all()
    return contacts


@realty_router.get("/realty/contacts/{contact_id}", response_model=ContactResponse)
def get_contact(contact_id: int, db: Session = Depends(get_mysql_db)):
    """Get a specific contact by ID"""
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contact with ID {contact_id} not found"
        )
    return contact


@realty_router.post("/realty/contacts", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
def create_contact(contact: ContactCreate, db: Session = Depends(get_mysql_db)):
    """Create a new contact"""
    db_contact = Contact(**contact.model_dump())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


@realty_router.put("/realty/contacts/{contact_id}", response_model=ContactResponse)
def update_contact(contact_id: int, contact: ContactUpdate, db: Session = Depends(get_mysql_db)):
    """Update an existing contact"""
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not db_contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contact with ID {contact_id} not found"
        )
    
    # Update only provided fields
    for field, value in contact.model_dump(exclude_unset=True).items():
        setattr(db_contact, field, value)
    
    db.commit()
    db.refresh(db_contact)
    return db_contact


@realty_router.delete("/realty/contacts/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(contact_id: int, db: Session = Depends(get_mysql_db)):
    """Delete a contact"""
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not db_contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contact with ID {contact_id} not found"
        )
    
    db.delete(db_contact)
    db.commit()
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
    query = db.query(Property)
    
    if property_type:
        query = query.filter(Property.property_type == property_type)
    if listing_type:
        query = query.filter(Property.listing_type == listing_type)
    if is_available is not None:
        query = query.filter(Property.is_available == is_available)
    
    properties = query.offset(skip).limit(limit).all()
    return properties


@realty_router.get("/realty/properties/{property_id}", response_model=PropertyResponse)
def get_property(property_id: int, db: Session = Depends(get_mysql_db)):
    """Get a specific property by ID with its images"""
    property = db.query(Property).filter(Property.id == property_id).first()
    if not property:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Property with ID {property_id} not found"
        )
    return property


@realty_router.post("/realty/properties", response_model=PropertyResponse, status_code=status.HTTP_201_CREATED)
def create_property(property: PropertyCreate, db: Session = Depends(get_mysql_db)):
    """Create a new property"""
    db_property = Property(**property.model_dump())
    db.add(db_property)
    db.commit()
    db.refresh(db_property)
    return db_property


@realty_router.put("/realty/properties/{property_id}", response_model=PropertyResponse)
def update_property(property_id: int, property: PropertyUpdate, db: Session = Depends(get_mysql_db)):
    """Update an existing property"""
    db_property = db.query(Property).filter(Property.id == property_id).first()
    if not db_property:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Property with ID {property_id} not found"
        )
    
    # Update only provided fields
    for field, value in property.model_dump(exclude_unset=True).items():
        setattr(db_property, field, value)
    
    db.commit()
    db.refresh(db_property)
    return db_property


@realty_router.delete("/realty/properties/{property_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_property(property_id: int, db: Session = Depends(get_mysql_db)):
    """Delete a property and its associated images"""
    db_property = db.query(Property).filter(Property.id == property_id).first()
    if not db_property:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Property with ID {property_id} not found"
        )
    
    db.delete(db_property)
    db.commit()
    return None


# ==================== PROPERTY IMAGE ENDPOINTS ====================

@realty_router.get("/realty/properties/{property_id}/images", response_model=List[PropertyImageResponse])
def list_property_images(property_id: int, db: Session = Depends(get_mysql_db)):
    """List all images for a specific property"""
    # Verify property exists
    property = db.query(Property).filter(Property.id == property_id).first()
    if not property:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Property with ID {property_id} not found"
        )
    
    images = db.query(PropertyImage).filter(
        PropertyImage.property_id == property_id
    ).order_by(PropertyImage.sort_order).all()
    return images


@realty_router.post("/realty/properties/{property_id}/images", response_model=PropertyImageResponse, status_code=status.HTTP_201_CREATED)
def add_property_image(property_id: int, image: PropertyImageCreate, db: Session = Depends(get_mysql_db)):
    """Add a new image to a property"""
    # Verify property exists
    property = db.query(Property).filter(Property.id == property_id).first()
    if not property:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Property with ID {property_id} not found"
        )
    
    db_image = PropertyImage(**image.model_dump(), property_id=property_id)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image


@realty_router.put("/realty/images/{image_id}", response_model=PropertyImageResponse)
def update_property_image(image_id: int, image: PropertyImageUpdate, db: Session = Depends(get_mysql_db)):
    """Update a property image"""
    db_image = db.query(PropertyImage).filter(PropertyImage.id == image_id).first()
    if not db_image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Image with ID {image_id} not found"
        )
    
    # Update only provided fields
    for field, value in image.model_dump(exclude_unset=True).items():
        setattr(db_image, field, value)
    
    db.commit()
    db.refresh(db_image)
    return db_image


@realty_router.delete("/realty/images/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_property_image(image_id: int, db: Session = Depends(get_mysql_db)):
    """Delete a property image"""
    db_image = db.query(PropertyImage).filter(PropertyImage.id == image_id).first()
    if not db_image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Image with ID {image_id} not found"
        )
    
    db.delete(db_image)
    db.commit()
    return None
