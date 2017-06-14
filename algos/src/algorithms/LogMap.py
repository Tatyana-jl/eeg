def LogRefl(FilePath, DataLen):
    import math
    from ReadSignal import ReadSignals
    import pandas as pd
    import numpy as np

    Signal = ReadSignals(FilePath)
    Data = ReadSignals.ReadDocument(Signal)
    R = []

    for k in range(len(Data)):
        Data_norm = []
        min_row = int(min(Data[k][1:DataLen]))
        max_row = int(max(Data[k][1:DataLen]))+math.fabs(min_row)+1
        for i in range(1, len(Data[k][1:DataLen])):
            Data_norm.append((Data[k][i] + math.fabs(min_row)+1)/max_row)
        r = []
        for i in range(len(Data_norm)-1):
            r.append(Data_norm[i]*(1.0 + Data_norm[i])/Data_norm[i+1])
        R.append(r)
    R = np.array(R)
    Perc = np.percentile(R, [9,25,50,75,91], axis=1)
    Result = []
    for i in range(len(Perc[0])):
        Result.append([Perc[0][i], Perc[1][i], Perc[2][i], Perc[3][i], Perc[4][i]])
    return Result



# column_names = ['Signal','Fp1', 'Fp2', 'F3', 'F4', 'F7', 'F8', 'T3', 'T4', 'C3',
#                         'C4', 'T5', 'T6', 'P3', 'P4', 'O1', 'O2']
#
# print LogRefl('/home/tanya/Documents/RS/Data/Pathology2/Babich -2014/ictal1.xlsx', 550)
