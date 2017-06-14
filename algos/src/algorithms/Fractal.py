def FractalDimension(FilePath, signal_name, DataLen, takeInd, Result):
    from ReadSignal import ReadSignals
    import numpy as np
    import pandas as pd
    import math
    from scipy.optimize import curve_fit

    def FD(Data):

        Data = np.array(Data).astype(np.float)
        max_Data = np.max(Data)
        min_Data = np.min(Data)
        dif = max_Data - min_Data
        r = np.array([dif / (2.0 ** i) for i in range(5, 0, -1)])
        data_n = np.array([Data[k+1] for k in range(len(Data)-1)])
        NotEmptyBoxes = [CountBoxes(Data[:-1], data_n, ri, dif, min_Data) for ri in r]
        return (NotEmptyBoxes, r)

    def CountBoxes(data, data_n, size, dif, min_data):

        boxes = []
        counts = 0
        for i in range(np.int(np.floor(dif/size))):
            for k in range(np.int(np.floor(dif/size))):
                boxes.append([min_data+i*size, min_data+(i+1)*size, min_data+k*size, min_data+(k+1)*size, False])
        boxes = pd.Series(boxes)
        for i in range(len(data)):
            for k in range(len(boxes)):
                condition = (boxes[k][0] <= data[i] and boxes[k][1] > data[i] and boxes[k][2] <= data_n[i] and boxes[k][3] > data_n[i])
                if condition:
                    boxes[k][4] = True
        for k in range(len(boxes)):
            if boxes[k][4]:
                counts += 1
        return counts

    def FD_count(Data, DataLen):
        Ni_ri = [(FD(Data[i][1:DataLen])) for i in range(len(Data))]
        Ni = [Ni_ri[i][0] for i in range(len(Ni_ri))]
        ri = [Ni_ri[i][1] for i in range(len(Ni_ri))]
        for i in range(len(Ni)):
            Ni[i] = [math.log(Ni[i][k]) for k in range(len(Ni[i]))]
            ri[i] = [math.log(1/ri[i][k]) for k in range(len(ri[i]))]
        def func(x, A, Df):
            return Df*x + A
        Ai = []
        Dfi = []
        for i in range(len(Data)):
            popt, pcov = curve_fit(func, ri[i], Ni[i])
            A, Df = popt
            Ai.append(A)
            Dfi. append(Df)
        return Dfi

    def Results(Dfi, Result, signal_name,  takeInd, column_names):
        index = [takeInd]
        Result['Signal'][takeInd] = signal_name
        for k in range(len(Dfi)):
            Result[column_names[k]][takeInd] = Dfi[k]
        return Result

    Signal = ReadSignals(FilePath)
    Data = ReadSignals.ReadDocument(Signal)
    column_names = [Data[i][0] for i in range(len(Data))]
    Dfi = FD_count(Data, DataLen)
    Results(Dfi, Result, signal_name, takeInd, column_names)

    return Result

# import pandas as pd
# column_names = ['Signal','Fp1', 'Fp2', 'F3', 'F4', 'F7', 'F8', 'T3', 'T4', 'C3',
#                         'C4', 'T5', 'T6', 'P3', 'P4', 'O1', 'O2']
# index = [1]
# Result = pd.DataFrame(index=index, columns=column_names)
# print FractalDimension('/home/tanya/Documents/RS/Data/Pathology2/Babich -2014/ictal1.xlsx', 'ictal', 10, 1, Result)