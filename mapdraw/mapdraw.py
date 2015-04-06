# ===== PACKAGES =====
import math
from netCDF4 import Dataset
from PIL import Image,PSDraw
from PIL.ImageColor import getrgb
from PIL.ImageDraw import Draw
from PIL.ImageFont import truetype
# === custom package ===
from rgb2hex import rgb2hex

# ===== ARGUMENT PARSING AND SETTING DEFAULTS =====
def setargs(args):
   if 'title' not in args:
      args['title'] = ''
   if 'colors' not in args:
      args['colors'] = ['#0000FF','#FFFFFF','#FF0000']
      args['colorp'] = [0,50,100]
   elif ':' not in args['colors']:
      args['colors'] = args['colors'].split(',')
      csp = int(round(100. / (len(args['colors']) - 1)))
      csp1 = 0
      args['colorp'] = []
      for c in range(len(args['colors'])):
         csp1 = csp * c
         args['colorp'].append(csp1)
   elif ':' in args['colors']:
      split1 = args['colors'].split(',')
      args['colors'] = []
      args['colorp'] = []
      for c in split1:
         split2 = c.split(':')
         args['colors'].append(split2[1])
         args['colorp'].append(int(split2[0]))
   if 'clr_min_max' not in args:
      args['clr_min_max'] = ['#FFFFFF','#FFFFFF']
   else:
      args['clr_min_max'] = args['clr_min_max'].split(',')
   if 'max' not in args:
      args['max'] = 100
   elif 'E' in args['max']:
      tmax = args['max'].split('E')
      args['max'] = (int(tmax[0]) * 10 ** int(tmax[1]))
   elif 'e' in args['max']:
      tmax = args['max'].split('e')
      args['max'] = (int(tmax[0]) * 10 ** int(tmax[1]))
   else:
      if '.' in args['max']:
         args['max'] = float(args['max'])
      else:
         args['max'] = int(args['max'])
   if 'min' not in args:
      args['min'] = -100
   elif 'E' in args['min']:
      tmin = args['min'].split('E')
      args['min'] = (int(tmin[0]) * 10 ** int(tmin[1]))
   elif 'e' in args['min']:
      tmin = args['min'].split('e')
      args['min'] = (int(tmin[0]) * 10 ** int(tmin[1]))
   else:
      if '.' in args['min']:
         args['min'] = float(args['min'])
      else:
         args['min'] = int(args['min'])
   if 'colorbar' not in args:
      args['colorbar'] = 50
   else: 
      args['colorbar'] = int(args['colorbar'])
   if 'y' not in args:
      args['y'] = 1000
   else:
      args['y'] = int(args['y'])
   if 'mask' in args:
      args['mask'] = args['mask'].split(',')
      args['mask'][0] = int(float(args['mask'][0]))
   if 'background' not in args:
      args['background'] = 'white'
   if 'display' not in args:
      args['display'] = 'yes'
   
   return args

# ===== DATA IMPORT =====
def dataload(args):
   lat0 = args['lat']
   lon0 = args['lon']
   data = args['data']
   depth = args['depth'].split(',')
   depth0 = depth[0]
   depth = int(depth[1])
#   data2 = args['data'].split(',')
#   data0 = data2[0]
#   depth = int(data2[1])
   f = Dataset(args['file'],'r')
   lon = f.variables[lon0]
   lat = f.variables[lat0]
   data = f.variables[data][depth,:,:]
   # check for masked array and remove masked values
   if hasattr(data,'fill_value'):
      data = data.filled(data.fill_value)
   
   # crop to subregion
   if 'crop' in args:
      latmin = lat[0]
      latmax = lat[len(lat)-1]
      lonmin = lon[0]
      lonmax = lon[len(lon)-1]
      # parse crop arg
      crop = args['crop'].split(',')
      args['crop'] = crop
      for i,c in enumerate(crop):
         crop[i] = float(c)
      # find position of crop range in lat and lon
      for i,y in enumerate(lat):
         if y >= crop[2] and lat[i-1] <= crop[2]:
            latmin = i
         if y >= crop[0] and lat[i-1] <= crop[0]:
            latmax = i
      for i,y in enumerate(lon):
         if y >= crop[3] and lon[i-1] <= crop[3]:
            lonmin = i
         if y >= crop[1] and lon[i-1] <= crop[1]:
            lonmax = i
      # crop lat and lon
      lat = lat[latmin:latmax]
      lon = lon[lonmin:lonmax]
      # crop data
      cdata = []
      for i in data:
         cdata.append(i[lonmin:lonmax])
      #data = map(list, zip(*cdata))
      data = [[row[idx] for row in cdata] for idx in xrange(len(cdata[0]))]
      cdata = []
      for i in data:
         cdata.append(i[latmin:latmax])
      data = [[row[idx] for row in cdata] for idx in xrange(len(cdata[0]))]
      
   
   # multipily by normalization factor
   if 'norm' in args:
      if 'E' in args['norm']:
         tmax = args['norm'].split('E')
         args['norm'] = (float(tmax[0]) * 10 ** float(tmax[1]))
      elif 'e' in args['norm']:
         tmax = args['norm'].split('e')
         args['norm'] = (float(tmax[0]) * 10 ** float(tmax[1]))
      else:
         if '.' in args['norm']:
            args['norm'] = float(args['norm'])
         else:
            args['norm'] = int(args['norm'])
      
      data = [i * args['norm'] for i in data]
   
   xlen = len(lon)
   ylen = len(lat)
   
   args['data'] = data
   args['lon'] = lon
   args['lat'] = lat
   args['xlen'] = xlen
   args['ylen'] = ylen
   return args

# ===== TRANSFORMATION =====

# === even lat/lon disparities ===
def transform(args):
   data = args['data']
   lat = args['lat']
   lat2 = []
   latmin = lat[0]
   latmax = lat[len(lat)-1]
   latrange = abs(latmax-latmin)
   
   #imagesize - human input
   args['size'] = 1000
   
   spc = latrange / args['size']
   for i in range(args['size']):
      lat2.append(latmin + ( i * spc ))
   
   lat3 = []
   val = 0
   for x in lat2[0:]:
      xf = round(float(x),4)
      for k,y in enumerate(lat[0:]):
         yf = round(float(y),4)
         if xf >= yf:
            val = k
      lat3.append(val)
   
   data2 = []
   for y in reversed(lat3):
      data2.append(data[y])
   
   data3 = [[row[idx] for row in data2] for idx in xrange(len(data2[0]))]
   
   lon = args['lon']
   lon2 = []
   lonmin = lon[0]
   lonmax = lon[len(lon)-1]
   lonrange = abs(lonmax - lonmin)
   xsize = lonrange / latrange * args['size']
   xspc = lonrange / xsize
   for i in range(int(xsize)):
      lon2.append(lonmin + ( i * xspc ))
   lon3 = []
   val = 0
   for x in lon2[0:]:
      xf = round(float(x),4)
      for k,y in enumerate(lon[0:]):
         yf = round(float(y),4)
         if xf >= yf:
            val = k
      lon3.append(val)
      
   data4 = []
   for y in lon3:
      data4.append(data3[y])
   
   data5 = [[row[idx] for row in data4] for idx in xrange(len(data4[0]))]
   
   args['data'] = data5
   args['lat'] = lat2
   args['lon'] = lon2
   args['ylen'] = len(lat2)
   args['xlen'] = len(lon2)
   return args

## === cylindrical equal area ===
#def transform1(args):
#   lat = args['lat']
#   lat0 = lat[0]
#   lat1 = lat[len(lat) - 1]
#   latnum = []
#   scale = 100
#   for i,y in enumerate(reversed(lat)):
#      #latnum.append( int(round(math.sin(y*math.pi/180+math.pi/2)/math.cos(math.pi/2)*scale)) )
#      latnum.append( int(round(math.sin(y*math.pi/180+math.pi/2)*scale)) )
#   
#   data = args['data']
#   ylen = args['ylen']
#   data2 = []
#   for i,row in enumerate(reversed(data)):
#      for k in range(latnum[i]):
#         data2.append(row)
#
#   total = len(data2)
#   data3 = data2[0::int(round(total/ylen))]
#   ylen = len(data3)
#   
#   args['data'] = data3
#   args['ylen'] = ylen
#   return args

# ===== COLOR MAP =====
def colormap(args): # make colormap
   cr_dict = {}
   for i,c in enumerate(args['colors']):
      if i >= 1:
         cr_dict[i] = rgb2hex.linear_gradient(args['colors'][(i-1)],c,int(20000 * (0.01 * (args['colorp'][i] - args['colorp'][(i-1)]))))['hex']
   crange = []
   for i in range(len(cr_dict)):
      crange.extend(cr_dict[(i+1)])
   if len(crange) <= 20000:
      lastc = []
      lastc.append(crange[(len(crange)-1)])
      diffc = 20001 - len(crange)
      lastc = diffc * lastc
      crange.extend(lastc)
      
   rangelen = args['max'] - args['min']
   rangemid = args['min'] + (rangelen / 2)
   rangemax = args['max']
   rangemin = args['min']
   
   incr = 20000./rangelen
   dictlist = {}
      
   for y,sl in enumerate(args['data']): # for each sublist within dataset (row)
      for x,val in enumerate(sl): # for each point in sublist (column)
      # assign colors
         if val < rangemin:
            if val <= args['mask'][0]:
               clr = args['mask'][1]
            else:
               clr = args['clr_min_max'][0]
         elif val > rangemax:
            clr = args['clr_min_max'][1]
         else:
            clrv = int((val - rangemin) * incr)
            clr = crange[clrv]
      # place pair color with coords      
         if clr in dictlist:
            dictlist[clr].append((x,y))
         else:
            dictlist[clr] = [(x,y)]
   
   args['datamap'] = dictlist
   

   widthclr = args['colorbar']
   heightclr = len(crange)

   imgclr = Image.new("RGB",(widthclr,heightclr),"white")
   drawclr = Draw(imgclr)
   
   for y,val in enumerate(reversed(crange)):
      for x in range(widthclr):
         #drawclr.point((x,y),getrgb(str(val)))
         drawclr.point((x,y),val)
   
   return args, imgclr

# ===== MAP IMAGE CREATION =====
def mapdraw(args,colorbar):
   
   img = Image.new('RGB',(args['xlen'],args['ylen']),'white')
   draw = Draw(img)
   
   # Draw Map
   for key,value in args['datamap'].iteritems():
      draw.point(value,getrgb(str(key)))
   
   if 'lines' in args:
      # Latitude Lines
      lat = [round(i,1) % int(args['lines']) for i in reversed(args['lat'])]
      io = 0
      for i,y in enumerate(lat):
         if y == 0.0:
            if io == 0:
               draw.line([(0,i),(args['xlen'],i)],getrgb('#aaaaaa'))
               io = 1
         else:
            io = 0
      # Longitude Lines
      lon = [round(i,1) % int(args['lines']) for i in args['lon']]
      io = 0
      for i,y in enumerate(lon):
         if y == 0.0:
            if io == 0:
               draw.line([(i,0),(i,args['ylen'])],getrgb('#aaaaaa'))
               io = 1
         else:
            io = 0
      

   #img2 = img.resize((args['y'],int(0.95*args['y'])), Image.BILINEAR)
   img2 = img
   #img2 = img.resize((int(args['xlen']*args['xlen']/args['ylen']),args['ylen']), Image.BILINEAR)
   
   imgclr = colorbar.resize((args['colorbar'],img2.size[1]), Image.BILINEAR)

   # ===== ENTIRE IMAGE CREATION W/ TEXT=====
   imgbox = Image.new('RGB',((300+img2.size[0]+args['colorbar']),(img2.size[1]+200)),args['background'])
   imgbox.paste(img2,(100,100))
   imgbox.paste(imgclr,((150+img2.size[0]),100))

   drawbox = Draw(imgbox)
   title = args['title']
   titlesize = 50 # future user input
#   font = truetype("/library/fonts/Arial.ttf",titlesize)
   font = truetype("mapdraw/fonts/Arial.ttf",titlesize)
   smfontsize = 30 # future user input
#   smfont = truetype("/library/fonts/Arial.ttf",smfontsize)
   smfont = truetype("mapdraw/fonts/Arial.ttf",smfontsize)
   titlewidth = font.getsize(title)[0]
   drawbox.text(((imgbox.size[0]/2 - titlewidth/2), titlesize/2),title,(0,0,0),font=font)

   drawbox.text(((imgbox.size[0] - 145),100),str(args['max']),(0,0,0),font=smfont)
   drawbox.text(((imgbox.size[0] - 145),(100 + img2.size[1] - smfontsize)),str(args['min']),(0,0,0),font=smfont)

   if args['display'] == 'yes':
      imgbox.show()
   
#   if 'title' in args:
#      title = args['title']+'.png'
#      title = args['title']+'_'+str(args['min'])+'_'+str(args['max'])+'.png'
#   else:
#      title = 'output_'+str(args['min'])+'_'+str(args['max'])+'.png'
   if 'save' in args:
#      imgbox.save(args['save']+'/'+title)
      imgbox.save(args['save'])
#   else:
#      imgbox.save(title)
