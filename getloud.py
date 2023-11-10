import streamlit as st
import librosa
import numpy as np
from scipy.io import wavfile
import io
import matplotlib.pyplot as plt
from collections import defaultdict
from tempfile import TemporaryFile

def get_loudest_timestamps(file):
    # Load the file as a numpy array with librosa
    data_wav, sr = librosa.load(file, sr=None)

    # Calculate amplitude
    amplitude = np.abs(librosa.stft(data_wav))

    # Find loudest timestamps
    n_loudest = 20
    duration = data_wav.shape[0] / sr
    timestamps = np.linspace(0, duration, amplitude.shape[1])
    loudest_points = np.argpartition(amplitude.mean(axis=0), -n_loudest)[-n_loudest:]
    loudest_timestamps = timestamps[loudest_points]

    return loudest_timestamps

def main():
    st.title('Audio Analysis with Streamlit')
    uploaded_file = st.file_uploader("Upload an audio file", type=['mp3'])

    if uploaded_file is not None:
        audio_file = TemporaryFile()
        audio_file.write(uploaded_file.read())
        audio_file.seek(0)  # Set position to the beginning of the file

        loudest_timestamps = get_loudest_timestamps(audio_file)
        st.write('The loudest timestamps are: ', loudest_timestamps)

if __name__ == "__main__":
    main()
