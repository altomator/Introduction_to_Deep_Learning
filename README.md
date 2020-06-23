# Introduction to Deep Learning
**Elementary introduction to deep learning through the case of convolutional neural networks (CNN)**

Use case: heritage images classification

# Goals 
Elementary introduction to neural networks and deep learning for non-technical persons in two parts.

## General introduction (60 mn)
This introduction presents the formal neuron model, neural networks and convolutional neural networks.

## Hands-on session (60 m)
The hands-on session is based on [Gallica](https://gallica.bnf.fr/) heritage images, brought into play in an image classification scenario, aiming to deduce the technique or genre of these images (picture, drawing, map...) using a CNN trained model (supervised approach).

![Picture class](https://gallica.bnf.fr/ark:/12148/btv1b53086966b/f1/.thumbnail)
![Drawing class](https://gallica.bnf.fr/ark:/12148/btv1b102201347/f1/.thumbnail)
![Filter class](https://gallica.bnf.fr/ark:/12148/btv1b10027545g/f1/.thumbnail)
![Map class](https://gallica.bnf.fr/ark:/12148/btv1b52504043q/f1/.thumbnail)

Using the Gallica content, the trainees have to:
- select and download images from Gallica and create a training dataset
- train a classification model (with commercial APIs or open source IA frameworks)
- apply the model to Gallica images extracted thanks to Gallica APIs (including IIIF)

# Educational resources

## Introduction to the formal neuron model, neural networks and CNN 
* Theoritical [presentation](https://github.com/altomator/Introduction_to_Deep_Learning/tree/master/ppt) (.ppt, French)

## Hands-on session

This [hands-on session](https://github.com/altomator/Introduction_to_Deep_Learning/blob/master/ppt/atelier-DL.pptx) illustrates a basic images classification use case.

The content to be classified are Gallica images handled thanks to the [IIIF](https://iiif.io/technical-details/) protocol. 
The documents metadata and files are extracted from the Gallica digital repository with the help of [Gallica's APIs](http://api.bnf.fr) and the [PyGallica](https://github.com/ian-nai/PyGallica) Python wrapper for the Gallica's APIs. Then, the image files are processed with a supervised classification approach. The [Wellcome Collection](https://wellcomecollection.org/) digital library is also used.

The session leverages SaS (IBM Watson, Google Cloud Vision) and deep learning platforms (Tensorflow) for the processing.

### Prerequisites
* IBM Watson Studio account or Google Cloud AutoML account for all participants (see the [setup document](https://github.com/altomator/Introduction_to_Deep_Learning/blob/master/ppt/setup_Watson-AutoML.docx))
* Basic scripting and command line skills for participants wishing to go through the Python scripts. 

### Session schedule
1. Use case definition: choice of the source images and the model classes; downloading of the images samples
2. Training with IBM Watson Visual Recognition or Google Cloud AutoML 
3. Test of the model (using IBM Watson/Google Cloud platforms)
4. Local test of the model with Python scripting (IBM Watson case). Launch the notebook with Binder here:
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/altomator/Introduction_to_Deep_Learning/master)
5. *For people with command line skills*: training and test on the same dataset with [TensorFlow Python scripts](https://github.com/altomator/Introduction_to_Deep_Learning/tree/master/classify-with-Tensorflow)

### Resources
* [Tutorial](https://github.com/altomator/Introduction_to_Deep_Learning/tree/master/ppt) (.ppt, French)
* IBM Watson use case: [Python 2 script](https://github.com/altomator/Introduction_to_Deep_Learning/blob/master/binder) for extracting documents from Gallica and inferencing images with IBM Watson + [Jupyter notebook](https://github.com/altomator/Introduction_to_Deep_Learning/tree/master/binder/classify-img-with-iiif-and-watson.ipynb) (English)
* Tensorflow use case: [Python 3 scripts](https://github.com/altomator/Introduction_to_Deep_Learning/tree/master/classify-with-Tensorflow)
* Gallica training [dataset](https://github.com/altomator/Introduction_to_Deep_Learning/tree/master/images) (4 classes, 100 images each)

# Other resources
* [IBM Watson](https://cloud.ibm.com/docs/services/assistant?topic=assistant-getting-started#getting-started) documentation
* [Google AutoML](https://cloud.google.com/vision/automl/docs) documentation
* Convolutional neural networks:
  * https://towardsdatascience.com/simple-introduction-to-convolutional-neural-networks-cdf8d3077bac (EN)
  * https://www.supinfo.com/articles/single/8037-deep-learning-reseau-convolution (FR)
* [Library of Congress Newspaper Navigator](https://github.com/LibraryOfCongress/newspaper-navigator)

