from marble import Marble
from circle import Circle


class Scene:
    def __init__(self):
        self.objects = []

    def add(self, _object):
        self.objects.append(_object)

    def convert_obj(self):
        data = ""
        index_map = {"vertices": {}, "faces": {}}
        for ind, obj in enumerate(self.objects):
            index_map["vertices"][ind] = len(obj.vertices)
            # Vertices
            for vertex in obj.vertices:
                data += f"v {vertex[0]} {vertex[1]} {vertex[2]}\n"

        for ind, obj in enumerate(self.objects):
            # Faces
            offset = 1
            if ind > 0:
                offset = ind * index_map["vertices"][ind - 1] + 1
            for face in obj.faces:
                temp = ""
                for vertex in face:
                    temp += f"{offset+vertex} "
                data += f"f {temp}\n"

        with open("./object.obj", "w") as fp:
            fp.write(data)


scene = Scene()
marb = Marble()
marb.move(-0.5, -0.5, -0.5)
scene.add(marb)

circ = Circle()
circ.rotate(180, 0)
scene.add(circ)
scene.convert_obj()
