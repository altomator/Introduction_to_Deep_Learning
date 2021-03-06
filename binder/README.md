## Image genres classification with IBM Watson Studio and Python

This [Jupyter notebook](https://github.com/altomator/Introduction_to_Deep_Learning/blob/master/binder/classify-img-with-iiif-and-watson.ipynb) extracts images from the Gallica and Welcome Collection digital libraries using the IIIF protocol. 
Then it inferes image genre classification  thanks to an existing Watson Studio/Visual Recognition classification model.

After the inference is done, a formal evaluation is done.

![Confusion matrix](https://github.com/altomator/Introduction_to_Deep_Learning/blob/master/images/confusion_matrix.png)

The notebook can be launched in your browser with [Binder](https://mybinder.org/v2/gh/altomator/Introduction_to_Deep_Learning/HEAD?filepath=https%3A%2F%2Fgithub.com%2Faltomator%2FIntroduction_to_Deep_Learning%2Fblob%2Fmaster%2Fbinder%2Fclassify-img-with-iiif-and-watson.ipynb).

*Prerequisites*:
- a pretrained Watson Sudio classification model identified with its ID,
- a Watson API key.

Look at the [tutorials](https://github.com/altomator/Introduction_to_Deep_Learning/tree/master/ppt) to learn how to proceed with Watson Studio.



