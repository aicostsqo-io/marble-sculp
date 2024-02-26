from marble import Marble
from circle import Circle
import json, time, random, uuid, copy
from typing import List
from scipy.spatial import ConvexHull
import numpy as np

from models import Discontinous
from utils import calculate_dip_and_dip_direction_from_unit_vec


class Scene:
    def __init__(self):
        self.objects = []

    def add(self, _object):
        self.objects.append(copy.deepcopy(_object))

    def convert_obj(self, filename: str) -> str:
        data = "mtllib object.mtl\n"
        index_map = {"vertices": {}, "faces": {}}
        for ind, obj in enumerate(self.objects):
            index_map["vertices"][ind] = len(obj.vertices)
            # Vertices
            data += f"o Marble{ind}\n"
            for vertex in obj.vertices:
                data += f"v {vertex[0]} {vertex[1]} {vertex[2]}\n"

        material = ""
        for ind in range(len(self.objects)):
            material += f"newmtl Material.{ind}\nNs 360.000000\nKa 1.000000 1.000000 1.000000\nKd {random.randint(0, 1000000)/1000000} {random.randint(0, 1000000)/1000000} {random.randint(0, 1000000)/1000000}\nKs 0.500000 0.500000 0.500000\nKe 0.000000 0.000000 0.000000\nNs 0.000000\nd 1.000000\nillum 9\n\n"

        with open(f"./static/{filename}.mtl", "w") as fp:
            fp.write(material)

        offset = 1
        for ind, obj in enumerate(self.objects):
            # Faces
            data += f"usemtl Material.{ind}\n"
            for face in obj.faces:
                temp = ""
                for vertex in face:
                    temp += f"{offset+vertex} "
                data += f"f {temp}\n"

            offset += index_map["vertices"][ind]

        with open(f"./static/{filename}.obj", "w") as fp:
            fp.write(data)
        return filename

    def polyhedron(self, size: List[int], pos: List[int], data: List[Discontinous]):
        marb = Marble(
            size=size,
            pos=pos,
        )
        temp_objects = []
        objects = [marb]
        processed = []
        for i in data:
            # print(i["positionX"], i["positionY"], i["positionZ"])
            # if [
            #     i["dip"],
            #     i["dipDirection"],
            #     round(i["positionX"], 5),
            #     round(i["positionY"], 5),
            #     round(i["positionZ"], 5),
            # ] in processed:
            #     continue
            # processed.append(
            #     [
            #         i["dip"],
            #         i["dipDirection"],
            #         round(i["positionX"], 5),
            #         round(i["positionY"], 5),
            #         round(i["positionZ"], 5),
            #     ]
            # )
            circ = Circle(radius=10)
            circ.rotate(i["dip"], i["dipDirection"])
            circ.move(i["positionX"], i["positionY"], i["positionZ"])
            # self.add(circ)
            for obj in objects:
                disc = circ.intersections(obj.edges, obj.vertices)
                if disc is None:
                    # print("None")
                    temp_objects.append(obj)
                    continue

                # self.add(disc)

                left = [d for d in disc.vertices]
                right = [d for d in disc.vertices]

                for j in obj.vertices:
                    # print(np.dot(disc.normal, np.array(j) - disc.normal))
                    # print(np.dot(disc.normal, np.array(j)) + circ.constant)

                    if np.dot(disc.normal, np.array(j)) + circ.constant < 0:
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
            self.add(i)

        print(len(objects), len(processed))


if __name__ == "__main__":
    # import numpy as np
    # from scipy.spatial import ConvexHull

    # scene = Scene()
    # marb = Marble(size=(10, 10, 10))
    # objects = [marb]
    # temp_objects = []
    # # scene.add(marb)
    # circ = Circle(radius=15)

    # with open("./test.json", "r") as fp:
    #     test_data = json.loads(fp.read())

    # processed = []
    # start = time.time()
    # for i in test_data[:]:
    #     if [i["dip"], i["dip_direction"]] in processed:
    #         continue
    #     processed.append([i["dip"], i["dip_direction"]])
    #     circ.rotate(i["dip"], i["dip_direction"])
    #     for obj in objects:
    #         disc = circ.intersections(obj.edges, obj.vertices)
    #         if disc is None:
    #             temp_objects.append(obj)
    #             continue

    #         left = [d for d in disc.vertices]
    #         right = [d for d in disc.vertices]

    #         for j in obj.vertices:
    #             if np.dot(circ.normal, j) < 0:
    #                 left.append(j)
    #             else:
    #                 right.append(j)

    #         if len(left) > 3:
    #             temp_objects.append(
    #                 Marble.from_points(
    #                     left, ConvexHull(left, qhull_options="QJ Pp").simplices
    #                 )
    #             )
    #         if len(right) > 3:
    #             temp_objects.append(
    #                 Marble.from_points(
    #                     right, ConvexHull(right, qhull_options="QJ Pp").simplices
    #                 )
    #             )
    #     objects = temp_objects
    #     temp_objects = []

    # # scene.add(circ)

    # for i in objects:
    #     scene.add(i)

    # print(len(objects))

    # print("Execution Time:", time.time() - start)
    # scene.convert_obj("ibo")
    # print("Total Time:", time.time() - start)
    start = time.time()
    scene = Scene()

    # marb = Marble()
    # # marb.move(-0.5, -0.5, -0.5)
    # # scene.add(marb)

    circ = Circle()
    # # circ.move(0, 0, 0)
    circ.rotate(0, 80)
    scene.add(circ)
    # # scene.add(circ.intersections(marb.edges, marb.vertices))
    # # scene.add(circ)

    # with open("./test.json", "r") as fp:
    #     test_data = json.loads(fp.read())

    # for i in test_data:
    #     circ.rotate(i["dip"], i["dip_direction"])
    #     disc = circ.intersections(marb.edges, marb.vertices)
    #     # scene.add(disc)
    #     for _ in range(5):
    #         bae = disc.baecher(i["dip"], i["dip_direction"], 3, "log", 5, 4)
    #         bae_rot = calculate_dip_and_dip_direction_from_unit_vec(bae["unit_vector"])
    #         print(
    #             i["dip"],
    #             i["dip_direction"],
    #             calculate_dip_and_dip_direction_from_unit_vec(disc.normal),
    #         )
    #         print(bae_rot)
    #         print("=====")
    #         circ2 = Circle()
    #         circ2.rotate(bae_rot[0], bae_rot[1])
    #         scene.add(circ2.intersections(marb.edges, marb.vertices))
    #     print("*" * 15)

    # print(len(scene.objects))
    scene.convert_obj("asds")
    # print("Execution Time:", time.time() - start)
