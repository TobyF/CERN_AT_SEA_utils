import os
import datetime
import json
import numpy as np
import math
#import magic
import time
import sys

def neighbourGen(pixelNo):
    neighbours = []
    for xChange in range(-1,2,2):
        for yChange in range(-1,2,2):
            neighbours.append(pixelNo+xChange+256*yChange)
    return neighbours

def surrogateFunction(tot, a, b, c, t):
    e = (t * a + tot - b + math.sqrt((b + t * a - tot) ** 2 + 4 * a * c)) / (2 * a)
    return e

class CASfile():
    def __init__(self,inputLoc, calibDataLoc="NOT IMPLEMENTED", outputLoc=None):
        print("New CAS File: Looking for Frame files! ")
        self.frames = []

        calibrationMatrixA = np.loadtxt(r"calibs\H05-W0240\caliba.txt").flatten()
        calibrationMatrixB = np.loadtxt(r"calibs\H05-W0240\calibb.txt").flatten()
        calibrationMatrixC = np.loadtxt(r"calibs\H05-W0240\calibc.txt").flatten()
        calibrationMatrixT = np.loadtxt(r"calibs\H05-W0240\calibt.txt").flatten()

        calibMatricies = {"a":calibrationMatrixA, "b":calibrationMatrixB,
                          "c":calibrationMatrixC, "t":calibrationMatrixT}

        for filename in os.listdir(inputLoc):
            extension = os.path.splitext(filename)[-1].lower()
            if extension == "" and os.path.isfile(os.path.join(inputLoc, filename+".dsc")): #A DSC file and mnt

                print("\tFound a NT file: "+filename+" with its .dsc file. Now processing...")

                with open(os.path.join(inputLoc, filename),"r") as ntFile: #Opens the file with all the frames in set
                    ntFileString = ntFile.read().split("#") #Splitting the file into frames

                with open(os.path.join(inputLoc, filename+".dsc"),"r") as dscFile: #Opens .dsc file
                    dscData = dscFile.read().split("[F") #Splits it at every Frame marker - [F1] = 2nd Frame

                frameNumber = 0

                for importedFrameString in ntFileString: #Go through all the frames
                    pixels = []

                    #Get the pixels
                    for importedPixelString in importedFrameString.split("\n"):
                        if importedPixelString.split("\t") != ['']: #Avoiding Blank Space Errors
                            pixels.append(importedPixelString.split("\t"))


                    for dscEntry in dscData:
                        #print(dscEntry)
                        if dscEntry.startswith(str(frameNumber)+"]"): #Checks if the correct entry has been found

                            dscEntry = dscEntry.split('\n')

                            for lineCounter in range(len(dscEntry)):
                                if dscEntry[lineCounter].startswith('"Acq time"'):
                                    acqTimeTemp = dscEntry[lineCounter+2]

                                if dscEntry[lineCounter].startswith('"Start time"'):
                                    startTimeTemp = dscEntry[lineCounter + 2]
                    #print(pixels)
                    self.frames.append(Frame(pixels, filename,
                                             frameNumber, calibMatricies,
                                             acqTimeTemp, startTimeTemp)) #Make the new frame with all its pixels

                    frameNumber+=1


                print("\tProcessed \n")

            if filename.endswith(".gps"):
                pass

        print("New File Initialised: Found "+str(len(self.frames))+" frames:")
        print(str(self.frames))

    def histogram(self):
        pass

    def map(self):
        pass

    def countrate(self,timeRange):
        pass

    def getFrame(self,frameNo):
        pass



class Frame():
    def __init__(self, nt, ntFileName, frameNumber, calibMatricies, acqTime=None, startTime=None):
        #print(nt)
        self.nt = [[int(string) for string in inner] for inner in nt]
        self.ntFileName = ntFileName
        self.frameNumber = frameNumber
        self.acqTime = acqTime
        self.startTimeRaw = startTime
        self.startTime = datetime.datetime.fromtimestamp(float(startTime))

        self.gammaEnergyList = []

        print("\t \tNew Frame Instance: Calibrating Data",end=" ")
        #print(self.nt)
        self.i = 0
        for pixel in self.nt:
            self.i+=1

            inCluster = False
            for neighbour in neighbourGen(int(pixel[0])):
                if neighbour in [pixel[0] for pixel in self.nt]:
                    inCluster = True

            if not inCluster and pixel[1] not in [1, 11810]: # Max and Min values for chip - taking out background data
                #print(type(pixel[0]))
                e = surrogateFunction(pixel[1],
                                      calibMatricies["a"][int(pixel[0])],
                                      calibMatricies["b"][int(pixel[0])],
                                      calibMatricies["c"][int(pixel[0])],
                                      calibMatricies["t"][int(pixel[0])])
                self.gammaEnergyList.append(e)

        print("Done.")

    def __repr__(self):
        return "Frame with: "+str(len(self.nt))+' pixels'


    def description(self):
        print("Frame Instance:")
        print("\tFrom the "+self.ntFileName+" file.")
        print("\tIt contains "+str(len(self.nt))+' activated pixels.')
        print("\tIt was started at time: "+self.startTime.isoformat()+".")
        print("\tIt was acquiring data for: "+self.acqTime+" second(s).")


    def get_xyc(self):
        if self.xyc == None:
            pass
        return self.xyc

    def get_array(self):
        if self.array ==None:
            pass
        return self.array

    def calibrateData(self):
        if not self.calibrated:
            pass
    def get_xye(self):
        pass

    def get_arraye(self):
        pass

testFile = CASfile(r"C:\Users\Toby\PycharmProjects\CERN@SEA_utils_\CAStest1")
#testFile.frames[0].description()
#testFile.frames[1].description()
#testFile.frames[2].description()
#testFile.frames[3].description()

#with open(r"C:\Users\Toby\PycharmProjects\CERN@SEA_utils_\CAStest1\FIRST YEAH.dsc", "r") as dscFILE:
    #jsonFile = json.load(dscFILE)