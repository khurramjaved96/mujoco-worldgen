from collections import OrderedDict

import numpy as np

from mujoco_worldgen.objs.obj import Obj
from mujoco_worldgen.util.types import store_args


class Floor(Obj):
    '''
    Floor() is essentially a special box geom used as the base of experiments.
    It has no joints, so is essentially an immovable object.
    Placement is calculated in a fixed position, and encoded in XML,
        as opposed to in qpos, which other objects use.
    '''

    @store_args
    def __init__(self, geom_type='plane'):
        super(Floor, self).__init__()

    def generate(self, random_state, world_params, placement_size):
        top = OrderedDict(origin=(0, 0, 0), size=placement_size)
        self.placements = OrderedDict(top=top)
        self.size = np.array([placement_size[0], placement_size[1], 0.0])

    def generate_xml_dict(self):
        # Last argument in size is visual mesh resolution (it's not height).
        # keep it high if you want rendering to be fast.
        pos = self.absolute_position
        pos[0] += self.size[0] / 2.0
        pos[1] += self.size[1] / 2.0
        # pos[2] = 2
        print("Position =", pos)
        geom = OrderedDict()

        geom['@name'] = self.name
        geom['@pos'] = pos
        if self.geom_type == 'box':
            geom['@size'] = np.array([self.size[0] / 2.0, self.size[1] / 2.0, 0.000001])
            geom['@type'] = 'box'

        elif self.geom_type == 'plane':
            geom['@size'] = np.array([self.size[0] / 2.0, self.size[1] / 2.0, 1.0])
            geom['@type'] = 'plane'
        else:
            raise ValueError("Invalid geom_type: " + self.geom_type)
        geom['@condim'] = 3
        geom['@name'] = self.name
        geom['@material'] = "MatPlane"

        # body is necessary to place sites.
        body = OrderedDict()
        body["@name"] = self.name
        body["@pos"] = pos

        worldbody = OrderedDict([("geom", [geom]),
                                 ("body", [body])])
        material = OrderedDict()
        material["@name"] = "MatPlane"
        material["@reflectance"] = "0.5"
        material["@texture"] = "texplane"
        material["@texrepeat"] = "1 1"
        material["@texuniform"] = "true"

        material2 = OrderedDict()
        material2["@name"] = "texplane"
        material2["@type"] = "2d"
        material2["@builtin"] = "checker"
        material2["@rgb1"] = ".2 .3 .4"
        material2["@rgb2"] = ".1 0.15 0.2"
        material2["@width"] = "512"
        material2["@height"] = "512"

        assets = OrderedDict([('texture', [material2]),
                                          ('material', [material])])
        # print(assets)
        # 0/0
        xml_dict = OrderedDict(asset=assets, worldbody=worldbody)
        xml_dict
        return xml_dict
