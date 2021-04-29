from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.views.generic import DetailView
from lxml.html import fromstring
import logging
from . import models
from dormanproject.dormanproject.crawl import crawl

import pandas as pd
import glob
import json
import os
import xlrd


class ScraperView(DetailView):
    template_name = 'scraper/show_result.html'

    def get(self, request, *args, **kwargs):
        global flag_stop
        flag_stop = False
        files = list(filter(os.path.isfile, glob.glob("static/result/*.xlsx")))
        files.sort(key=lambda x: os.path.getatime(x), reverse=True)
        files = [os.path.basename(file) for file in files]
        return render(request, self.template_name, {
            'search': '',
            'files': files,
        })


    def post(self, request):
        final_postings = []
        list4 = []
        if request.POST.get('ckb_site4') == 'on' and flag_stop is False:
            if request.method == 'POST' and request.FILES:
                list4 = scrapesearch(request)
        final_postings.append(list4)


def scrapesearch(request):
    output_filename = "static/result/dorman_output"
    if request.POST.get('ckb_autonew') == 'on':
        fileIndex = 1
        fname = output_filename
        while os.path.isfile(fname + ".xlsx") == True:
            fname = "%s_%06d" % (output_filename, fileIndex)
            fileIndex = fileIndex + 1
        output_filename = fname
    final_postings = []
    if request.method == 'POST' and request.FILES:
        input4 = request.FILES['input_file']
        fs = FileSystemStorage("upload_dorman/")
        filename = fs.save(input4.name, input4)
        uploaded_file = fs.path(filename)
        print(uploaded_file)
    else:
        return final_postings
    df = pd.read_excel(uploaded_file, usecols='A')
    codelist = df['Compressed Old number'].to_list()
    print(codelist)
    event = codelist
    scrape(event,output=output_filename)


def scrape(event={}, context={},output=None):
    crawl(event,output)
