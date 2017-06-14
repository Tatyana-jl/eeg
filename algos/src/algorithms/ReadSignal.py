class ReadSignals(object):

    def __init__(self, filepath):
        self.__filepath=filepath

    def ReadDocument(self):

        import xlrd
        rb = xlrd.open_workbook(self.__filepath)
        sheet = rb.sheet_by_index(0)
        Data = [sheet.col_values(i) for i in range(sheet.ncols)]

        return Data

