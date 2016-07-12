import datasetreader

#dataset = datasetreader.CASfile(r"C:\Users\Toby\PycharmProjects\CERN@SEA_utils_\CAStest1")

with open(r"C:\Users\Toby\PycharmProjects\CERN@SEA_utils_\DataFiles1\mnc_test") as file:
    i = 0
    for line in file.readlines():
        print(line)
        i += 1
    print((100*i)/(255**2))