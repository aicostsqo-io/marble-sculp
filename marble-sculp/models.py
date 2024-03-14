from enum import Enum
from typing import List
from typing_extensions import TypedDict
from pydantic import BaseModel


class FractureTypes(str, Enum):
    exp = "exp"
    log = "log"
    det = "det"


class Discontinous(TypedDict):
    dip: int
    dipDirection: int
    positionX: float
    positionY: float
    positionZ: float


class FractureModel(BaseModel):
    filename: str
    positionX: float
    positionY: float
    positionZ: float
    sizeX: float
    sizeY: float
    sizeZ: float
    maxFractureCount: int
    fisherConstant: float
    distributionSize: FractureTypes
    meanFractureSize: float
    sigmaFractureSize: float
    data: List[Discontinous]


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
