
import sys
sys.path.append("./iilvd_interface/python") # <- you're likely going to need to change that string
                                            # make it the path to your `iilvd_interface/python` folder

from video_toolkit import DB, Oracle, Node, DatabaseVideo, VideoSelect

#
# simple access to nodes
#
    # Node.random_nodes()
    # node.has_labels
    # node.neighbors
    # node.info
    # Oracle.ask(node=a_node, index=1)
    # Oracle.question_count

# a generator that returns randomly sampled nodes
# NOTE:
#     - these nodes are guarenteed to have neighbors and labels
#     - there are approximately 1200 fully labeled nodes
#       But this for-loop will continue sampling indefinitely
#       meaning you'll eventually start re-sampling nodes
for each_node in Node.random_nodes():
    
    # check a particular label at a particular index by asking the oracle
    print('Oracle.ask(each_node, 1) = ', Oracle.ask(each_node, index=1))
    # returns one of:
    #      True = labeled as true
    #      False = labeled as false
    #      None = index out of bounds/no label info
    
    # returns a list of neighboring nodes
    # BUT! the neighbors are Not guarenteed to have labels
    # (they might be unlabeled)
    print('each_node.neighbors = ', each_node.neighbors)
    
    # basic_info
    print('each_node.info = ', each_node.info)
    
    # access to video-object (see the next for loop for more info)
    print('each_node.database_video = ', each_node.database_video)
    
    # a way to better understand the labels
    # (kind of a debugging tool, and a way to get around asking the Oracle)
    print('each_node.all_labels = ', each_node.all_labels)
    
    # this is just an example so end after one iteration
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
    
    # the raw data straight from the database
    # (can sometimes be a lot of data becase of thousands of frames)
    print('each_video.data  = ', each_video.data)
    
    # makes a network call for "related_videos"
    # note: some neighbor-id's might not exist/have-data in the database
    # (this is like a graph-edge with no node)
    ids_of_related_videos = each_video["related_videos"].keys()
    
    # setup all related videos (no network calls, just adding a wrapper-class)
    related_videos = [ DatabaseVideo(each_id) for each_id in ids_of_related_videos ]
    
    # makes a network call of ONLY the basic info of the related video
    print('related_videos[0]["basic_info"] = ', related_videos[0]["basic_info"])
    
    # this is just an example so end after one iteration
    break


#
# even more direct access
#

# example of a MongoDB query call
# see: https://docs.mongodb.com/manual/reference/operator/query/
ids_of_videos_longer_than_5_min = DB.find({ "basic_info.duration" : { "$gt": (5 * 60)  } })