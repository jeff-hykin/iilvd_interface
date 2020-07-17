
import sys
import time
sys.path.append("./iilvd_interface/python") # <- you're likely going to need to change that string
                                            # make it the path to your `iilvd_interface/python` folder

from video_toolkit import DB, Oracle, Node, DatabaseVideo, VideoSelect

#
# simple access to nodes
#
    # Node.random_nodes()
    # node.neighbors
    # node.info
    # Oracle.ask(node=a_node, index=1)
    # Oracle.question_count

# a generator that returns randomly sampled nodes (that are guarenteed to have neighbors) 
for each_node in Node.random_nodes():
    
    # check a particular label by asking the oracle
    print('Oracle.ask(each_node, 1) = ', Oracle.ask(each_node, index=1))
    # True = has label
    # False = doesn't have the label
    # None = index out of bounds 
    
    # returns a list of neighboring nodes 
    print(each_node.neighbors)
    
    # basic_info
    print(each_node.info)
    
    # access to video-object (see next for loop)
    print(each_node.database_video)
    
    # a way to better understand the data
    # (kind of a debugging tool, and a way to get around asking the Oracle)
    print(each_node.all_labels)
    
    break

#
# more direct access
#
    # each_video.id
    # each_video.url
    # each_video.data    # all database data for this video as a dict
    # each_video.frames  # downloads the video automatically, returns/is a generator
    # each_video.path    # returns None if video hasn't been downloaded

# a generator that returns all videos that are related to some other video
for each_video in VideoSelect().has_related_videos.retrive():
    # video object
    print('each video: ', each_video)
    
    print('each_video.id = ', each_video.id)
    # "special" attributes
    
    # the raw data straight from the database (can be a lot of data becase of thousands of frames)
    print('each_video.data  = ', each_video.data)
    
    # makes a network call for "related_videos"
    ids_of_related_videos = each_video["related_videos"].keys()
    
    # setup all related videos (no network calls, just adding a wrapper-class)
    related_videos = [ DatabaseVideo(each_id) for each_id in ids_of_related_videos ]
    
    # makes a network call of ONLY the basic info of the related video
    print('related_videos[0]["basic_info"] = ', related_videos[0]["basic_info"])
    
    time.sleep(10)
    break


#
# even more direct access
#

# example of a MongoDB query call
# see: https://docs.mongodb.com/manual/reference/operator/query/
ids_of_videos_longer_than_5_min = DB.find({ "basic_info.duration" : { "$gt": (5 * 60)  } })