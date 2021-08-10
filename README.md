# mackay_exercise_6_18
Testing out some code for Exercise 6.18 in "Information Theory, Inference, and Learning Algorithms" by David Mackay

Exercise 6.18 asks us to maximize the rate of information transfer where different symbols take different lengths of time to transmit (e.g. symbols 1,2,3,.... cost time l_n = n). But there are different ways to compute an 'average' here. The book maximises the average bit content per symbol divided by the average time per symbol. This is different to maximising the average 'bits per time' across the symbols, which will be different to minimising the average 'time per bit'. Here I've tried maximizing 'bits per time' instead, and will compare performance of my code to the book's solution on simulated data.

Book's choice of function to maximize does do better, as you'd expect. Comments on why that might be are at the bottom of the code.
