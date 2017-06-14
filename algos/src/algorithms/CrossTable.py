def CrossT(FilePath, signal_name, DataLen, takeInd, Result):
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

    def CountInTable(Data_encode, n):
        starLen = len(Data_encode)
        def FindMax(Data_encode, column_name, row_name):
            CompressTable = pd.DataFrame(0, index=row_name, columns=column_name) #number of row - firts letter, of column - second
            for i in range(0, len(Data_encode)-1):
                CompressTable[Data_encode[i+1]][Data_encode[i]] = CompressTable[Data_encode[i+1]][Data_encode[i]] + 1

            max_col = max(CompressTable[column_name[0]])
            m_col = column_name[0]
            m_row = column_name[0]
            for col in column_name:
               if max_col < CompressTable[col].max():
                   max_col = CompressTable[col].max()
                   m_col = col
                   m_row = CompressTable[col].idxmax()
            return m_col, m_row, max_col

        abt = string.ascii_lowercase
        Data_encode = ''.join(Data_encode)
        column_name = [abt[i] for i in range(n)]
        row_name = [abt[i] for i in range(n)]
        max_col = 2
        letter = 0
        while max_col > 1 and letter < len(abt)-n:
            m_col, m_row, max_col = FindMax(Data_encode, column_name, row_name)
            column_name.append(abt[n+letter])
            row_name.append(abt[n + letter])
            Data_encode = Data_encode.replace(m_row+m_col, abt[n + letter])
            letter += 1
        Data_encode = Data_encode.replace(m_row + m_col, abt[n + letter - 1])
        return len(Data_encode)*1.0/starLen



    def Results(TableArchiv, Result, signal_name, takeInd, column_names):
        index = [takeInd]
        Result['Signal'][takeInd] = signal_name
        for k in range(len(TableArchiv)):
            Result[column_names[k]][takeInd] = TableArchiv[k]
        return Result

    def countArch(Data, signal_name, DataLen, takeInd, Result, column_names):
        TableArchiv = []
        
        for k in range(len(Data)):
            Data_encode, al_len = Sterdg(Data[k][1:DataLen])
            TableArchiv.append(CountInTable(Data_encode, al_len))
        return Results(TableArchiv, Result, signal_name,  takeInd, column_names)

    Signal = ReadSignals(FilePath)
    Data = ReadSignals.ReadDocument(Signal)
    column_names = [Data[i][0] for i in range(len(Data))]
    Result = countArch(Data, signal_name, DataLen, takeInd, Result, column_names)

    return Result

import pandas as pd
column_names = ['Signal', 'Fp1', 'Fp2', 'F3', 'F4', 'F7', 'F8', 'T3', 'T4', 'C3',
                         'C4', 'T5', 'T6', 'P3', 'P4', 'O1', 'O2']
index = [1]
Result = pd.DataFrame(index=index, columns=column_names)
print CrossT('/home/tanya/Documents/RS/Data/Pathology2/Babich -2014/ictal1.xlsx', 'ictal', 550, 1, Result)
