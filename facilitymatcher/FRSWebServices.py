#Functions to return facility info from FRS web service
#Limitation - the web service only matches on facility at a time
#Should be refactored if useful

import requests
import json
#base url

base = 'http://ofmpub.epa.gov/enviro/frs_rest_services'
facilityquery = base + '.get_facilities?'
pgm_sys_id = 'pgm_sys_id='
pgm_sys_acrnm = 'pgm_sys_acrnm='
stateabbr = 'state_abbr='
output='output=JSON'


#example
id='2'
program_acronym='EGRID'

def getFRSIDforProgramNameandIDfromAPI(program_acronym,id):
      url = facilityquery + pgm_sys_acrnm + program_acronym + '&'  + pgm_sys_id + id  + '&'  + output
      facilityresponse = requests.get(url)
      facilityjson = json.loads(facilitylistresponse.text)['Results']
      facilityinfo = facilityjson['FRSFacility']
      FRSID = facilityinfo[0]['RegistryId']
      return FRSID

#test
print(getFRSIDforProgramNameandIDfromAPI(program_acronym,id))
