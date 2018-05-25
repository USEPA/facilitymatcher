import zipfile
import io
import requests

def download_extract_FRS_single_national(FRSpath):
    url = 'https://www3.epa.gov/enviro/html/fii/downloads/state_files/national_combined.zip'
    request = requests.get(url).content
    zip_file = zipfile.ZipFile(io.BytesIO(request))
    zip_file.extractall(FRSpath)

def filter_bridges_by_program_list(bridges,program_list):
    bridges = bridges[bridges['PGM_SYS_ACRNM'].isin(program_list)]
    return bridges

def filter_bridges_by_facility_list(bridges,facility_list):
    bridges = bridges[bridges['REGISTRY_ID'].isin(facility_list)]
    return bridges

def list_facilities_not_in_bridge(bridges, facility_list):
    facilities = bridges[bridges['REGISTRY_ID'].isin(facility_list)]
    return bridges
