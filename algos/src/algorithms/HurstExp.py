def Hurst(FilePath, signal_name, DataLen, takeInd, Result):
    from ReadSignal import ReadSignals
    import math
    import numpy as np
    from scipy.optimize import curve_fit

    def Prepare(DataRow, DataLen):
        Data=[]
        for i in range(len(DataRow)):
            Data.append(DataRow[i][1:DataLen])
        DataNew = [[] for i in range(len(Data))]
        for i in range(len(Data)):
            min_row = int(min(Data[i]))
            for k in range(len(Data[i])):
                DataNew[i].append(Data[i][k]+math.fabs(min_row)+1.0)
        return DataNew

    def CountForN(Data, n):
        I = [Data[i:i+n] for i in range(0, len(Data)-n, n)]
        if len(Data) % n != 0:
            left = len(Data)-n*(len(Data)//n)+1
            I.append(Data[-left:])
        EIa = []
        for i in range(len(I)):
            EIa.append(sum(I[i])/n)
        X = [[] for i in range(len(I))]
        for i in range(0, len(I)):
            for k in range(len(I[i])):
                X[i].append(I[i][k]-EIa[i])
        R = []
        for i in range(0, len(I)):
            R.append(max(X[i])-min(X[i]))
        S = []
        for i in range(0, len(I)):
            countS = math.sqrt((1.0/n)*sum([math.pow(I[i][k]-EIa[i], 2) for k in range(len(I[i]))]))
            S.append(countS)
        RS = sum([R[i]/S[i] for i in range(len(I))])/len(I)
        return RS

    def Analysis(Data, DataLen):
        Data = Prepare(Data, DataLen)
        Graff = []
        for k in range(len(Data)):
            Graff.append(AnalysisOfSignal(Data[k]))
        return Graff


    def AnalysisOfSignal(eefSignal):
        signalLn = []
        for i in range(1, len(eefSignal)):
            dif = eefSignal[i] / eefSignal[i - 1]
            signalLn.append(math.log(dif))
        rs = []
        x = []
        for n in range(3, len(signalLn)//2):
            x.append(math.log(n))
            rs_n = CountForN(signalLn, n)
            rs.append(math.log(rs_n))
        return [x, rs]

    def HurstExponent(Axis):
        coef = []

        def func(x, c, H):
            return H * x + c

        stopnum = []
        for k in range(len(Axis)):
            i = 20
            step = 10
            perr = [0, 0]
            H = 0.
            while perr[1] < 0.005 and i+step < len(Axis[k][0]):
                X = np.array(Axis[k][0][:i])
                Y = np.array(Axis[k][1][:i])
                popt, pcov = curve_fit(func, X, Y)
                c, H = popt
                perr = np.sqrt(np.diag(pcov))
                i = i+step
            stopnum.append(i)
            coef.append([H, c])
        return coef, stopnum

    def Results(Coef, Result, signal_name,  takeInd, column_names):
        import pandas as pd
        index = [takeInd]
        Result['Signal'][takeInd] = signal_name
        for k in range(len(Coef)):
            Result[column_names[k]][takeInd] = Coef[k][0]
        return Result

    Signal = ReadSignals(FilePath)
    Data = ReadSignals.ReadDocument(Signal)
    column_names = [Data[i][0] for i in range(len(Data))]
    Axis = Analysis(Data, DataLen)
    Coef, stop_num = HurstExponent(Axis)
    Results = Results(Coef, Result, signal_name, takeInd, column_names)

    return Results