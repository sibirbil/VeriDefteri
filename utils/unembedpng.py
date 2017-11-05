#!/usr/bin/env python3
# Removes embedded png images from an HTML file
# Creates separate image files. 
# Fixes img tags accordingly.
# Overwrites the original HTML file.

# Usage:  unembedpng.py <filename>.html

# Generated files: <filename>_image0.png, <filename>_image1.png, etc.

import sys
from bs4 import BeautifulSoup
from binascii import a2b_base64

filename = sys.argv[1]
fileext = filename.split(".")[-1]
filestem = ".".join(filename.split(".")[:-1])
if fileext != "html":
    print("Please use an html file.")
    sys.exit()

with open(filename) as fin:
    html = fin.read()
    
soup = BeautifulSoup(html, 'html.parser')

i = 0
for img in soup.find_all("img"):
    if "data:image/png;base64" in img["src"]:
        data = img["src"].split(",")[1].replace("\n","")
        binary_data = a2b_base64(data)
        with open('{}_image{}.png'.format(filestem,i), 'wb') as fout:
            fout.write(binary_data)
        img["src"]='{}_image{}.png'.format(filestem,i)
        i += 1

with open(filename,"w") as fout:
    fout.write(str(soup))
