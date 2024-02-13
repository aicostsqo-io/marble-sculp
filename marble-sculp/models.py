from typing import List
from typing_extensions import TypedDict
from pydantic import BaseModel


class Discontinous(TypedDict):
    dip: int
    dipDirection: int
    positionX: float
    positionY: float
    positionZ: float


class DiscModel(BaseModel):
    filename: str
    positionX: float
    positionY: float
    positionZ: float
    sizeX: float
    sizeY: float
    sizeZ: float
    data: List[Discontinous]


class RPModel(BaseModel):
    filename: str
    positionX: float
    positionY: float
    positionZ: float
    sizeX: float
    sizeY: float
    sizeZ: float


class SiteModel(BaseModel):
    positionX: float
    positionY: float
    positionZ: float
    sizeX: float
    sizeY: float
    sizeZ: float


class SiteModel(BaseModel):
    filename: str
    data: List[SiteModel]
