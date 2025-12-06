"""
Database models for Weather Data API
"""
from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.sql import func
from database import Base

class WeatherData(Base):
    """Weather data model for storing weather measurements"""
    __tablename__ = "weather_data"
    
    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, index=True, nullable=False)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    pressure = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    def __repr__(self):
        return f"<WeatherData(location='{self.location}', temp={self.temperature}°C)>"
