from pytube import YouTube
from fastapi import FastAPI, HTTPException, status, Response, Depends
from io import BytesIO
from fastapi.responses import StreamingResponse
from database import Base, engine, get_db
import models
from sqlalchemy.orm import Session

app = FastAPI(title="YouTube Video and Audio Downloader")


models.Base.metadata.create_all(bind=engine)

# Define the video download endpoint
@app.post('/download/video')
def video_download(link: str, quality: str = "highest", db:Session=Depends(get_db)):
    # Download the video
    video = YouTube(link)
    videos = video.streams.filter(file_extension='mp4')
    if quality == "highest":
        selected_video = videos.get_highest_resolution()
    elif quality == "lowest":
        selected_video = videos.get_lowest_resolution()
    else:
        selected_video = None
        for v in videos:
            if quality in str(v):
                selected_video = v
                break
        if not selected_video:
            return {"message": "Invalid quality selected"}

    # Download the file as bytes
    buffer = BytesIO()
    selected_video.stream_to_buffer(buffer)
    file_bytes = buffer.getvalue()


    # Save the video metadata and download information in the database
    video_data = models.Video(
        url=link,
        file=file_bytes,
        title=video.title,
        author=video.author,
        length=video.length,
        filesize=selected_video.filesize,
        filename=selected_video.default_filename
    )
    db.add(video_data)
    db.commit()
    db.refresh(video_data)

    # Return the video file as a download
    response = StreamingResponse(BytesIO(file_bytes), media_type='video/mp4')
    response.headers['Content-Disposition'] = 'attachment; filename="%s"' % selected_video.default_filename
    return response
    


# Define the audio download endpoint
@app.post('/download/audio')
def audio_download(link: str, db:Session=Depends(get_db)):
    # Download the video
    video = YouTube(link)
    audio_streams = video.streams.filter(only_audio=True, file_extension='mp4')
    selected_audio = audio_streams.filter(abr='128kbps').first()

    
    # Download the file as bytes
    buffer = BytesIO()
    selected_audio.stream_to_buffer(buffer)
    file_bytes = buffer.getvalue()

    # Save the video metadata and download information in the database
    audio_data = models.Audio(
        url=link,
        file=file_bytes,
        title=video.title,
        author=video.author,
        length=video.length,
        filesize=selected_audio.filesize,
        filename=selected_audio.default_filename
    )
    db.add(audio_data)
    db.commit()
    db.refresh(audio_data)

    # Return the audio file as a download
    response = StreamingResponse(BytesIO(file_bytes), media_type='audio/mp4')
    response.headers['Content-Disposition'] = 'attachment; filename="%s"' % selected_audio.default_filename
    return response
