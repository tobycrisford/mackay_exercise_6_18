# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 15:20:19 2021

@author: tobycrisford

Exercise 6.18 asks us to maximize the rate of information transfer where
different symbols take different lengths of time to transmit
(e.g. symbols 1,2,3,.... cost time l_n = n).

But there are different ways to compute an 'average' here. The book maximises
the average bit content per symbol divided by the average time per symbol.

This is different to maximising the average 'bits per time' across the symbols,
which will be different to minimising the average 'time per bit'.
Here I've tried maximizing 'bits per time' instead, and will
compare performance of my code to the book's solution on simulated data.

"""
import numpy as np

#Compute expected bits per second on a single symbol of my solution
#Compares to 1 bit per second of book's solution

n = np.array([i for i in range(1,10000)])
an = 0.5 * ((2/3)**n) * (np.log(3) / np.log(2) - 1 + (1/n))
print("Expected bits per second on each symbol:")
print(np.sum(an))

#Huffman coding algorithm
#Use to map planned symbol probabilities to bit strings
#such that bit strings are close to random

def huffman(probs):
    if len(probs) == 2:
        return [[True], [False]]
    order = np.argsort(probs)
    new_probs = np.concatenate((probs[np.logical_and(order != 0, order != 1)],
                                [probs[order[0]] + probs[order[1]]]))
    coding = huffman(new_probs)
    a = min(order[0], order[1])
    b = max(order[0], order[1])
    coding = coding[0:a] + [coding[len(coding)-1] + [True]] + coding[a:(b-1)] + [coding[len(coding) - 1] + [False]] + coding[(b-1):(len(coding)-1)]
    return coding
    

#data structure for huffman decoding
class Huffman_tree:
    tree_left = None
    tree_right = None
    symbol = None
    
    
    def add(self, code, symbol):
        if len(code) == 0:
            self.symbol = symbol
        else:
            if code[0]:
                if self.tree_left is None:
                    self.tree_left = Huffman_tree()
                self.tree_left.add(code[1:len(code)], symbol)
            else:
                if self.tree_right is None:
                    self.tree_right = Huffman_tree()
                self.tree_right.add(code[1:len(code)], symbol)
    
    def decode(self, code):
        if len(code) == 0:
            return [self.symbol, code]
        else:
            if code[0]:
                if self.tree_left is None:
                    return [self.symbol, code]
                return self.tree_left.decode(code[1:len(code)])
            else:
                if self.tree_right is None:
                    return [self.symbol, code]
                return self.tree_right.decode(code[1:len(code)])
            


#Test the above on (a,0.25), (b,0.25), (c,0.2), (d,0.15), (e, 0.15)

symbols = ['a','b','c','d','e']
huffman_code = huffman(np.array([0.25,0.25,0.2,0.15,0.15]))
huffman_tree = Huffman_tree()
for i in range(0, len(huffman_code)):
    huffman_tree.add(huffman_code[i], symbols[i])
plain_sequence = ['a', 'e', 'b','b','d','c','e','a']
print("Plain sequence:")
print(plain_sequence)
code_sequence = []
for p in plain_sequence:
    code_sequence = code_sequence + huffman_code[np.where(np.array(symbols) == p)[0][0]]
print("Huffman code:")
print(code_sequence)
decode_sequence = []
while len(code_sequence) > 0:
    decode_out = huffman_tree.decode(code_sequence)
    decode_sequence = decode_sequence + [decode_out[0]]
    code_sequence = decode_out[1]
print("Decoded sequence:")
print(decode_sequence)



#Now test the performance of book's solution on encoding random bits, 
#vs alternative. Will fix time, and see how many bits we can transmit in
#fixed time. Generate 1000 random bits, and allow only 500 seconds to transmit.
#Expected performance of book solution: 500 bits transmitted

def solution_test(bits, n_seconds, probs):
    
    huffman_code = huffman(probs)
    huffman_tree = Huffman_tree()
    for i in range(0, len(huffman_code)):
        huffman_tree.add(huffman_code[i], i+1)
        
    encoded_sequence = []
    working_bits = np.copy(bits)
    while len(working_bits) > 0:
        encode_out = huffman_tree.decode(working_bits)
        encoded_sequence = encoded_sequence + [encode_out[0]]
        working_bits = encode_out[1]
    
    score = 0
    timecount = 0
    bitcount = 0
    for i in range(0, len(encoded_sequence)):
        timecount = timecount + encoded_sequence[i]
        if timecount > n_seconds:
            score = bitcount
            break
        bitcount = bitcount + len(huffman_code[encoded_sequence[i] - 1])
    return [encoded_sequence, score]

random_bits = np.random.rand(10000) >= 0.5

probs_book_raw = 2**(-np.array([i for i in range(1,101)], dtype=float))
probs_book = probs_book_raw / np.sum(probs_book_raw)

probs_me_raw = 0.5 * (2/3)**(np.array([i for i in range(1,101)], dtype=float))
probs_me = probs_me_raw / np.sum(probs_me_raw)

encoded_book = solution_test(random_bits, 500, probs_book)
encoded_me = solution_test(random_bits, 500, probs_me)

print("Book score:")
print(encoded_book[1])
print("My score:")
print(encoded_me[1])

#Book does better! So book average does make most sense.

"""
Why is this?
Think it's to do with going from average over a symbol to average over
a long sequence of symbols. Calculating average quantities *per symbol* means
you can just add them up over a long sequence, by linearity of expectation.
But averaging 'bits per second' over a symbol can't then be aggregated up to
give you the average 'bits per second' on a long string.

Nevertheless book's definition of information transfer rate is not going to
quite equal what you'd get if you calculated the rate on lots of different trials
for fixed number of symbols, and computed an average
(average of ratio =/= to ratio of averages, in general).
Although in this example, bit content of each symbol is mathematically equal
to its length, so is a special case where this does actually hold.
"""