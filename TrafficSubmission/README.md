Originally I first tried to implement the model using just one layer dense layer and one convolution layer.
This worked well for a smaller dataset. I also used fewer neurons in each layer and only one pooling / convolution.
However, when I tried the larger dataset my neural network failed to accuractely train and went from having an accuracy of
close to 98% to know around 5%. I attributed this to the fact that I needed more convolution layers to learn the more features
I would see when classifying 48 road signs as opposed to 3 road signs. I also created layers in such a way that the first layer
had the least amount of filters so it can sort things like lines, curves, and then build on top of these features. Each following
layer would have more features to capture the finer details in the pictures before I finally consolidated everything into 43 bins
and gave each a probability distribution using the softmax function. After using 3 convolution layers and 1 dense layer I was able to get my accuracy back to 98.5%.
