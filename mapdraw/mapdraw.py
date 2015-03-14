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
      args['mask'][0] = int(args['mask'][0]) 
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

# === cylindrical equal area ===
def transform(args):
   lat = args['lat']
   lat0 = lat[0]
   lat1 = lat[len(lat) - 1]
   latnum = []
   scale = 100
   for i,y in enumerate(reversed(lat)):
      latnum.append( int(round(math.sin(y*math.pi/180+math.pi/2)*scale)) )
   
   data = args['data']
   ylen = args['ylen']
   data2 = []
   for i,row in enumerate(reversed(data)):
      for k in range(latnum[i]):
         data2.append(row)

   total = len(data2)
   data3 = data2[0::int(round(total/ylen))]
   ylen = len(data3)
   
   args['data'] = data3
   args['ylen'] = ylen
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
            if val < args['mask'][0]:
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
   
   # ------------------------------------------
   
#   if 'def' not in args:
#      incr = int(20000/rangelen)
#      if incr <= 1:
#         args['incrm'] = int(1 / (20000./rangelen))
#         incr = 1
##         print args['incrm']
#   else:
#      incr = int(args['def'])
#   
##   print incr
#   
#   if 'incrm' in args:
#      incrm = args['incrm']
#      cr2 = rgb2hex.linear_gradient(args['colors'][1],args['colors'][2],10001)['hex']
#      cr1 = rgb2hex.linear_gradient(args['colors'][0],args['colors'][1],10001)['hex']
#      incr = 1./incrm
#      
#   #   crlen = len(cr2)
#   #   cr4 = []
#   #   cr3 = []
#   #   for c in cr2:
#   #      cr5 = [c]
#   #      cr6 = cr5 * incrm
#   #      cr4.extend(cr6)
#   #   cr2 = cr4
#   #   cr2.extend(cr5)
#   #   for c in cr1:
#   #      cr5 = [c]
#   #      cr6 = cr5 * incrm
#   #      cr3.extend(cr6)
#   #   cr1 = cr3
#   #   cr1.extend(cr5)
#   
#   else:
#      cr2 = rgb2hex.linear_gradient(args['colors'][1],args['colors'][2],(int(rangelen/2*incr))+1)['hex']
#      cr1 = rgb2hex.linear_gradient(args['colors'][0],args['colors'][1],(int(rangelen/2*incr))+1)['hex']
#   
#   dictlist = {}
#   
#   toph = (rangemin + rangelen/2)
#
#   # === PAIR DATA WITH COLOR MAP ===
#   for y,sl in enumerate(args['data']): # for each sublist within dataset (row)
#      for x,i in enumerate(sl): # for each point in sublist (column)
#         val = args['colors'][1]
#         #top half of data range
#         if i > rangemid:
#            if i <= rangemax:
#               val = cr2[int((i - toph) * incr)]
#            else:
#               val = args['colors'][1]
##               val = args['colors'][2]
#         #bottom half of data range
#         elif i < rangemid:
#            if i >= rangemin:
#               val = cr1[int((i - rangemin) * incr)]
#            else:
#               val = args['colors'][1]
##               val = args['colors'][0] 
#         # mask
#         if 'mask' in args:
#            if i <= args['mask'][0]:
#               val = args['mask'][1]
#         # add to dict
#         if val in dictlist:
#            dictlist[val].append((x,y))
#         else:
#            dictlist[val] = [(x,y)]
#            
#   args['datamap'] = dictlist
#
   # ===== COLORBAR CREATION =====
#   clr = (cr1 + cr2)
##   clr = clr[::-1000]

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

   for key,value in args['datamap'].iteritems():
      draw.point(value,getrgb(str(key)))

   img2 = img.resize((args['y'],int(0.95*args['y'])), Image.BILINEAR)

   imgclr = colorbar.resize((args['colorbar'],img2.size[1]), Image.BILINEAR)

   # ===== ENTIRE IMAGE CREATION W/ TEXT=====
   imgbox = Image.new('RGB',((300+args['y']+args['colorbar']),(img2.size[1]+200)),args['background'])
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
