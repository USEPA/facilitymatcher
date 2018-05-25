import pandas as pd
import os
import logging
from facilitymatcher.globals import filter_bridges_by_program_list

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

try: modulepath = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/') + '/'
except NameError: modulepath = 'facilitymatcher/'

output_dir = modulepath + 'output/'

stewi_programs = ['EIS','NPDES','TRIS','RCRAINFO','EGRID','E-GGRT']

def get_matches_for_StEWI(program_list=stewi_programs):
    facilitymatches = pd.read_csv(output_dir+'FacilityMatchList_forStEWI.csv',dtype={"REGISTRY_ID":"str","PGM_SYS_ID":"str"})
    facilitymatches = filter_bridges_by_program_list(facilitymatches,program_list)
    return facilitymatches

def get_matches_from_program_to_program_of_interest(from_program_acronym,to_program_acronym):
    facilitymatches = get_matches_for_StEWI()
    from_program_bridge = filter_bridges_by_program_list(facilitymatches,[from_program_acronym])
    to_program_bridge = filter_bridges_by_program_list(facilitymatches,[to_program_acronym])
    matches = pd.merge(from_program_bridge,to_program_bridge,on='REGISTRY_ID',how='left')
    matches = matches[['PGM_SYS_ID_x','PGM_SYS_ID_y']]
    return matches

