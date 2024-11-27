from pydantic import BaseModel

class Coordinates(BaseModel):
    lat: float
    lng: float

class Location(BaseModel):
    coordinates: Coordinates
    time: int
