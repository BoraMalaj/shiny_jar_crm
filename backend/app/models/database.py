from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from backend.app.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Business relationship
    business_id = Column(UUID(as_uuid=True), ForeignKey("businesses.id"))
    business = relationship("Business", back_populates="users")
    
    transactions = relationship("Transaction", back_populates="user")
    customers = relationship("Customer", back_populates="owner")

class Business(Base):
    __tablename__ = "businesses"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    instagram_handle = Column(String)
    description = Column(String)
    currency = Column(String, default="EUR")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    users = relationship("User", back_populates="business")
    transactions = relationship("Transaction", back_populates="business")
    customers = relationship("Customer", back_populates="business")
    categories = relationship("Category", back_populates="business")
    suppliers = relationship("Supplier", back_populates="business")

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    amount = Column(Float, nullable=False)
    type = Column(Enum('expense', 'income', 'transfer', name='transaction_type'))
    category = Column(String)
    date = Column(DateTime, default=datetime.utcnow)
    description = Column(String)
    payment_method = Column(String)
    
    # Foreign keys
    business_id = Column(UUID(as_uuid=True), ForeignKey("businesses.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=True)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=True)
    
    # Relationships
    business = relationship("Business", back_populates="transactions")
    user = relationship("User", back_populates="transactions")
    customer = relationship("Customer", back_populates="transactions")
    category_ref = relationship("Category", back_populates="transactions")

class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    instagram_handle = Column(String, unique=True, index=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    address = Column(String)
    notes = Column(String)
    first_order_date = Column(DateTime)
    last_order_date = Column(DateTime)
    total_spent = Column(Float, default=0.0)
    tags = Column(String)  # Comma-separated tags
    
    # Foreign keys
    business_id = Column(UUID(as_uuid=True), ForeignKey("businesses.id"), nullable=False)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Relationships
    business = relationship("Business", back_populates="customers")
    owner = relationship("User", back_populates="customers")
    transactions = relationship("Transaction", back_populates="customer")

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    type = Column(Enum('expense', 'income', name='category_type'))
    color = Column(String, default="#3B82F6")  # For UI
    icon = Column(String, default="📦")
    
    business_id = Column(UUID(as_uuid=True), ForeignKey("businesses.id"), nullable=False)
    
    # Relationships
    business = relationship("Business", back_populates="categories")
    transactions = relationship("Transaction", back_populates="category_ref")

class Supplier(Base):
    __tablename__ = "suppliers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    contact_person = Column(String)
    email = Column(String)
    phone = Column(String)
    website = Column(String)
    notes = Column(String)
    
    business_id = Column(UUID(as_uuid=True), ForeignKey("businesses.id"), nullable=False)
    
    business = relationship("Business", back_populates="suppliers")