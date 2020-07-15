
import sys
import time
sys.path.append("./iilvd_interface/python")
from video_toolkit import DB, DatabaseVideo, VideoSelect, Node


for each in Node.random_nodes():
    print(each.info)
    break

# a generator that returns all videos that are related to some other video
# for each_video in VideoSelect().has_related_videos.retrive():
#     # video object
#     print('each video: ', each_video)
    
#     print('each_video.id = ', each_video.id)
#     # "special" attributes
#     # each_video.id
#     # each_video.data
#     # each_video.url
#     # each_video.frames  # downloads video automatically
#     # each_video.path    # returns None if video hasn't been downloaded
    
#     # the raw data straight from the database
#     print('each_video.data  = ', each_video.data)
    
#     # makes a network call
#     # ids_of_related_videos = each_video["related_videos"]
    
#     # setup all related videos (no network calls, just adding a wrapper-class)
#     # related_videos = [ DatabaseVideo(each_id) for each_id in ids_of_related_videos ]
    
#     # makes a network call of ONLY the basic info of the related video
#     # print('related_videos[0]["basic_info"] = ', related_videos[0]["basic_info"])
#     break
#     time.sleep(10)
    

# example of a MongoDB query call
# see: https://docs.mongodb.com/manual/reference/operator/query/
# ids_of_videos_longer_than_5_min = DB.find({ "basic_info.duration" : { "$gt": (5 * 60)  } })