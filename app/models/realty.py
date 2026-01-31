from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, func, Enum
from sqlalchemy.orm import relationship
from app.configs.db_config import MySQLBase


class Contact(MySQLBase):
    """Model for contacts table"""
    __tablename__ = "contacts"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name_ = Column("name_", String(100), nullable=False)  # Column is 'name_' in DB
    phone = Column(String(15), nullable=False)
    email = Column(String(150), nullable=False)
    message = Column(String(250), nullable=False)
    status = Column(
        Enum('new', 'contacted', 'closed', name='contact_status'),
        default='new',
        nullable=True
    )
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=True)


class Property(MySQLBase):
    """Model for properties table"""
    __tablename__ = "properties"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    property_name = Column(String(150), nullable=False)
    location = Column(String(150), nullable=False)
    phone = Column(String(15), nullable=True)
    map_link = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)
    property_type = Column(
        Enum('PG', '1RK', '1BHK', '2BHK', name='property_type_enum'),
        nullable=False
    )
    furnishing = Column(
        Enum('fully_furnished', 'semi_furnished', 'unfurnished', name='furnishing_enum'),
        nullable=True
    )
    private_price = Column(Integer, nullable=True)  # For 1BHK, 1RK etc
    single_price = Column(Integer, nullable=True)
    double_price = Column(Integer, nullable=True)
    triple_price = Column(Integer, nullable=True)
    listing_type = Column(
        Enum('buy', 'rent', name='listing_type_enum'),
        nullable=False
    )
    is_available = Column(Boolean, default=True, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=True)
    
    # Relationship to property images
    images = relationship("PropertyImage", back_populates="property", cascade="all, delete-orphan")


class PropertyImage(MySQLBase):
    """Model for property_images table"""
    __tablename__ = "property_images"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    property_id = Column(Integer, ForeignKey('properties.id', ondelete='CASCADE'), nullable=False)
    image_url = Column(String(500), nullable=False)
    is_primary = Column(Boolean, default=False, nullable=False)
    sort_order = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    # Relationship to property
    property = relationship("Property", back_populates="images")
