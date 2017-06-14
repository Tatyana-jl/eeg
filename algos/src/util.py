def format_df_to_dictlist(data_frame):
    dictlist = []
    for i in data_frame.index:
        dct = {}
        dct['s_name'] = data_frame['Signal'][i]
        dct['categories'] = list(data_frame.columns[1:])
        val_all = []
        k = 1
        for col in dct['categories']:
            if col != 'Signal':
                val_all.append([k, data_frame[col][i]])
                k += 1
                dct['values'] = val_all
        dictlist.append(dct)
    return dictlist