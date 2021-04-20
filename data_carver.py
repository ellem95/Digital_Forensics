#                                                                 Project 2
#                                                                Data Carver
#                                                                July, 17 2020
#                                                                Chidima Okafor
#                                                                Eloise Morris
#                                                                Wil Boshell
#                                                                Joel Sweeney
#################################################################################################################################################################################

#! /usr/bin/env python3

import sys
import re
import os
import hashlib
import shutil

file_number = 0

#create directory to store the carved files
os.makedirs("Morris", exist_ok=True)

#creates a function to write the defined 'subdata' to a new file in the directory.
def carvefucntion(datasub):
    filename = os.path.join(save_path, "carve_" + str(file_number) + ext)

    with open(filename, 'wb') as carve_obj:
        carve_obj.write(datasub)

    #create single hashes.txt file
    with open('hashes.txt', 'ab') as save_hash:
        filehash = hashlib.md5(subdata.strip()).hexdigest()
        save_hash.write(filehash.encode())
        save_hash.write('\n'.encode())




#creates a variable to save the file to the new directory
save_path = './Morris/'

fname = sys.argv[1]

#defines the file magic numbers that will be searched
PNG_SOF = b'\x89\x50\x4E\x47'
PNG_EOF = b'\x49\x45\x4E\x44\xAE\x42\x60\x82'
PDF_SOF = b'\x25\x50\x44\x46'
PDF_EOF = b'\x25\x25\x45\x4F\x46'
JPG_SOF = b'\xFF\xD8'
JPG_EOF = b'\xFF\xD9'

#reads the file and creates a list of SOF and EOFs for each file type
fname_obj = open(fname, 'rb')
data = fname_obj.read()
fname_obj.close()
PNG_SOF_list = [match.start() for match in re.finditer(re.escape(PNG_SOF),data)]
PNG_EOF_list = [match.start() for match in re.finditer(re.escape(PNG_EOF),data)]
PDF_SOF_list = [match.start() for match in re.finditer(re.escape(PDF_SOF),data)]
PDF_EOF_list = [match.start() for match in re.finditer(re.escape(PDF_EOF),data)]
JPG_SOF_list = [match.start() for match in re.finditer(re.escape(JPG_SOF),data)]
JPG_EOF_list = [match.start() for match in re.finditer(re.escape(JPG_EOF),data)]


#Pairs each SOF with every possible EOF that follows before calling the carve fuction to write the file
for SOF in PNG_SOF_list:
    for EOF in PNG_EOF_list:
        if EOF > SOF:
            filesize = int(EOF-SOF+8)
            ext = ".png"
            print("Found png file. SOF =", str(SOF),"EOF =", str(EOF), "File Size =", filesize, "bytes")
            subdata = data[SOF:EOF+8]
            carvefucntion(subdata)
            file_number += 1

for SOF in JPG_SOF_list:
    for EOF in JPG_EOF_list:
        if EOF > SOF:
            filesize = int(EOF-SOF+2)
            ext = ".jpg"
            print("Found jpg file. SOF =", str(SOF),"EOF =", str(EOF), "File Size =", filesize, "bytes")
            subdata = data[SOF:EOF+2]
            carvefucntion(subdata)
            file_number += 1

# For PDFs we check for every possible variation of trailers before carving each file.
for SOF in PDF_SOF_list:
     for EOF in PDF_EOF_list:
         if EOF > SOF:
             delta=5 #Offset counter.
             if data[EOF+5]==0x0D: #Immeadiately after the 0x46 byte.
                 delta+=1
                 if data[EOF+6]== 0x0A:
                     delta+=1
             elif data[EOF+5]==0x0A: #These cases should properly increment the EOF counter.
                 delta+=1
             filesize = int(EOF-SOF+delta)
             ext = ".pdf"
             print("Found pdf file. SOF =", str(SOF),"EOF =", str(EOF), "File Size =", filesize, "bytes")
             subdata = data[SOF:EOF+delta]
             carvefucntion(subdata)
             file_number += 1

#moves hashes.txt into the same directory as the carved files.          
shutil.move('hashes.txt', './Morris/')
