# Facility Matcher

Produces faclity matches in a standard format across different EPA inventories, drawing on the
 Facility Registry Service and facility information from the EPA 
 
THIS CODE IS STILL IN EARLY DEVELOPMENT. OUTPUT FILES HAVE NOT YET BEEN TESTED.

## Standard Format
The standard format is a condensed version of the same format used by FRS for the 
[FRS_PROGRAM_FACILITY](https://ofmpub.epa.gov/enviro/ef_metadata_html_frs.ef_metadata_table?p_topic=FRS&p_table_name=FRS_PROGRAM_FACILITY) table.

Field | Type | Required? | Description
----- | ---- | --------  | -----------
REGISTRY_ID|String|Y|EPA FRS ID
PGM_SYS_ACRNM|String|Y|
PGM_SYS_ID|String|Y|


## Disclaimer
The United States Environmental Protection Agency (EPA) GitHub project code is provided on an "as is" basis 
and the user assumes responsibility for its use.  EPA has relinquished control of the information and no longer 
has responsibility to protect the integrity , confidentiality, or availability of the information. 
Any reference to specific commercial products, processes, or services by service mark, trademark, manufacturer, 
or otherwise, does not constitute or imply their endorsement, recommendation or favoring by EPA.  
The EPA seal and logo shall not be used in any manner to imply endorsement of any commercial product or activity 
by EPA or the United States Government.

   