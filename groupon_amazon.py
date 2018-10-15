#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import re
import os

#run delimiter normalization process which makes the file readable and orderly
os.system('''perl -lpe 's/"/""/g; s/^|$/"/g; s/\t/","/g' < AmazonCategories_2018-10-01.csv  > groupon_amazon_fullsample_2018-10-01.csv''')

#open blosm file and reference file where blosm file contains the super majority of deliverable data and the reference file contains the groupon categories needed for output file

blosm_file = pd.read_csv(u"groupon_amazon_fullsample_2018-10-01.csv", low_memory=False, encoding='latin-1')

reference_file = pd.read_csv(u"referencefile_groupon_amazon.csv", encoding='latin-1')

#strip carriage return from blosm file

blosm_file['shelf_url'] = pd.DataFrame({'shelf_url': [i.strip() for i in blosm_file['shelf_url\r']]})
del blosm_file['shelf_url\r']

#clean blosm file merge column

blosm_file['shelf_url'] = blosm_file['shelf_url'].str.split('&page').str[0]

#merge files

ndf = pd.merge(blosm_file, reference_file, on='shelf_url', how='inner')

#assign and rename columns

ndf['week'] = '10/01/2018'

ndf.rename(columns={
	'skuid':'asin',
	'GRT L1':'groupon_l1',
	'GRT L2':'groupon_l2',
	'GRT L3':'groupon_l3',
	'GRT L4':'groupon_l4',
	'Groupon PDS':'groupon_pds'}, inplace=True)

header = [
	"week",
	"product_title",
	"seller_name",
	"brand",
	"breadcrumb",
	"groupon_l1",
	"groupon_l2",
	"groupon_l3",
	"groupon_l4",
	"groupon_pds",
	"shelf_rank",
	"shelf_url",
	"current_price",
	"number_of_reviews",
	"product_rating",
	"asin",
	"imageurl",
	"product_url"
	]

ndf.to_csv("2018-10-01_Amazon.csv", columns=header, index=False)
