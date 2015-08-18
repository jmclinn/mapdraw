import os,time

## File Variable (USER INPUT)
## ==========================
## if multiple files are being accessed to create movie...
## ...specify the beginning and ending of the file names...
## ...and the date list text file in the variables below

## Please use True or False to set whether multiple files will be accessed for movie
file_is_variable = False

## If file_is_variable = True
path_to_files = '/scratch/haluie/Ocean/POPdata/'
file_part1 = 'h.14c.'
file_part2 = '.nc'
dates_list_text_file = '/scratch/haluie/Ocean/POPdata/dates_short.txt'

## If file_is_variable = False
file = '/scratch/haluie/Ocean/POPdata/h.14c.19980302.nc'


## Variables (USER INPUT)
## ======================
## all variable lists must be the same length
## set unused variables equal to '_empty_'
## if variable requires double-quotes on command line include them --> '" ... "'
## -----------------------------------------------------------------------------

data = 'sgsflux' #cannot be '_empty_'
lat = 'u_lat' #cannot be '_empty_'
lon = 'u_lon' #cannot be '_empty_'
depth = 'w_dep,9' #cannot be '_empty_'
mask = '-1e33,#000000'
maxr = '100' #use for 'max'
minr = '-100' #use for 'min'
norm = '_empty_'
colors = '"0:#0000AA,45:#0000FF,50:#FFFFFF,55:#FF0000,100:#AA0000"'
clr_min_max = '_empty_'
title = '_empty_'
crop = '_empty_'
lines = '_empty_'

## Primary Variable (USER INPUT)
## =============================
## choose from the variables above
## specify without quotes
## if not a list will only output single result
## --------------------------------------------

primary_variable = file

## Save Location (USER INPUT)
## ==========================
## provide folder location (without filename(s))
## ---------------------------------------------

save = '/scratch/haluie/Ocean/AnalOutput/movie/'

## Image Filename Prefix (USER INPUT)
## ==================================
## prefix for output filenames before auto-incremented counter
## -----------------------------------------------------------

file_prefix = 'SGSmov_'

## Image Counter Start (USER INPUT)
## ================================
## start of auto-incremented counter 
## ---------------------------------

count_start = 0

## Image File Type (USER INPUT)
## ============================
## ex: '.png' or '.jpg'
## --------------------

img_type = '.png'

## Display Toggle (USER INPUT)
## ==========================
## toggle if each image displays in the loop
## use 'yes' or 'no' to control display preference
## -----------------------------------------------

display = 'no'

# # # # # # # # # # # # # # # # # # # # # # # # #
#   ---- NO USER INPUTS AFTER THIS POINT ----   #
# # # # # # # # # # # # # # # # # # # # # # # # #

## If 'file' is variable this establishes list of files to loop through (Do Not Alter)
## ===================================================================================
if file_is_variable:
   file1 = []
   file0 = open(dates_list_text_file,'r').read().splitlines()
   for line in file0:
      file1.append(str(path_to_files) + str(file_part1) + str(line) + str(file_part2))
   file = file1
   primary_variable = file


## Defining & Executing Command Expression (Do Not Alter)
## ======================================================

displayx = 'display ' + display
command = displayx
if title != '_empty_':
   titlex = ' title ' + str(title)
   command = command + titlex
if lines != '_empty_':
   linesx = ' lines ' + str(lines)
   command = command + linesx

if type(primary_variable) is list:
   loop_len = len(primary_variable)
else:
   loop_len = 1

for i in range(loop_len):
   savex = ' save ' + str(save) + str(file_prefix) + str(i + int(count_start)) + str(img_type)
   command = command + savex
   
   if type(file) is list:
      filei = file[i]
   else:
      filei = file
   if i != '_empty_':
      filex = ' file ' + str(filei)
      command = command + filex
   
   
   if type(data) is list:
      datai = data[i]
   else:
      datai = data
   if datai != '_empty_':
      datax = ' data ' + str(datai)
      command = command + datax

   if type(lat) is list:
      lati = lat[i]
   else:
      lati = lat
   if lati != '_empty_':
      latx = ' lat ' + str(lati)
      command = command + latx
   
   if type(lon) is list:
      loni = lon[i]
   else:
      loni = lon
   if loni != '_empty_':
      lonx = ' lon ' + str(loni)
      command = command + lonx
   
   if type(depth) is list:
      depthi = depth[i]
   else:
      depthi = depth
   if depthi != '_empty_':
      depthx = ' depth ' + str(depthi)
      command = command + depthx
   
   if type(mask) is list:
      maski = mask[i]
   else:
      maski = mask
   if maski != '_empty_':
      maskx = ' mask ' + str(maski)
      command = command + maskx
   
   if type(maxr) is list:
      maxri = maxr[i]
   else:
      maxri = maxr
   if maxri != '_empty_':
      maxrx = ' max ' + str(maxri)
      command = command + maxrx
   
   if type(minr) is list:
      minri = minr[i]
   else:
      minri = minr
   if minri != '_empty_':
      minrx = ' min ' + str(minri)
      command = command + minrx
   
   if type(norm) is list:
      normi = norm[i]
   else:
      normi = norm
   if normi != '_empty_':
      normx = ' norm ' + str(normi)
      command = command + normx
      
   if type(crop) is list:
      cropi = crop[i]
   else:
      cropi = crop
   if cropi != '_empty_':
      cropx = ' crop ' + str(cropi)
      command = command + cropx
   
   if type(colors) is list:
      colorsi = colors[i]
   else:
      colorsi = colors
   if colorsi != '_empty_':
      colorsx = ' colors ' + str(colorsi)
      command = command + colorsx
   
   if type(clr_min_max) is list:
      clr_min_maxi = clr_min_max[i]
   else:
      clr_min_maxi = clr_min_max
   if clr_min_maxi != '_empty_':
      clr_min_maxx = ' clr_min_max ' + str(clr_min_maxi)
      command = command + clr_min_maxx
   
   time0 = time.time()
   os.system('python map.py ' + command)
   if display == 'no':
      print str(i) + ' - ' + str(time.time() - time0) + ' sec'