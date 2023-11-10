import streamlit as st
import ffmpeg

from pydub import AudioSegment
from tempfile import NamedTemporaryFile

def find_loudest_timestamps(audio, num_timestamps):
    loudest_timestamps = []
    for _ in range(num_timestamps):
        loudest_position = audio.dBFS
        loudest_time = 0
        chunk_duration = 1000  # 1 second
        for start in range(0, len(audio), chunk_duration):
            chunk = audio[start:start + chunk_duration]
            if chunk.dBFS > loudest_position:
                loudest_position = chunk.dBFS
                loudest_time = start / 1000  # Convert milliseconds to seconds

        loudest_timestamps.append(loudest_time)

        # Remove the loudest part to avoid selecting it again
        audio = audio[:int(loudest_time * 1000)] + audio[int((loudest_time + 1) * 1000):]

    return loudest_timestamps

def main():
    st.title("Audio Analyzer")
    audio_file = st.file_uploader("Upload your mp3", type=['mp3'])
    num_timestamps = st.number_input("Number of timestamps to find", min_value=1, value=10, step=1)
    
    if audio_file is not None and num_timestamps is not None:
        tfile = NamedTemporaryFile(delete=False) 
        tfile.write(audio_file.read())
        audio = AudioSegment.from_mp3(tfile.name)

        # Find the loudest timestamps
        loudest_timestamps = find_loudest_timestamps(audio, num_timestamps)

        # Print the timestamps
        st.write(f"Top {num_timestamps} Loudest Timestamps (in seconds):", loudest_timestamps)
            
if __name__ == "__main__":
    main()
