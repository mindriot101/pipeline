#!/usr/bin/env python2.5

import sys
import os
from optparse import OptionParser
from subprocess import Popen, call, PIPE, STDOUT
from ApObs import Aperture
#from IPython.Shell import IPShellEmbed


def getAperNumbers(fl, d):
    """Arguments:
        fl = filelist, list of strings containing 
                filenames
        d = dir, directory where fl is

    Returns:
        list of numbers of apertures"""


    t = open(d + '/' + fl[0])
    tmp = t.readlines()
    t.close()

    nums = []

    for line in tmp:
        if '#' not in line:
            nums.append(line.split()[0])

    return nums

def main(options, args):
    dir = args[0].rstrip('/')
    p = Popen('ls %s' % dir, shell=True, stdout=PIPE, stderr=PIPE)
    filelist = p.communicate()[0].split()
    #filelist = os.listdir(dir)
    filelist.remove('cmd')
    aperNums = getAperNumbers(filelist, dir)
    # create dictionary of apertures
    aperlist = {} 
    for i in aperNums:
        aperlist[i] = Aperture(i)




    # read in data to aperture objects
    for file in filelist:
        fptr = open(dir + '/' + file)
        data = []
        for line in fptr.readlines():
            if '#' not in line:
                data.append(line.rstrip('\n'))

        for line in data:
            vals = line.split()
            num = vals[0] 
            coords = float(vals[1]), float(vals[2])
            flux = {'sky': float(vals[5]), 'aper': float(vals[6])}
            err = float(vals[4])
            mag = float(vals[3])

            aperlist[num].addLine((coords[0], coords[1], flux['sky'], flux['aper'], err, mag))


    #write data to stdout
    for i in range(len(filelist)):
        for val in aperlist.values():
            print val.flux[i],
        print


if __name__ == '__main__':

    parser = OptionParser(usage="usage: %prog [options] <dir>", conflict_handler="resolve",
            version="0.1")
    

    (options, args) = parser.parse_args()

    if len(args) != 1:
        print >> sys.stderr, "Program usage: %s [options] <dir>" % sys.argv[0]
        exit(1)
    


    main(options, args)

