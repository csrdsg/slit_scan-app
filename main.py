import streamlit as st
import numpy as np
import pandas as pd
from moviepy.editor import VideoFileClip
from PIL import Image
import tempfile

st.title('Slit Scan')

f = st.file_uploader("Upload file")
if f is None:
    st.stop()
else: pass


tfile = tempfile.NamedTemporaryFile(delete=False) 
tfile.write(f.read())
clip = VideoFileClip(tfile.name)
st.text(f'{f} is {clip.fps} fps, for {clip.duration} seconds at {clip.size}')       
    
img = np.zeros((clip.size[1], clip.size[0], 3), dtype='uint8')
target_fps = clip.size[0] / clip.duration
slitwidth = 1
slitpoint = st.slider('Slide me', min_value=0, max_value=clip.size[0])
last_frame = clip.size[0] - slitwidth
    

def one_image(slitpoint):
  currentX = 0
  for i in clip.iter_frames(fps=target_fps, dtype='uint8'):
      if currentX < last_frame:
          frame =  i[:,slitpoint:slitpoint + slitwidth,:]
          img[:,currentX:currentX + slitwidth,:] = frame
      currentX += slitwidth
  output = Image.fromarray(img)
  st.image(output)   

def one_image_average(slitpoint):
  currentX = 0
  for i in clip.iter_frames(fps=target_fps, dtype='uint8'):
      if currentX < last_frame:
          frame =  i[:,slitpoint:slitpoint + slitwidth,:]
          frame = frame.mean(axis=0).mean(axis=0)
          img[:,currentX:currentX + slitwidth,:] = frame
      currentX += slitwidth
  output = Image.fromarray(img)
  st.image(output)

def one_image_dominant(slitpoint):
  currentX = 0
  for i in clip.iter_frames(fps=target_fps, dtype='uint8'):
      if currentX < last_frame:
          frame =  i[:,slitpoint:slitpoint + slitwidth,:]
          colors, count = np.unique(frame, axis=0, return_counts=True)
          frame = np.array(colors[count.argmax()], dtype='uint8')
          img[:,currentX:currentX + slitwidth,:] = frame
      currentX += slitwidth
  output = Image.fromarray(img)
  st.image(output)

mode = st.radio('Select', ['Normal','Average','Dominant'])

if st.button('Generate img'):
    if mode == "Normal":
        one_image(slitpoint)
    elif mode == "Average":
        one_image_average(slitpoint)
    elif mode == "Dominant":
        one_image_dominant(slitpoint)