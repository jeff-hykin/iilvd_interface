# Overview
- download code with git clone 
- install pip modules
- connect to the tamu VPN
- import the classes
- tell the classes what videos you want to retrieve

# What does repo provide?
- Lets you query what kinds of videos are avalible
- Lets you analyze duration, fps, height-in-pixels, related videos, etc
- Auto-downloads videos and retrieves them frame-by-frame as cv2 images


# Problems / Errors
If you have any challenges getting it setup, or if the code is broken, [create an issue on GitHub](https://github.com/jeff-hykin/iilvd_interface/issues)

<br><br>

# How to use

## 1. Installation
<details>
  <summary>Click For Installation Details</summary>
You'll need
  
- python3 (≥3.6)
- pip3
- youtube-dl
- ffmpeg (optional, only needed for a_video.save_frame)
- git (for setup only)

You'll also need the pip modules mentioned in [requirements.txt](https://github.com/jeff-hykin/iilvd_interface/blob/51b78bad14b93b6b2801d36a6a5890d5fdaeb08b/requirements.txt#L20) 

### For MacOS this just means run
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
brew install git
brew install python3
brew install youtube-dl
brew install ffmpeg
pip3 install $(curl https://raw.githubusercontent.com/jeff-hykin/iilvd_interface/51b78bad14b93b6b2801d36a6a5890d5fdaeb08b/requirements.txt) 
```
### For Windows 10
I recommend installing all of them with [Scoop](https://scoop.sh/) or [Chocolatey](https://chocolatey.org/install)<br>but here's some guides encase you don't want to use those tools<br>
[git install guide](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)<br>
[python3 guide](https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-local-programming-environment-on-windows-10)<br>
[youtube-dl guide](http://ytdl-org.github.io/youtube-dl/download.html)<br>
[ffmpeg guide](https://www.wikihow.com/Install-FFmpeg-on-Windows)<br>

### For Linux
Seeing as you are a superior programmer, you've probably installed all those before even reading this sentence. For completeness sake though, basically repeat the MacOS commands, but replace `brew install` with your package manager (probably `apt-get install`)
</details>


## 2. Connection
Make sure you're connected to the TAMU VPN, you'll get a connection error otherwise

## 3. Your project

(FYI: If you know what you're doing, you can probably skip parts or do them your own way)

- Presumably you have a project of your own in a folder somewhere
- And presumably you are using git to manage your project
- (If you don't, then please [make a git repository](https://thegeeksalive.com/how-to-create-a-new-git-repository-and-push-it-to-github/) for your project) 

We need to download the code to your project, import it, and then use it
1. Download <br>
Open up a terminal/CMD/console to that project. e.g. `cd YourProjectFolder`<br> 
Then run `git submodule add https://github.com/jeff-hykin/iilvd_interface`.<br>
This will add a `iilvd_interface` folder to your project.
2. Importing the code<br>
Presumably you have a python file, lets say `your_code.py`. <br> And inside `your_code.py` you want to get access to some videos.<br>There's a full example of how to do that here: [python/example.py](https://github.com/jeff-hykin/iilvd_interface/blob/51b78bad14b93b6b2801d36a6a5890d5fdaeb08b/python/example.py#L4)<br> Here's the basic steps that are done inside that example. To import the code you'll need to add that folder (iilvd_interface) to your Python path.<br><br>
   ```python
   import sys
   import time
   sys.path.append("./iilvd_interface/python") # <- you're likely going to need to change that string
                                               # make it the path to the `iilvd_interface` folder whereever
                                               # that folder might be
   ```
   Then you want to import the actual tools<br><br>
   ```python
   from video_toolkit import DB, DatabaseVideo, VideoSelect, Node
   ```
## Using the tools
<br>

See [the example file here](https://github.com/jeff-hykin/iilvd_interface/blob/236a3b4518fa1ea4230d9fa5c0f1ab5922660f6f/python/example.py) for a jumpstart into all the tools. That file should 

<br><br>




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



