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


#Create hybrid eGRID and EIA-860 matches
#eia = filter_bridges_by_program_list(FRS_Bridges,['EIA-860'])
#egrid = filter_bridges_by_program_list(FRS_Bridges,['EGRID'])

#eia_egrid = pd.merge(eia,egrid,on='REGISTRY_ID',how='left')



#Write matches to bridge
FRS_Bridges.to_csv('facilitymatcher/output/FacilityMatchList_forStEWI.csv',index=False)

