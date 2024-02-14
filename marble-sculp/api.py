from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from scipy.spatial import ConvexHull
import numpy as np
from pprint import pprint
from copy import deepcopy

from scene import Scene
from marble import Marble
from circle import Circle
from models import *
from utils import calculate_dip_and_dip_direction_from_unit_vec


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


@app.post("/site")
async def site(request: Request, payload: SiteModel):
    scene = Scene()
    for i in payload.data:
        marb = Marble(
            size=[i.sizeX, i.sizeY, i.sizeZ],
            pos=[i.positionX, i.positionY, i.positionZ],
        )
        scene.add(marb)

    scene.convert_obj(filename="site/" + payload.filename)

    return JSONResponse(
        {
            "obj": f"/static/site/{payload.filename}.obj",
            "mtl": f"/static/site/{payload.filename}.mtl",
        }
    )


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

    # circ.move(0, 0, 5)
    # scene.add(circ)
    # circ.rotate(430, 0)
    # disc = circ.intersections(marb.edges, marb.vertices)
    # scene.add(disc)

    for i in payload.data:
        circ = Circle(radius=5)
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
        circ = Circle()
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
    scene.polyhedron(
        size=[payload.sizeX, payload.sizeY, payload.sizeZ],
        pos=[payload.positionX, payload.positionY, payload.positionZ],
        data=payload.data,
    )

    scene.convert_obj(filename="poly/" + payload.filename)

    return JSONResponse(
        {
            "obj": f"/static/poly/{payload.filename}.obj",
            "mtl": f"/static/poly/{payload.filename}.mtl",
        }
    )


@app.post("/extend")
async def extend(request: Request, payload: DiscModel):
    scene = Scene()
    marb = Marble(
        size=[payload.sizeX, payload.sizeY, payload.sizeZ],
        pos=[payload.positionX, payload.positionY, payload.positionZ],
    )
    # scene.add(marb)

    discons = []

    for u in range(1, 2):
        for i in range(-1 * u, 2 * u - (u - 1)):
            for j in range(-1 * u, 2 * u - (u - 1)):
                print("I:", i, "J:", j)
                # if i == 0 and j == 0:
                #     continue
                for k in range(len(payload.data)):
                    discon = deepcopy(payload.data[k])

                    temp_circ = Circle(radius=10)
                    temp_circ.rotate(discon["dip"], discon["dipDirection"])
                    temp_circ.move(
                        i * payload.sizeX + payload.positionX + discon["positionX"],
                        payload.positionY + discon["positionY"],
                        j * payload.sizeZ + payload.positionZ + discon["positionZ"],
                    )
                    # scene.add(temp_circ)
                    # print(temp_circ.normal)
                    # TODO: Use disc pos too when moving
                    disc = temp_circ.intersections(marb.edges, marb.vertices)
                    if disc:
                        # scene.add(temp_circ)
                        # scene.add(disc)
                        discon["positionX"] = (
                            i * payload.sizeX + payload.positionX + discon["positionX"]
                        )
                        discon["positionY"] = payload.positionY + discon["positionY"]
                        discon["positionZ"] = (
                            j * payload.sizeZ + payload.positionZ + discon["positionZ"]
                        )
                        discons.append(discon)

    print("Total Dics:", len(discons))

    # print(discons)

    scene.polyhedron(
        size=[payload.sizeX, payload.sizeY, payload.sizeZ],
        pos=[payload.positionX, payload.positionY, payload.positionZ],
        data=discons,
    )

    scene.convert_obj(filename="extend/" + payload.filename)

    return JSONResponse(
        {
            "obj": f"/static/extend/{payload.filename}.obj",
            "mtl": f"/static/extend/{payload.filename}.mtl",
        }
    )


if __name__ == "__main__":
    uvicorn.run("api:app", reload=True)
