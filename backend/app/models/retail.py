from datetime import datetime
from sqlalchemy import Column, String, Integer, Numeric, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from backend.app.core.database import Base

class Category(Base):
    __tablename__ = "categories"

    category_id = Column(String(50), primary_key=True, index=True)
    category_name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    products = relationship("Product", back_populates="category", cascade="all, delete-orphan")


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(String(50), primary_key=True, index=True)
    customer_name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True)
    city = Column(String(100), nullable=False)
    region = Column(String(50), nullable=False, index=True)
    segment = Column(String(50), nullable=False, default="Consumer")
    signup_date = Column(Date, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    orders = relationship("Order", back_populates="customer", cascade="all, delete-orphan")


class Product(Base):
    __tablename__ = "products"

    product_id = Column(String(50), primary_key=True, index=True)
    product_name = Column(String(200), nullable=False)
    category_id = Column(String(50), ForeignKey("categories.category_id"), nullable=False, index=True)
    price = Column(Numeric(10, 2), nullable=False)
    cost = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    category = relationship("Category", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(String(50), primary_key=True, index=True)
    customer_id = Column(String(50), ForeignKey("customers.customer_id"), nullable=False, index=True)
    order_date = Column(Date, nullable=False, index=True)
    ship_date = Column(Date, nullable=True)
    ship_mode = Column(String(50), default="Standard Class")
    region = Column(String(50), nullable=False, index=True)
    payment_method = Column(String(50), nullable=False)
    order_status = Column(String(50), default="Completed")
    created_at = Column(DateTime, default=datetime.utcnow)

    customer = relationship("Customer", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    order_item_id = Column(String(50), primary_key=True, index=True)
    order_id = Column(String(50), ForeignKey("orders.order_id"), nullable=False, index=True)
    product_id = Column(String(50), ForeignKey("products.product_id"), nullable=False, index=True)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    discount = Column(Numeric(5, 2), nullable=False, default=0.00)
    line_total = Column(Numeric(12, 2), nullable=False)
    line_profit = Column(Numeric(12, 2), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")
