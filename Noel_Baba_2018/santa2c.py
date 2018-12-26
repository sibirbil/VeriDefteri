#!/usr/bin/env python
# santa2c.py
# CSV dosyasındaki verileri C array olarak içeren bir data.c dosyası yaratır.

import numpy as np
cities = np.loadtxt("data/cities.csv", delimiter=",",skiprows=1, usecols=(1,2))

from sympy import sieve
primeids = sieve.primerange(0,197769)
        
with open("data.c","w") as f:
    # Asal olan şehir numaralarını sıralı bir diziye yaz.
    f.write("unsigned int asalsehirler[] = {")
    for p in primeids:
        f.write( str(p)+"," )
    f.write( "};\n" )
    
    # Şehirlerin x koordinatlarını bir diziye yaz.
    f.write( "double x[]={"+str(cities[0,0]) )
    for x in cities[1:,0]:
        f.write( ","+str(x) )
    f.write( "};\n" )

    # Şehirlerin y koordinatlarını bir diziye yaz.
    f.write( "double y[]={"+str(cities[0,1]) )
    for y in cities[1:,1]:
        f.write( ","+str(y) )
    f.write( "};\n" )