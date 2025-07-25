import fairhelp
import numpy as np

hubmap_id = "HBM666.NDQZ.365"

# square = fairhelp.score(hubmap_id)
metadata = fairhelp.__get_metadata(hubmap_id)
print(metadata)
