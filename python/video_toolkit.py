import sys
import logging
import os
from os.path import isabs, isfile, isdir, join, dirname, basename, exists, splitext, relpath
from os import remove, getcwd, makedirs, listdir, rename, rmdir, system
from shutil import move
from itertools import count
import glob
import regex as re
import numpy as np
import numpy
import pickle
import random
import itertools
import time
import subprocess
from subprocess import call
import json
from pathlib import Path
import cv2 as cv
import cv2
import yaml


PATHS = {
    "video_cache" : "../video.nosync.cache",
    "youtube-dl": "youtube-dl",
}
PARAMETERS = {
    "database_url" : "http://127.0.0.1:3000",
}


# 
# simple helpers
# 
from copy import deepcopy

def recursively_update(old_data, new_data):
    x = old_data
    y = new_data
    z = {}
    overlapping_keys = x.keys() & y.keys()
    for key in overlapping_keys:
        # merge lists
        if type(x[key]) == list and type(y[key]) == list:
            try:
                z[key] = deepcopy(x[key])
            except expression as identifier:
                z[key] = x[key]
            # add all the new values from y
            z[key] += [ each_y for each_y in y[key] if each_y not in x[key] ]
        elif type(x[key]) == dict and type(y[key]) == dict:
            z[key] = recursively_update(x[key], y[key])
        else:
            z[key] = y[key]
    for key in x.keys() - overlapping_keys:
        try:
            z[key] = deepcopy(x[key])
        except:
            z[key] = x[key]
    for key in y.keys() - overlapping_keys:
        try:
            z[key] = deepcopy(y[key])
        except expression as identifier:
            z[key] = y[key]
    return z


def ndarray_to_list(ndarray):
    if type(ndarray) != numpy.ndarray:
        return ndarray
    else:
        as_list = ndarray.tolist()
        new_list = []
        for each in as_list:
            new_list.append(ndarray_to_list(each))
        return new_list


import os
import glob
import shutil
class FileSystem():
    @classmethod
    def write(self, data, to=None):
        # make sure the path exists
        FileSystem.makedirs(os.path.dirname(to))
        with open(to, 'w') as the_file:
            the_file.write(str(data))
    
    @classmethod
    def read(self, filepath):
        try:
            with open(filepath,'r') as f:
                output = f.read()
        except:
            output = None
        return output    
        
    @classmethod
    def delete(self, filepath):
        if isdir(filepath):
            shutil.rmtree(filepath)
        else:
            try:
                os.remove(filepath)
            except:
                pass
    
    @classmethod
    def makedirs(self, path):
        try:
            os.makedirs(path)
        except:
            pass
        
    @classmethod
    def copy(self, from_=None, to=None, new_name="", force= True):
        if new_name == "":
            raise Exception('FileSystem.copy() needs a new_name= argument:\n    FileSystem.copy(from_="location", to="directory", new_name="")\nif you want the name to be the same as before do new_name=None')
        elif new_name is None:
            new_name = os.path.basename(from_)
        
        # get the full path
        to = os.path.join(to, new_name)
        # if theres a file in the target, delete it
        if force and FileSystem.exists(to):
            FileSystem.delete(to)
        # make sure the containing folder exists
        FileSystem.makedirs(os.path.dirname(to))
        if os.path.isdir(from_):
            shutil.copytree(from_, to)
        else:
            return shutil.copy(from_, to)
    
    @classmethod
    def move(self, from_=None, to=None, new_name="", force= True):
        if new_name == "":
            raise Exception('FileSystem.move() needs a new_name= argument:\n    FileSystem.move(from_="location", to="directory", new_name="")\nif you want the name to be the same as before do new_name=None')
        elif new_name is None:
            new_name = os.path.basename(from_)
        
        # get the full path
        to = os.path.join(to, new_name)
        # make sure the containing folder exists
        FileSystem.makedirs(os.path.dirname(to))
        shutil.move(from_, to)
    
    @classmethod
    def exists(self, *args):
        return FileSystem.does_exist(*args)
    
    @classmethod
    def does_exist(self, path):
        return os.path.exists(path)
    
    @classmethod
    def is_folder(self, *args):
        return FileSystem.is_directory(*args)
        
    @classmethod
    def is_dir(self, *args):
        return FileSystem.is_directory(*args)
        
    @classmethod
    def is_directory(self, path):
        return os.path.isdir(path)
    
    @classmethod
    def is_file(self, path):
        return os.path.isfile(path)

    @classmethod
    def list_files(self, path="."):
        return [ x for x in FileSystem.ls(path) if FileSystem.is_file(x) ]
    
    @classmethod
    def list_folders(self, path="."):
        return [ x for x in FileSystem.ls(path) if FileSystem.is_folder(x) ]
    
    @classmethod
    def ls(self, filepath="."):
        glob_val = filepath
        if os.path.isdir(filepath):
            glob_val = os.path.join(filepath, "*")
        return glob.glob(glob_val)

    @classmethod
    def touch(self, path):
        FileSystem.makedirs(FileSystem.dirname(path))
        if not FileSystem.exists(path):
            FileSystem.write("", to=path)
    
    @classmethod
    def touch_dir(self, path):
        FileSystem.makedirs(path)
    
    @classmethod
    def dirname(self, path):
        return os.path.dirname(path)
    
    @classmethod
    def basename(self, path):
        return os.path.basename(path)
    
    @classmethod
    def extname(self, path):
        filename, file_extension = os.path.splitext(path)
        return file_extension
    
    @classmethod
    def path_pieces(self, path):
        """
        example:
            *folders, file_name, file_extension = FileSystem.path_pieces("/this/is/a/filepath.txt")
        """
        folders = []
        while 1:
            path, folder = os.path.split(path)

            if folder != "":
                folders.append(folder)
            else:
                if path != "":
                    folders.append(path)

                break
        folders.reverse()
        *folders, file = folders
        filename, file_extension = os.path.splitext(file)
        return [ *folders, filename, file_extension ]
    
    @classmethod
    def join(self, *paths):
        return os.path.join(*paths)
    
    @classmethod
    def absolute_path(self, path):
        return os.path.abspath(path)
    
FS = FileSystem


class Image(object):
    def __init__(self, arg1):
        """
        @arg1: can either be a string (the path to an image file) or an ndarray (a cv2 image)
        """
        if type(arg1) == str:
            self.path = arg1
            self.img = cv.imread(arg1)
        elif type(arg1) == numpy.ndarray:
            self.path = None
            self.img = arg1
        else:
            raise Exception('Not sure how to create an image using ' + str(arg1))
    
    def show(self):
        print("Press ESC (on the image window) to exit the image")
        if self.path != None:
            name = self.path
        else:
            name = "img"
        cv2.imshow(name, self.img)
        while True:
            key = cv2.waitKey(1)
            if key == 27:  #ESC key to break
                break
        cv2.destroyWindow(name)
    
    def with_points(self, array_of_points, color=(255, 255, 00), radius=3):
        img_copy = self.img.copy()
        for x, y, in array_of_points:
            cv.circle(img_copy, (x, y), radius, color, thickness=-1, lineType=8, shift=0)
        return Image(img_copy)
    
    def save(self, to, image_type="png"):
        FS.makedirs(FS.dirname(to))
        result = cv2.imwrite(FS.absolute_path(to+"."+image_type), self.img)
        if not result:
            raise Exception("Could not save image:"+str(to))

class Video(object):
    def __init__(self, path=None):
        self.path = path
        if path is None:
            raise Exception("you're creating a Video(), but the first argument (path) is None")

    def save_frame(self, at_time, to):
        quality = "2" # can be 1-31, lower is higher quality
        call(["ffmpeg", "-ss", at_time, '-i', self.path , "-vframes", "1", "-q:v", quality, to])

    def frames(self):
        """
        returns: a generator, where each element is a image as a numpyarray 
        """
        # Path to video file 
        video_capture = cv2.VideoCapture(self.path)
        # Check if video opened successfully
        if (video_capture.isOpened()== False): 
            raise Exception(f"Error, tried opening {self.path} with cv2 but wasn't able to")
        
        # checks whether frames were extracted 
        success = 1
        while True: 
            # function extract frames 
            success, image = video_capture.read()
            if not success:
                video_capture.release()
                return None
            yield image
        
    
    def save_with_labels(self, list_of_labels, to=None):
        # 
        # extract video data
        # 
        video_capture = cv2.VideoCapture(self.path)
        frame_width  = int(video_capture.get(3))
        frame_height = int(video_capture.get(4))
        # Find OpenCV version
        (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
        if int(major_ver) < 3:
            fps = video_capture.get(cv2.cv.CV_CAP_PROP_FPS)
        else:
            fps = video_capture.get(cv2.CAP_PROP_FPS)
        video_capture.release()
        
        # 
        # create new video source
        # 
        frame_dimensions = (frame_width, frame_height)
        if to is None:
            *folders, name, ext = FS.path_pieces(self.path)
            output_file = FS.join(*folders, name+".labelled"+ext)
        else:
            output_file = to
        new_video = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'mp4v'), fps, frame_dimensions)
        # Read until video is completed
        for each_frame, each_label in zip(self.frames(), list_of_labels):
            if each_frame is None:
                break
            # Write text to frame
            text = str(each_label)
            text_location = (100, 100)
            font = cv2.FONT_HERSHEY_SIMPLEX
            thickness = 1
            color = (255, 255, 255)
            new_video.write(cv2.putText(each_frame, text, text_location, font, thickness, color, 2, cv2.LINE_AA))
        
        # combine the resulting frames into a video
        new_video.release()
        
import requests
class VideoDatabase(object):
    def __init__(self, url=None):
        self.url = url or PARAMETERS["database_url"]
    
    def all(self):
        return self.safe_json_post(self.url+"/all", {})
        
    def get(self, *key_list):
        return self.safe_json_post(self.url+"/get", { "keyList": key_list })

    def size(self):
        return self.safe_json_post(self.url+"/size", {})
    
    def keys(self):
        return self.safe_json_post(self.url+"/keys", {})

    def find(self, data):
        return self.safe_json_post(self.url+"/find", data)
        
    def __getitem__(self, *args):
        # keys will end up always being the list of elements inside
        # the []'s of ThisClass()["<video_id>", "next_key"]
        # this is an annoying workaround of python's poortly designed edgecase behavior
        keys = args[0]
        if type(keys) == tuple:
            keys = list(keys)
        else:
            keys = [keys]
            
        return self.get(*keys)

    def json_post(self, url, a_dict):
        return requests.post(url, json=a_dict)
    
    def safe_json_post(self, url, a_dict):
        data = self.json_post(url, a_dict).json()
        value = data.get("value", None)
        error = data.get("error", None)
        exists = data.get("exists", None)
        if error != None:
            raise Exception(f"\n\nError from database server: {error}\ndata sent: {a_dict}")
        
        return value

DB = VideoDatabase()


class DatabaseVideo(Video):
    def __init__(self, id=None):
        self.id = id
        self._data = None

    @classmethod
    def _lookup_table_of_cached_videos(self):
        all_paths = FS.list_files(PATHS["video_cache"])
        video_id_hash = {}
        for each in all_paths:
            *parent_dirs, file_name, file_ext = FS.path_pieces(each)
            if file_ext == ".mp4":
                video_id = re.sub(r'.*_',"",file_name)
                # assign the id to a path
                video_id_hash[video_id] = each
                # this second time is a poor workaround for videos that have _ in their name
                # TODO: improve this later
                video_id = re.sub(r'.*?_',"",file_name)
                # assign the id to a path
                video_id_hash[video_id] = each
        return video_id_hash
    
    @classmethod
    def _get_cached_video_path(self, video_id):
        all_paths = FS.list_files(PATHS["video_cache"])
        video_path = DatabaseVideo._lookup_table_of_cached_videos().get(video_id, None)
        if video_path is None:
            return None
        else:
            return video_path
        return None

    @classmethod
    def _download_video(self, video_id):
        video_path = DatabaseVideo._get_cached_video_path(video_id)
        if video_path is None:
            print(f'A video {video_id} wasn\'t avalible locally, downloading it now')
            # run the downloader
            url = str("https://www.youtube.com/watch?v="+video_id)
            path_to_video = FS.join(PATHS["video_cache"], f"name_{video_id}.mp4")
            call([PATHS["youtube-dl"], url, "-f", 'bestvideo[ext=mp4]', "-o" , path_to_video])
            # will return null if there was a download error
            return DatabaseVideo._get_cached_video_path(video_id)
        else:
            return video_path 
    
    @property
    def data(self):
        # if data hasn't been retrived, then 
        if self._data == None:
            self._data = DB[self.id]
        return self._data
    
    @property
    def url(self):
        return "https://www.youtube.com/watch?v=" + self.id
    
    @property
    def path(self):
        return DatabaseVideo._lookup_table_of_cached_videos().get(self.id, None)
    
    @property
    def frames(self):
        # download it if needed
        DatabaseVideo._download_video(self.id)
        return super().frames()
    
    def __getitem__(self, *args):
        # keys will end up always being the list of elements inside
        # the []'s of ThisClass()["<video_id>", "next_key"]
        # this is an annoying workaround of python's poortly designed edgecase behavior
        keys = args[0]
        if type(keys) == tuple:
            keys = list(keys)
        else:
            keys = [keys]
        
        list_copy = [ self.id ] + keys
        return DB[tuple(list_copy)]

# needs re, FS, DB, and Video
class VideoSelect(object):
    """
    if you need to retrive videos already stored on the disk 
    or if you need to retrive videos that meet a specific metadata requirement
    or if you need to pop a video off of a priority stack
    this tool is the right one for the job
    
    videos will be downloaded as-needed
    
    To get a generator for all videos do: 
        videos = VideoSelect().retrive()
    
    To get a generator for all downloaded videos do:
        videos = VideoSelect().is_downloaded.retrive()
    
    """
    
    def __init__(self):
        self.db_query_stack = [{}]
    
    def _add_query_restriction(self, new_restriction):
        # prefer the first restriction when there's a conflict
        self.db_query_stack[-1] = recursively_update(new_restriction, self.db_query_stack[-1])
    
    def retrive(self):
        """
        this method will trigger the actual database call.
        @return: A generator where each element is a video
        """
        already_seen_videos = set()
        # create a generator function that spits out video objects one at a time
        for each_query in self.db_query_stack:
            results_of_query = DB.find(each_query)
            print('results_of_query = ', type(results_of_query))
            # this only cares about the keys (video id's)
            unseen_videos = set(results_of_query) - already_seen_videos 
            for each_video_id in unseen_videos:
                # output full objects
                yield DatabaseVideo(each_video_id)
            # all the unseen have now been seen
            already_seen_videos |= unseen_videos

    @property
    def then(self):
        # create a new stack
        self.db_query_stack.append({})
        return self
        
    @property
    def has_basic_info(self):
        self._add_query_restriction({ "basic_info" : { "$exists": True } })
        return self

    @property
    def has_related_videos(self):
        # has at least 1 related video
        self._add_query_restriction({ "related_videos": { "$exists": True, "$not": {"$size": 0} }})
        return self
    
    @property
    def is_downloaded(self):
        # lookup the id's of all the cached videos
        prefered_ids = []
        lookup_table = DatabaseVideo._lookup_table_of_cached_videos()
        prefered_ids = lookup_table.keys()
        if len(prefered_ids) > 0:
            # add them as a restriction
            self._add_query_restriction({ "_id" : { "$in": list(prefered_ids) } })
        else:
            # remove the current query because it is impossible to meet the requirements of
            # (impossible because there are no download videos)
            self.db_query_stack.pop()
        return self