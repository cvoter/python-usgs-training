import requests
import os
import pandas as pd

def get_NWIS(station_id):
    '''
    This is a super awesome nwis pullermatic machine
    run it like so:
    get_nwis(station_id) --> station_id should be a USGS proper station id
    '''

    # url to pull station id from NWIS
    url='http://waterservices.usgs.gov/nwis/gwlevels/?format=rdb,1.0&sites={0}&startDT=1880-01-01&endDT=2018-01-01&siteType=GW'.format(station_id)
    
    # get object pointing to file at url
    dv_file = requests.get(url)

    # write file to the local disk
    with open(os.path.join('data',"{0}.dat".format(station_id)), 'w') as ofp:
        for carp in dv_file:
            ofp.write(carp.decode())
    
    NWISfilename = os.path.join('data',"{0}.dat".format(station_id))
    reconnoiter = open(NWISfilename, 'r').readlines()
    
    # loop over lines of file to find the number of contents
    numhash = 0 #let's use the as the counter
    for line in reconnoiter:
        if line.startswith('#'):
            numhash +=1
        else:
            break
    
    # get column names from the file
    colnames = reconnoiter[numhash].rstrip().split()
    
    # read in the file to a pandas dataframe
    nwis_df = pd.read_csv(url, 
                          sep='\t',
                          skiprows = numhash + 2,
                          names = colnames,
                          parse_dates = True,
                          index_col = 3)
    
    return nwis_df