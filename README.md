
# Overview
- download code with git clone 
- import a module
- tell the module what videos you want to retrieve

# What does repo provide?
- Lets you query what kinds of videos are avalible
- Lets you analyze duration, fps, height-in-pixels, related videos, etc
- Auto-downloads videos and retrieves them frame-by-frame as cv2 images

<br><br>

# Python: How to use

## 1. Installation
Install all the needed pip modules. Check the [requirements.txt](https://github.com/jeff-hykin/iilvd_interface/blob/51b78bad14b93b6b2801d36a6a5890d5fdaeb08b/requirements.txt#L20) file to see all of those and their versions.

## 2. Connection
Make sure you're connected to the TAMU VPN, you'll get a connection error otherwise

## 3. Your project
- Presumably you have a project of your own in a folder somewhere
- And presumably you are using git to manage your project
- (If you don't, then please make a git repository for your project) 

We need to download the code to your project, import it, and then use it
1. Download <br>
Open up a terminal/CMD/console to that project. e.g. `cd YourProjectFolder`<br> 
Then run `git submodule add https://github.com/jeff-hykin/iilvd_interface`.<br>
This will add a `iilvd_interface` folder to your project.
2. Importing the code<br>
Presumably you have a python file, lets say `yourCode.py`. <br> There's a full example of how to import the code here: [python/example.py](https://github.com/jeff-hykin/iilvd_interface/blob/51b78bad14b93b6b2801d36a6a5890d5fdaeb08b/python/example.py#L4)<br>To import the code you'll need to add that folder (iilvd_interface) to your Python path.<br><br>
   ```python
   import sys
   import time
   sys.path.append("./iilvd_interface/python")
   ```
   Then you want to import the actual tools<br><br>
   ```python
   import DB, DatabaseVideo, VideoSelect from video_toolkit
   ```
## Using the tools
<br><br><br>
### Selecting Videos
Get all the videos, in no particular order, do the following
```python
for each_video_object in VideoSelect().retrive():
    print("its a video id:", each_video_object.id)
``` 
You probably don't want all the videos though because lots of them don't have any information. So lets get all the ones with basic information with `has_basic_info`.

```python
for each_video_object in VideoSelect().has_basic_info.retrive():
    print("its a video id:", each_video_object.id) 
```

There is also the `has_related_videos` filter, and `is_downloaded` filter. (There will be more of these in the future)
<br><br><br>
### Data about a video

There's a lot of data you get get about a video. I'll go over the basics here, but if you want to see every possible option take a look at the [data_format.yaml](https://github.com/jeff-hykin/iilvd_interface/blob/51b78bad14b93b6b2801d36a6a5890d5fdaeb08b/data_format.yaml#L4). Note! most of the fields are <b>optional</b>, so your code will need to check to make sure they exist.

```
# get a video
video_id_as_a_string = "Dnuzr2PnzF4"
video_object = DatabaseVideo(video_id_as_a_string)

# Video attributes (smart data)
video_object.url     # the youtube url to the video
video_object.frames  # a generator returning each frame as a cv2 img
video_object.data    # all of the metadata as a dict()
video_object.path    # path to .mp4 file IF the video is downloaded

# Video database retrival (directly from data_format.yaml)
video_object["basic_info", "duration"] # makes a network request for only the duration
video_object["related_videos", 0] # makes a requst for only related videos (returns a list of id's)
```
<br><br><br>
### Advanced Data Access

The database uses MongoDB on the backend. If you want to make your own efficient custom queries you can use the [MongoDB find-queries](https://docs.mongodb.com/manual/reference/operator/query/) directly as follows:
```
# get a list of id's to all the videos shorter than 5 minutes
video_ids = DB.find({ "basic_info.duration": { "$lt" : 5 * 60 } })
``` 



