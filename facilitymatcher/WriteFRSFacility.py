import pandas as pd

FRSpath = '../FRS/'
FRS_facility_file = 'NATIONAL_FACILITY_FILE.CSV'
FRS_facility_file_path = FRSpath + FRS_facility_file

FRS_facility = pd.read_csv(FRS_facility_file_path, header=0, nrows=10)
FRS_facility.head()
cols_to_keep=['REGISTRY_ID', 'PRIMARY_NAME','LOCATION_ADDRESS', 'CITY_NAME', 'STATE_CODE', 'POSTAL_CODE',
              'COUNTY_NAME','LATITUDE83','LONGITUDE83']
dtype_dict = {'REGISTRY_ID':"str",'PRIMARY_NAME':"str",'LOCATION_ADDRESS':"str",
              'CITY_NAME':"str",'STATE_CODE':"str",'POSTAL_CODE':"str",
              'LATITUDE83':"str",'LONGITUDE83':"str"}

#Now read it in chunks for memory management
FRS_facility = pd.DataFrame()
for chunk in pd.read_csv(FRS_facility_file_path, header=0,usecols=cols_to_keep,dtype=dtype_dict,chunksize=100000):
    FRS_facility = pd.concat([FRS_facility,chunk])

FRS_facility.to_csv('facilitymatcher/output/FRS_Facility.csv',index=False)
#Pickle it for faster retrieval later
FRS_facility.to_pickle('facilitymatcher/output/FRS_Facility.pk')
