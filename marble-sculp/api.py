from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn, time
from fastapi.middleware.cors import CORSMiddleware
from scipy.spatial import ConvexHull
import numpy as np
from pprint import pprint
from copy import deepcopy
from random import randint

from scene import Scene
from marble import Marble
from circle import Circle
from models import *
from utils import calculate_dip_and_dip_direction_from_unit_vec

from dotenv import dotenv_values
from contextlib import asynccontextmanager
from pymongo import MongoClient

from typing import Callable
from pyinstrument import Profiler
from pyinstrument.renderers.html import HTMLRenderer
from pyinstrument.renderers.speedscope import SpeedscopeRenderer

config = dotenv_values(".env")


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.client = MongoClient(config["MONGO_DB_URI"])
    app.db = app.client["test"]
    yield
    app.client.close()


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

PROFILING = True  # Set this from a settings model


# @app.middleware("http")
# async def profile_request(request: Request, call_next: Callable):
#     """Profile the current request

#     Taken from https://pyinstrument.readthedocs.io/en/latest/guide.html#profile-a-web-request-in-fastapi
#     with small improvements.

#     """
#     # we map a profile type to a file extension, as well as a pyinstrument profile renderer
#     profile_type_to_ext = {"html": "html", "speedscope": "speedscope.json"}
#     profile_type_to_renderer = {
#         "html": HTMLRenderer,
#         "speedscope": SpeedscopeRenderer,
#     }

#     # if the `profile=true` HTTP query argument is passed, we profile the request
#     if request.query_params.get("profile", False):

#         # The default profile format is speedscope
#         profile_type = request.query_params.get("profile_format", "speedscope")

#         # we profile the request along with all additional middlewares, by interrupting
#         # the program every 1ms1 and records the entire stack at that point
#         with Profiler(interval=0.001, async_mode="enabled") as profiler:
#             response = await call_next(request)

#         # we dump the profiling into a file
#         extension = profile_type_to_ext[profile_type]
#         renderer = profile_type_to_renderer[profile_type]()
#         with open(f"profile.{extension}", "w") as out:
#             out.write(profiler.output(renderer=renderer))
#         return response

#     # Proceed without profiling
#     return await call_next(request)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    print(
        "Time took to process the request and return response is {} sec".format(
            time.time() - start_time
        )
    )
    return response


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
        if disc:
            count = randint(1, 7)
            for _ in range(count):
                bae = disc.baecher(i["dip"], i["dipDirection"], 3, "log", 5, 4)
                bae_rot = calculate_dip_and_dip_direction_from_unit_vec(
                    bae["unit_vector"]
                )
                circ2 = Circle()
                circ2.rotate(bae_rot[0], bae_rot[1])
                scene.add(circ2.intersections(marb.edges, marb.vertices))

    scene.convert_obj(filename="dfn/" + payload.filename)

    return JSONResponse(
        {
            "obj": f"/static/dfn/{payload.filename}.obj",
            "mtl": f"/static/dfn/{payload.filename}.mtl",
            "count": len(scene.objects),
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
    a = 0
    processed = []

    for u in range(1, 2):
        for i in range(-1 * u, 2 * u - (u - 1)):
            for j in range(-1 * u, 2 * u - (u - 1)):
                for k in range(-1 * u, 2 * u - (u - 1)):
                    print("I:", i, "J:", j)
                    a += 1
                    # if i == 0 and j == 0:
                    #     continue
                    for d in range(len(payload.data)):
                        discon = deepcopy(payload.data[d])

                        temp_circ = Circle(radius=10)
                        temp_circ.rotate(discon["dip"], discon["dipDirection"])
                        temp_circ.move(
                            i * payload.sizeX + payload.positionX + discon["positionX"],
                            j * payload.sizeY + payload.positionY + discon["positionY"],
                            k * payload.sizeZ + payload.positionZ + discon["positionZ"],
                        )
                        # scene.add(temp_circ)
                        # print(temp_circ.normal)
                        # TODO: Use disc pos too when moving
                        disc = temp_circ.intersections(marb.edges, marb.vertices)
                        if disc:
                            if [
                                round(disc.pos[0], 5),
                                round(disc.pos[1], 5),
                                round(disc.pos[2], 5),
                            ] in processed:
                                continue
                            processed.append(
                                [
                                    round(disc.pos[0], 5),
                                    round(disc.pos[1], 5),
                                    round(disc.pos[2], 5),
                                ]
                            )
                            # scene.add(temp_circ)
                            # scene.add(disc)

                            discon["positionX"] = (
                                i * payload.sizeX
                                + payload.positionX
                                + discon["positionX"]
                            )
                            discon["positionY"] = (
                                j * payload.sizeY
                                + payload.positionY
                                + discon["positionY"]
                            )
                            discon["positionZ"] = (
                                k * payload.sizeZ
                                + payload.positionZ
                                + discon["positionZ"]
                            )
                            discons.append(discon)

    print("Total Dics:", len(discons), a)

    # print(discons)
    # for i in processed:
    #     print(i)

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
    uvicorn.run("api:app", reload=True, workers=5)
