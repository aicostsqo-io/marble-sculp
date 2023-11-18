from marble import Marble
from circle import Circle
import json, time, random
from utils import calculate_dip_and_dip_direction_from_unit_vec


class Scene:
    def __init__(self):
        self.objects = []

    def add(self, _object):
        self.objects.append(_object)

    def convert_obj(self):
        data = "mtllib object.mtl\n"
        index_map = {"vertices": {}, "faces": {}}
        for ind, obj in enumerate(self.objects):
            index_map["vertices"][ind] = len(obj.vertices)
            # Vertices
            for vertex in obj.vertices:
                data += f"v {vertex[0]} {vertex[1]} {vertex[2]}\n"

        material = ""
        for ind in range(len(self.objects)):
            material += f"newmtl Material.{ind}\nNs 360.000000\nKa 1.000000 1.000000 1.000000\nKd {random.randint(0, 1000000)/1000000} {random.randint(0, 1000000)/1000000} {random.randint(0, 1000000)/1000000}\nKs 0.500000 0.500000 0.500000\nKe 0.000000 0.000000 0.000000\nNs 0.000000\nd 1.000000\nillum 2\n\n"

        with open("./object.mtl", "w") as fp:
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

        with open("./object.obj", "w") as fp:
            fp.write(data)


start = time.time()
scene = Scene()
marb = Marble()
marb.move(-0.5, -0.5, -0.5)
# scene.add(marb)

circ = Circle()
circ.move(0, 0, 0)
# circ.rotate(60, 45)
# scene.add(circ.intersections(marb.edges, marb.vertices))
# scene.add(circ)

with open("./test.json", "r") as fp:
    test_data = json.loads(fp.read())

for i in test_data:
    circ.rotate(i["dip"], i["dip_direction"])
    disc = circ.intersections(marb.edges, marb.vertices)
    for _ in range(5):
        bae = disc.baecher(i["dip"], i["dip_direction"], 3, "log", 5, 4)
        bae_rot = calculate_dip_and_dip_direction_from_unit_vec(bae["unit_vector"])
        print(
            i["dip"],
            i["dip_direction"],
            calculate_dip_and_dip_direction_from_unit_vec(disc.normal),
        )
        print(bae_rot)
        print("=====")
        scene.add(disc)
        # circ2 = Circle()
        # circ2.rotate(bae_rot[0], bae_rot[1])
        # scene.add(circ2)
    print("*" * 15)

scene.convert_obj()
print("Execution Time:", time.time() - start)
