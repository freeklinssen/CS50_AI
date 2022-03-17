I started my experimentation process by rebuilding the neural network
that was used as an example in the lecture. When I did this, at first, the data
was not yet normalized outside the `get_model()` function and achieved therefore only an accuracy around 5%.
I found a way  to normalize the data with the `layers.experimental.preprocessing.Rescaling()` function. This helped a lot,
implementing the same model immediately achieved an accuracy of around 95% when the data was normalized.

I tried to make this already quiet accurate model even better by increasing the number of hidden layers, 
but this did not have a large effect the performance while it increased the number of trainable parameters a lot.
Increasing the number of convolutional and pooling layers did have a positive effect on the accuracy. 
Increasing the number of convolutional and pooling layers to two increased the accuracy to around 97% without too much extra training time.
I also tried three convolutional a and pooling layers but this did not really increase the performance while it took much longer to train this model.

After getting the number of layers right, I tried changing the size of the filters and noticed that 5x5 filters improved the performance by another 1%.
I did not change the size of the pool size for the pooling layers, instead  I tried a smaller strides in order to shrink the picture less per pooling layer,
using `strides = 1` did not improve the performance much, while it took much longer to train this model. This was expected because when the picture is shrunk 
less, there are more trainable parameters especially in the last layers.
At last, I noticed that decreasing the Dropout to 0.30 increased the model a little-bit. 

I choose to Submit this model because I believe it gives the best tradeoff between accuracy and training speed, although other models with more
layers and strides set to 1 where a tiny bit more accurate, they took much longer to train, hence my decision for
this model.