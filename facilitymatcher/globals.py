def filter_bridges_by_program_list(bridges,program_list):
    bridges = bridges[bridges['PGM_SYS_ACRNM'].isin(program_list)]
    return bridges

def filter_bridges_by_facility_list(bridges,facility_list):
    bridges = bridges[bridges['REGISTRY_ID'].isin(facility_list)]
    return bridges

def list_facilities_not_in_bridge(bridges, facility_list):
    facilities = bridges[bridges['REGISTRY_ID'].isin(facility_list)]
    return bridges
