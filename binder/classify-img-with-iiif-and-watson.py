"""This Python 3 notebook extracts images of a Gallica document (using the IIIF protocol),
and then applies an IBM Watson classification model to the images

- Extract the document technical image metadata from its IIIF manifest, and then the images
- Classify the images with a Watson Cloud Vision model (the model must be available)

Prerequisites:
- a pretrained Watson Sudio classification model identified with its ID
- a Watson API key"""

import requests
import json
#import pycurl
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
doc_export_factor = 20
# CSV export
output = "OUT_csv"
# get doc_max images
doc_max = 2

# Gallica IIIF base URL
METADATA_BASEURL = 'https://gallica.bnf.fr/iiif/ark:/'
# IBM Watson base URL
WATSON_BASEURL = 'https://gateway.watsonplatform.net/visual-recognition/api/v3/classify?version=2018-03-19'
WATSON_KEY = '2DZdFVOxmhJnQIq3MOQsUOg-7RqARAWa35q-Gh31NnSK'
WATSON_MODEL = 'DefaultCustomModel_1457318034' # classification of images genres : photo, drawing, map, filter class
WATSON_VERSION = (('version', '2018-03-19'),)

#######################
outputDir = os.path.realpath(output)
if not os.path.isdir(outputDir):
	print(f"\n  Output .csv directory {outputDir} does not exist!")
	os.mkdir( outputDir);
else:
	print (f"\n... CSV files will be saved to {outputDir}")

#######################
# Get the document metadata with the Gallica OAI API
# return a dictionary
#xml_dict4doc = Document.OAI(docID)

# Get some metadata
#print (xml_dict4doc['results']['title'])
#print (xml_dict4doc['results']['notice']['record']['metadata']['oai_dc:dc'])

#######################
# Get the document IIIF manifest to have access to the images
req_url = "".join([METADATA_BASEURL, docID, '/manifest.json'])
print ("... getting the IIIF manifest",req_url)
r = requests.get(req_url)
r.raise_for_status()

# we parse the JSON manifest and get a dictionary
json_4img = r.json()
#print (json_4img.keys())
#print json_4img.get('attribution')

# get the sequence of images -> list
sequences = json_4img.get('sequences')
# get the canvas first element of the list. Its a dict
canvas = sequences[0]
#print (canvas.keys())
# parse each canvas data for each image
# each canvas has these keys: [u'height', u'width', u'@type', u'images', u'label', u'@id', u'thumbnail']
urlsIIIF = [] # the array of URLs we're going to build
n_images = 0
print ("... getting image metadata from the IIIF manifest")
for c in canvas.get('canvases'):
    n_images += 1
    print ("    label:",c.get('label')," width:",c.get('width'), " height:",c.get('height'))
    thumbnail = c.get('thumbnail')
    urlThumbnail = thumbnail.get('@id')
    # we build the IIIF URL. We ask for the full image with a size factor of docExportFactor
    urlIIIF = "".join([docID,'/f',str(n_images)]), 'full', "".join(['pct:',str(doc_export_factor)]), '0', 'native', 'jpg'
    urlsIIIF.append(urlIIIF)
    if n_images >= doc_max:
        break
print ("--------------")
print (f"... we get {doc_max} images on {len(canvas.get('canvases'))}\n")



# get the images metadata: alternative with the IIIF info.json for each image
"""for i in range(1, n_images+1):
    #print ("--- getting image metadata from info.json...")
    #xml_dict4img = IIIF.metadata("".join([docID,'/f',str(i)]))
    #print (xml_dict4img)"""

# get the image files #x to #y (we only process y-x images)
"""for i in range(12, 13):
    #print ("--- getting image", i, "...")
    IIIF.iiif("".join([docID,'/f',str(i)]), 'full', "".join(['pct:',str(doc_export_factor)]), '0', 'native', 'jpg')
    if nImages >= docMax:
        break
print ("\n")"""

# loading the images
print ("... now downloading the images")
[IIIF.iiif(u[0],u[1],u[2],u[3],u[4],u[5]) for u in urlsIIIF]
print ("... done")

#######################
# Now we have to call the Watson classification model on the local image files
print ("\n... now infering")

def process_image(file_name):
    # we use the requests package
    files = {
        'images_file': (file_name, open(file_name, 'rb')),
        'classifier_ids': (None, WATSON_MODEL),
    }
    # calling the Watson API
    return requests.post('https://gateway.watsonplatform.net/visual-recognition/api/v3/classify',params=WATSON_VERSION, files=files, auth=('apikey', '2DZdFVOxmhJnQIq3MOQsUOg-7RqARAWa35q-Gh31NnSK'))

def process_json(watson_json):
    images = watson_json.get('images')
    watson_class = images[0].get('classifiers')[0].get('classes')[0].get('class')
    watson_score = images[0].get('classifiers')[0].get('classes')[0].get('score')
    print ("    -> classification:",watson_class)
    print ("    -> confidence score:",watson_score)
    return(watson_class,watson_score)

# writing the results in out_path
out_path = os.path.join(output, "classifications.csv" )
out_file = open(out_path,"w")

# reading the images folder
entries = fnmatch.filter(os.listdir(docID), '*.jpg')
i = 1
for file in entries:
    file_name = "".join([docID,"/",file])
    print ("--- infering image ",file_name," ...")
    # we display the image
    #img = Image.open(file_name)
    #img.show()
    img = Image.open(file_name)
    img.show()
    # calling the Watson API
    watson_json = process_image(file_name).json()
    # Watson returns a JSON with classification and confidence score informations
    #print(json.dumps(json_watson, sort_keys=True, indent=4))
    result = process_json(watson_json)
    predicted_class = result[0]
    predicted_class = predicted_class[:-3]
    # write in file
    print ("%s\t%s" % (file_name,predicted_class.lower()), file=out_file)

print (f"\n ... writing classification data in {output} \n")
out_file.close()
exit(0)
#########################



#########################
# We evaluate the performances relatively to a ground truth
GT_folder = "GT"
labels = []
predictions = []
predictions = []
trues = []

# infering the GT data
folders = fnmatch.filter(os.listdir(GT_folder), '*')
for f in folders:
    folder_name = "".join([GT_folder,"/",f])
    if os.path.isdir(folder_name):
        print ("\n--- GT class ",f," ...")
        labels.append(f)
        images = fnmatch.filter(os.listdir(folder_name), '*.jpg')
        for i in images:
            trues.append(f)
            file_name = "".join([GT_folder,"/",f,"/",i])
            print ("    infering image:",file_name," ...")
            watson_json = process_image(file_name).json()
            result = process_json(watson_json)
            predicted_class = result[0]
            predicted_class = predicted_class[:-3] # remove the "_30" (class names in the Watson model)
            predictions.append(predicted_class.lower())
print ("classes:",labels)
print ("GT:", trues)
print ("predictions:",predictions)

# computing the preformances: confusion matrix, recall, precision
import seaborn
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import f1_score

def plot_confusion_matrix(data, labels, output_filename):
    """Plot confusion matrix using heatmap.

    Args:
        data (list of list): List of lists with confusion matrix data.
        labels (list): Labels which will be plotted across x and y axis.
        output_filename (str): Path to output file.

    """
    seaborn.set(color_codes=True)
    plt.figure(1, figsize=(9, 6))

    plt.title("Confusion Matrix")

    seaborn.set(font_scale=1.4)
    ax = seaborn.heatmap(data, annot=True, cmap="YlGnBu", cbar_kws={'label': 'Scale'})

    ax.set_xticklabels(labels)
    ax.set_yticklabels(labels)

    ax.set(ylabel="True Label", xlabel="Predicted Label")

    plt.savefig(output_filename, bbox_inches='tight', dpi=120)
    plt.close()


# create confusion matrix
matrix = confusion_matrix(trues, predictions, labels=labels)
print (matrix)

# compute the recall score
# https://simonhessner.de/why-are-precision-recall-and-f1-score-equal-when-using-micro-averaging-in-a-multi-class-problem/
# 'micro': Calculate metrics globally by counting the total true positives, false negatives and false positives.
# 'macro': Calculate metrics for each label, and find their unweighted mean. This does not take label imbalance into account.
print ("\nrecall score:", recall_score(trues, predictions, labels=labels, average='micro'))
print ("precision score:", precision_score(trues, predictions, labels=labels, average='micro'))
print ("F1 mesure:", f1_score(trues, predictions, labels=labels, average='micro'))

# draw the matrix
plot_confusion_matrix(matrix, labels, "confusion_matrix.png")
display(Image(filename="confusion_matrix.png"))
exit(0)

#######################
# we can do the same on URL images
print ("***************************")
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
print ("--- infering image ",iiifURL," ...")
img = Image.open(requests.get(iiifURL, stream=True).raw)
img.show()
# call to the Watson API
response = requests.post('https://gateway.watsonplatform.net/visual-recognition/api/v3/classify',params=curlParams, auth=('apikey', WATSON_KEY))
json_watson = response.json()
print(json.dumps(json_watson, sort_keys=True, indent=4))
