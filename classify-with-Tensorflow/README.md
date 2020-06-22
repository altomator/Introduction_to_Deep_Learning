[Inception-v3](https://www.tensorflow.org/tutorials/image_recognition) model (Google's convolutional neural network, CNN) has been retrained on a multiclass ground truth datasets (photos, drawings, maps, music scores, comics... 12k images). Three Python scripts (within the Tensorflow framework) are used to train (and evaluate) a model:
- split.py: the GT dataset is splited in a training set (e.g. 2/3) and an evaluation set (1/3). The GT dataset path and the training/evaluation ratio must be defined in the script.
- retrain.py: the training set is used to train the last layer of the Inception-v3 model. The training dataset path and the generated model path must be defined.
- label_image.py: the evaluation set is labeled by the model. The model path and the input images path must be defined.

>python3 split.py 

>python3 retrain.py 

>python3 label_image.py 

To classify a set of images, the following steps must be chained:

1. Extract the image files from a documents metadata folder thanks to the IIIF protocol:
>perl toolbox.pl -extr IN_md

Mind to set a reduction factor in the "facteurIIIF" parameter (eg: `$factIIIF`=50) as the CNN resizes all images to a 299x299 matrix.

2. Move the OUT_img folder to a place where it will be found by the next script.

3. Classify the images with the CNN trained model:
>python3 label_image.py > data.csv

This will output a line per classified image:

```csv
bd	carte	dessin	filtrecouv	filtretxt	gravure	photo	foundClass	realClass	success	imgTest
0.01	0.00	0.96	0.00	0.00	0.03	0.00	dessin	OUT_img	0	./imInput/OUT_img/btv1b10100491m-1-1.jpg
0.09	0.10	0.34	0.03	0.01	0.40	0.03	gravure	OUT_img	0	./imInput/OUT_img/btv1b10100495d-1-1.jpg
...
```

Each line describes the best classified class (according to its probability) and also the probability for all the other classes.
