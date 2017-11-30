In this project we made a solver to the Hangman game in which we are supposed to guess the alphabets of a word, in less than
a few tries, after which you lose. 

We initially preprocess the data and then later for the initial guessing, we used the frequency based decision tree, which 
guesses the next letter based on the conditional probability of all the characters, given the guessed and marked characters.

Then we use the ngram based language modelling, to learn from the bigrams, trigrams, quad grams and pent grams and weight 
them accordingly.

How to run : 

train file consists of the training words from the language, in which you want to play hangman. This is generic, so not just for 
english, but plug the dictionary of any language and it will learn the language model from it.

test file consists of test words, which the solver replaces with all blanks and starts trying to guess the word in less
than a few failures. 


Replace the above two files with the files of your choice and run "make", to get the results of the word and character level 
predictions.

Results on the given training and test file : 
The mean lavenshtein's distane is ~ 0.70, i.e mean failure(edit distance) per word is 0.7 characters.