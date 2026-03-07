from sqlalchemy import Column, Integer, String, Float
from database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    dietary_preference = Column(String)


class IngredientData(Base):
    __tablename__ = "ingredients"
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    health_score = Column(Float)   # positive = healthy, negative = unhealthy
    flags = Column(String)         # e.g., "vegan,keto-friendly,allergen"