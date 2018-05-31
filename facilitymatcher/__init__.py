import pandas as pd
import os
import logging
from facilitymatcher.globals import filter_bridges_by_inventory_list
from facilitymatcher.globals import filter_bridges_by_program_list
from facilitymatcher.globals import get_programs_for_inventory_list
from facilitymatcher.globals import invert_inventory_to_FRS

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

try: modulepath = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/') + '/'
except NameError: modulepath = 'facilitymatcher/'

output_dir = modulepath + 'output/'

stewi_inventories = ['NEI','DMR','TRI','RCRAInfo','eGRID','GHGRP']

def get_matches_for_inventories(inventory_list=stewi_inventories):
    program_list = get_programs_for_inventory_list(inventory_list)
    facilitymatches = pd.read_csv(output_dir+'FacilityMatchList_forStEWI.csv',dtype={"REGISTRY_ID":"str","PGM_SYS_ID":"str"})
    facilitymatches = filter_bridges_by_program_list(facilitymatches,program_list)
    #Set program names back to inventory names
    FRS_to_inventory_pgm_acronymn = invert_inventory_to_FRS()
    facilitymatches['PGM_SYS_ACRNM'].replace(FRS_to_inventory_pgm_acronymn, inplace=True)
    return facilitymatches

def get_matches_from_inventory_to_inventories_of_interest(from_inventory_acronym,list_of_to_inventory_acronyms):
    inventory_acronyms = []
    inventory_acronyms.append(from_inventory_acronym)
    for l in list_of_to_inventory_acronyms:
        inventory_acronyms.append(l)
    facilitymatches = get_matches_for_inventories(inventory_acronyms)
    from_inventory_acronym_list = []
    from_inventory_acronym_list.append(from_inventory_acronym)
    from_program_bridge = filter_bridges_by_inventory_list(facilitymatches,from_inventory_acronym_list)
    to_program_bridge = filter_bridges_by_inventory_list(facilitymatches,list_of_to_inventory_acronyms)
    matches = pd.merge(from_program_bridge,to_program_bridge,on='REGISTRY_ID')
    return matches

def get_table_of_matches_from_inventory_to_inventories_of_interest(from_inventory_acronym,list_of_to_inventory_acronyms):
    matches = get_matches_from_inventory_to_inventories_of_interest(from_inventory_acronym, list_of_to_inventory_acronyms)
    table_of_matches = matches[['REGISTRY_ID','PGM_SYS_ACRNM_x','PGM_SYS_ID_x','PGM_SYS_ACRNM_y','PGM_SYS_ID_y']]
    return table_of_matches

#A table of match counts
def count_matches_from_inventory_to_inventories_of_interest(from_inventory_acronym,list_of_to_inventory_acronyms):
    matches = get_matches_from_inventory_to_inventories_of_interest(from_inventory_acronym, list_of_to_inventory_acronyms)
    matches_group = matches.groupby(['PGM_SYS_ACRNM_x','PGM_SYS_ACRNM_y'])['REGISTRY_ID'].count()
    matches_flat = matches_group.reset_index()
    matches_flat.columns = ['From_Inventory','To_Inventory','Count_of_Facility_Matches']
    return matches_flat

