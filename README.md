# photomath-lite
(lite == very very very lite :) )

A very simple math expression solver which takes hand-written expression as input, attempts to recognize the characters and returns the calculated result. Created as a personal project following the specifications of [this assignment](https://github.com/photomath/ml-assignments/blob/main/assignment-A.pdf).

## Usage instructions
Try it out: [click here](https://muffinlime.eu.pythonanywhere.com)

For the software to work:
* photo should contain **only** the white-ish background (no lines) and the expression
* photo should be correctly rotated
* the expression should be written with a dark marker (pen most likely won't work)
* digits should be "MNIST pretty" (check the sample photos)
* the lighting should be somewhat even across the photo

## Sample input photos
![alt text](https://i.imgur.com/YnlktUA.jpeg "Sample photo 1")

![alt text](https://i.imgur.com/q8oWWyX.jpeg "Sample photo 2")

![alt text](https://i.imgur.com/bQcLUzZ.jpeg "Sample photo 3")

## Metrics and real-world performance
As requested in the assignment, the metrics I found important are model accuracy and average inference time. 

Accuracy on a test set consisting of MNIST and hand-written symbols: ~99.5%

Inference time:
* ~5.5s on base Apple M1 chip
* ~15s on pythonanywhere's servers (where the app is hosted)

Is this good enough? Well no, not really, who'd want to wait 15 seconds for a solution. If my memory serves me correctly, the author of this assignment said that taking it below 0.3s presents no added value to the user, so only 14.7s to go :) ([source](https://www.youtube.com/watch?v=bR-9LM30RUw)). Since the inputs are expected to be pretty, it would make sense to choose a lot simpler model and sacrifice some of the accuracy on the (not so pretty) MNIST instances to reduce inference time. Also, I imagine it would work a lot faster on Google Cloud but for some reason they wouldn't accept my CC info so I couldn't test it.

How could inference time be improved?
* use a simpler model
* reduce or change the preprocessing steps
* implement a more efficient solving algorithm
* run it on a faster machine, but that is obvious

Other things that could be improved:
* better preprocessing steps that would allow the software to work on a wider range of photos
* a model trained on a more relevant dataset

## How it works
A short description of how each component works, check the code for details.
### Localization
Takes the photo as input and returns an array of cropped character photos. Preprocessing for contour extraction includes converting to grayscale, adjusting the brightness and contrast, blurring the photo and finally thresholding. External contours are extracted from the thresholded photo and sorted by their left-most coordinate (arranged from left to right). A median contour area is calculated and contours whose areas are below 10% of the median are discarded. This is a very simple attempt at waste clearing.

### Recognition
Takes the array of localized character images as input and returns an array of predictions. Each character image is again preprocessed by resizing it to 20x20 while preserving ratio, and then padded with zeros for a final size of 28x28. The training dataset was processed the same way. The model then predicts the label of each image, which is in turn decoded and saved.
#### Training data
The model was trained on a slightly modified MNIST dataset. Each MNIST character was re-centered by it's arithmetic center (w/2, h/2). In the original MNIST dataset, characters are centered by their center of mass ([more details here](http://yann.lecun.com/exdb/mnist/)). The dataset was completed by 10 unique hand-written instances of [+, -, x, /, (, )], of which each is multiplied 600 times, totaling 6000 images per character. (A rather low sample size of only 10 unique instances but it seemed to work fairly well so I decided it was good enough).
#### Model architecture
Performs rather well on the original MNIST dataset, and it did so here as well.

![alt text](https://i.imgur.com/awGAow7.png "Model architecture")

### Solver
Takes the array of predicted expression characters as input and calculates the result. Returns both the expression and the result. First it merges the adjacent digits and converts them to integers while converting subtraction to addition of negative numbers. Then it goes through a recursive algorithm looking for parentheses and sending the inner-most (mini) expressions to the solver which just loops through them doing the multiplication and division operations first and the addition and subtraction second.

## What if I get an error?
Well, either the localization algorithm failed to localize correctly which in turn broke the recognition algorithm which in turn broke the solving algorithm or it localized correctly but the recognition algorithm failed (for instance predicting 7 as /) which broke the solving algorithm as well.
