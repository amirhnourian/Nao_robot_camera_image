# Copyright 1996-2022 Cyberbotics Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Controller example for the Robot Wrestling Tournament.
Demonstrates how to access the LEDs and play a custom motion file.
Beats Bob by moving forwards and pushing him to the ground.
"""
from controller import Robot, Motor
import sys
sys.path.append('..')
from utils.camera import Camera
import cv2
from PIL import Image
from utils.motion_library import MotionLibrary



class Charlie (Robot):
    def __init__(self):
        Robot.__init__(self)
        self.time_step = int(self.getBasicTimeStep())

        # there are 7 controllable LEDs on the NAO robot, but we will use only the ones in the eyes
        self.leds = {
            'right': self.getDevice('Face/Led/Right'),
            'left':  self.getDevice('Face/Led/Left')
        }
        # HeadPitch
        self.HeadPitch = self.getDevice("HeadPitch")
        self.HeadPitch.setPosition(0.25)

        self.library = MotionLibrary()
        # adding a custom motion to the library
        self.library.add('Shove', './Shove.motion', loop=True)
        self.camera = Camera(self)
        self.sampleCamera = 1

    def run(self):
        self.library.play('Stand')

        self.leds['right'].set(0xff0000)  # set the eyes to red
        self.leds['left'].set(0xff0000)

        while self.step(self.time_step) != -1:
            # When the robot is done standing for stabilization, it moves forwards
            t = self.getTime()
            print(t)

            if t == self.sampleCamera:
                img = self.camera.get_image()
                output = img.copy()
                make_file_name = str(t)+'.png'
                im = Image.fromarray(output)
                # im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
                # im = im.convert('RGB')
                im.save(make_file_name)
                self.sampleCamera += 1

            if self.library.get('Stand').isOver():
                self.library.play('TurnLeft60')  # walk forward
                self.library.play('Shove')        # play the shove motion


# create the Robot instance and run main loop
wrestler = Charlie()
wrestler.run()
