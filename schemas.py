"""
Pydantic schemas for Weather Data API
"""
from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional


class WeatherDataCreate(BaseModel):
    """Schema for creating weather data"""
    location: str
    temperature: float
    humidity: float
    pressure: float
    description: str
    
    @validator('temperature')
    def temperature_must_be_reasonable(cls, v):
        if v < -100 or v > 60:
            raise ValueError('Temperature must be between -100 and 60 degrees Celsius')
        return v
    
    @validator('humidity')
    def humidity_must_be_valid(cls, v):
        if v < 0 or v > 100:
            raise ValueError('Humidity must be between 0 and 100 percent')
        return v
    
    @validator('pressure')
    def pressure_must_be_valid(cls, v):
        if v < 800 or v > 1200:
            raise ValueError('Pressure must be between 800 and 1200 hPa')
        return v
    
    @validator('location')
    def location_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Location cannot be empty')
        return v.strip()


class WeatherDataResponse(BaseModel):
    """Schema for weather data response"""
    id: int
    location: str
    temperature: float
    humidity: float
    pressure: float
    description: str
    timestamp: datetime
    
    class Config:
        from_attributes = True


class WeatherStats(BaseModel):
    """Schema for weather statistics response"""
    location: str
    period_days: int
    record_count: int
    temperature_avg: float
    temperature_min: float
    temperature_max: float
    humidity_avg: float
    pressure_avg: float
    start_date: datetime
    end_date: datetime