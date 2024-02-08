from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from typing import List
from typing_extensions import TypedDict
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from scipy.spatial import ConvexHull
import numpy as np

from scene import Scene
from marble import Marble
from circle import Circle
from utils import calculate_dip_and_dip_direction_from_unit_vec


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
    sizeX: int
    sizeY: int
    sizeZ: int
    data: List[Discontinous]


class RPModel(BaseModel):
    filename: str
    positionX: float
    positionY: float
    positionZ: float
    sizeX: int
    sizeY: int
    sizeZ: int


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.get("/test")
async def test(request: Request):
    return request.client.host


@app.post("/rp")
async def rp(request: Request, payload: RPModel):
    scene = Scene()
    marb = Marble(
        size=[payload.sizeX, payload.sizeY, payload.sizeZ],
        pos=[payload.positionX, payload.positionY, payload.positionZ],
    )
    scene.add(marb)

    scene.convert_obj(filename="rp/" + payload.filename)

    return JSONResponse(
        {
            "obj": f"/static/rp/{payload.filename}.obj",
            "mtl": f"/static/rp/{payload.filename}.mtl",
        }
    )


@app.post("/disc")
async def marble(request: Request, payload: DiscModel):
    scene = Scene()
    marb = Marble(
        size=[payload.sizeX, payload.sizeY, payload.sizeZ],
        pos=[payload.positionX, payload.positionY, payload.positionZ],
    )
    # scene.add(marb)

    circ = Circle(radius=5)
    # circ.move(0, 0, 5)
    # scene.add(circ)
    # circ.rotate(430, 0)
    # disc = circ.intersections(marb.edges, marb.vertices)
    # scene.add(disc)

    for i in payload.data:
        circ.rotate(i["dip"], i["dipDirection"])
        circ.move(i["positionX"], i["positionY"], i["positionZ"])
        # scene.add(circ)
        disc = circ.intersections(marb.edges, marb.vertices)
        if disc:
            scene.add(disc)

    scene.convert_obj(filename="disc/" + payload.filename)

    return JSONResponse(
        {
            "obj": f"/static/disc/{payload.filename}.obj",
            "mtl": f"/static/disc/{payload.filename}.mtl",
        }
    )


@app.post("/dfn")
async def dfn(request: Request, payload: DiscModel):
    scene = Scene()
    marb = Marble(
        size=[payload.sizeX, payload.sizeY, payload.sizeZ],
        pos=[payload.positionX, payload.positionY, payload.positionZ],
    )
    circ = Circle()

    for i in payload.data:
        circ.rotate(i["dip"], i["dipDirection"])
        circ.move(i["positionX"], i["positionY"], i["positionZ"])
        disc = circ.intersections(marb.edges, marb.vertices)
        for _ in range(5):
            bae = disc.baecher(i["dip"], i["dipDirection"], 3, "log", 5, 4)
            bae_rot = calculate_dip_and_dip_direction_from_unit_vec(bae["unit_vector"])
            circ2 = Circle()
            circ2.rotate(bae_rot[0], bae_rot[1])
            scene.add(circ2.intersections(marb.edges, marb.vertices))

    scene.convert_obj(filename="dfn/" + payload.filename)

    return JSONResponse(
        {
            "obj": f"/static/dfn/{payload.filename}.obj",
            "mtl": f"/static/dfn/{payload.filename}.mtl",
        }
    )


@app.post("/poly")
async def poly(request: Request, payload: DiscModel):
    scene = Scene()
    marb = Marble(
        size=[payload.sizeX, payload.sizeY, payload.sizeZ],
        pos=[payload.positionX, payload.positionY, payload.positionZ],
    )
    temp_objects = []
    objects = [marb]
    processed = []
    for i in payload.data:
        if [i["dip"], i["dipDirection"]] in processed:
            continue
        processed.append([i["dip"], i["dipDirection"]])
        circ = Circle(radius=15)
        circ.move(i["positionX"], i["positionY"], i["positionZ"])
        circ.rotate(i["dip"], i["dipDirection"])
        # scene.add(circ)
        for obj in objects:
            disc = circ.intersections(obj.edges, obj.vertices)
            if disc is None:
                temp_objects.append(obj)
                continue

            # scene.add(disc)

            left = [d for d in disc.vertices]
            right = [d for d in disc.vertices]

            for j in obj.vertices:

                if np.dot(disc.normal, np.array(j) - disc.normal) < 0:
                    left.append(j)
                else:
                    right.append(j)

            if len(left) > 3:
                temp_objects.append(
                    Marble.from_points(
                        left, ConvexHull(left, qhull_options="QJ Pp").simplices
                    )
                )

                # pass
            if len(right) > 3:
                temp_objects.append(
                    Marble.from_points(
                        right, ConvexHull(right, qhull_options="QJ Pp").simplices
                    )
                )
                # pass
        objects = temp_objects
        temp_objects = []

    for i in objects:
        scene.add(i)

    scene.convert_obj(filename="poly/" + payload.filename)

    return JSONResponse(
        {
            "obj": f"/static/poly/{payload.filename}.obj",
            "mtl": f"/static/poly/{payload.filename}.mtl",
        }
    )


if __name__ == "__main__":
    uvicorn.run("api:app", reload=True)
