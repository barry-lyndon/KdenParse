"""
 KdenParse attempts to extract and present useful information 
 from a .kdenlive XML project file.
 
 Kdenlive video editing software can be found here:
 http://www.kdenlive.org
 
 Usage:
 Set the project file as shown at the bottom of this document.
 kp = KdenParse('/home/dave/project.kdenlive')
 
 Run it.
 $ python kdenparse.py

 Yep - this be hackage.
"""

from xml.dom import minidom

class KdenParse:
        
    def __init__(self, kdenliveFile):
        self.xmldoc = minidom.parse(kdenliveFile)
    
    def getProjectProfile(self):
        profileDict = {}
        profile = self.xmldoc.getElementsByTagName("profile")
        keyList = profile.item(0).attributes.keys()
        for a in keyList:
            profileDict[a] = profile.item(0).attributes[a].value
        return profileDict
    
    def getTracks(self):
        tracks = []
        t = self.xmldoc.getElementsByTagName("track")
        for track in t:
            tracks.append(track.attributes["producer"].value) 
        return tracks
    
    def getPlaylists(self):
        playlistList = []
        playlists = self.xmldoc.getElementsByTagName("playlist")
        for p in playlists:
            eventList = []
            plDict = {}
            plDict["pid"] = p.attributes["id"].value
            events = p.getElementsByTagName("entry")
            for event in events:
                evDict = {}
                evDict["producer"] = event.attributes["producer"].value
                evDict["inTime"] = event.attributes["in"].value
                evDict["outTime"] = event.attributes["out"].value
                eventList.append(evDict)
            plDict["events"] = eventList
            playlistList.append(plDict)
        return playlistList
    
    def getKProducers(self):
        profile = self.xmldoc.getElementsByTagName("kdenlive_producer")
        for i in profile:
            keyList = i.attributes.keys()
            for a in keyList:
                print i.attributes[a].name + ": " + i.attributes[a].value

    def getProducers(self):
        producerList = []
        producers = self.xmldoc.getElementsByTagName("producer")
        for p in producers:
            pDict = {}
            pDict["pid"] = p.attributes["id"].value
            pDict["inTime"] = p.attributes["in"].value
            pDict["outTime"] = p.attributes["out"].value
            
            properties = p.getElementsByTagName("property")
            for props in properties:
                pDict[props.attributes["name"].value.replace(".","_")] = props.firstChild.data 
                
            producerList.append(pDict)
        return producerList
    
    def linkReferences(self):
        sourceLinks = {}
        for i in self.getProducers():
            srcPid = i["pid"]
            srcFile = i["resource"]
            sourceLinks[srcPid] = srcFile
        return sourceLinks
    
    def createEdl(self):
        sourceLinks = self.linkReferences()
        for playlist in self.getPlaylists():
            EdlEventCnt = 1
            progIn = 0 # showtime tally
            progOut = 0
            srcChannel = "C" # default channel/track assignment 
            print "\n === " + playlist["pid"] + " === \n"
            for event in playlist["events"]:
                prod = event["producer"]
                prodChunks = prod.split("_")
                srcType = prodChunks[-1].capitalize()[:1] 
                
                # if it's an audio event, extract channel info from producer id
                if srcType == "A":
                    srcChannel = prodChunks[1]
                
                fileName = sourceLinks[prod].split("/")[-1]

                srcIn = int(event["inTime"])
                srcOut = int(event["outTime"])
                srcDur = srcOut - srcIn
                progOut = progOut + srcDur
        
                print "* FROM CLIP NAME: " + fileName
                print str(EdlEventCnt) + "\t" + prod + " \t" + srcType + "\t" + srcChannel + "\t" + str(srcIn) + "\t" + str(srcOut) + "\t" + str(progIn) + "\t" + str(progOut)
        
                if EdlEventCnt == 1:
                    progIn = progIn + 1
                    
                progIn = progIn + srcDur
                EdlEventCnt = EdlEventCnt + 1

kp = KdenParse('../sample/KdenParse_sample.kdenlive')
#x.getKProducers()
kp.createEdl()
