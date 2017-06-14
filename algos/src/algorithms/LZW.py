from HurstExp import Hurst

def LZWcompl(FilePath, signal_name, DataLen, takeInd, Result):
    from ReadSignal import ReadSignals
    import string
    import pandas as pd
    import numpy as np
    import math

    def Sterdg(Data):
        abt = string.ascii_lowercase
        n = 1 + int(math.log(len(Data), 2))
        step = math.ceil((max(Data) - min(Data))/n)
        EncodeDict = {abt[i]: [min(Data)+i*step, min(Data)+(i+1)*step] for i in range(n)}
        al_len = len(set(EncodeDict))
        for i in range(len(Data)):
            for k in EncodeDict.keys():
                if Data[i] >= EncodeDict.get(k)[0] and Data[i] <= EncodeDict.get(k)[1]:
                    Data[i] = k
        return Data, al_len

    def LZW(Data_encode, n):
        import string
        def CheckDict(Dictionary_ch, let):
            return Dictionary_ch.get(let) == None

        abt = string.ascii_lowercase
        Data_encode = ''.join(Data_encode)
        Dictionary = {abt[i]: i for i in range(n)}
        i = 0
        compress = []
        decompress = []
        while i < len(Data_encode):
            k = 2
            let = Data_encode[i:i + k]
            while CheckDict(Dictionary, let) != True:
                k += 1
                if i + k <= len(Data_encode):
                    let = Data_encode[i:i + k]
                else:
                    left = Data_encode[i:]
                    compress.append(left)
                    let = 'empty'
            Dictionary[let] = len(Dictionary)
            compress.append(let[:-1])
            i = i + k - 1
        for r in range(len(compress) - 1):
            compress[r] = Dictionary[compress[r]]
        for r in range(len(compress) - 1):
            for key, val in Dictionary.items():
                if val == compress[r]:
                    decompress.append(key)
        decompress = ''.join(decompress)
        compare = len(compress) * 1.0 / len(Data_encode)
        return compare


    def Results(TableArchiv, Result, signal_name, takeInd, column_names):
        index = [takeInd]
        Result['Signal'][takeInd] = signal_name
        for k in range(len(TableArchiv)):
            Result[column_names[k]][takeInd] = TableArchiv[k]
        return Result

    def countArch(Data, signal_name, DataLen, takeInd, Result, column_names):
        LZWArchiv = []
        for k in range(len(Data)):
            Data_encode, al_len = Sterdg(Data[k][1:DataLen])
            LZWArchiv.append(LZW(Data_encode, al_len))
        return Results(LZWArchiv, Result, signal_name,  takeInd, column_names)

    Signal = ReadSignals(FilePath)
    Data = ReadSignals.ReadDocument(Signal)
    column_names = [Data[i][0] for i in range(len(Data))]
    Result = countArch(Data, signal_name, DataLen, takeInd, Result, column_names)

    return Result

#
# import pandas as pd
# column_names = ['Signal','Fp1', 'Fp2', 'F3', 'F4', 'F7', 'F8', 'T3', 'T4', 'C3',
#                         'C4', 'T5', 'T6', 'P3', 'P4', 'O1', 'O2']
# index = [1]
# Result = pd.DataFrame(index=index, columns=column_names)
# # print CrossT('/home/tanya/Documents/RS/Data/Pathology2/Babich -2014/ictal1.xlsx', 'ictal', 550, 1, Result)
# print Hurst('/home/tanya/Documents/RS/Data/Pathology2/Babich -2014/ictal1.xlsx', 'ictal', 550, 1, Result)