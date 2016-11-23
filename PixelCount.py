import os
import Tkinter as tk
import tkFileDialog

root = tk.Tk() #Opens the main window
root.wm_title("hey")

threshFreqFrame = tk.Frame(root)
threshFreqFrame.pack()

threshFreqEntry = tk.Entry(threshFreqFrame)
threshFreqEntry.pack()


inputLoc = tkFileDialog.askdirectory(parent = root) #Asks for a directory to look for RasPix data
directoryData = {"FileCount":0,"FrameCount":0,"PixelCount":0}

for filename in os.listdir(inputLoc): #For all of the files (regardless of type in the directory)

        extension = os.path.splitext(filename)[-1].lower() #Find tis extension

        if extension == "": #If it dosnt have one (the RasPix data files dont :( )
            #XT refers to type of file that raspix outputs, X is the position, T is the TimeOverThreshold.

            print("Found a XT file: " + filename + ". Now processing...")
            directoryData["FileCount"] += 1

            with open(os.path.join(inputLoc, filename), "r") as ntFile:  # Opens the file with all the frames in set
                xtList = ntFile.read().split("#")  # Splitting the file into frames (which have # between them)

            for frame in xtList:
                directoryData["FrameCount"] += 1

                for pixel in frame:
                    directoryData["PixelCount"] += 1




print(directoryData)

root.mainloop()