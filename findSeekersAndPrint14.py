print "Goal: Finding Seekers"import csvfrom sets import Setimport liblyticsprint "Translating video names..."#read in video list with nice namesvideoNames = {}with open("Video Names F14 2.csv", "rU") as f:    reader = csv.reader(f)    for row in reader:        videoNames[row[0]] = row[1] #cannot remember how this line works exactlyprint "Determing valid usernames..."#make usernames into a setusernames = Set()with open("SPOC Grades Edited.csv", "rb") as f:    reader = csv.reader(f)    for row in reader:        usernames.add(row[1])print "Putting videos with usernames..."#add usernames and video ids associated with "play_video" to datadata = {}for line in liblytics.read_log_file("umass_boston-edge-events-ALL.gz"):    if line["event_type"] == "seek_video":        username = line["username"]        if (username != ""):            if username not in data:                data[username] = Set()                            event = line["event"]            if not isinstance(event, dict):                try:                    event = eval(event)                except (NameError):                    event = event.replace("null", "0")                    event = eval(event)            data[username].add(event["id"])            for cleanName in sorted(videoNames):                if videoNames[cleanName] in data[username]:                    data[username] = data[username] + 1                else:                    data[username] = 0                                data[username] = str(data[username])                    print "Looking for unmatched videos..."unmatchedVideos = Set()for username in data:	for video in data[username]:		if video not in videoNames.values():			unmatchedVideos.add(video)	print "   Found these that were not in Video Names file:"for name in unmatchedVideos:	print nameprint "Determining who watched what..."#writing to a new csv file#determining if a video has been watched by a userf = open("Testing F14 Seek 2.csv", "w")f.write("username,")for cleanName in sorted(videoNames):    f.write (cleanName)    f.write (",")f.write (" \n")for username in sorted(data):    if username in usernames:        f.write (username)        f.write (",")        f.write (data[username])        f.write (" \n")f.close()print "All Done!"