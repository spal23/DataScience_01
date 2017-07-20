
'''
Hacked by spal23 (dgpoundall@gmail.com)
'''

import sys

# =================================================== Apply Filters to CSV files
files = ['accidents.csv']
fKey = 'key.csv'

ignore = {'accidents.csv': \
          [
          'Accident_Index',\
          'Longitude',\
          'Latitude',\
          'Date',\
          'Time',\
          'Police_Force',\
          'Local_Authority_(Highway)',\
          'Local_Authority_(District)',\
          'Location_Easting_OSGR',\
          'Location_Northing_OSGR',\
          '1st_Road_Number',\
          '2nd_Road_Number',\
          'LSOA_of_Accident_Location' \
          ], \
          'vehicles': [], \
          'casualties': [] \
          }

kst = ['Dataset','Attribute','Code','Label']        # key structure
badData = ['-1']

# Open the Key file
lines = open(fKey).readlines()                      # open the file and grab the lines
headers = lines[0].split(',')                       # grab the headers
dx = {}
for h in headers: dx[h.strip('\n')] = len(dx)           # index the headers

# Create the keys object group
ooKeys={}
for n in range(1,len(lines)):
    a1 = lines[n].strip('\n').split(',')            # Disseminate field data
    a = a1[dx[kst[0]]]
    b = a1[dx[kst[1]]]
    c = a1[dx[kst[2]]]
    if a not in ooKeys.keys(): ooKeys[a] = {}
    if b not in ooKeys[a].keys(): ooKeys[a][b] = {}
    if c not in ooKeys[a][b].keys(): ooKeys[a][b][c] = a1[dx[kst[3]]]

# --------------------------------------------------- Now checkout the data files
for file in files:
    dx={}
    
    # Open the csv file and index the columns
    f = open(file)                              # open the file
    lines = f.readlines()                       # grab the lines
    headers = lines[0].split(',')               # grab the headers
    for h in headers: dx[h.strip('\n')] = len(dx)           # index the headers   

    # Work down each column in the CSV.
    for hdr in headers:
        h = hdr.strip(' \n')                # Strip spaces and carriage returns from ends of hdr
        # Run down each column...
        # .. Collate the column data into groups (grp), 
        # .. Display the grp quantities,
        # .. Lookup the group id's (gid) in the key object (ooKeys)
        # .. Print the results in the debug window
        if h not in ignore[f.name]:
            print('-----------------------',h)
            # --------------
            # Collate and count
            grp = {}
            for n in range(1,len(lines)):
                a1 = lines[n].strip('\n').split(',')        # Split to columns
                gid = a1[dx[h]]                             # Grab the data (group id) for the column named h     
                if gid not in grp.keys(): 
                    grp[gid] = 1             # initialise the group
                else: 
                    grp[gid] += 1            # increment the number of occurence in the group
            # --------------
            # Now use the key object to decode the 
            # group id's (gid) collated in each column
            for gid in grp.keys():
                fn = file.split('.')[0]       # Grab dataset name  
                if gid not in badData:
                    if fn in ooKeys.keys():
                        if h in ooKeys[fn].keys():
                            if gid in ooKeys[fn][h].keys():
                                print(grp[gid],'=',ooKeys[fn][h][gid])      # print the translated gid info
                        else:
                            print(grp[gid],'=',gid)         # print the gid as is.
            print('')
    
print('DONE')

