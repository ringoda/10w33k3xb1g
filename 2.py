from PIL import Image
import numpy as np
from resizeimage import resizeimage
from os import listdir

#This function takes in an array and compares each value in each row to the next value in that row
# and if the current value is higher then the next value we append true to a list, the list is then
# appended to list of list and when we have gone through all values the method returns an array.
def compare(matrix):
    compare_matrix=[]
    for row in matrix:
        line = []
        for index in range(len(row)-1):
            if row[index] > row[index+1]:
                line.append(True)
            else:
                line.append(False)
        compare_matrix.append(line)
    return np.asarray(compare_matrix)

#This function takes in an array of true and false which is then hexed and the hexed values added
# to a string, when all the values have been hexed and added to the string we have our hash string
# which is then returned.
def hash(compare_matrix):
    hash_string = ''
    for line in compare_matrix:
        decimal_value = 0
        hex_list = []
        for index, value in enumerate(line):
            if value:
                decimal_value += 2**(index % 8)
            if (index % 8) == 7:
                hex_list += hex(decimal_value)[2:].rjust(2, '0')
                hash_string += hex_list[0] + hex_list[1]
                decimal_value = 0
    return hash_string


path = "./pics/"
hash_list = []
#Loop over the pictures in the folder pics
for filename in listdir(path):
    with open(path + filename, 'r+b') as f:
        with Image.open(f) as image:
            #Grey scale the picture
            image = image.convert('L')
            #Resize the picture
            image = resizeimage.resize_cover(image, [9, 8])
            image_matrix = np.asarray( image, dtype="int32" )
    # compare adjacent values
    pic = compare(image_matrix)
    # convert to hash and put into list hashes for all images
    hash_list.append(hash(pic))
print hash_list

