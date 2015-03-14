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

### Attribution and Acknowledgement

The rgb2hex code used to create linear color gradients was taken from code written by Ben Southgate, available at https://github.com/bsouthga/blog/blob/master/app/posts/color-gradients-with-python.md.

I have not received any express permission to use Ben's code, which I found originally on his site http://bsou.io as a public blog post. I was unable to find any license information about this code prior to implementing it into mapdraw.

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

| KEY         | VALUE                             | DEFAULT                           | EXAMPLE                       |
| ----------- |:--------------------------------- |:--------------------------------- |:----------------------------- |
| file        | path/to/file                      | FAILURE                           | "/example/path/to/file.dat"   |
| data        | data variable in file             | FAILURE                           | data                          |
| lat         | latitude variable in file         | FAILURE                           | lat                           |
| lon         | longitude variable in file        | FAILURE                           | lon                           |
| depth       | depth variable in file & index    | FAILURE                           | dep,0                         |
| mask        | land mask number & color          | (no mask is applied)              | -2146435700000000,#000000     |
| max         | maximum range value               | 100                               | 10000 (or) 1E4 (or) 1e4       |
| min         | minimum range value               | -100                              | -10000 (or) -1E4 (or) -1e4    |
| norm        | normalization multiplier          | 1                                 | 1000 (or) 1E3 (or) 1e3        |
| save        | path/to/save/file                 | (no file saved)                   | "/example/path/to/file.png"   |
| display     | print result to screen            | yes                               | no                            |
| colors      | color range (\%:color)            | "0:#0000FF,50:#FFFFFF,100:#FF0000"| "0:#000000,100:#FFFFFF"       |
| clr_min_max | colors for range exceeding values | "#FFFFFF,#FFFFFF"                 | "#0000FF,#FF0000"             |
| title       | title of resulting map            | (no title)                        | "Data Plot Title"             |

------------
###### Notes
------------

**mask**

This is a minimum value mask that is used for land values. If land values are set to an extremely low number you can use this command to display them as 'land'. All values BELOW the given numerical value will be considered land and masked to the given color.

**colors**

The ordering convention used is min to max when specifying colors. If the color list lacks percentages it will evenyl distribute the listed colors throughout the color range set by **max** and **min**. It is still recommended to include the percentages even with an evenly distributed color range.

Hex values are used to specify colors. For reference to color/hex combinations you can go to https://www.colorcodehex.com/html-color-picker.html.

**clr_min_max**

The order follows the same ordering convention as **colors**. Min to max.
