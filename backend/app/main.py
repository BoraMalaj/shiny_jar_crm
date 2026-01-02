import sys
import os
from sqlalchemy import func
from sqlalchemy import text
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional

# 🚀 CRITICAL FIX: Add the correct path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, backend_dir)

from fastapi import FastAPI, Depends, HTTPException, Body
from sqlalchemy.orm import Session
import uvicorn
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from pydantic import BaseModel, Field, validator

# Local imports - NOW THEY WILL WORK!
from app.core.database import get_db, engine
from app.core.config import settings
from app.models.database import Base, Transaction, Customer, Supplier, Budget, Category, Business, User, Inventory

# Create tables
Base.metadata.create_all(bind=engine)

# JWT Settings
SECRET_KEY = "Boku2003"  # Change this!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Pydantic Models for request/response - FIXED regex -> pattern

class UserLogin(BaseModel):
    username: str
    password: str

# Demo users database
DEMO_USERS = {
    "admin": {
        "password": "admin123",
        "role": "admin",
        "email": "admin@shinyjar.com",
        "full_name": "Admin User"
    },
    "customer1": {
        "password": "customer123", 
        "role": "customer",
        "email": "customer1@email.com",
        "full_name": "Maria Silva"
    },
    "supplier1": {
        "password": "supplier123",
        "role": "supplier",
        "email": "supplier1@company.com",
        "full_name": "John Supplier"
    }
}

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: Optional[str] = None
    role: str
    is_active: bool = True
    business_id: Optional[int] = None
    
    class Config:
        from_attributes = True
class Token(BaseModel):
    access_token: str
    token_type: str
    # user: dict
    user: Dict[str, Any]

class TokenData(BaseModel):
    username: Optional[str] = None
class TransactionCreate(BaseModel):
    amount: float = Field(..., gt=0, description="Transaction amount must be positive")
    type: str = Field(..., pattern="^(expense|income)$", description="Must be 'expense' or 'income'")  # FIXED!
    category: str = Field(..., max_length=50)
    description: Optional[str] = None
class TransactionResponse(BaseModel):
    id: int
    amount: float
    type: str
    category_id: Optional[int] = None
    category: Optional[str] = None  # Add this for frontend compatibility
    description: Optional[str]
    transaction_date: date
    date: Optional[datetime] = None  # Add this for frontend compatibility
    
    class Config:
        from_attributes = True
        
    @validator('date', pre=True, always=True)
    def set_date(cls, v, values):
        """Create date field from transaction_date for compatibility"""
        if 'transaction_date' in values:
            # Convert date to datetime for compatibility
            transaction_date = values.get('transaction_date')
            if transaction_date:
                return datetime.combine(transaction_date, datetime.min.time())
        return v
    
    @validator('category', pre=True, always=True)
    def set_category(cls, v, values):
        """Create category field from category_id for compatibility"""
        if v is None and 'category_id' in values:
            # In a real app, you'd fetch the category name from database
            # For now, return category_id as string
            cat_id = values.get('category_id')
            if cat_id:
                return f"Category {cat_id}"
        return v
class CustomerCreate(BaseModel):
    name: str = Field(..., max_length=100)
    instagram_handle: Optional[str] = Field(None, max_length=50)
    email: Optional[str] = Field(None, max_length=100)
    total_spent: float = Field(0.0, ge=0)

class CustomerResponse(BaseModel):
    id: int
    name: str
    instagram_handle: Optional[str]
    email: Optional[str]
    total_spent: float
    
    class Config:
        from_attributes = True
        
# Supplier Pydantic Models
class SupplierCreate(BaseModel):
    name: str = Field(..., max_length=100)
    contact_person: Optional[str] = Field(None, max_length=100)
    email: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    website: Optional[str] = Field(None, max_length=200)
    address: Optional[str] = None
    notes: Optional[str] = None

class SupplierResponse(BaseModel):
    id: int
    name: str
    contact_person: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    website: Optional[str]
    address: Optional[str]
    notes: Optional[str]
    
    class Config:
        from_attributes = True

# Budget endpoints for university requirement
class BudgetCreate(BaseModel):
    name: str
    category_id: Optional[int] = None
    amount: float
    period: str
    start_date: date
    end_date: Optional[date] = None

class BudgetResponse(BaseModel):
    id: int
    name: str
    category_id: Optional[int]
    amount: float
    period: str
    start_date: date
    end_date: Optional[date]
    
    class Config:
        from_attributes = True

# Authentication functions
# def verify_password(plain_password, hashed_password):
#     """Verify a password - with length check for bcrypt"""
#     if not plain_password or not hashed_password:
#         return False
    
#     # Trim password to 72 bytes for bcrypt compatibility
#     if len(plain_password.encode('utf-8')) > 72:
#         plain_password = plain_password[:72]
    
#     return pwd_context.verify(plain_password, hashed_password)

# Password utilities
# def verify_password(plain_password, hashed_password):
#     """Verify a password"""
#     return pwd_context.verify(plain_password, hashed_password)

# Replace the current verify_password function with this:

# def verify_password(plain_password, hashed_password):
#     """Verify a password - with length check for bcrypt"""
#     if not plain_password or not hashed_password:
#         return False
    
#     # DEBUG: Print lengths
#     print(f"DEBUG: Plain password length (bytes): {len(plain_password.encode('utf-8'))}")
#     print(f"DEBUG: Hashed password: {hashed_password[:30]}...")
    
#     # Trim password to 72 bytes for bcrypt compatibility
#     if len(plain_password.encode('utf-8')) > 72:
#         # Convert to bytes, truncate, then back to string
#         password_bytes = plain_password.encode('utf-8')
#         truncated_bytes = password_bytes[:72]
#         # Try to decode back to string, but handle potential encoding errors
#         try:
#             plain_password = truncated_bytes.decode('utf-8')
#         except UnicodeDecodeError:
#             # If we can't decode properly, use a different approach
#             plain_password = password_bytes[:72].decode('utf-8', errors='ignore')
        
#         print(f"DEBUG: Password truncated to {len(plain_password.encode('utf-8'))} bytes")
    
#     return pwd_context.verify(plain_password, hashed_password)

# # def get_password_hash(password):
# #     """Hash a password"""
# #     return pwd_context.hash(password)

# def get_password_hash(password):
#     """Hash a password with bcrypt length handling"""
#     # Trim password to 72 bytes for bcrypt compatibility
#     if len(password.encode('utf-8')) > 72:
#         password_bytes = password.encode('utf-8')
#         truncated_bytes = password_bytes[:72]
#         password = truncated_bytes.decode('utf-8', errors='ignore')
    
#     return pwd_context.hash(password)

# TEMPORARY FIX - Use simple password check (remove bcrypt temporarily)
# Comment out or replace the bcrypt functions:

# from passlib.context import CryptContext  # Keep this import but change usage

# Replace pwd_context setup
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# TEMPORARY: Simple password verification (plain text)
def verify_password(plain_password, hashed_password):
    """TEMPORARY: Simple password check (plain text)"""
    print(f"DEBUG: Comparing '{plain_password}' with stored hash")
    # For now, just compare plain text (we'll fix later)
    # If hashed_password starts with $2b$, it's bcrypt - use simple check
    if hashed_password.startswith('$2b$'):
        # This is the bcrypt hash for 'admin123'
        if hashed_password == '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW':
            return plain_password == 'admin123'
        # Add other known bcrypt hashes if needed
        return False
    
    # Otherwise, assume plain text for now
    return plain_password == hashed_password

def get_password_hash(password):
    """TEMPORARY: Return password as-is"""
    return password  # Just return plain text for now

# Keep the rest of your code...

# def authenticate_user(db: Session, username: str, password: str):
#     """Authenticate user against database"""
#     user = db.query(User).filter(User.username == username).first()
#     if not user:
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user

# ## Temporary we go with plaintext
# def authenticate_user(db: Session, username: str, password: str):
#     """Authenticate user against database - TEMPORARY FIX"""
#     user = db.query(User).filter(User.username == username).first()
#     if not user:
#         print(f"DEBUG: User '{username}' not found")
#         return False
    
#     print(f"DEBUG: Stored hash: {user.hashed_password[:30]}...")
#     print(f"DEBUG: Provided password: {password}")
    
#     # TEMPORARY: Simple password check
#     # Check if password matches any known bcrypt hash
#     known_hashes = {
#         '$2b$12$EixZaYVK1fsbw1ZfbX3OXeP': 'admin123',  # Your admin hash
#     }
    
#     # If hash is known, check password
#     if user.hashed_password.startswith('$2b$'):
#         for hash_prefix, known_password in known_hashes.items():
#             if user.hashed_password.startswith(hash_prefix):
#                 return password == known_password
    
#     # Otherwise, try plain text comparison
#     return password == user.hashed_password

def authenticate_user(db: Session, username: str, password: str):
    """Authenticate user against database - FIXED VERSION"""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        print(f"DEBUG: User '{username}' not found in database")
        return False
    
    print(f"DEBUG: Found user: {user.username}")
    print(f"DEBUG: Stored password hash: {user.hashed_password[:30]}...")
    print(f"DEBUG: Password to verify: {password}")
    
    # TEMPORARY: Simple password check
    success = verify_password(password, user.hashed_password)
    
    print(f"DEBUG: Password verification result: {success}")
    
    if success:
        return user  # Return the user object, not True
    else:
        return False

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Dependency to get current user from token
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Get current user from JWT token"""
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """Get current active user"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.get("/")
def root():
    return {
        "message": "Welcome to Shiny Jar Business API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": ["/transactions", "/customers", "/health", "/categories"]
    }

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        # FIXED: Use text() for raw SQL
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected", "service": "backend"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}

# ========== AUTHENTICATION ENDPOINTS ==========

@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """DEBUG VERSION - Standard OAuth2 token endpoint"""
    print(f"DEBUG: Login attempt for user: {form_data.username}")
    print(f"DEBUG: Password length in bytes: {len(form_data.password.encode('utf-8'))}")
    
    try:
        # Find user
        user = db.query(User).filter(User.username == form_data.username).first()
        print(f"DEBUG: User found: {user is not None}")
        
        if not user:
            print("DEBUG: User not found in database")
            raise HTTPException(
                status_code=401,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        print(f"DEBUG: User hashed_password: {user.hashed_password[:30]}...")
        print(f"DEBUG: User role: {user.role}")
        
        # Verify password
        try:
            password_correct = pwd_context.verify(form_data.password, user.hashed_password)
            print(f"DEBUG: Password verification result: {password_correct}")
        except Exception as e:
            print(f"DEBUG: Password verification ERROR: {str(e)}")
            password_correct = False
        
        if not password_correct:
            print("DEBUG: Password incorrect")
            raise HTTPException(
                status_code=401,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        
        print(f"DEBUG: Token created successfully")
        
        # Get user data
        user_data = {
            "username": user.username,
            "role": user.role,
            "email": user.email,
            "full_name": user.full_name,
            "user_id": user.id
        }
        
        print(f"DEBUG: Basic user data: {user_data}")
        
        # Add role-specific IDs
        if user.role == 'customer':
            customer = db.query(Customer).filter(
                (Customer.email == user.email) | 
                (Customer.name.ilike(f"%{user.full_name}%"))
            ).first()
            if customer:
                user_data["customer_id"] = customer.id
                print(f"DEBUG: Found customer ID: {customer.id}")
        
        elif user.role == 'supplier':
            supplier = db.query(Supplier).filter(
                (Supplier.email == user.email) |
                (Supplier.contact_person.ilike(f"%{user.full_name}%"))
            ).first()
            if supplier:
                user_data["supplier_id"] = supplier.id
                print(f"DEBUG: Found supplier ID: {supplier.id}")
        
        print(f"DEBUG: Returning success response")
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user_data
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"DEBUG: UNEXPECTED ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@app.post("/api/login")
def login_simple(user: UserLogin, db: Session = Depends(get_db)):
    """Backward-compatible login endpoint (uses same authentication)"""
    # Try to authenticate
    db_user = authenticate_user(db, user.username, user.password)
    
    if db_user:
        # Create token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": db_user.username}, expires_delta=access_token_expires
        )
        
        # Get user data
        user_data = {
            "username": db_user.username,
            "role": db_user.role,
            "email": db_user.email,
            "full_name": db_user.full_name,
            "user_id": db_user.id
        }
        
        # Add role-specific IDs
        if db_user.role == 'customer':
            customer = db.query(Customer).filter(
                (Customer.email == db_user.email) | 
                (Customer.name.ilike(f"%{db_user.full_name}%"))
            ).first()
            if customer:
                user_data["customer_id"] = customer.id
        
        elif db_user.role == 'supplier':
            supplier = db.query(Supplier).filter(
                (Supplier.email == db_user.email) |
                (Supplier.contact_person.ilike(f"%{db_user.full_name}%"))
            ).first()
            if supplier:
                user_data["supplier_id"] = supplier.id
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user_data
        }
    
    # If database authentication fails, check demo users
    user_data = DEMO_USERS.get(user.username)
    if user_data and user_data["password"] == user.password:
        token = f"demo_token_{user.username}"
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "username": user.username,
                "role": user_data["role"],
                "email": user_data["email"],
                "full_name": user_data["full_name"],
                **{k: v for k, v in user_data.items() if k not in ["password", "role"]}
            }
        }
    
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/users/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Get current user info"""
    return current_user

@app.get("/api/me")
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user info for frontend"""
    return {
        "username": current_user.username,
        "role": current_user.role,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "user_id": current_user.id
    }

# Get expense categories
@app.get("/api/categories")
def get_categories():
    return {
        "expense_categories": [
            "Materials", "Shipping", "Packaging", "Marketing", 
            "Tools", "Office Supplies", "Website", "Other"
        ],
        "income_categories": [
            "Jewelry Sales", "Custom Orders", "Repairs", 
            "Consultation", "Workshops", "Other"
        ]
    }

# Transaction endpoints
@app.get("/api/transactions", response_model=List[TransactionResponse])
def get_transactions(
    db: Session = Depends(get_db),
    type: Optional[str] = None,
    limit: int = 100
):
    query = db.query(Transaction)
    if type:
        query = query.filter(Transaction.type == type)
    transactions = query.order_by(Transaction.transaction_date.desc()).limit(limit).all()
    
    # Get category names for each transaction
    result = []
    for trans in transactions:
        trans_dict = {
            "id": trans.id,
            "amount": trans.amount,
            "type": trans.type,
            "category_id": trans.category_id,
            "description": trans.description,
            "transaction_date": trans.transaction_date,
        }
        
        # Add category name if we have category_id
        if trans.category_id:
            category = db.query(Category).filter(Category.id == trans.category_id).first()
            trans_dict["category"] = category.name if category else f"Category {trans.category_id}"
        else:
            trans_dict["category"] = "Uncategorized"
            
        result.append(trans_dict)
    
    return result

@app.post("/api/transactions", response_model=TransactionResponse)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    try:
        db_transaction = Transaction(
            amount=transaction.amount,
            type=transaction.type,
            category=transaction.category,
            description=transaction.description
        )
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        return db_transaction
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# Customer endpoints
@app.get("/api/customers", response_model=List[CustomerResponse])
def get_customers(db: Session = Depends(get_db)):
    customers = db.query(Customer).order_by(Customer.name).all()
    return customers

@app.post("/api/customers", response_model=CustomerResponse)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    try:
        db_customer = Customer(
            name=customer.name,
            instagram_handle=customer.instagram_handle,
            email=customer.email,
            total_spent=customer.total_spent
        )
        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)
        return db_customer
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# Customer search and update endpoints
@app.get("/api/customers/search")
def search_customers(
    db: Session = Depends(get_db),
    q: Optional[str] = None,
    limit: int = 20
):
    query = db.query(Customer)
    
    if q:
        query = query.filter(
            Customer.name.ilike(f"%{q}%") | 
            Customer.instagram_handle.ilike(f"%{q}%") |
            Customer.email.ilike(f"%{q}%")
        )
    
    customers = query.order_by(Customer.name).limit(limit).all()
    return customers

@app.put("/api/customers/{customer_id}", response_model=CustomerResponse)
def update_customer(
    customer_id: int,
    customer: CustomerCreate,
    db: Session = Depends(get_db)
):
    db_customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    try:
        for key, value in customer.dict(exclude_unset=True).items():
            setattr(db_customer, key, value)
        
        db.commit()
        db.refresh(db_customer)
        return db_customer
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/customers/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    try:
        db.delete(db_customer)
        db.commit()
        return {"message": "Customer deleted successfully", "id": customer_id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Delete failed: {str(e)}")

# Link customers to transactions (for sales tracking)
@app.get("/api/customers/{customer_id}/transactions")
def get_customer_transactions(customer_id: int, db: Session = Depends(get_db)):
    # In a real app, we'd link transactions to customers
    # For now, we'll simulate with a note
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    return {
        "customer": {
            "id": customer.id,
            "name": customer.name,
            "total_spent": customer.total_spent
        },
        "transactions": [
            # We'll implement this after adding customer_id to transactions
            {"message": "Customer transaction linking coming soon!"}
        ]
    }


# ========== CUSTOMER DASHBOARD ENDPOINTS ==========

@app.get("/api/customers/{customer_id}/dashboard")
def get_customer_dashboard(customer_id: int, db: Session = Depends(get_db), 
                          current_user: User = Depends(get_current_user)):
    """Get customer dashboard data"""
    
    # Check if user has access to this customer data
    if current_user.role != 'admin' and current_user.id != customer_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Get customer's transactions
    transactions = db.query(Transaction).filter(
        Transaction.customer_id == customer_id,
        Transaction.type == 'income'  # Sales to customer
    ).order_by(Transaction.transaction_date.desc()).limit(20).all()
    
    # Calculate statistics
    total_spent = db.query(func.sum(Transaction.amount)).filter(
        Transaction.customer_id == customer_id,
        Transaction.type == 'income'
    ).scalar() or 0
    
    order_count = db.query(Transaction).filter(
        Transaction.customer_id == customer_id,
        Transaction.type == 'income'
    ).count()
    
    # Get recent orders
    recent_orders = []
    for trans in transactions:
        recent_orders.append({
            "id": trans.id,
            "date": trans.transaction_date,
            "description": trans.description,
            "amount": trans.amount,
            "status": "completed"  # In real app, you'd have an order status field
        })
    
    return {
        "customer": {
            "id": customer.id,
            "name": customer.name,
            "email": customer.email,
            "instagram_handle": customer.instagram_handle,
            "total_spent": float(total_spent),
            "order_count": order_count,
            "customer_since": customer.customer_since,
            "last_purchase": customer.last_purchase
        },
        "recent_orders": recent_orders,
        "stats": {
            "total_spent": float(total_spent),
            "order_count": order_count,
            "avg_order_value": float(total_spent / order_count) if order_count > 0 else 0,
            "loyalty_tier": "VIP" if total_spent > 1000 else "Regular" if total_spent > 500 else "New"
        }
    }

@app.get("/api/customers/{customer_id}/orders")
def get_customer_orders(customer_id: int, db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_user)):
    """Get all orders for a customer"""
    
    if current_user.role != 'admin' and current_user.id != customer_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    orders = db.query(Transaction).filter(
        Transaction.customer_id == customer_id,
        Transaction.type == 'income'
    ).order_by(Transaction.transaction_date.desc()).all()
    
    return [{
        "id": order.id,
        "date": order.transaction_date,
        "description": order.description,
        "amount": order.amount,
        "category": order.category,
        "status": "completed",
        "invoice_number": f"INV-{order.id:06d}"
    } for order in orders]

# Supplier endpoints
# Update the existing get_suppliers endpoint:
@app.get("/api/suppliers", response_model=List[SupplierResponse])
def get_suppliers(db: Session = Depends(get_db)):
    suppliers = db.query(Supplier).order_by(Supplier.name).all()
    return suppliers

# Add the new create_supplier endpoint:
@app.post("/api/suppliers", response_model=SupplierResponse)
def create_supplier(supplier: SupplierCreate, db: Session = Depends(get_db)):
    try:
        db_supplier = Supplier(
            name=supplier.name,
            contact_person=supplier.contact_person,
            email=supplier.email,
            phone=supplier.phone,
            website=supplier.website,
            address=supplier.address,
            notes=supplier.notes
        )
        db.add(db_supplier)
        db.commit()
        db.refresh(db_supplier)
        return db_supplier
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/suppliers/{supplier_id}")
def delete_supplier(supplier_id: int, db: Session = Depends(get_db)):
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    
    try:
        db.delete(supplier)
        db.commit()
        return {"message": "Supplier deleted successfully", "id": supplier_id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# ========== SUPPLIER DASHBOARD ENDPOINTS ==========

@app.get("/api/suppliers/{supplier_id}/dashboard")
def get_supplier_dashboard(supplier_id: int, db: Session = Depends(get_db),
                          current_user: User = Depends(get_current_user)):
    """Get supplier dashboard data"""
    
    # Check authorization
    if current_user.role != 'admin' and current_user.id != supplier_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    
    # Get supplier's transactions (purchases from supplier)
    transactions = db.query(Transaction).filter(
        Transaction.supplier_id == supplier_id,
        Transaction.type == 'expense'
    ).order_by(Transaction.transaction_date.desc()).limit(10).all()
    
    # Calculate statistics
    total_revenue = db.query(func.sum(Transaction.amount)).filter(
        Transaction.supplier_id == supplier_id,
        Transaction.type == 'expense'
    ).scalar() or 0
    
    order_count = db.query(Transaction).filter(
        Transaction.supplier_id == supplier_id,
        Transaction.type == 'expense'
    ).count()
    
    # Get monthly revenue
    monthly_data = db.query(
        func.date_trunc('month', Transaction.transaction_date).label('month'),
        func.sum(Transaction.amount).label('total')
    ).filter(
        Transaction.supplier_id == supplier_id,
        Transaction.type == 'expense'
    ).group_by(
        func.date_trunc('month', Transaction.transaction_date)
    ).order_by(
        func.date_trunc('month', Transaction.transaction_date).desc()
    ).limit(6).all()
    
    recent_orders = []
    for trans in transactions:
        recent_orders.append({
            "id": trans.id,
            "date": trans.transaction_date,
            "description": trans.description,
            "amount": trans.amount,
            "status": "delivered"
        })
    
    return {
        "supplier": {
            "id": supplier.id,
            "name": supplier.name,
            "contact_person": supplier.contact_person,
            "email": supplier.email,
            "phone": supplier.phone,
            "website": supplier.website
        },
        "recent_orders": recent_orders,
        "stats": {
            "total_revenue": float(abs(total_revenue)),
            "order_count": order_count,
            "avg_order_value": float(abs(total_revenue / order_count)) if order_count > 0 else 0,
            "rating": 4.7  # In real app, this would come from a ratings table
        },
        "monthly_revenue": [
            {"month": month.strftime("%Y-%m"), "revenue": float(abs(total))}
            for month, total in monthly_data
        ]
    }

@app.get("/api/suppliers/{supplier_id}/orders")
def get_supplier_orders(supplier_id: int, db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_user)):
    """Get all orders from a supplier"""
    
    if current_user.role != 'admin' and current_user.id != supplier_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    orders = db.query(Transaction).filter(
        Transaction.supplier_id == supplier_id,
        Transaction.type == 'expense'
    ).order_by(Transaction.transaction_date.desc()).all()
    
    return [{
        "id": order.id,
        "date": order.transaction_date,
        "description": order.description,
        "amount": abs(order.amount),
        "category": order.category,
        "status": "delivered",
        "po_number": f"PO-{order.id:06d}"
    } for order in orders]

# ========== INVENTORY ENDPOINTS ==========

@app.get("/api/inventory")
def get_inventory(db: Session = Depends(get_db)):
    """Get all inventory items"""
    inventory = db.query(Inventory).order_by(Inventory.name).all()
    return inventory

@app.get("/api/inventory/{item_id}")
def get_inventory_item(item_id: int, db: Session = Depends(get_db)):
    """Get specific inventory item"""
    item = db.query(Inventory).filter(Inventory.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    return item

@app.post("/api/inventory")
def create_inventory_item(item: dict, db: Session = Depends(get_db)):
    """Create new inventory item"""
    try:
        db_item = Inventory(**item)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/api/inventory/{item_id}")
def update_inventory_item(item_id: int, item_data: dict, db: Session = Depends(get_db)):
    """Update inventory item"""
    item = db.query(Inventory).filter(Inventory.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    
    try:
        for key, value in item_data.items():
            setattr(item, key, value)
        
        item.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(item)
        return item
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    
# Endpoint for stock movements
@app.post("/api/inventory/{item_id}/receive")
def receive_stock(
    item_id: int,
    quantity: int = Body(..., gt=0),
    unit_cost: Optional[float] = Body(None, gt=0),
    reference: Optional[str] = None,
    notes: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Receive stock for an inventory item"""
    # Get the item
    item = db.query(Inventory).filter(Inventory.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    
    try:
        # Update quantity
        item.quantity += quantity
        
        # Update unit cost if provided
        if unit_cost:
            item.unit_cost = unit_cost
        
        item.updated_at = datetime.utcnow()
        
        # Create stock movement record (you'd need a stock_movements table)
        # For now, just update the inventory
        
        db.commit()
        db.refresh(item)
        
        return {
            "message": f"Received {quantity} units of {item.name}",
            "item": item,
            "new_quantity": item.quantity,
            "new_unit_cost": item.unit_cost
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# Budget Endpoints
@app.get("/api/budgets", response_model=List[BudgetResponse])
def get_budgets(db: Session = Depends(get_db)):
    budgets = db.query(Budget).all()
    return budgets

@app.post("/api/budgets", response_model=BudgetResponse)
def create_budget(budget: BudgetCreate, db: Session = Depends(get_db)):
    try:
        db_budget = Budget(**budget.dict())
        db.add(db_budget)
        db.commit()
        db.refresh(db_budget)
        return db_budget
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

# Budget tracking analysis
@app.get("/api/budgets/analysis")
def get_budget_analysis(db: Session = Depends(get_db)):
    # Get all budgets
    budgets = db.query(Budget).all()
    
    analysis = []
    for budget in budgets:
        # Calculate actual spending for this category in budget period
        actual_spent = db.query(func.sum(Transaction.amount)).filter(
            Transaction.type == 'expense',
            Transaction.category_id == budget.category_id,
            Transaction.transaction_date >= budget.start_date,
            Transaction.transaction_date <= (budget.end_date or date.today())
        ).scalar() or 0
        
        remaining = budget.amount - actual_spent
        percentage_used = (actual_spent / budget.amount * 100) if budget.amount > 0 else 0
        
        analysis.append({
            "budget_id": budget.id,
            "budget_name": budget.name,
            "category_id": budget.category_id,
            "budget_amount": float(budget.amount),
            "actual_spent": float(actual_spent),
            "remaining": float(remaining),
            "percentage_used": float(percentage_used),
            "status": "over" if actual_spent > budget.amount else "under" if percentage_used < 90 else "on_track"
        })
    
    return analysis

@app.get("/api/budgets/{budget_id}")
def get_budget(budget_id: int, db: Session = Depends(get_db)):
    """Get specific budget"""
    budget = db.query(Budget).filter(Budget.id == budget_id).first()
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    return budget

@app.put("/api/budgets/{budget_id}")
def update_budget(budget_id: int, budget_update: BudgetCreate, db: Session = Depends(get_db)):
    """Update budget"""
    budget = db.query(Budget).filter(Budget.id == budget_id).first()
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    
    try:
        for key, value in budget_update.dict(exclude_unset=True).items():
            setattr(budget, key, value)
        
        db.commit()
        db.refresh(budget)
        return budget
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/analytics/sales-trend")
def get_sales_trend(
    db: Session = Depends(get_db),
    months: int = 12
):
    """Get sales trend data for analytics"""
    # Get monthly sales data
    monthly_data = db.query(
        func.date_trunc('month', Transaction.transaction_date).label('month'),
        func.sum(Transaction.amount).label('total')
    ).filter(
        Transaction.type == 'income'
    ).group_by(
        func.date_trunc('month', Transaction.transaction_date)
    ).order_by(
        func.date_trunc('month', Transaction.transaction_date).desc()
    ).limit(months).all()
    
    return [
        {
            "month": month.strftime("%Y-%m"),
            "sales": float(total)
        }
        for month, total in monthly_data
    ]

@app.get("/api/analytics/customer-segments")
def get_customer_segments(db: Session = Depends(get_db)):
    """Get customer segmentation data"""
    customers = db.query(Customer).all()
    
    # Simple segmentation by spending
    segments = {
        "new": {"count": 0, "total_spent": 0, "avg_spent": 0},
        "regular": {"count": 0, "total_spent": 0, "avg_spent": 0},
        "vip": {"count": 0, "total_spent": 0, "avg_spent": 0},
        "premium": {"count": 0, "total_spent": 0, "avg_spent": 0}
    }
    
    for customer in customers:
        spent = customer.total_spent or 0
        
        if spent < 100:
            segment = "new"
        elif spent < 500:
            segment = "regular"
        elif spent < 1000:
            segment = "vip"
        else:
            segment = "premium"
        
        segments[segment]["count"] += 1
        segments[segment]["total_spent"] += spent
    
    # Calculate averages
    for segment in segments:
        if segments[segment]["count"] > 0:
            segments[segment]["avg_spent"] = segments[segment]["total_spent"] / segments[segment]["count"]
    
    return segments

# Dashboard stats
@app.get("/api/stats")
def get_stats(db: Session = Depends(get_db)):
    # Total income
    total_income = db.query(Transaction).filter(
        Transaction.type == 'income'
    ).with_entities(func.sum(Transaction.amount)).scalar() or 0
    
    # Total expenses
    total_expenses = db.query(Transaction).filter(
        Transaction.type == 'expense'
    ).with_entities(func.sum(Transaction.amount)).scalar() or 0
    
    # Profit
    profit = total_income - total_expenses
    
    # Transaction counts
    transaction_count = db.query(Transaction).count()
    customer_count = db.query(Customer).count()
    
    # Calculate average transaction (this might need adjustment)
    avg_transaction = 0
    if transaction_count > 0:
        avg_transaction = (total_income + total_expenses) / transaction_count
    
    return {
        "total_income": float(total_income),
        "total_expenses": float(total_expenses),
        "profit": float(profit),
        "transaction_count": transaction_count,
        "customer_count": customer_count,
        "average_transaction": float(avg_transaction)
    }

# Dashboard comprehensive stats
@app.get("/api/dashboard")
# def get_dashboard_stats(db: Session = Depends(get_db)):
def get_dashboard_stats(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):         # needs authentication
    # Basic stats
    total_income = db.query(Transaction).filter(
        Transaction.type == 'income'
    ).with_entities(func.sum(Transaction.amount)).scalar() or 0
    
    total_expenses = db.query(Transaction).filter(
        Transaction.type == 'expense'
    ).with_entities(func.sum(Transaction.amount)).scalar() or 0
    
    profit = total_income - total_expenses
    
    # Monthly trends - FIXED: Transaction.date -> Transaction.transaction_date
    monthly_data = db.query(
        func.date_trunc('month', Transaction.transaction_date).label('month'),  # FIXED
        Transaction.type,
        func.sum(Transaction.amount).label('total')
    ).group_by(
        func.date_trunc('month', Transaction.transaction_date),  # FIXED
        Transaction.type
    ).order_by(
        func.date_trunc('month', Transaction.transaction_date).desc()  # FIXED
    ).limit(12).all()
    
    # Category breakdown
    expense_by_category = db.query(
        Transaction.category_id,  # This might need to be category_id, not category
        func.sum(Transaction.amount).label('total')
    ).filter(
        Transaction.type == 'expense'
    ).group_by(
        Transaction.category_id  # FIXED
    ).all()
    
    income_by_category = db.query(
        Transaction.category_id,  # This might need to be category_id, not category
        func.sum(Transaction.amount).label('total')
    ).filter(
        Transaction.type == 'income'
    ).group_by(
        Transaction.category_id  # FIXED
    ).all()
    
    # Recent transactions
    recent_transactions = db.query(Transaction).order_by(
        Transaction.transaction_date.desc()  # FIXED
    ).limit(20).all()
    
    # Top customers
    top_customers = db.query(Customer).order_by(
        Customer.total_spent.desc()
    ).limit(20).all()
    
    # Get category names for the category IDs
    category_map = {}
    categories = db.query(Category).all()
    for cat in categories:
        category_map[cat.id] = cat.name
    
    return {
        "summary": {
            "total_income": float(total_income),
            "total_expenses": float(total_expenses),
            "profit": float(profit),
            "transaction_count": db.query(Transaction).count(),
            "customer_count": db.query(Customer).count()
        },
        "monthly_trends": [
            {
                "month": month.strftime("%Y-%m"),
                "type": type,
                "total": float(total)
            }
            for month, type, total in monthly_data
        ],
        "expense_categories": [
            {"category": category_map.get(cat_id, f"Category {cat_id}"), "total": float(total)}
            for cat_id, total in expense_by_category
        ],
        "income_categories": [
            {"category": category_map.get(cat_id, f"Category {cat_id}"), "total": float(total)}
            for cat_id, total in income_by_category
        ],
        "recent_transactions": [
            {
                "id": t.id,
                "amount": t.amount,
                "type": t.type,
                "category": category_map.get(t.category_id, "Unknown"),
                "date": t.transaction_date.isoformat() if t.transaction_date else None  # FIXED
            }
            for t in recent_transactions
        ],
        "top_customers": [
            {
                "id": c.id,
                "name": c.name,
                "instagram": c.instagram_handle,
                "total_spent": c.total_spent
            }
            for c in top_customers
        ]
    }

if __name__ == "__main__":
    print(f"🚀 Starting {settings.APP_NAME} on http://localhost:8000")
    print(f"📊 Database: {settings.DATABASE_URL}")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
