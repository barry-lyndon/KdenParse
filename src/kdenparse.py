#!/usr/bin/python
# Copyright 2011 Will Riley
# Distributed under the terms of the GNU General Public License v3

"""
 kdenparse.py
 
 KdenParse attempts to extract and present useful information 
 from a .kdenlive XML project file.
 
 Kdenlive video editing software can be found here:
 http://www.kdenlive.org

 Yep - this be hackage.
"""
import os, sys, argparse

argparser = argparse.ArgumentParser(prog="kdenparse.py", 
    add_help=True,
    description="Parses .kdenlive project files for various metadata and timeline informations.")
argparser.add_argument('-V', '--version', 
    action='version', 
    version='%(prog)s 0.1.0')
argparser.add_argument('--edl', action='store_true', default=False,
    dest='create_edl',
    help='Generate EDL output.')
argparser.add_argument('--deref-proxy', action='store_true', default=False,
    dest='deref_proxy',
    help='Dereference proxy clip (show original filenames)')
argparser.add_argument('--frames', action='store_true', default=False,
    dest='show_frames',
    help='Show frames instead of TC when using --edl.')
argparser.add_argument('--links', action='store_true', default=False,
    dest='show_links',
    help='Show source id to filename association.')
argparser.add_argument('--profile', action='store_true', default=False,
    dest='get_profile',
    help='Generate project profile metadata.')
argparser.add_argument('--producers', action='store_true', default=False,
    dest='get_producers',
    help='Show MLT producers (media file) metadata.')
argparser.add_argument('--kproducers', action='store_true', default=False,
    dest='get_kproducers',
    help='Show Kdenlive producers (media file) metadata.')
argparser.add_argument('projectFile')

args = argparser.parse_args()

if not os.path.isfile(args.projectFile):
    print "Not a file we can work with..."
    sys.exit(1)

try: 
    args.projectFile.rindex(".kdenlive",-9)
except ValueError:
    print "Invalid filename. Exiting."
    sys.exit(1)

from xml.dom import minidom
from decimal import Decimal,getcontext,ROUND_DOWN
from math import modf

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
        kProducerList = []
        profile = self.xmldoc.getElementsByTagName("kdenlive_producer")
        for i in profile:
            kpDict = {}
            keyList = i.attributes.keys()
            for a in keyList:
                kpDict[i.attributes[a].name] = i.attributes[a].value
            kProducerList.append(kpDict)
        return kProducerList
    
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
            sourceLinks[srcPid] = i["resource"]
        return sourceLinks
    
    def derefProxy(self):
        proxyLinks = {}
        for i in self.getKProducers():
            try:
                if i["proxy"]:
                    _proxy = i["proxy"]
                    proxyLinks[_proxy] = i["resource"]
            except KeyError:
                return False
        return proxyLinks
    
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

                srcIn = int(event["inTime"]) # source clip IN time
                srcOut = int(event["outTime"]) # source clip OUT time
                if EdlEventCnt != 1:
                    srcOut = srcOut + 1
                srcDur = srcOut - srcIn 
                progOut = progOut + srcDur # increment program tally
                
                sourceFile = sourceLinks[prod]
                proxyList = self.derefProxy()
                if proxyList:
                    try:
                        fileName = "(" + proxyList[sourceFile].split("/")[-1] + ") " + sourceFile.split("/")[-1]  
                    except KeyError:
                        fileName = sourceFile.split("/")[-1] 
                else:
                    # extract filename from full path to file
                    fileName = sourceFile.split("/")[-1] 
                
                print "* FROM CLIP NAME: " + fileName
                print str(EdlEventCnt) + "  " + prod + "  ",
                print srcType + "  " + srcChannel + "  ", 
                
                if args.show_frames:
                    print str(srcIn) + " " + str(srcOut) + "",
                    print str(progIn) + " " + str(progOut)
                else:
                    print self.framesToTc(srcIn) + " " + self.framesToTc(srcOut) + "",
                    print self.framesToTc(progIn) + " " + self.framesToTc(progOut)
        
                if EdlEventCnt == 1:
                    progIn = progIn + 1
                    
                progIn = progIn + srcDur
                EdlEventCnt = EdlEventCnt + 1

    def framesToTc(self, frameCount):
        getcontext().prec = 10
        getcontext().rounding = ROUND_DOWN
        projectMeta = self.getProjectProfile()
        frameRate = Decimal(projectMeta["frame_rate_num"]) / Decimal(projectMeta["frame_rate_den"])
        frameDuration = 1 / frameRate
        #print "fps = " + str(frameRate)
        #print "1 fr = " + str(frameDuration)  + " secs"
        absDuration = Decimal(frameCount) * Decimal(frameDuration) # frameCount length in seconds
        #print "TC = " + str(absDuration)
        f, w = modf(absDuration) # split float at decimal (fraction, whole)
        #print "Split: " + "%f + %f" % (w, f)
        frameRemainder = Decimal(str(f)) / Decimal(frameDuration)
        m, s = divmod(w, 60)
        h, m = divmod(m, 60)
        tc = "%d:%02d:%02d:%02d" % (h, m, s, frameRemainder)
        return tc
        
kp = KdenParse(args.projectFile)

if args.create_edl:
    kp.createEdl()

if args.get_profile:
    for i in kp.getProjectProfile().keys():
        print i + ": " + kp.getProjectProfile()[i]    

if args.get_producers:
    for i in kp.getProducers():
        print "\n=================\n"
        for kv in i:
            print kv + ": " + i[kv]

if args.get_kproducers:
    for i in kp.getKProducers():
        print "\n=================\n"
        for kv in i:
            print kv + ": " + i[kv]
        
if args.deref_proxy:
    for i in kp.derefProxy():
        print i + ": " + kp.derefProxy()[i]
        
if args.show_links:
    for i in kp.linkReferences():
        print i + ": " + kp.linkReferences()[i]

