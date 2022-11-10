"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
from moviepy.editor import VideoFileClip
import moviepy
import skimage
import numpy as np
import os


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, filename = "", OutputDirectory = ""):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',   # will show up in GRC
            in_sig=[],
            out_sig=[np.float32]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.filename = filename
        self.OutputDirectory = OutputDirectory
        self.Line = 1
        self.opened = 0
        self.outvect = np.empty(0)


    def work(self, input_items, output_items):



        if os.listdir("frames") == []:
            vid = VideoFileClip("Snapchat-2027161104.mp4")

            # Convert to greyscale
            vid = moviepy.video.fx.all.blackwhite(vid)
            vid = vid.resize((720,486))

            # extract sound and save to wav
            sound = vid.audio
            sound.write_audiofile('audioout.mp3')
            TestFiles = np.empty([0], dtype='U50')

            frames = 0

            # Clear directory
            dir = 'frames'
            for file in os.scandir(dir):
                os.remove(file.path)

            # Extract frames and convert to array
            for i in range(0, int(vid.duration * 30), 1):
                framename = "frames/frame" + str(i) + ".jpeg"
                TestFiles.resize(TestFiles.size + 1)
                TestFiles[TestFiles.size - 1] = framename
                vid.save_frame(framename, float((i * vid.duration) / 30))

                if (i == 0):
                    vidvect = skimage.io.imread(TestFiles[0], as_gray=True).ravel()
                else:
                    vidvect = np.append(vidvect, skimage.io.imread(TestFiles[i], as_gray=True).ravel())
                frames = frames + 1

            firstrun = 0
        if self.opened == 0:
            self.opened = 1
            i = 0
            #FIX ORDER FILES ARE OPENED THEY ARE OPENING ALPHABETICALLY
            for file in os.listdir("frames"):
                filename = "frames/" + file
                if (i == 0):
                    print(i)
                    vidvect = skimage.io.imread(filename, as_gray=True).ravel()
                    i = 1
                else:
                    print(file)
                    vidvect = np.append(vidvect, skimage.io.imread(filename, as_gray=True).ravel())
            self.outvect.resize(vidvect.size)
            self.outvect = vidvect
            self.outvect = np.reshape(self.outvect,(-1, 720))
            print(self.outvect.shape)
        print(output_items[0])
        if output_items[0].size > self.outvect.shape[1]:
            for k in range(self.outvect.shape[1]):
                output_items[0][k] = self.outvect[self.Line, k]

        self.Line = self.Line + 1
        #
        # if Line < vidvect.shape[0] - 1:
        #     Line = Line + 1
        # else:
        #      Line = 0
        return len(output_items[0])




