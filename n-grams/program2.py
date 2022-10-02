#Arjun Venkat - asv180003
#Arjun Balasubramanian - axb200075 

import nltk
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
import pickle


def getPreds(filename, outputfile):
    
    ## 2.a
    ## unpickle the dictionaries and load them in
    uni_eng = pickle.load(open('uni_eng.p', 'rb'))
    bi_eng = pickle.load(open('bi_eng.p', 'rb'))
    uni_fr = pickle.load(open('uni_fr.p', 'rb'))
    bi_fr = pickle.load(open('bi_fr.p', 'rb'))
    uni_it = pickle.load(open('uni_it.p', 'rb'))
    bi_it = pickle.load(open('bi_it.p', 'rb'))
    
    ## 2.b
    f = open(filename, 'r', encoding = 'utf-8') ## open the file with t
    line = f.readline() ## read the first line
    preds = [] ## list to hold the predictions
    while(line): ## go by line to predict
        
        uni = word_tokenize(line) ## tokenize the line 
        bi = list(ngrams(uni, 2))  ## get the bigrams from the line
        
        ## initialize the laplace values
        laplace_eng = 1
        laplace_fr = 1
        laplace_it = 1
        
        for bigram in bi: ## go through the bigrams in the line
            
            
            b_eng = bi_eng[bigram] if bigram in bi_eng else 0 ## get the number of bigram occurrences in the training
            u_eng = uni_eng[bigram[0]] if bigram[0] in uni_eng else 0 ## get the number of unigram occurrences in the training
            v_eng  =  len(uni_eng) ## get the size of the vocab
            
            b_fr = bi_fr[bigram] if bigram in bi_fr else 0 ## get the number of bigram occurences in the training
            u_fr = uni_fr[bigram[0]] if bigram[0] in uni_fr else 0 ## get the number of unigram occurrences in the training
            v_fr  =  len(uni_fr) ## get the size of the vocab
            
            b_it = bi_it[bigram] if bigram in bi_it else 0 ## get the number of bigram occurences in the training
            u_it = uni_it[bigram[0]] if bigram[0] in uni_it else 0 ## get the number of unigram occurrences in the training
            v_it  =  len(uni_it) ## get the size of the vocab
            
            ## Use the laplace equation to update the value based on the current bigram
            laplace_eng = laplace_eng * ((b_eng + 1) / (u_eng + v_eng))
            laplace_fr = laplace_fr * ((b_fr + 1) / (u_fr + v_fr))
            laplace_it = laplace_it * ((b_it + 1) / (u_it + v_it))

        ## Find the highest probability language based on the laplace value for each language
        if(laplace_eng > laplace_fr and laplace_eng > laplace_it):
            preds.append("English") ## append the predicition to the list
        elif (laplace_fr > laplace_it):
            preds.append("French") ## append the predicition to the list
        else:
            preds.append("Italian") ## append the predicition to the list
        
        line = f.readline() ## go to the next line
    f.close() ## close the file
    
    f = open(outputfile, 'w') ## open the output file
    
    for i in range(len(preds)): ## iterate through the predictions
        line = str(i + 1) + ' ' + preds[i] + '\n' ## create the string
        f.write(line) ## write the line to the file
        
    f.close() ## close the file
    
        
    return(preds) ## return the predictions
    
    
## 2.b
def getAccuracy(preds, filename): 
    
    f = open(filename, 'r', encoding = 'utf-8') ## open the actual language file
    actual = f.read() ## read all the data
    actual = ''.join([i for i in actual if not i.isdigit()]) ## remove the digits
    actual = actual.replace(' ', '').split('\n') ## remove the spaces and make it a list for easy comparison
    
    correct = 0 ## count the correct predictions
    incorrect = [] ## keep track of the incorrect line numbers
    for i in range(len(preds)): ## iterate through the predictions
        if preds[i] == actual[i]: ## check if pred = actual
            correct = correct + 1 ## add 1 to correct if pred == actual
        else:
            incorrect.append(i + 1) ## else add the line to the incorrect lines
            
    accuracy = correct/len(preds) ## calculate the accuracy

    return accuracy, incorrect ## return the accuracy and the incorrect lines

if __name__ == '__main__':
    preds = getPreds('ngram_files/LangId.test', 'output.txt') ## get the prediction and write them
    accuracy, incorrect = getAccuracy(preds, 'ngram_files/LangId.sol') ## get the accuracy and incorrect lines
    ## 2.c
    print("The accuracy we get is " + str(accuracy)) ## outpt the accuracy
    print("We have incorrect classifications on the following lines :") ## output the incorrect lines
    for i in incorrect:
        print(i)