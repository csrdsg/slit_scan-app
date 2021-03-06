import streamlit as st
import numpy as np
import pandas as pd
from moviepy.editor import VideoFileClip
from PIL import Image
import tempfile

st.title('Slit Scan')
st.markdown('On a slit scan image, one row of pixels is extracted from each frame of the video and placed adjacent to the same row from the next frame. Each row of pixels represents a duration of time. For start choose a video from your library.')

f = st.file_uploader("Upload file")
if f is None:
    st.stop()
else: pass

# makes a temporary file 
tfile = tempfile.NamedTemporaryFile(delete=False) 
tfile.write(f.read())

# converting to VideoFileClip
clip = VideoFileClip(tfile.name)
st.info(f'Info: {f.name} is {clip.fps} fps, for {clip.duration} seconds at {clip.size} resolution.')       

# in this case your keep the original resolution
# this image right now just a bunch of zeros    
img = np.zeros((clip.size[1], clip.size[0], 3), dtype='uint8')
target_fps = clip.size[0] / clip.duration
target_fps_horizontal = clip.size[1] / clip.duration

#if you one a use horizontal scanning
horizontal = st.checkbox('Horizontal', value=0)

# slider for slitwidth
if st.checkbox('Unique slit size?', value=0) == 0:
    slitwidth = 1
else:
    slitwidth = st.slider('Slit size (one by deafult)', min_value=1, max_value=50)

last_frame = clip.size[0] - slitwidth
last_frame_horizontal = clip.size[1] - slitwidth

uniq_slit = st.checkbox('Unique slit point? (the middle point is the deafult)', value=0)
# slider for slitpoint
if uniq_slit == 0 and horizontal == 0:
    slitpoint = clip.size[0] // 2
elif uniq_slit == 1 and horizontal ==0:
    slitpoint = st.slider('Choose the slit position', min_value=0, max_value=clip.size[0])
elif uniq_slit == 0 and horizontal == 1:
    slitpoint = clip.size[1] // 2
else:
    slitpoint = st.slider('Choose the slit position', min_value=0, max_value=clip.size[1])


# here the width of the pics depens about the lenght of the video
all_frame = int(clip.fps * clip.duration) * slitwidth

img2 = np.zeros((clip.size[1], all_frame, 3), dtype='uint8')
img2_horizontal = np.zeros((all_frame, clip.size[0], 3), dtype='uint8')
last_frame2 = all_frame - slitwidth


def one_image(slitpoint: int, mode: str):
  currentX = 0
  for i in clip.iter_frames(fps=target_fps, dtype='uint8'):
      if currentX <= last_frame:
          frame =  i[:,slitpoint:slitpoint + slitwidth,:]
          if mode == 'norm':
              pass
          if mode == 'avg':
              frame = frame.mean(axis=0).mean(axis=0)
          if mode == 'dom':
              colors, count = np.unique(frame, axis=0, return_counts=True)
              frame = np.array(colors[count.argmax()], dtype='uint8')
          img[:,currentX:currentX + slitwidth,:] = frame
      currentX += slitwidth
  output = Image.fromarray(img)
  st.image(output)

def one_image_origin(slitpoint: int, mode: str):
  currentX = 0
  for i in clip.iter_frames(fps=clip.fps, dtype='uint8'):
      if currentX < last_frame2:
          frame =  i[:,slitpoint:slitpoint + slitwidth,:]
          if mode == 'norm':
              pass
          if mode == 'avg':
              frame = frame.mean(axis=0).mean(axis=0)
          if mode == 'dom':
              colors, count = np.unique(frame, axis=0, return_counts=True)
              frame = np.array(colors[count.argmax()], dtype='uint8')
          img2[:,currentX:currentX + slitwidth,:] = frame
      currentX += slitwidth
  output = Image.fromarray(img2)
  st.image(output)

def one_image_horizontal(slitpoint: int, mode: str):
  currentX = 0
  for i in clip.iter_frames(fps=target_fps_horizontal, dtype='uint8'):
      if currentX <= last_frame_horizontal:
          frame =  i[slitpoint:slitpoint + slitwidth,:,:]
          if mode == 'norm':
              pass
          if mode == 'avg':
              frame = frame.mean(axis=0).mean(axis=0)
          if mode == 'dom':
              colors, count = np.unique(frame, axis=0, return_counts=True)
              frame = np.array(colors[count.argmax()][0], dtype='uint8')
          img[currentX:currentX + slitwidth,:,:] = frame
      currentX += slitwidth
  output = Image.fromarray(img)
  st.image(output)

def one_image_origin_horizontal(slitpoint: int, mode: str):
  currentX = 0
  for i in clip.iter_frames(fps=clip.fps, dtype='uint8'):
      if currentX < last_frame2:
          frame =  i[slitpoint:slitpoint + slitwidth,:,:]
          if mode == 'norm':
              pass
          if mode == 'avg':
              frame = frame.mean(axis=0).mean(axis=0)
          if mode == 'dom':
              colors, count = np.unique(frame, axis=0, return_counts=True)
              frame = np.array(colors[count.argmax()][0], dtype='uint8')
          img2_horizontal[currentX:currentX + slitwidth,:,:] = frame
      currentX += slitwidth
  output = Image.fromarray(img2_horizontal)
  st.image(output)

# buttons and selectors
mode = st.radio('Select', ['Normal','Average','Dominant'])
t = st.checkbox('Preserve original resolution', value=1)
if t == 0:
    st.info(f'The pictures height/width now depends from the lenght of the video. It will be around {all_frame} pixel.')


gen_button = st.button('Generate img')
# the generator button and when all the magic happens
if gen_button and horizontal == 0:
    if mode == "Normal"  and t == 1:
        one_image(slitpoint, 'norm')
    elif mode == "Average" and t == 1:
        one_image(slitpoint, 'avg')
    elif mode == "Dominant" and t == 1:
        one_image(slitpoint, 'dom')
    elif mode == "Normal"  and t == 0:
        one_image_origin(slitpoint, 'norm')
    elif mode == "Average" and t == 0:
        one_image_origin(slitpoint, 'avg')
    elif mode == "Dominant" and t == 0:
        one_image_origin(slitpoint, 'dom')
elif gen_button and horizontal == 1:
    if mode == "Normal"  and t == 1:
        one_image_horizontal(slitpoint, 'norm')
    elif mode == "Average" and t == 1:
        one_image_horizontal(slitpoint, 'avg')
    elif mode == "Dominant" and t == 1:
        one_image_horizontal(slitpoint, 'dom')
    elif mode == "Normal"  and t == 0:
        one_image_origin_horizontal(slitpoint, 'norm')
    elif mode == "Average" and t == 0:
        one_image_origin_horizontal(slitpoint, 'avg')
    elif mode == "Dominant" and t == 0:
        one_image_origin_horizontal(slitpoint, 'dom')