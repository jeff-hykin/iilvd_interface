import sys
import time
sys.path.append("./")
import video_toolkit
import DB from video_toolkit

for each_video in video_toolkit.VideoSelect().has_related_videos.retrive():
    print('each video: ', each_video)
    print('each_video.id = ', each_video.id)
    print('each_video.data  = ', each_video.data)
    
    # makes a network call
    ids_of_related_videos = each_video["related_videos"]
    
    # setup all related videos (no network calls, just adding a wrapper-class)
    related_videos = [ video_toolkit.DatabaseVideo(each_id) for each_id in ids_of_related_videos ]
    
    # makes a network call of ONLY the basic info of the related video
    if len(related_videos) > 0:
        print('related_videos[0]["basic_info"] = ', related_videos[0]["basic_info"])
    
    time.sleep(10)
    

# example of a MongoDB query call
# see: https://docs.mongodb.com/manual/reference/operator/query/
ids_of_videos_longer_than_5_min = DB.find({ "basic_info.duration" : { "$gt": (5 * 60)  } })