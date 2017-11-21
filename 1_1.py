import json
import math
from collections import Counter
import numpy as np
import os
import time
from sklearn.ensemble import RandomForestClassifier

#Lets measure the time
start = time.time()
#Placeholder for our words
words = set()
#Get all our filenames
filenames =  os.listdir("./full/")
#We need a counter to keep track of the number of articles we have
counter = 0

#Here we loop through our files and create the list of unique words
for filename in filenames:
    #Open file
    with open("./full/"+filename) as f:
        #Load json
        json_content = json.load(f)
        for content in json_content:
            #Check if we want the content
            if "topics" in content and "body" in content:
                #Increment counter
                counter += 1

                #Add words to our set from the body of the article
                for word in content["body"].lower().split() :
                    words.add(word)

#Placeholder for bag of words
word_bag = np.zeros((counter,len(words)), dtype = np.int)

#Placeholder for our results
res = np.zeros(counter, dtype = np.int)
#Counter to keep track of where we are for our result matrix and our bag of words
counter1 = 0

#Here we loop through our files and create the bag of words
for filename in filenames:
    #Open file
    with open("./full/"+filename) as f:
        #Load json
        json_content = json.load(f)
        for content in json_content:
            #Check if we want the content
            if "topics" in content and "body" in content:
                #Get the words in lowercase
                currentWords = content["body"].lower().split()
                #User Counter from collections to count the words
                counter_words = Counter(currentWords)
                #Find the row
                row = [counter_words.get(word, 0) for word in words]
                #Add it to our word_bag
                word_bag[counter1] = row
                #Check if it is a earn topic and add to our results accordingly
                if "earn" in content["topics"]:
                    res[counter1] = 1
                else:
                    res[counter1] = 0
                counter1 += 1

#Print the size of our matrix for the bag of words
print "Size of matrix: " + str(word_bag.shape)


#Use the random tree forest classifier with 50 trees
classifier = RandomForestClassifier(n_estimators=50)
#Train on 80% of the data
classifier = classifier.fit(word_bag[:int(math.floor(0.8*word_bag.shape[0]))], res[:int(math.floor(0.8*len(res)))])

#Print the fraction on how correct it is on the rest of the data
print "Fraction: " + str(classifier.score(word_bag[int(math.floor(0.8*word_bag.shape[0])):], res[int(math.floor(0.8*len(res))):]))

#Print the fraction on how correct it is on the rest of the data
print "Runtime: " + str(time.time() - start)


