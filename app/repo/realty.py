from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.realty import Contact, Property, PropertyImage

# Contact Repo
def get_contacts(db: Session, skip: int = 0, limit: int = 100, status: Optional[str] = None):
    query = db.query(Contact)
    if status:
        query = query.filter(Contact.status == status)
    return query.offset(skip).limit(limit).all()

def get_contact_by_id(db: Session, contact_id: int):
    return db.query(Contact).filter(Contact.id == contact_id).first()

def create_contact(db: Session, contact_data: dict):
    db_contact = Contact(**contact_data)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def update_contact(db: Session, db_contact: Contact, update_data: dict):
    for field, value in update_data.items():
        setattr(db_contact, field, value)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def delete_contact(db: Session, db_contact: Contact):
    db.delete(db_contact)
    db.commit()

# Property Repo
def get_properties(db: Session, skip: int = 0, limit: int = 100, property_type: Optional[str] = None, listing_type: Optional[str] = None, is_available: Optional[bool] = None):
    query = db.query(Property)
    if property_type:
        query = query.filter(Property.property_type == property_type)
    if listing_type:
        query = query.filter(Property.listing_type == listing_type)
    if is_available is not None:
        query = query.filter(Property.is_available == is_available)
    return query.offset(skip).limit(limit).all()

def get_property_by_id(db: Session, property_id: int):
    return db.query(Property).filter(Property.id == property_id).first()

def create_property(db: Session, property_data: dict):
    db_property = Property(**property_data)
    db.add(db_property)
    db.commit()
    db.refresh(db_property)
    return db_property

def update_property(db: Session, db_property: Property, update_data: dict):
    for field, value in update_data.items():
        setattr(db_property, field, value)
    db.commit()
    db.refresh(db_property)
    return db_property

def delete_property(db: Session, db_property: Property):
    db.delete(db_property)
    db.commit()

# Property Image Repo
def get_property_images(db: Session, property_id: int):
    return db.query(PropertyImage).filter(PropertyImage.property_id == property_id).order_by(PropertyImage.sort_order).all()

def get_property_image_by_id(db: Session, image_id: int):
    return db.query(PropertyImage).filter(PropertyImage.id == image_id).first()

def create_property_image(db: Session, image_data: dict, property_id: int):
    db_image = PropertyImage(**image_data, property_id=property_id)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image

def update_property_image(db: Session, db_image: PropertyImage, update_data: dict):
    for field, value in update_data.items():
        setattr(db_image, field, value)
    db.commit()
    db.refresh(db_image)
    return db_image

def delete_property_image(db: Session, db_image: PropertyImage):
    db.delete(db_image)
    db.commit()
