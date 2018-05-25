import facilitymatcher

inventories_to_get = {"TRI":"2014","eGRID":"2014"}

inventory_to_FRS_pgm_acronymn = {"TRI":"TRIS","eGRID":"EGRID"}
program_list = []
for k in inventories_to_get.keys():
    pgm_acronym = inventory_to_FRS_pgm_acronymn[k]
    program_list.append(pgm_acronym)

facilitymatches = facilitymatcher.get_matches_for_StEWI(program_list)




