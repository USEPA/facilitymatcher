import pandas as pd

datapath = 'facilitymatcher/data/'
output_folder = 'facilitymatcher/output/'

#Load bridges from pickle
FRS_Bridges = pd.read_pickle('frsbridges.pk')
#FRS_Bridges = pd.read_csv(FRS_BridgeFile, header=0,usecols=['REGISTRY_ID','PGM_SYS_ACRNM', 'PGM_SYS_ID',],dtype={'REGISTRY_ID':"str",'PGM_SYS_ACRNM':"str",'PGM_SYS_ID':"str"})

#Limit to EPA programs of interest
from facilitymatcher.globals import filter_bridges_by_program_list
program_list = ['EIS','NPDES','TRIS']
FRS_Bridges_2 = filter_bridges_by_program_list(FRS_Bridges,program_list)

#Limit to facilities of interest
from facilitymatcher.globals import filter_bridges_by_facility_list
facilities = pd.read_csv(datapath+'examplefacilitylistforfilter.csv',header=None,dtype="str")
facility_list = list(facilities[0])
FRS_Bridges_3 = filter_bridges_by_facility_list(FRS_Bridges_2,facility_list)
FRS_Bridges_3.to_csv('facilitymatcher/output/examplefacilitymatchtable2.csv',index=False)

