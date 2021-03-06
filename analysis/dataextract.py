#!/usr/bin/env python2.5

import sys
import os
from optparse import OptionParser
from subprocess import Popen, call, PIPE, STDOUT
from srw import Aperture, getAperNumbers, orderDict
#from IPython.Shell import IPShellEmbed


def main(options, args):
    dir = args[0].rstrip('/')
    p = Popen('ls %s' % dir, shell=True, stdout=PIPE, stderr=PIPE)
    filelist = p.communicate()[0].split()
    #filelist = os.listdir(dir)
    aperNums = getAperNumbers(filelist, dir)
    # create dictionary of apertures
    print '#',
    for val in sorted(int(x) for x in aperNums):
        print val,
    print

    aperlist = orderDict({})
    for i in aperNums:
        aperlist[i] = Aperture(i)




    # read in data to aperture objects
    for file in filelist:
        try:
            fptr = open(dir + '/' + file)
        except IOError:
            print >> sys.stdout, "Error opening file %s" % (dir + '/' + file)
            exit(1)
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
    if options.lightcurve:
        for i in range(len(filelist)):
            for val in aperlist.sorted():
                print "%f" % val.flux[i],
            print

    elif options.coords:
        for i in range(len(filelist)):
            for val in aperlist.sorted():
                print "%f %f" % (val.xcoord[i], val.ycoord[i]),
            print

    elif options.sky:
        for i in range(len(filelist)):
            for val in aperlist.sorted():
                print val.sky[i],
            print

    elif options.errors:
        for i in range(len(filelist)):
            for val in aperlist.sorted():
                print val.getErrors()[i],
            print


if __name__ == '__main__':

    parser = OptionParser(usage="usage: %prog -[lcse] <dir>", conflict_handler="resolve",
            version="0.1")
   
    parser.add_option('-l', '--lc', action="store_true", dest="lightcurve",
            help="Output sky-subtracted flux data", default=False)


    parser.add_option('-s', '--sky', action="store_true", dest="sky",
            help="Output raw sky data", default=False)

    parser.add_option('-c', '--coords', action="store_true", dest="coords",
            help="Output coordinate data separated by ' '", default=False)

    parser.add_option('-e', '--errors', action="store_true", dest="errors",
            help="Output error data", default=False)

    (options, args) = parser.parse_args()

    if len(args) != 1:
        print >> sys.stderr, "Program usage: %s -[lcse] <dir>" % sys.argv[0]
        exit(1)
   
    if (options.lightcurve and options.sky) or (options.lightcurve and options.coords) or \
    (options.sky and options.coords) or (options.errors and options.lightcurve) or \
    (options.errors and options.coords) or (options.errors and options.sky):
        parser.error('Options are mutually exclusive')
    elif not options.lightcurve and not options.sky and not options.coords and not options.errors:
        parser.error('One option of lcs required')


    main(options, args)

