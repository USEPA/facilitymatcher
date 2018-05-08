import numpy as np
import pandas as pd
from facilitymatcher.globals import filter_bridges_by_program_list

datapath = 'facilitymatcher/data/'

#This script gets FRS data in the form of the FRS single national files
#'NATIONAL_ENVIRONMENTAL_INTEREST_FILE.CSV' for bridges across programs and the
#'NATIONAL_FACILITY_FILE.csv' for facility information.
#Example files 'examplefrsbridge' and 'examplefrsfacility' are used here

#Import FRS bridge which provides ID matches
FRS_BridgeFile = datapath + 'examplefrsbridge.csv'
FRS_Bridges = pd.read_csv(FRS_BridgeFile, header=0,usecols=['REGISTRY_ID','PGM_SYS_ACRNM', 'PGM_SYS_ID',],dtype={'REGISTRY_ID':"str",'PGM_SYS_ACRNM':"str",'PGM_SYS_ID':"str"})
#Or Load all bridges from pickle
FRS_Bridges = pd.read_pickle('frsbridges.pk')

#Limit to EPA programs of interest

programs_of_interest  = ['EIS','NPDES','TRIS','BR','RCRAINFO','EGRID']
FRS_Bridges = filter_bridges_by_program_list(FRS_Bridges,programs_of_interest)
#or for one program
FRS_Bridges = filter_bridges_by_program_list(FRS_Bridges,['EIS'])

#Import national facility file
frs_national_file = datapath + 'examplefrsfacility.csv'
FRS_National = pd.read_csv(frs_national_file, header=0, usecols=['REGISTRY_ID', 'PRIMARY_NAME','LOCATION_ADDRESS', 'CITY_NAME', 'STATE_CODE', 'POSTAL_CODE','LATITUDE83','LONGITUDE83'])
#or load from pickle
FRS_National = pd.read_pickle('frs_national.pk')

#import facility info from an inventory. These file will come from StEWI
nei2014_facility_file = datapath + 'exampleinventoryfacilitytable.csv'
NEI2014facilityinfo = pd.read_csv(nei2014_facility_file, header=0, dtype={'FacilityID':"str",'Name':"str",'Address':"str",'City':"str",'State':"str",'Zip':"str",'Latitude':np.float64,'Longitude':np.float64})
NEI2014facilityinfo.rename(columns={'FacilityID':'NEI'}, inplace=True)


##LOCATION_BASED MATCHING
#Converting from String to Numeric datatype
FRS_National['LATITUDE'] = pd.to_numeric(FRS_National['LATITUDE83'],errors='coerce')
FRS_National['LONGITUDE'] = pd.to_numeric(FRS_National['LONGITUDE83'],errors='coerce')

#Round lat to 3 and try to match
NEI2014facilityinfo['Latitude3']=round(NEI2014facilityinfo['Latitude'],3)
NEI2014facilityinfo['Longitude3']=round(NEI2014facilityinfo['Longitude'],3)
FRS_National['Latitude3'] = round(FRS_National['LATITUDE'],3)
FRS_National['Longitude3'] = round(FRS_National['LONGITUDE'],3)

matches_at_3_digit = pd.merge(FRS_National,NEI2014facilityinfo,on=['Latitude3','Longitude3'],how='inner')
print ("Identified "+ str(len(matches_at_3_digit)) + " match at 3 decimals.")

#Reformat with only needed columns
matches_to_add = matches_at_3_digit[['REGISTRY_ID','NEI']]
matches_to_add['PGM_SYS_ACRNM']='EIS'
matches_to_add.rename(columns={"NEI":"PGM_SYS_ID"},inplace=True)

all_bridges = pd.concat([FRS_Bridges,matches_to_add])

#Add matches to bridge
all_bridges.to_csv('facilitymatcher/output/examplefaciltymatchingtable.csv',index=False)

