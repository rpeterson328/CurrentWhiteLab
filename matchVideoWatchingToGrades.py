import csv
from sets import Set
import liblytics

#read in data of who watched what video
data = {}
with open("Video Data for Analysis.csv", "rU") as f:
    reader = csv.reader(f)
    next(reader, None)
    for row in reader:
        username = row[0]
        percentWatched = float(row[131])
        percentWatched = percentWatched * 100
        data[username] = percentWatched
print data

#make grades into a dict
grades = {}
with open("F13 Spoc and Grades - exam total.csv", "rb") as f:
    reader = csv.reader(f)
    next(reader, None)
    for row in reader:
        username = row[0]
        grade = float(row[19])
        grades[username] = grade

#writing to a new csv file
#getting rid of the SPOC username from the data
f = open("Testing Grade Match 2.csv", "w")
f.write("percent watched,")
f.write("grade, \n")
for username in sorted(grades):
    if username in data.keys():
        s = "%f,%f\n" % (data[username], grades[username])
        f.write (s)
f.close()

