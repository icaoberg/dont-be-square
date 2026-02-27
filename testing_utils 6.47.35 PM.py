import fair.utils 
import pandas as pd
import os

'''path = 'fair/hubmap_data.csv'
if not os.path.exists(path):
    print('File not found!')
    df = fair.utils.existing_names_to_df()'''

df = fair.utils.read_json_fair()
assay = 'RNAseq'
name = 'Stanford TMC'
###################################

print('\nSearch by lab')
lab_result = (fair.utils.search_by_lab(df,name))
result = fair.utils.mean_fair_results(lab_result)
fair.utils.create_heatmap_for(result, name)
print(f'Lab: {name} \nResult: {result}')

###################################
print('\nSearch by assay')
assay_result = (fair.utils.search_by_assay(df,assay))
result = fair.utils.mean_fair_results(assay_result)
fair.utils.create_heatmap_for(result, assay)
print(f'Assay: {assay} \nResult: {result}')

###################################

print('\nSearch by lab/assay')
lab_assay_result = (fair.utils.search_by_lab_assay(df,name,assay))
result = fair.utils.mean_fair_results(lab_assay_result)
fair.utils.create_heatmap_for(result, f'{name}/{assay}')
print(f'Lab: {name} \nAssay: {assay} \nResult: {result}')

'''print('\nSearch all')
all_result = (fair.utils.search_all_id(df))
result = fair.utils.mean_fair_results(all_result)
print(f'All datasets \nResult: {result}')'''