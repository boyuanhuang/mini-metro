from shapely.geometry import Polygon
from descartes import PolygonPatch
import matplotlib.pyplot as plt

# Polygon exterior:
polygone_exterior = [(0, 100), (600, 100), (700, 500), (900, 500), (900, 550), (300, 550), (150, 150), (0, 150), (0, 100)]
island = [(250, 150), (450, 150), (650, 500), (450, 500), (250, 150)]

# Define interior "holes":
interiors = {}
interiors[0] = island
i_p = {k: Polygon(v) for k, v in interiors.items()}


WATERZONE = Polygon(polygone_exterior, [zone.exterior.coords for zone in i_p.values() \
                                        if zone.within(Polygon(polygone_exterior)) is True])

fig, ax = plt.subplots()
patch = PolygonPatch(WATERZONE.buffer(0))
ax.add_patch(patch)
ax.set_xlim(0, 900)
ax.set_ylim(0, 700)
plt.show()