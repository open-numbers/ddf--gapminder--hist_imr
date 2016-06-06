# -*- coding: utf-8 -*-

import pandas as pd
import os
from ddf_utils.str import to_concept_id
from ddf_utils.index import create_index_file


source = '../source/gapdata002.xlsx'
out_dir = '../../'

# the datapoint name and datapoint id
dp_name_sheet = 'Infant Mortality Rate'
dp_name = dp_name_sheet
dp_id = to_concept_id(dp_name)

if __name__ == '__main__':

    # reading data
    data001 = pd.read_excel(source, sheetname='Data', na_values=['-', '.'])
    data001 = data001.rename(columns={dp_name_sheet: 'area'})

    data001_dp = data001.set_index('area').T
    data001_dp = data001_dp.unstack().reset_index()
    data001_dp.columns = ['area', 'year', 'infant_mortality_rate']

    # entities
    area = data001_dp['area'].unique()
    area_id = list(map(to_concept_id, area))
    ent = pd.DataFrame([], columns=['area', 'name'])
    ent['area'] = area_id
    ent['name'] = area
    path = os.path.join(out_dir, 'ddf--entities--area.csv')
    ent.to_csv(path, index=False)

    # datapoints
    data001_dp['area'] = data001_dp['area'].map(to_concept_id)
    path = os.path.join(out_dir, 'ddf--datapoints--{}--by--area--year.csv'.format(dp_id))
    data001_dp.sort_values(by=['area', 'year']).dropna().to_csv(path, index=False)

    # concepts
    conc = [dp_id, 'area', 'year', 'name']

    cdf = pd.DataFrame([], columns=['concept', 'name', 'concept_type'])

    cdf['concept'] = conc
    cdf['name'] = [dp_name, 'Area', 'Year', 'Name']
    cdf['concept_type'] = ['measure', 'entity_domain', 'time', 'string']

    # index
    create_index_file(out_dir)

    print('Done.')
