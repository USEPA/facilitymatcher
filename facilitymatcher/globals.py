import zipfile
import io
import requests

inventory_to_FRS_pgm_acronymn = {"NEI":"EIS","TRI":"TRIS","eGRID":"EGRID","GHGRP":"E-GGRT","RCRAInfo":"RCRAINFO","DMR":"NPDES"}

def download_extract_FRS_single_national(FRSpath):
    url = 'https://www3.epa.gov/enviro/html/fii/downloads/state_files/national_combined.zip'
    request = requests.get(url).content
    zip_file = zipfile.ZipFile(io.BytesIO(request))
    zip_file.extractall(FRSpath)

def filter_bridges_by_program_list(bridges,program_list):
    bridges = bridges[bridges['PGM_SYS_ACRNM'].isin(program_list)]
    return bridges

def filter_bridges_by_inventory_list(bridges,inventory_list):
    bridges = bridges[bridges['PGM_SYS_ACRNM'].isin(inventory_list)]
    return bridges

def filter_bridges_by_facility_list(bridges,facility_list):
    bridges = bridges[bridges['REGISTRY_ID'].isin(facility_list)]
    return bridges

def list_facilities_not_in_bridge(bridges, facility_list):
    facilities = bridges[bridges['REGISTRY_ID'].isin(facility_list)]
    return bridges

#Returns list of acronymns for inventories that correspond to
def get_programs_for_inventory_list(list_of_inventories):
    program_list = []
    for l in list_of_inventories:
        pgm_acronym = inventory_to_FRS_pgm_acronymn[l]
        program_list.append(pgm_acronym)
    return program_list

def invert_inventory_to_FRS():
    FRS_to_inventory_pgm_acronymn = {v: k for k, v in inventory_to_FRS_pgm_acronymn.items()}
    return FRS_to_inventory_pgm_acronymn


