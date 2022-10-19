from moviepy.audio.io.ffmpeg_audiowriter import ffmpeg_audiowrite
from moviepy.Clip import Clip
from moviepy.decorators import requires_duration
from moviepy.tools import deprecated_version_of, extensions_dict
from moviepy.editor import VideoFileClip
import moviepy
import scipy
import skimage
from skimage import io

#import test video file
vid = VideoFileClip("Snapchat-2027161104.mp4")

#Convert to greyscale
vid = moviepy.video.fx.all.blackwhite(vid)

#extract sound and save to wav
sound = vid.audio
sound.write_audiofile('audioout.mp3')

#Extract frames and convert to array
for i in range(0,int(vid.duration*30),1):
     framename = "frames/frame" + str(i) + ".jpeg"
     vid.save_frame(framename,float((i*vid.duration)/30))





