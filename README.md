# Instagram-Captioning
 Run Instagram photos through a pytorch neural network for captioning and compare the result to the captions given.
 
 Models are pretrained and can be found at https://github.com/yunjey/pytorch-tutorial/tree/master/tutorials/03-advanced/image_captioning.
 
 The model files themselves are not included but they can be downloaded from the link above.

This is an example of the output run on the Instagram profile "Photos":

![Alt text](captions.png)

As you can see, the captioning does not work for certain pictures, usually ones that are just pictures of scenery without a defined subject or selfies.

In order to run on your machine:

1. Clone the repo
2. Download the models from https://www.dropbox.com/s/ne0ixz5d58ccbbz/pretrained_model.zip?dl=0 and place them into /models
3. Run captionIG.py with **python captionIG.py --user_name=[Instagram Username] --output_path=[path to output image]**
