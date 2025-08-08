import fairhelp
import numpy as np

from fair.findable import findable
from fair.accessible import accessible
from fair.interoperable import interoperable
from fair.reproducible import reproducible

hubmap_id = "HBM666.NDQZ.365"

#"HBM666.NDQZ.365"


# square = fairhelp.score(hubmap_id)
findable = findable(hubmap_id)
accessible = accessible(hubmap_id)
interoperable = interoperable(hubmap_id)
reproducible = reproducible(hubmap_id)

fair = [findable, accessible, interoperable, reproducible]
print(fair)
fairhelp.create_fair_plot(
    np.array(fair).reshape(2, 2), scale=100, dpi=100, curated=False
)
