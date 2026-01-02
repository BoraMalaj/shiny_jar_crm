from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.app.core.database import Base

class Business(Base):
    __tablename__ = "businesses"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    instagram_handle = Column(String(50))
    currency = Column(String(3), default="EUR")
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    users = relationship("User", back_populates="business")
    categories = relationship("Category", back_populates="business")
    suppliers = relationship("Supplier", back_populates="business")
    customers = relationship("Customer", back_populates="business")
    transactions = relationship("Transaction", back_populates="business")
    budgets = relationship("Budget", back_populates="business")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    full_name = Column(String(100))
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String(20), default="user")
    business_id = Column(Integer, ForeignKey("businesses.id"))
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    business = relationship("Business", back_populates="users")
    transactions = relationship("Transaction", back_populates="user")

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    type = Column(String(10))  # expense, income, both
    color = Column(String(7), default="#3B82F6")
    business_id = Column(Integer, ForeignKey("businesses.id"))
    
    # Relationships
    business = relationship("Business", back_populates="categories")
    transactions = relationship("Transaction", back_populates="category")
    budgets = relationship("Budget", back_populates="category")

class Supplier(Base):
    __tablename__ = "suppliers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    contact_person = Column(String(100))
    email = Column(String(100))
    phone = Column(String(20))
    website = Column(String(200))
    address = Column(Text)
    notes = Column(Text)
    business_id = Column(Integer, ForeignKey("businesses.id"))
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    business = relationship("Business", back_populates="suppliers")
    transactions = relationship("Transaction", back_populates="supplier")
    inventory = relationship("Inventory", back_populates="supplier")

class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    instagram_handle = Column(String(50))
    email = Column(String(100))
    phone = Column(String(20))
    address = Column(Text)
    customer_since = Column(Date, default=func.current_date())
    total_spent = Column(Float, default=0.0)
    last_purchase = Column(Date)
    notes = Column(Text)
    business_id = Column(Integer, ForeignKey("businesses.id"))
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    business = relationship("Business", back_populates="customers")
    transactions = relationship("Transaction", back_populates="customer")

class Inventory(Base):
    __tablename__ = "inventory"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    category = Column(String(50))
    unit_cost = Column(Float, nullable=False)
    quantity = Column(Integer, default=0)
    reorder_level = Column(Integer, default=10)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    business_id = Column(Integer, ForeignKey("businesses.id"))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    supplier = relationship("Supplier", back_populates="inventory")
    business = relationship("Business")

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    transaction_date = Column(Date, nullable=False, default=func.current_date())
    amount = Column(Float, nullable=False)
    type = Column(String(10), nullable=False)  # expense or income
    category_id = Column(Integer, ForeignKey("categories.id"))
    description = Column(Text)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    business_id = Column(Integer, ForeignKey("businesses.id"))
    payment_method = Column(String(20))
    reference_number = Column(String(50))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    @property
    def date(self):
        return self.transaction_date
    
    @date.setter
    def date(self, value):
        self.transaction_date = value
        
    @property
    def category(self):
        return str(self.category_id) if self.category_id else "Unknown"
    
    # Relationships
    category = relationship("Category", back_populates="transactions")
    customer = relationship("Customer", back_populates="transactions")
    supplier = relationship("Supplier", back_populates="transactions")
    user = relationship("User", back_populates="transactions")
    business = relationship("Business", back_populates="transactions")

class Budget(Base):
    __tablename__ = "budgets"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))
    amount = Column(Float, nullable=False)
    period = Column(String(20))  # daily, weekly, monthly, quarterly, yearly
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    business_id = Column(Integer, ForeignKey("businesses.id"))
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    category = relationship("Category", back_populates="budgets")
    business = relationship("Business", back_populates="budgets")




############ Initial Model of Database ###############

# from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text
# from sqlalchemy.sql import func
# from backend.app.core.database import Base

# class Transaction(Base):
#     __tablename__ = "transactions"
    
#     id = Column(Integer, primary_key=True, index=True)
#     amount = Column(Float, nullable=False)
#     type = Column(String(10), nullable=False)  # 'expense' or 'income'
#     category = Column(String(50))
#     description = Column(Text)
#     date = Column(DateTime, default=func.now())
#     business_id = Column(Integer, default=1)  # Default to Shiny Jar business
#     user_id = Column(Integer, default=1)  # Default to admin user
#     # add to optionally link transactions to customers
#     # customer_id = Column(Integer, nullable=True)
    
#     # For frontend display
#     # def to_dict(self):
#     #     return {
#     #         "id": self.id,
#     #         "amount": self.amount,
#     #         "type": self.type,
#     #         "category": self.category,
#     #         "description": self.description,
#     #         "date": self.date.isoformat() if self.date else None,
#     #         "customer_id": self.customer_id
#     #     }

# class Customer(Base):
#     __tablename__ = "customers"
    
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(100), nullable=False)
#     instagram_handle = Column(String(50))
#     email = Column(String(100))
#     phone = Column(String(20))
#     first_order_date = Column(DateTime)
#     total_spent = Column(Float, default=0.0)
#     business_id = Column(Integer, default=1)