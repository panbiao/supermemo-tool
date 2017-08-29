'''
Created on 2017-02-16

@author: ccc
'''

import os
import sys
import struct

def splitPCMFile(fileName):
    outFileName = os.path.basename(fileName)
    fpcm = open(fileName, 'rb')
    fout_l = open(outFileName + '_l.pcm', 'wb')
    fout_r = open(outFileName + '_r.pcm', 'wb')
    
    filedata = fpcm.read()
    filesize = fpcm.tell()
    file_byte = bytearray(filedata)
    fpcm.close()
    
    index = 0
    while(index < filesize):
        tmp_data = struct.pack("BB", file_byte[index], file_byte[index+1])
        fout_l.write(tmp_data)
        tmp_data = struct.pack("BB", file_byte[index+2], file_byte[index+3])
        fout_r.write(tmp_data)
        index += 4
    fout_l.flush()
    fout_l.close()
    fout_r.flush()
    fout_r.close()


if __name__ == '__main__' :
    if len(sys.argv) != 2 :
        print("splitpcm PCMFileName")
        exit()
    splitPCMFile(sys.argv[1])