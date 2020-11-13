"""This Python 2 notebook extracts images of a Gallica document (using the IIIF protocol), and then applies an IBM Watson classification model to the images

- Extract the document technical image metadata from its IIIF manifest, and then the images
- Classify the images with a Watson Cloud Vision model (the model must be available)

Prerequisites:
- a pretrained Watson Sudio classification model identified with its ID
- a Watson API key"""

import requests
import json
import pycurl
import IPython.display
from PIL import Image

from document_api import Document
#from bs4 import BeautifulSoup
from iiif_api import IIIF
#import xmltodict
import os,fnmatch

# Gallica ARK identifier
docID = '12148/btv1b103365619'
# IIIF export factor (%)
docExportFactor = 25

# Gallica IIIF base URL
METADATA_BASEURL = 'https://gallica.bnf.fr/iiif/ark:/'
# IBM Watson base URL
WATSON_BASEURL = 'https://gateway.watsonplatform.net/visual-recognition/api/v3/classify?version=2018-03-19'
WATSON_KEY = '***'
WATSON_MODEL = 'DefaultCustomModel_1457318034' # classification of images genres : photo, drawing, map, filter class
WATSON_VERSION = (('version', '2018-03-19'),)

#######################
# Get the document metadata with the Gallica OAI API
# return a dictionary
xml_dict4doc = Document.OAI(docID)

# Get some metadata
print xml_dict4doc['results']['title']
print xml_dict4doc['results']['notice']['record']['metadata']['oai_dc:dc']

#######################
# Get the document IIIF manifest to have access to the images
req_url = "".join([METADATA_BASEURL, docID, '/manifest.json'])
print req_url
r = requests.get(req_url)
r.raise_for_status()

# parse the JSON manifest and get a dictionary
json_4img = r.json()
print json_4img.keys()
#print json_4img.get('attribution')

# get the sequence of images -> list
sequences = json_4img.get('sequences')
# get the canvas -> dict
canvas = sequences[0]
#print canvas.keys()
# parse the canvas data for each image
nImages = 0
for c in canvas.get('canvases'):
    print "--- getting image metadata from the IIIF manifest..."
    nImages += 1
    print " label:",c.get('label')," width:",c.get('width'), " height:",c.get('height')
    thumbnail = c.get('thumbnail')
    print " thumbnail: ",thumbnail.get('@id')
print "-------"
print "images:", nImages
print

# get the images metadata: alternative with the IIIF info.json for each image
for i in range(1, nImages+1):
    print "--- getting image metadata from info.json..."
    #xml_dict4img = IIIF.metadata("".join([docID,'/f',str(i)]))
    #print xml_dict4img
print

#######################
# get the image files #12 to #13
# (we only process 2 images)
for i in range(12, 13):
    print "--- getting image", i, "..."
    IIIF.iiif("".join([docID,'/f',str(i)]), 'full', "".join(['pct:',str(docExportFactor)]), '0', 'native', 'jpg')
print

# calling the Watson classification model on the image files
print "***************************"
entries = fnmatch.filter(os.listdir(docID), '*.jpg')
i = 1
for file in entries:
    print "--- infering image ",i," ..."
    fileName = "".join([docID,"/",file])
    #req_url = "".join(["curl -X POST -u 'apikey:",WATSON_KEY,"' -F 'images_file=@",fileName,"' -F 'classifier_ids=",WATSON_MODEL,"' '",WATSON_BASEURL,"'"])
    print(fileName)
    img = Image.open(fileName)
    img.show()
    files = {
        'images_file': (fileName, open(fileName, 'rb')),
        'classifier_ids': (None, WATSON_MODEL),
    }
    # calling the Watson API with requests
    response = requests.post('https://gateway.watsonplatform.net/visual-recognition/api/v3/classify', params=WATSON_VERSION, files=files, auth=('apikey', WATSON_KEY ))
    json_watson = response.json()
    print(json.dumps(json_watson, sort_keys=True, indent=4))

    i +=1
print
print

#images = json_watson.get('images')
#print "-> classification:",images[0].get('classifiers')[0].get('classes')[0].get('class')
#print "-> confidence score:",images[0].get('classifiers')[0].get('classes')[0].get('score')

#if (i-1 != nImages):
    #print " # wrong number of images! #"
    #print " expected: ", nImages," found: ", i
#print

#######################
# same on URL images
print "***************************"
import requests
# Wellcome collection
iiifURL = "https://iiif.wellcomecollection.org/image/L0009407.jpg/1,1,1568,1213/1000,/0/default.jpg"
# Gallica
#iiifURL = "https://gallica.bnf.fr/iiif/ark:/12148/bpt6k4628326j/f1/4317.695641814265,2899.28514719721,1006.9642711679644,774.944853848157/217,167/0/native.jpg"
CURL_URL = (('url', iiifURL),)
WATSON_CLASSIFIER = (('classifier_ids', WATSON_MODEL),)
curlParams = {
        'url': (None, iiifURL),
        'classifier_ids': (None, WATSON_MODEL),
        'version': (None, '2018-03-19')
    }
print "--- infering image ",iiifURL," ..."
img = Image.open(requests.get(iiifURL, stream=True).raw)
img.show()
# call to the Watson API
response = requests.post('https://gateway.watsonplatform.net/visual-recognition/api/v3/classify',params=curlParams, auth=('apikey', WATSON_KEY))
json_watson = response.json()
print(json.dumps(json_watson, sort_keys=True, indent=4))
