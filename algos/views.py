# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from eeg.settings import BASE_DIR
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http.response import JsonResponse
from .src.loader import Loader
from .src.algorithms import HurstExp
from .src.algorithms import CrossTable
from .src.algorithms import Fractal
from .src.algorithms import LogMap
from .src.algorithms import LZW
from .src.algorithms import PrepareTable
from .src.algorithms import Sep
from .src.util import format_df_to_dictlist
from .src.forms import SForm
import collections


# Create your views here.


def index(request):
    context = {}
    # if this is a POST request we need to process the form data

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            # getting form data
            s_names = []
            s_len = int(form.cleaned_data['s_len'])

            algos = request.POST.getlist('algos[]')
            algos = [int(algos[i]) for i in range(len(algos))]

            # handling file upload
            files = list()
            f_uploaded = request.FILES.getlist('file')
            for f in f_uploaded:
                s_names.append(Sep.separate(f.name, '.')[0])
                f_name = Loader.handle_loaded(f)
                files.append(f_name)
            context['s_names'] = s_names
            s_numb = len(s_names)
            result = PrepareTable.ResultTable(files[0], s_numb)

            for alg_id in algos:
                if alg_id is 1:
                    ResultHurst = result
                    for k in range(len(files)):
                        ResultHurst = HurstExp.Hurst(files[k], s_names[k], s_len, k + 1, ResultHurst)
                    context['ResultHurst_table'] = ResultHurst.to_html(float_format=lambda x: "%.3f" % x)
                    hurst_dictlist = format_df_to_dictlist(ResultHurst)
                    context['hurst_dictlist'] = hurst_dictlist
                    hurst = {a: [] for a in ResultHurst.columns if a != 'Signal'}
                    for col in ResultHurst.columns:
                        if col != 'Signal':
                            for i in ResultHurst.index:
                                hurst[col].append(ResultHurst[col][i])
                    context['hurst_graph_dict'] = hurst

                elif alg_id is 2:
                    LogR = []
                    for k in range(len(files)):
                        LogR.append(LogMap.LogRefl(files[k], s_len))
                    context['s_categories'] = list(result.columns)[1:]
                    context['LogR'] = LogR

                elif alg_id is 3:
                    ResultFractal = result
                    for k in range(len(files)):
                        ResultFractal = Fractal.FractalDimension(files[k], s_names[k], s_len, k+1, ResultFractal)
                    context['ResultFractal_table'] = ResultFractal.to_html(float_format=lambda x: "%.3f" % x)
                    fractal_dictlist = format_df_to_dictlist(ResultFractal)
                    context['fractal_dictlist'] = fractal_dictlist
                    fractal_graph_dict = {a: [] for a in ResultFractal.columns if a != 'Signal'}
                    for col in ResultFractal.columns:
                        if col != 'Signal':
                            for i in ResultFractal.index:
                                fractal_graph_dict[col].append(ResultFractal[col][i])

                    context['fractal_graph_dict'] = fractal_graph_dict

                elif alg_id is 4:
                    ResultCross = result
                    for k in range(len(files)):
                        ResultCross = CrossTable.CrossT(files[k], s_names[k], s_len, k + 1, ResultCross)
                    context['ResultCross_table'] = ResultCross.to_html(float_format=lambda x: "%.3f" % x)
                    cross_dictlist = format_df_to_dictlist(ResultCross)
                    context['cross_dictlist'] = cross_dictlist
                    cross = {a: [] for a in ResultCross.columns if a != 'Signal'}
                    for col in ResultCross.columns:
                        if col != 'Signal':
                            for i in ResultCross.index:
                                cross[col].append(ResultCross[col][i])
                    context['cross_graph_dict'] = cross


                elif alg_id is 5:
                    ResultLZW = result
                    for k in range(len(files)):
                        ResultLZW = LZW.LZWcompl(files[k], s_names[k], s_len, k + 1, ResultLZW)
                    context['ResultLZW_table'] = ResultLZW.to_html(float_format=lambda x: "%.3f" % x)
                    lzw_dictlist = format_df_to_dictlist(ResultLZW)
                    context['lzw_dictlist'] = lzw_dictlist
                    lzw = {a: [] for a in ResultLZW.columns if a != 'Signal'}
                    for col in ResultLZW.columns:
                        if col != 'Signal':
                            for i in ResultLZW.index:
                                lzw[col].append(ResultLZW[col][i])
                    context['lzw_graph_dict'] = lzw

            html = render_to_string('algos/_results.html', context)
            return JsonResponse({'success': True, 'html': html})
        else:
            raise Exception(form.errors)
            # return render(request, 'algos/index.html', context)
    else:
        form = SForm()
    context['form'] = form
    return render(request, 'algos/index.html', context)


def test(request):
    # file = loader.load_file()
    f = BASE_DIR + '/algos/files/ictal1.xlsx'
    files = list()
    files.append(f)

    signalNames = 'ictal'
    DataLen = 550
    signal_name = Sep.separate(signalNames, ',')
    numOfSignals = len(signal_name)

    iterable_list = [i for i in range(1,numOfSignals+1)]

    if numOfSignals != len(files):
        raise Exception('len of files array and number of signal names should be equal')

    result = PrepareTable.ResultTable(files[0], numOfSignals)
    ResultHurst = result
    ResultFractal = result
    ResultCross = result
    ResultLZW = result
    LogR = []

    for k in range(len(files)):
        ResultHurst = HurstExp.Hurst(files[k], signal_name[k], DataLen, k+1, ResultHurst)
        # ResultFractal = Fractal.FractalDimension(files[k], signal_name[k], DataLen, k+1, ResultFractal)
        ResultCross = CrossTable.CrossT(files[k], signal_name[k], DataLen, k+1, ResultCross)
        ResultLZW = LZW.LZWcompl(files[k], signal_name[k], DataLen, k+1, ResultLZW)
        LogR.append(LogMap.LogRefl(files[k], DataLen))
        # raise Exception(ResultHurst)
    context = {'ResultHurst': ResultHurst.to_html(float_format=lambda x: "%.3f" % x)}
               # 'ResultFractal': ResultFractal,
               # 'ResultCross': ResultCross,
               # 'ResultLZW': ResultLZW,
               # 'LogR': LogR}
    return render(request, 'algos/test.html', context)