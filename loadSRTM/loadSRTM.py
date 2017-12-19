# -*- coding: utf-8 -*-
import os
import math
# import progressbar
import urllib2
import re
import logging
#import gdal
from tqdm import tqdm
import zipfile
from datetime import datetime, timedelta
from multiprocessing.dummy import Pool # use threads


logger = logging.getLogger(__name__)

def printbbox(bbox):
    print("{:^30}".format(bbox[3]))
    print("{0:>6}{1:-<20}{2:<6}".format("+", "", "+"))
    print("{0:>6}{1:<20}{2:<6}".format("|", "", "|"))
    print("{0:>6}{1:<20}{2:<6}".format("|", "", "|"))
    print(("{0}|{1:<20}|{2}".format(bbox[0], "", bbox[2])))
    print("{0:>6}{1:<20}{2:<6}".format("|", "", "|"))
    print("{0:>6}{1:<20}{2:<6}".format("|", "", "|"))
    print("{0:>6}{1:-<20}{2:<6}".format("+", "", "+"))
    print("{:^30}".format(bbox[1]))

class loadSRTM(object):

    serviceURL = "https://dds.cr.usgs.gov/srtm/version2_1/SRTM30/"


    def __init__(self, bbox, targetDir = None):
        #bbox: [minlon, minlat, maxlon, maxlat]
        #bbox: [left, bottom, right, top]
        self.bbox = bbox
        self.targetDir = targetDir
        self.fileURLs = []
        #path list also stores fileURLs so maybe change methods to accomodate that and remove
        self.pathList = []

    def createFileList(self):
        """Creates file names based on bounding box.

        Parameters
        ----------
        
        Return
        ------
        list:
            list with tilenames
        """
        curlon = -180
        startlat = -60
        curlat = startlat

        bblonmin = math.ceil((self.bbox[0] + 180)/40) * 40 - 180
        bblonmax = math.floor((self.bbox[2] + 180)/40) * 40 - 180
        bblatmin = math.ceil((self.bbox[1] + 60)/50) * 50 - 60
        bblatmax = math.floor((self.bbox[3] + 60)/50) * 50 - 60

        #printbbox(self.bbox)
        #printbbox([bblonmin, bblatmin, bblonmax, bblatmax])

        while curlon <= bblonmax:
            #print(curlon)
            if bblonmin <= curlon + 40:
                #print("curlon: {}".format(curlon +40))
                if curlon < 0:
                    lonpref = "w"
                else:
                    lonpref = "e"
                while curlat <= bblatmax:
                    #print(curlat)
                    if bblatmin <= curlat + 50:
                        #print("curlat: {}".format(curlat + 50))
                        if curlat + 50 < 0:
                            latpref = "s"
                        else:
                            latpref = "n"

                        tile = lonpref + "{:0>3}".format(abs(curlon)) + latpref + str(abs(curlat + 50))
                        demurl = os.path.join(self.serviceURL, tile, tile + ".dem.zip")
                        prjurl = os.path.join(self.serviceURL, tile, tile + ".prj.zip")
                        hdrurl = os.path.join(self.serviceURL, tile, tile + ".hdr.zip")

                        self.fileURLs.append(demurl)
                        self.fileURLs.append(prjurl)
                        self.fileURLs.append(hdrurl)

                    curlat += 50
            
            #reset curlat to start value for each lon iteration
            curlat = startlat
            curlon += 40
                
        #print(tiles)
        return 

        
    def downloadFiles(self, directory = None, maxRetries = 5, multiproc = False, numproc = 3):
        """Download URLs.

        Parameters
        ----------
        directory: str
            Base directory where to save files
        maxRetries: int
            Maximum number of retrys to open the url
        multiproc: boolean
            Download multiple files at the same time.
        numproc: int optional
            Number of processes if multiproc is set to True

        
        Return
        ------
        """
        if self.targetDir is None or directory is None:
            print("No target directory given.")
            if directory is None:
                directory = self.targetDir

        def pathTuple(url, directory = directory):
            return((url, directory))

        def download(itemtuple):
            #unpack tuple
            url = itemtuple[0]
            directory = itemtuple[1]

            fname = os.path.basename(url)
            fpath = os.path.join(directory, fname)


            attempts = 0
            while attempts < maxRetries:
                try:
                    response = urllib2.urlopen(url)
                    attempts += 1
                except urllib2.URLError as e:
                    logger.debug(e)
                    logger.debug("File {0} failed to download with the above error".format(url))
                    pass

            with open(fpath, "wb") as f:
                f.write(response.read())

            #update progressbar
            pbar.update(1)


            return


        try:
            if directory is not None:
                self.pathList = list(map(pathTuple, self.fileURLs))
            else:
                raise TypeError
        except TypeError:
            print("""No target directory were to store files given. Instantiate search obejct with 
                    directory or set the directory parameter of downloadFiles.""")
        
        #create year directories separate to avoid race condition when
        #using it in the download function itself and multiprocessing enabled
        for d in set([x[1] for x in self.pathList]):
            #check if fpath exists. create if necessary 
            if not os.path.exists(d):
                os.makedirs(d)

        logger.debug("Starting download of files...")
        print("Starting download of files...")

        pbar = tqdm(total = len(self.pathList))

        if multiproc:
            p = Pool(numproc)
            p.map(download, self.pathList)
            p.close()
            p.join()
        else:
            map(download, self.pathList)
        
        pbar.close()


        #check if file was downloaded correctly else download again

        pass


    def unpack(self):
        """Unpack downloaded zip files

        Parameters
        ----------
        param: dtype
            description

        
        Return
        ------
        """
        def up(file, targetdir = "."):
            with ZipFile(file, "r") as zfile:
                zfile.extractall(targetdir)
            return


        logger.debug("Unziping files...")
        print("Unziping files...")

        map(download, self.pathList)
        
        pass

# if __name__ == "__main__":
