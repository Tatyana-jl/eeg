def ResultTable(FilePath, numOfSignals):
    from ReadSignal import ReadSignals
    import pandas as pd
    Signal = ReadSignals(FilePath)
    Data = ReadSignals.ReadDocument(Signal)
    column_names = [Data[i][0] for i in range(len(Data))]
    column_names.insert(0, 'Signal')
    index = [i for i in range(1, numOfSignals+1)]
    Result = pd.DataFrame(index=index, columns=column_names)
    return Result

# print ResultTable('/home/tanya/Documents/eeg/algos/files/ictal1.xlsx', 5)

