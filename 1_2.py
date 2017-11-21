import json
import math
from collections import Counter
import os
import time
from sklearn.ensemble import RandomForestClassifier

#Lets measure the time
start = time.time()

#Placeholder for result
res = []
#Placeholder for the matrix
matrix = []

#Get all our filenames
filenames = os.listdir("./full/")

#Here we loop through our files and hash the words
for filename in filenames:
    #Open file
    with open("./full/"+filename) as f:
        #Load json
        json_content = json.load(f)
        
        for content in json_content:
            #Check if we want the content
            if "topics" in content and "body" in content:
                r = [0] * 1000

                #The actual hashing
                for w in content["body"].lower().split():
                    token = hash(w)%1000
                    r[token] += 1
                
                #Append it to our matrix
                matrix.append(r)
                
                #Check if it is a earn topic and add to our results accordingly
                if "earn" in content["topics"]:
                    res.append(1)
                else:
                    res.append(0)


#Use the random tree forest classifier with 50 trees
classifier = RandomForestClassifier(n_estimators=50)
#Train on 80% of the data
classifier = classifier.fit(matrix[:int(math.floor(0.8*len(matrix)))], res[:int(math.floor(0.8*len(res)))])

#Print the fraction on how correct it is on the rest of the data
print "Fraction: " + str(classifier.score(matrix[int(math.floor(0.8*len(matrix))):], res[int(math.floor(0.8*len(res))):]))

#Print the runtime
print "Runtime: " + str(time.time() - start)
