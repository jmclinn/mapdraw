# mapdraw
Python tool accessed via command line for mapping scientific oceanographic data

### Necessary Python packages required to use mapdraw


###### Pillow

https://pypi.python.org/pypi/netCDF4

https://pillow.readthedocs.org/

###### netCDF4 (w/ HDF5 headers)

https://pypi.python.org/pypi/netCDF4

https://github.com/Unidata/netcdf4-python

http://unidata.github.io/netcdf4-python/

### Usage

This code has only been tested and run on Mac OSX and Linux systems with Python 2.76 - 2.79. It has been used to read data off of *.dat and *.nc files with data saved in the netCDF-4 format and containing the following necessary data:

**latitude** : list of latitude range (must match **data**)

**longitude** : list of longitude range (must match **data**)

**depth** : list of depth values corresponding to datasets within the **data** variable

**data** : list of datasets at varying depths in the following format:

````
  [
    [ 
      [ x , x , x , ... ],
      [ x , x , x , ... ],
      [ x , x , x , ... ],
      ...
    ],
    [ 
      [ x , x , x , ... ],
      [ x , x , x , ... ],
      [ x , x , x , ... ],
      ...
    ],
    ...
  ]
````

To use mapdraw, first move into the mapdraw parent folder on the command line or terminal window.

Run **$ python map.py \{list of key/value pair arguments here\}**

The order the following arguments are written does not matter, just that the appropriate value follows its key.

----------------------------------
###### Arguments (key/value pairs)
----------------------------------
(values where DEFAULT is FAILURE are necessary arguments)

| KEY         | VALUE                             | DEFAULT                           | EXAMPLE                        |
| ----------- | --------------------------------- | --------------------------------- | -----------------------------  |
| file        | path/to/file                      | FAILURE                           | "/example/path/to/file.dat"    |
| data        | data variable in file             | FAILURE                           | data                           |
| lat         | latitude variable in file         | FAILURE                           | lat                            |
| lon         | longitude variable in file        | FAILURE                           | lon                            |
| depth       | depth variable in file & index    | FAILURE                           | dep,0                          |
| mask        | land mask number & color          | (no mask is applied)              | -2146435700000000,#000000      |
| max         | maximum range value               | 100                               | 10000 (or) 1E4 (or) 1e4        |
| min         | minimum range value               | -100                              | -10000 (or) -1E4 (or) -1e4     |
| norm        | normalization multiplier          | 1                                 | 1000 (or) 1E3 (or) 1e3         |
| save        | path/to/save/file                 | (no file saved)                   | "/example/path/to/file.png"    |
| display     | print result to screen            | yes                               | no                             |
| colors      | color range (\%:color)            | "0:#0000FF,50:#FFFFFF,100:#FF0000"| "0:#000000,100:#FFFFFF"        |
| clr_min_max | colors for range exceeding values | "#FFFFFF,#FFFFFF"                 | "#0000FF,#FF0000"              |
| title       | title of resulting map            | (no title)                        | "Data Plot Title"              |
| crop        | lat/lon degree limits to crop map | (no crop - maps entire dataset)   | 60,0,0,-30                     |
| lines       | controls for lon/lat markings     | (no lat/lon markings or lines)    | "(-45,-10,0),(30,20,10),False" |

----------------------------------
###### SPHERE Arguments
----------------------------------
Mapping data onto a sphere requires a new set of arguments and nullifies certain of the above arguments. Including 'sphere' utilizes a different mapping process that takes approximately twice as long due to the mathematical processing required.

| KEY         | VALUE                              | DEFAULT                           | EXAMPLE                        |
| ----------- | ---------------------------------  | --------------------------------- | -----------------------------  |
| sphere      | lon and lat value to center sphere | (will not map as sphere)          | "/example/path/to/file.dat"    |
| zoom        | data variable in file              | 1 (no zoom)                       | 1.5                            |

------------
###### Notes
------------

**mask**

This is a minimum value mask that is used for land values. If land values are set to an extremely low number you can use this command to display them as 'land'. All values BELOW the given numerical value will be considered land and masked to the given color.

**colors**

The ordering convention used is min to max when specifying colors. If the color list lacks percentages it will evenly distribute the listed colors throughout the color range set by **max** and **min**. It is still recommended to include the percentages even with an evenly distributed color range.

The color/percentage combinations listed will also be printed alongside the colorbar for easy reference specifically where it is needed.

Hex values are used to specify colors. For reference to color/hex combinations you can go to https://www.colorcodehex.com/html-color-picker.html.

**clr_min_max**

The order follows the same ordering convention as **colors**. Min to max.

**crop**

The 4 values given define the sides of the 'box' created by the crop. The order of the values is top latitude, right longitude, bottom latitude, left latitude.

**lines**

This argument is a list of three values. 1 - This is a tuple of longitude values to be marked along the bottom of the image. 2 - This is a tuple of the latitude values to be marked along the left side of the image. 3 - This is either 'True' or 'False' depending on whether lines should be drawn across the image at the desired lat/lon values. If 'False' markings will just be ticks along the edges instead of lines across the image.

**sphere (initiates spherical mapping)**

The spherical representation is centered around a given pair of longitude and longitude values. In this current version the outlines of coastlines are included. The ability to toggle these (and alter their color) will be available in future updates.

**zoom (only used in conjunction with 'sphere')**

This method is currently being enhanced. In this most basic form the sphere can be zoomed in to varying degrees. A value of '2' would return an image where the 'radius' of the sphere/Earth is doubled. The area outside the initial viewing area will be cropped. Later versions will allow for lateral movement of the sphere along with zooming to map very specific subregions of Earth at the desired angle.

NOTE - This feature could cause image pixelation depending on the data density, image size, and amount of zoom requested. Reducing this potential side effect is a current primary goal.

### movie.py

The primary files used in mapdraw are 'map.py' and 'mapdraw/mapdraw.py'. However, to allow for processing variable arguments, and/or from multiple datasets, there is 'movie.py'. (It can also be used to simply cirvumvent the command line by hard coding your variables inside the file for repeated uses.) It has the ability to output a single image, but was designed for multiple successive images.

This file requires a text editor to edit user inputs within it. The first part of the file is only for user inputs. The second part is for parsing the variable data and running the code. No user inputs are required in the second half.

Express instructions for 'movie.py' are included in the file.

To use mapdraw from movie.py, first move into the mapdraw parent folder on the command line or terminal window.

Run **$ python movie.py**


### Attribution and Acknowledgement

The rgb2hex code used to create linear color gradients was taken from code written by Ben Southgate, available at https://github.com/bsouthga/blog/blob/master/app/posts/color-gradients-with-python.md.

I have not received any express permission to use Ben's code, which I found originally on his site http://bsou.io as a public blog post. I was unable to find any license information about this code prior to implementing it into mapdraw.
