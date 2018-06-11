#This script gets FRS data in the form of the FRS combined national files
#https://www.epa.gov/enviro/epa-state-combined-csv-download-files
#It uses the bridges in the 'NATIONAL_ENVIRONMENTAL_INTEREST_FILE.CSV'
#It writes facility matching file for StEWI (github.com/usepa/standardizedinventories) programs

import pandas as pd
import os

from facilitymatcher.globals import filter_bridges_by_program_list
from facilitymatcher.globals import download_extract_FRS_combined_national

FRSpath = '../FRS/'

FRS_bridge_file = 'NATIONAL_ENVIRONMENTAL_INTEREST_FILE.CSV'
FRS_bridge_file_path = FRSpath + FRS_bridge_file

#Check to see if file exists
if not(os.path.exists(FRS_bridge_file_path)):
    download_extract_FRS_combined_national()

#Import FRS bridge which provides ID matches
FRS_Bridges = pd.read_csv(FRS_bridge_file_path, header=0,usecols=['REGISTRY_ID','PGM_SYS_ACRNM', 'PGM_SYS_ID'],dtype={'REGISTRY_ID':"str",'PGM_SYS_ACRNM':"str",'PGM_SYS_ID':"str"})
#Or Load all bridges from pickle
FRS_Bridges = pd.read_pickle('frsbridges.pk')

#See programs available
pd.unique(FRS_Bridges['PGM_SYS_ACRNM'])

#Limit to EPA programs of interest for StEWI
programs_of_interest  = ['EIS','NPDES','TRIS','RCRAINFO','EGRID','E-GGRT','EIA-860']

FRS_Bridges = filter_bridges_by_program_list(FRS_Bridges,programs_of_interest)

#Separate out eGRID and EIA-860 matches to identify EIA matches to add to eGRID set
eia = filter_bridges_by_program_list(FRS_Bridges,['EIA-860'])
egrid = filter_bridges_by_program_list(FRS_Bridges,['EGRID'])

#get a list of all FRS in each
eia_unique_frs = set(list(pd.unique(eia['REGISTRY_ID'])))
egrid_unique_frs = set(list(pd.unique(egrid['REGISTRY_ID'])))

eia_not_in_egrid = eia_unique_frs - egrid_unique_frs
eia_to_add = eia[eia['REGISTRY_ID'].isin(eia_not_in_egrid)]
len(eia_to_add)
eia_to_add.head(5)
#Will add 1781

#Rename to EGRID
eia_to_add['PGM_SYS_ACRNM'] = 'EGRID'
#Now add this subset back
FRS_Bridges = pd.concat([FRS_Bridges,eia_to_add])

len(FRS_Bridges[FRS_Bridges['PGM_SYS_ACRNM'] == 'EGRID'])



#Write matches to bridge
FRS_Bridges.to_csv('facilitymatcher/output/FacilityMatchList_forStEWI.csv',index=False)

