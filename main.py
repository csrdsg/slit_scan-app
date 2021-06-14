import streamlit as st
import numpy as np
import pandas as pd
from moviepy.editor import VideoFileClip
from PIL import Image
import glob
import tempfile

st.title('Slit Scan')
f = st.file_uploader("Upload file") 


def load_data():
    tfile = tempfile.NamedTemporaryFile(delete=False) 
    tfile.write(f.read())
    clip = VideoFileClip(tfile.name)
    img = np.zeros((clip.size[1], clip.size[0], 3), dtype='uint8')
    target_fps = clip.size[0] / clip.duration
    slitwidth = 1
    slitpoint = clip.size[0] // 2
    last_frame = clip.size[0] - slitwidth
    currentX = 0
    for i in clip.iter_frames(fps=target_fps, dtype='uint8'):
        if currentX < last_frame:
            img[:,currentX:currentX + slitwidth,:] = i[:,slitpoint:slitpoint + slitwidth,:]
        currentX += slitwidth
    output = Image.fromarray(img)
    st.image(output)

data_load_state = st.text('Loading data...')
if st.button('Press'):
    data = load_data()
data_load_state.text("Done! (using st.cache)")