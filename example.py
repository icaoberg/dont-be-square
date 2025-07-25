import fairhelp
import numpy as np

hubmap_id = "HBM666.NDQZ.365"

# square = fairhelp.score(hubmap_id)
findable = fairhelp.findable(hubmap_id)
accessible = fairhelp.accessible(hubmap_id)
interoperable = fairhelp.interoperable(hubmap_id)
reproducible = fairhelp.reproducible(hubmap_id)

fair = [findable, accessible, interoperable, reproducible]
print(fair)
fairhelp.create_fair_plot(
    np.array(fair).reshape(2, 2), scale=100, dpi=100, curated=False
)
