import fairhelp
import numpy as np

from fair.findable import findable
from fair.accessible import accessible
from fair.interoperable import interoperable
from fair.reproducible import reproducible
from fair.utils import list_of_names_df
from fair.utils import existing_names_to_df

df = existing_names_to_df()
print(df.head())

'''
all_assay_results = []
data = { 'data': 'HBM573.VSJK.526'}
    "10x multiome": "HBM738.KGBN.464",
    "codex": "HBM734.XBSR.357",
    "atacseq": "HBM426.JKVD.368",
    'codex_test':"HBM666.NDQZ.365",
    "10x_test": "HBM295.QRXK.297",
    "2d image": "HBM465.SSNC.296",
    "3d image": "HBM778.VHHR.349",
    "atacseq": "HBM426.JKVD.368",
    "scrna seq": "HBM642.GNSK.367",
    "visium (no probes)": "HBM937.RTLZ.357",
    "seqFISH": "HBM682.TWTR.428"
    }

for assay, hubmap_id in data.items():
    print(f'Dataset: {assay} - {hubmap_id}')
    

    hubmap_id = str(hubmap_id)
    is_findable,score_findable = findable((hubmap_id))
    is_accessible,score_accessible = accessible(hubmap_id)
    is_interoperable,score_interoperable = interoperable(hubmap_id)
    is_reproducible,score_reproducible = reproducible(hubmap_id)


    fair = [is_findable, is_accessible, is_interoperable, is_reproducible]
    #print(f'\t{fair}')
    score =[score_findable, score_accessible,score_interoperable,
            score_reproducible]

    results_tuple = ((assay,hubmap_id,score))
    all_assay_results.append(results_tuple)

'''

'''
    fairhelp.create_fair_plot(
        np.array(fair).reshape(2, 2), scale=100, dpi=100, curated=False
    )
'''

'''
print('########## List of all FAIR datasets ##########')
for assay in all_assay_results:
    print('####################')   
    print(f'{assay[0]}')
    print(f'\t{assay[1]}')

    print(f'\tF: {assay[2][0]}')
    print(f'\tA: {assay[2][1]}')
    print(f'\tI: {assay[2][2]}')
    print(f'\tR: {assay[2][3]}')

df = list_of_names_df()
print(df.head())

'''