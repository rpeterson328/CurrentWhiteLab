import liblytics
import csv
import time
from sets import Set

videoNames = {}
with open("Video Names 3.csv", "rU") as f:
    reader = csv.reader(f)
    for row in reader:
        videoNames[row[0]] = row[1] #cannot remember how this line works exactly
        
usernames = Set()
with open("Names for SPOC.csv", "rb") as f:
	reader = csv.reader(f)
	for row in reader:
		usernames.add(row[3])

data={} #first dict with username (key) : second dict (value)
def parseEventText(eventLine):
	line = eventLine.replace("{","")
	line = line.replace("}","")
	units = line.split(",")
	result = {}
	for unit in units:
		pieces = unit.split(":")
		result[pieces[0].replace('"',"")] = pieces[1].replace('"',"")

	return result


for line in liblytics.read_log_file("tracking_700x_UMass__Fall_2013.log.gz"): #Reads line in log file
	if (line["event_type"] == "play_video"):  # Grabs only play_videos
		username=line["username"]
		t = time.strptime(line['time'].split('+')[0], "%Y-%m-%dT%H:%M:%S.%f") 
		times = time.mktime(t)
		#first loop creates first dict
		if username != "": 
			videoName = parseEventText(line["event"])["id"]
			if username not in data:
				data[username] = {}
			usersDict = data[username]
			#creates third dict with playCount and Times (keys) and their values
			if videoName not in usersDict: #second loop creates third dict
				videoDict = {}
				videoDict["Times"] = []
				videoDict["Playcount"] = 1
				usersDict[videoName] = videoDict
			videoDict = usersDict[videoName]
			videoDict["Times"].append(times)
			videoDict["Playcount"] = len(videoDict["Times"])
			usersDict[videoName] = videoDict
			data[username] = usersDict

#for username in data:
#	for videoName in data[username]:
#		print data[username][videoName]["Playcount"]

f = open("Testing Plays 10.csv", "w")
f.write("username,")
for cleanName in sorted(videoNames):
	f.write(cleanName)
	f.write(",")
f.write(" \n")
##for username in sorted(data):
	##if username in usernames:
for username in sorted(usernames):
	if username in data:
		f.write(username)
		f.write(",")
		for cleanName in sorted(videoNames):
			if videoNames[cleanName] in data[username]:
				f.write(str(data[username][videoNames[cleanName]]["Playcount"]))
				f.write(",")	
			else:
				f.write("0,")
		f.write(" \n")
	
f.close()
