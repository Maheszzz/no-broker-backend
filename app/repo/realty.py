"""Repository layer for Realty models with transaction safety."""
from sqlalchemy.orm import Session, joinedload, subqueryload
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from app.models.realty import Contact, Property, PropertyImage


# ==================== CONTACT REPO ====================

def get_contacts(db: Session, skip: int = 0, limit: int = 100, status: Optional[str] = None) -> List[Contact]:
    """Retrieve contacts with optional status filter and pagination."""
    query = db.query(Contact)
    if status:
        query = query.filter(Contact.status == status)
    return query.offset(skip).limit(limit).all()


def get_contact_by_id(db: Session, contact_id: int) -> Optional[Contact]:
    """Retrieve a single contact by ID."""
    return db.query(Contact).filter(Contact.id == contact_id).first()


def create_contact(db: Session, contact_data: dict) -> Contact:
    """Create a new contact with transaction safety."""
    try:
        db_contact = Contact(**contact_data)
        db.add(db_contact)
        db.commit()
        db.refresh(db_contact)
        return db_contact
    except SQLAlchemyError:
        db.rollback()
        raise


def update_contact(db: Session, db_contact: Contact, update_data: dict) -> Contact:
    """Update an existing contact with transaction safety."""
    try:
        for field, value in update_data.items():
            setattr(db_contact, field, value)
        db.commit()
        db.refresh(db_contact)
        return db_contact
    except SQLAlchemyError:
        db.rollback()
        raise


def delete_contact(db: Session, db_contact: Contact) -> None:
    """Delete a contact with transaction safety."""
    try:
        db.delete(db_contact)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise


# ==================== PROPERTY REPO ====================

def get_properties(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    property_type: Optional[str] = None,
    listing_type: Optional[str] = None,
    is_available: Optional[bool] = None
) -> List[Property]:
    """Retrieve properties with filters and eager-loaded images."""
    query = db.query(Property).options(subqueryload(Property.images))
    if property_type:
        query = query.filter(Property.property_type == property_type)
    if listing_type:
        query = query.filter(Property.listing_type == listing_type)
    if is_available is not None:
        query = query.filter(Property.is_available == is_available)
    return query.offset(skip).limit(limit).all()


def get_property_by_id(db: Session, property_id: int) -> Optional[Property]:
    """Retrieve a single property by ID with eager-loaded images."""
    return db.query(Property).options(joinedload(Property.images)).filter(Property.id == property_id).first()


def create_property(db: Session, property_data: dict) -> Property:
    """Create a new property with transaction safety."""
    try:
        db_property = Property(**property_data)
        db.add(db_property)
        db.commit()
        db.refresh(db_property)
        return db_property
    except SQLAlchemyError:
        db.rollback()
        raise


def update_property(db: Session, db_property: Property, update_data: dict) -> Property:
    """Update an existing property with transaction safety."""
    try:
        for field, value in update_data.items():
            setattr(db_property, field, value)
        db.commit()
        db.refresh(db_property)
        return db_property
    except SQLAlchemyError:
        db.rollback()
        raise


def delete_property(db: Session, db_property: Property) -> None:
    """Delete a property with transaction safety."""
    try:
        db.delete(db_property)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise


# ==================== PROPERTY IMAGE REPO ====================

def get_property_images(db: Session, property_id: int) -> List[PropertyImage]:
    """Retrieve all images for a property, ordered by sort_order."""
    return db.query(PropertyImage).filter(
        PropertyImage.property_id == property_id
    ).order_by(PropertyImage.sort_order).all()


def get_property_image_by_id(db: Session, image_id: int) -> Optional[PropertyImage]:
    """Retrieve a single property image by ID."""
    return db.query(PropertyImage).filter(PropertyImage.id == image_id).first()


def create_property_image(db: Session, image_data: dict, property_id: int) -> PropertyImage:
    """Create a new property image with transaction safety."""
    try:
        db_image = PropertyImage(**image_data, property_id=property_id)
        db.add(db_image)
        db.commit()
        db.refresh(db_image)
        return db_image
    except SQLAlchemyError:
        db.rollback()
        raise


def update_property_image(db: Session, db_image: PropertyImage, update_data: dict) -> PropertyImage:
    """Update an existing property image with transaction safety."""
    try:
        for field, value in update_data.items():
            setattr(db_image, field, value)
        db.commit()
        db.refresh(db_image)
        return db_image
    except SQLAlchemyError:
        db.rollback()
        raise


def delete_property_image(db: Session, db_image: PropertyImage) -> None:
    """Delete a property image with transaction safety."""
    try:
        db.delete(db_image)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise
