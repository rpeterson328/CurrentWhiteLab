print "Goal: Finding Watchers of Videos"

import csv
from sets import Set
import liblytics

print "Translating video names..."
#read in video list with nice names
videoNames = {}
with open("Video Names 3.csv", "rU") as f:
    reader = csv.reader(f)
    for row in reader:
        videoNames[row[0]] = row[1] #cannot remember how this line works exactly

print "Determing valid usernames..."
#make usernames into a set
usernames = Set()
with open("Names for SPOC.csv", "rb") as f:
    reader = csv.reader(f)
    for row in reader:
        usernames.add(row[3])

print "Putting videos with usernames..."
#add usernames and video ids associated with "play_video" to data
data = {}
for line in liblytics.read_log_file("tracking_700x_UMass__Fall_2013.log.gz"):
    if line["event_type"] == "play_video":
        username = line["username"]
        if (username != ""):
            if username not in data:
                data[username] = Set()
            event = line["event"]
            if not isinstance(event, dict):
                try:
                    event = eval(event)
                except (NameError):
                    event = event.replace("null", "0")
                    event = eval(event)
            data[username].add(event["id"])

print "Determining who watched what..."
#writing to a new csv file
#determining if a video has been watched by a user
f = open("Testing Counting.csv", "w")
f.write("username,")
for cleanName in sorted(videoNames):
    f.write (cleanName)
    f.write (",")
f.write (" \n")
for username in sorted(data):
    if username in usernames:
        f.write (username)
        f.write (",")
        for cleanName in sorted(videoNames):
        	if videoNames[cleanName] in data[username]:
        		playcount = 0
        	for videoNames[cleanName] in data[username]:
        		print playcount
        		#playCount = playcount + 1
        		#f.write (str(playCount))
        	#f.write (",")
        #f.write (" \n")
#f.close()


print "All Done! Open your file."
