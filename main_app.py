import streamlit as st
from pytube import YouTube
import ffmpeg
import io
from moviepy.editor import AudioFileClip
import os
from tempfile import NamedTemporaryFile

st.title('YouTube Converter')


st.write('拡張子:mp4')

# URL入力
input_url = st.text_input('URLを入力してください')


# YouTubeの動画をMP4としてダウンロード
def dl_as_mp4(link):
    try:
        yt = YouTube(link)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        if stream:
            video_bytes = io.BytesIO()
            stream.stream_to_buffer(video_bytes)
            video_bytes.seek(0)
            return video_bytes, stream.default_filename
        else:
            return None, "No suitable stream found."
    except Exception as e:
        return None, str(e)

# ダウンロードと変換の実行
if input_url:
    video_data, filename = dl_as_mp4(input_url)
    if video_data:
        st.download_button("Download MP4", video_data, file_name=filename, mime='video/mp4')

st.write('拡張子:mp3')
uploaded_file = st.file_uploader("動画ファイルをアップロードしてください", type=['mp4'])

if uploaded_file is not None:
    # アップロードされたファイルを一時的に保存
    temp_video_path = uploaded_file.name
    with open(temp_video_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # MP3ファイルへの変換
    try:
        video_clip = AudioFileClip(temp_video_path)
        mp3_path = temp_video_path.replace(".mp4", ".mp3")
        video_clip.write_audiofile(mp3_path)
        video_clip.close()
        
        # MP3ファイルをダウンロードするためのリンクを提供
        with open(mp3_path, "rb") as mp3_file:
            st.download_button(label="Download MP3", data=mp3_file, file_name=os.path.basename(mp3_path), mime="audio/mpeg")
        
        # 変換後の一時ファイルを削除
        os.remove(temp_video_path)
        os.remove(mp3_path)
    except Exception as e:
        st.error(f"変換エラー: {e}")
