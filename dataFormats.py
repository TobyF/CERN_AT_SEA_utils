#XYC is 1 file per frame with X (x coordinate) Y (y coordinate) and C (charge/ToT) per line
#NC is 1 file per frame with N (pixel number) and C (charge/ToT) per line
#MNC is a multi frame version of NC and is a series of NC files separated by a single "#" <-- This is the default output of a RasPix
#import matplotlib.pyplot as plt
import numpy as np

def MNC2XYC(mncFile):
    output = []
    #print(mncFile)
    for frame in mncFile:
        outputFrame = []
        #print("Frame:"+str(frame))
        for pixel in frame:
            #print(outputFrame)
            #print(pixel)
            Y = pixel[0]//255
            X = pixel[0]%255
            outputFrame.append([X,Y,pixel[1]])
        output.append(outputFrame)
    return output


def MNCtoNCs(mncFile, outputFileNamePrefix = "NC"):
    i = 0
    for line in mncFile.readlines():
        if line.strip() == "#": i+=1
        else:
            with open(outputFileNamePrefix + str(i), "a") as output: output.write(line)


def isMNC(potentialFile):
    for line in potentialFile.readlines():
        if line.strip() == "#": return True
    return False

def importMNC(mncFile):
    #Output is a 3D array. output[FrameNumber][Pixel(NotNumbered)][0=PixelNumber,1=ToT]
    currentFrame = []
    outputMNClist = []
    for line in mncFile.readlines():
        if line.strip() == "#":
            outputMNClist.append(currentFrame)
            currentFrame = []
        elif line.split()[1] not in ["1","11810"]:
            currentFrame.append(list(map(int,line.split())))
    return outputMNClist


with open("DataFiles\mnc_test") as file:
    mnc = importMNC(file)

    #print(mnc)
    #print(MNC2XYC(mnc))