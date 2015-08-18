# -*- coding: utf-8 -*-

# ===== PACKAGES =====
import math
import pickle
from netCDF4 import Dataset
from PIL import Image,PSDraw
from PIL.ImageColor import getrgb
from PIL.ImageDraw import Draw
from PIL.ImageFont import truetype
# === custom packages ===
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
         args['colorp'].append(float(split2[0]))
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
   if 'height' in args:
      args['height'] = int(args['height'])
   if 'mask' in args:
      args['mask'] = args['mask'].split(',')
      args['mask'][0] = int(float(args['mask'][0]))
   if 'sphere' in args:
      args['sphere'] = args['sphere'].split(',')
      args['sphere'][0] = float(args['sphere'][0])
      args['sphere'][1] = float(args['sphere'][1])
   if 'background' not in args:
      args['background'] = 'white'
   else:
      if len(args['background'].split('#')) == 2:
         args['background'] = getrgb(args['background'])
   if 'display' not in args:
      args['display'] = 'yes'
   if 'lines' in args:
      args['lines'] = eval(args['lines'])
      args['lonm'] = args['lines'][0]
      args['latm'] = args['lines'][1]
      args['lines'] = args['lines'][2]
   
   return args

# ===== DATA IMPORT =====
def dataload(args):
   lat0 = args['lat']
   lon0 = args['lon']
   data = args['data']
   depth = args['depth'].split(',')
   depth0 = depth[0]
   depth = int(depth[1])
   f = Dataset(args['file'],'r')
   lon00 = f.variables[lon0]
   lat00 = f.variables[lat0]
   data00 = f.variables[data][depth,:,:]
   # check for masked array and remove masked values
   if hasattr(data00,'fill_value'):
      data00 = data00.filled(data00.fill_value)
   
   # convert from numpy format for quicker operation
   data = []
   lat = []
   lon = []
   for i in data00:
      data.append(i)
   for i in lat00:
      lat.append(i)
   for i in lon00:
      lon.append(i)
   
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
# (for flat plane mapping)

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
   
   args['crange'] = crange
   
   #colorbar creation
   widthclr = args['colorbar']
   heightclr = len(crange)

   imgclr = Image.new("RGB",(widthclr,heightclr),"white")
   drawclr = Draw(imgclr)
   
   for y,val in enumerate(reversed(crange)):
      for x in range(widthclr):
         drawclr.point((x,y),val)
   
   return args, imgclr

def colorset(args): # map colors to pixel location based on data
   crange = args['crange']
   rangelen = args['max'] - args['min']
   rangemid = args['min'] + (rangelen / 2)
   rangemax = args['max']
   rangemin = args['min']
   
   incr = 20000./rangelen
   
   if 'sphere' not in args:
      dictlist = {}
      
      # Flat plane color map creation
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
   
   # Spherical color map creation   
   else:
      lon0r = math.radians(args['sphere'][0])
      lat0r = math.radians(args['sphere'][1])
      colormapped = []
      latlonmapped = []
      for i,y in enumerate(args['data']):
         colormapped0 = []
         latlonmapped0 = []
         for k,x in enumerate(y):
      
            # LatLon Mapping ---
            lonr = math.radians(args['lon'][k])
            latr = math.radians(args['lat'][i])
            cosc = math.sin(lat0r) * math.sin(latr) + math.cos(lat0r) * math.cos(latr) * math.cos(lonr - lon0r)
            if cosc >= 0:
               xx = math.cos(latr) * math.sin(lonr - lon0r)
               yy = math.cos(lat0r) * math.sin(latr) - math.sin(lat0r) * math.cos(latr) * math.cos(lonr - lon0r)
               latlonmapped0.append((xx,-yy))
      
               # Color Mapping ---
               if x < rangemin:
                  if x <= args['mask'][0]:
                     clr = args['mask'][1]
                  else:
                     clr = args['clr_min_max'][0]
               elif x > rangemax:
                  clr = args['clr_min_max'][1]
               else:
                  clrv = int((x - rangemin) * incr)
                  clr = crange[clrv]
               colormapped0.append(clr)
      
         latlonmapped.append(latlonmapped0)
         colormapped.append(colormapped0)
         
         args['latlonmapped'] = latlonmapped
         args['colormapped'] = colormapped
   
   return args

# ===== MAP IMAGE CREATION =====
def mapdraw(args,colorbar):
   
   # Map creation on flat plane
   if 'sphere' not in args:
      
      img = Image.new('RGBA',(args['xlen'],args['ylen']),'white')
      draw = Draw(img)
   
      # Draw Map
      for key,value in args['datamap'].iteritems():
         draw.point(value,getrgb(str(key)))
   
      if 'lines' in args:
         # Longitude
         lonm = []
         lonmp = []
         for i in args['lonm']:
            io = 0
            for x,k in enumerate(args['lon']):
               if io == 0:
                  if round(k,1) == round(i,1):
                     lonm.append(int((float(x)+1) / len(args['lon']) * args['xlen']))
                     lonmp.append(i)
                     io = 1
         #Latitude            
         latm = []
         latmp = []
         for i in args['latm']:
            io = 0
            for x,k in enumerate(reversed(args['lat'])):
               if io == 0:
                  if round(k,1) == round(i,1):
                     latm.append(int((float(x)+1) / len(args['lat']) * args['ylen']))
                     latmp.append(i)
                     io = 1
         
         # --original version-- #
         ## Latitude Lines
         #lat = [round(i,1) % int(args['lines']) for i in reversed(args['lat'])]
         #io = 0
         #for i,y in enumerate(lat):
         #   if y == 0.0:
         #      if io == 0:
         #         draw.line([(0,i),(args['xlen'],i)],getrgb('#aaaaaa'))
         #         io = 1
         #   else:
         #      io = 0
         ## Longitude Lines
         #lon = [round(i,1) % int(args['lines']) for i in args['lon']]
         #io = 0
         #for i,y in enumerate(lon):
         #   if y == 0.0:
         #      if io == 0:
         #         draw.line([(i,0),(i,args['ylen'])],getrgb('#aaaaaa'))
         #         io = 1
         #   else:
         #      io = 0
   
   # Map creation on sphere   
   else:
      filename = 'mapdraw/world/coastmask'
      fileobject = open(filename,'r') 
      land = pickle.load(fileobject)
      
      lon0r = math.radians(args['sphere'][0])
      lat0r = math.radians(args['sphere'][1])
      imgxsize = args['y']
      imgysize = args['y']
      # without zoom (full sphere)
      offsetx = 0
      offsety = 0
      radius = imgysize / 2
      ## with zoom
      #if 'zoom' in args:
      #   offsetx = 0
      #   offsety = 0
      #   radius = 1000 / 2
      
      img = Image.new('RGBA',(imgxsize+1,imgysize+1),'white')
      draw = Draw(img)

      for i,colorlist in enumerate(args['colormapped']):
         for k,color in enumerate(colorlist):
            x,y = args['latlonmapped'][i][k]
            draw.point((round(x*radius+imgxsize/2+offsetx),round(y*radius+imgysize/2+offsety)),getrgb(color))
      
      for value in land:
         if type(value) is tuple:
            x,y = value
            latr = math.radians(y*2-90)
            lonr = math.radians(x*2+180)
   
            cosc = math.sin(-lat0r) * math.sin(latr) + math.cos(-lat0r) * math.cos(latr) * math.cos(lonr - lon0r)
            if cosc >= 0:
               x = math.cos(latr) * math.sin(lonr - lon0r)
               y = math.cos(-lat0r) * math.sin(latr) - math.sin(-lat0r) * math.cos(latr) * math.cos(lonr - lon0r)
               draw.point((x*radius+imgxsize/2+offsetx,y*radius+imgysize/2+offsety),getrgb('#00aa00'))#aaffaa
         
      if 'zoom' not in args:
         draw.ellipse((0,0,1000,1000),outline=getrgb('#00aa00'),fill=None)
      else:
         img = img.crop((100,100,900,700))
         #resize of crop
         if 'height' in args:
            resizeratio = float(args['height']) / img.size[1]
            img = img.resize((int(img.size[0]*resizeratio),args['height']))#,Image.ANTIALIAS)

   img2 = img
   
   imgclr = colorbar.resize((args['colorbar'],img2.size[1]))#, Image.BILINEAR)

   # ===== ENTIRE IMAGE CREATION W/ TEXT=====
   imgbox = Image.new('RGBA',((300+img2.size[0]+args['colorbar']),(img2.size[1]+200)),args['background'])
   imgbox.paste(img2,(100,100))
   imgbox.paste(imgclr,((150+img2.size[0]),100))

   drawbox = Draw(imgbox)
   title = args['title']
   titlesize = 50 # future user input?
   font = truetype("mapdraw/fonts/Arial.ttf",titlesize)
   smfontsize = int( img2.size[1] * .03 ) #30 @ 1000px
   #smfontsize = 30
   smfont = truetype("mapdraw/fonts/Arial.ttf",smfontsize)
   titlewidth = font.getsize(title)[0]
   drawbox.text(((imgbox.size[0]/2 - titlewidth/2), titlesize/2),title,(0,0,0),font=font)
   
   # -- original colorbar value marking (min/max) -- #
   #drawbox.text(((imgbox.size[0] - 135),85),str(args['max']),(0,0,0),font=smfont)
   #drawbox.text(((imgbox.size[0] - 135),(80 + img2.size[1])),str(args['min']),(0,0,0),font=smfont)
   
   # Colorbar value text printing
   
   #textbox = Image.new("RGB",(1000,200),"white")
   #drawtext = Draw(textbox)
   #txthtr = int(img2.size[1] / 1000.)
   
   for per in args['colorp']:
      colper = img2.size[1] * (1 - per / 100)
      colval = (args['max'] - args['min']) * per / 100. + args['min']
      if colval >= 0:
         colx = 144 - int(0.3 * smfontsize) #135 @ 30px
      else:
         colx = 144
      drawbox.text(((imgbox.size[0] - colx),((100 - smfontsize/2) + colper)),str(round(colval,1)),(0,0,0),font=smfont)
   
   # Lon/Lat Tick/Value printing
   if 'lines' in args and 'sphere' not in args:
      lonlatcol = '#444444' # future user input?
      degsym = u'\xb0'
      for p,i in enumerate(lonm):
         lontxtimg = Image.new("RGB",(75,50),"white")
         drawlonimg = Draw(lontxtimg)
         drawlonimg.text((0,0),str(lonmp[p])+degsym,(0,0,0),font=smfont)
         lontxtimg = lontxtimg.rotate(-90)
         imgbox.paste(lontxtimg,((65+i),(125+args['ylen'])))
         if args['lines']:
            drawbox.line([((100+i),(100)),((100+i),(115+args['ylen']))],fill=getrgb(lonlatcol),width=1)
         else:
            drawbox.line([((100+i),(100+args['ylen'])),((100+i),(115+args['ylen']))],fill='black',width=3)
      for p,i in enumerate(latm):
         drawbox.text((20,85+i),str(latmp[p])+degsym,(0,0,0),font=smfont)
         if args['lines']:
            drawbox.line([((85),(100+i)),((100+args['xlen']),(100+i))],fill=getrgb(lonlatcol),width=1)
         else:
            drawbox.line([((85),(100+i)),((100),(100+i))],fill='black',width=3)
   
   # Display image
   if args['display'] == 'yes':
      imgbox.show()
   #if args['display']:
   #   imgbox.show()
   
#   if 'title' in args:
#      title = args['title']+'.png'
#      title = args['title']+'_'+str(args['min'])+'_'+str(args['max'])+'.png'
#   else:
#      title = 'output_'+str(args['min'])+'_'+str(args['max'])+'.png'
   if 'save' in args:
      imgbox.save(args['save'])
