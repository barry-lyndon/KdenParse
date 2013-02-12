KdenParse
=========

Kdenlive xml file processor

Sample output command:

    $ python ./kdenparse.py --edl samplefile.kdenlive 

It's in a quasi-CMX3600 format. Edit-point (location) units are H:M:S:fr.

    * FROM CLIP NAME: <source file name>
    <index> <source id> <Audio/Video> <channel> <src in> <src out> <showtime in> <showtime out>

     === black_track === 
    
    * FROM CLIP NAME: black
    1  black   B  C   0:00:00:00 0:00:50:08 0:00:00:00 0:00:50:08
    
     === playlist1 === 
    
    
     === playlist2 === 
    
    * FROM CLIP NAME: 00000.MTS
    1  13_2_audio   A  2   0:00:02:13 0:00:09:04 0:00:00:00 0:00:06:15
    * FROM CLIP NAME: 00001.MTS
    2  2_2_audio   A  2   0:00:04:01 0:00:07:13 0:00:06:16 0:00:10:03
    * FROM CLIP NAME: 00002.MTS
    3  3_2_audio   A  2   0:00:08:15 0:00:11:08 0:00:10:04 0:00:12:20
    * FROM CLIP NAME: 00000.MTS
    4  13_2_audio   A  2   0:00:14:11 0:00:21:02 0:00:12:21 0:00:19:11
    * FROM CLIP NAME: 00003.MTS
    5  4_2_audio   A  2   0:00:00:00 0:00:02:01 0:00:19:12 0:00:21:12
    * FROM CLIP NAME: 00004.MTS
    6  5_2_audio   A  2   0:00:02:21 0:00:07:01 0:00:21:13 0:00:25:16
    * FROM CLIP NAME: 00005.MTS
    7  6_2_audio   A  2   0:00:02:02 0:00:04:16 0:00:25:17 0:00:28:06
    * FROM CLIP NAME: 00006.MTS
    8  7_2_audio   A  2   0:00:03:07 0:00:05:08 0:00:28:07 0:00:30:07
    * FROM CLIP NAME: 00000.MTS
    9  13_2_audio   A  2   0:00:05:08 0:00:11:05 0:00:30:08 0:00:36:04
    * FROM CLIP NAME: 00007.MTS
    10  8_2_audio   A  2   0:00:03:18 0:00:05:19 0:00:36:05 0:00:38:05
    * FROM CLIP NAME: 00008.MTS
    11  9_2_audio   A  2   0:00:09:05 0:00:14:01 0:00:38:06 0:00:43:02
    * FROM CLIP NAME: 00009.MTS
    12  10_2_audio   A  2   0:00:00:00 0:00:02:01 0:00:43:03 0:00:45:03
    * FROM CLIP NAME: 00010.MTS
    13  11_2_audio   A  2   0:00:01:07 0:00:03:22 0:00:45:04 0:00:47:18
    * FROM CLIP NAME: 00011.MTS
    14  12_2_audio   A  2   0:00:00:00 0:00:02:01 0:00:47:19 0:00:49:19
    
     === playlist3 === 
    
    
     === playlist4 === 
    
    * FROM CLIP NAME: 00000.MTS
    1  13_video   V  C   0:00:02:13 0:00:09:04 0:00:00:00 0:00:06:15
    * FROM CLIP NAME: 00001.MTS
    2  2_video   V  C   0:00:04:01 0:00:07:13 0:00:06:16 0:00:10:03
    * FROM CLIP NAME: 00002.MTS
    3  3_video   V  C   0:00:08:15 0:00:11:08 0:00:10:04 0:00:12:20
    * FROM CLIP NAME: 00000.MTS
    4  13_video   V  C   0:00:14:11 0:00:21:02 0:00:12:21 0:00:19:11
    * FROM CLIP NAME: 00003.MTS
    5  4_video   V  C   0:00:00:00 0:00:02:01 0:00:19:12 0:00:21:12
    * FROM CLIP NAME: 00004.MTS
    6  5_video   V  C   0:00:02:21 0:00:07:01 0:00:21:13 0:00:25:16
    * FROM CLIP NAME: 00005.MTS
    7  6_video   V  C   0:00:02:02 0:00:04:16 0:00:25:17 0:00:28:06
    * FROM CLIP NAME: 00006.MTS
    8  7_video   V  C   0:00:03:07 0:00:05:08 0:00:28:07 0:00:30:07
    * FROM CLIP NAME: 00000.MTS
    9  13_video   V  C   0:00:05:08 0:00:11:05 0:00:30:08 0:00:36:04
    * FROM CLIP NAME: 00007.MTS
    10  8_video   V  C   0:00:03:18 0:00:05:19 0:00:36:05 0:00:38:05
    * FROM CLIP NAME: 00008.MTS
    11  9_video   V  C   0:00:09:05 0:00:14:01 0:00:38:06 0:00:43:02
    * FROM CLIP NAME: 00009.MTS
    12  10_video   V  C   0:00:00:00 0:00:02:01 0:00:43:03 0:00:45:03
    * FROM CLIP NAME: 00010.MTS
    13  11_video   V  C   0:00:01:07 0:00:03:22 0:00:45:04 0:00:47:18
    * FROM CLIP NAME: 00011.MTS
    14  12_video   V  C   0:00:00:00 0:00:02:01 0:00:47:19 0:00:49:19
    
And here's a project profile dump sample:

    $ python ./kdenparse.py --project samplefile.kdenlive

Which outputs the following:

    sample_aspect_den: 1
    display_aspect_num: 16
    colorspace: 0
    description: HD 1080p 23.976 fps
    progressive: 1
    display_aspect_den: 9
    frame_rate_num: 24000
    sample_aspect_num: 1
    height: 1088
    width: 1920
    frame_rate_den: 1001
