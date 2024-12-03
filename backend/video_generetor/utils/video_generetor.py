from spire.presentation.common import *
from spire.presentation import *
from gtts import gTTS
from moviepy import ImageClip, concatenate_videoclips, AudioFileClip
import os
from typing import List, Tuple
from datetime import datetime


# GIVE PATH TO PPTX FILES AND SCRIPTS
def convert_pptx_to_png(pptx_file: str) -> str:
    try:
        presentation = Presentation()
        presentation.LoadFromFile(pptx_file)
        
        png_file = f"slide_{os.path.splitext(os.path.basename(pptx_file))[0]}.png"
        image = presentation.Slides[0].SaveAsImage()
        image.Save(png_file)
        
        image.Dispose()
        presentation.Dispose()
        return png_file
    except Exception as e:
        print(f"Error converting {pptx_file}: {str(e)}")
        return None

def create_audio_file(script: str, index: int) -> str:
    try:
        audio_file = f"audio_{index}.mp3"
        tts = gTTS(text=script, lang='en')
        tts.save(audio_file)
        return audio_file
    except Exception as e:
        print(f"Error creating audio file {index}: {str(e)}")
        return None

def process_files(pptx_files: List[str], scripts: List[str]) -> Tuple[List[str], List[str]]:
    # print(pptx_files)
    # print("process_to png and audio start")
    # print(datetime.now().strftime("%H:%M:%S"))
    png_files, audio_files = [], []

    # print(os.getcwd())
    for file in pptx_files:
        result = convert_pptx_to_png(file)
        if result:
            png_files.append(result)

    for idx, script in enumerate(scripts):
        result = create_audio_file(script, idx)
        if result:
            audio_files.append(result)

    # print("process_to png and audio done")
    # print(datetime.now().strftime("%H:%M:%S"))
    return sorted(png_files), sorted(audio_files)

def create_video_clip(files: Tuple[str, str]) -> ImageClip:
    png_file, audio_file = files
    try:
        img_clip = ImageClip(png_file)
        audio_clip = AudioFileClip(audio_file)
        img_clip.duration = (audio_clip.duration)
        img_clip.audio= (audio_clip)

        return img_clip
    except Exception as e:
        print(f"Error creating clip for {png_file}: {str(e)}")
        return None

def process_clips(png_files: List[str], audio_files: List[str]) -> List[ImageClip]:
    # print("create_video_start")
    # print(datetime.now().strftime("%H:%M:%S"))
    file_pairs = list(zip(png_files, audio_files))
    video_clips = []
    
    for pair in file_pairs:
        clip = create_video_clip(pair)
        if clip is not None:
            video_clips.append(clip)
    # print("create_video_done")
    # print(datetime.now().strftime("%H:%M:%S"))
    
    return video_clips

def create_video(png_files: List[str], audio_files: List[str]):
    if len(png_files) != len(audio_files):
        print("Mismatch between number of slides and audio files.")
        return

    try:
        video_clips = process_clips(png_files, audio_files)
        
        if video_clips:
            final_video = concatenate_videoclips(video_clips, method="compose")
            
            video_dir = "videos"
            if not os.path.exists(video_dir):
                os.makedirs(video_dir)
            
            video_file = os.path.join(video_dir, "final_video.mp4")
            final_video.write_videofile(video_file, fps=24)
            final_video.close()

    finally:
        for clip in video_clips:
            try:
                clip.close()
            except:
                pass

def cleanup_temp_files(files: List[str]):
    for file in files:
        try:
            os.remove(file)
        except OSError as e:
            print(f"Error removing file {file}: {e}")

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dir = base_dir + "/pptx_out"
    pptx_files = [f"{dir}/ppt1.pptx", f"{dir}/ppt2.pptx", f"{dir}/ppt3.pptx", f"{dir}/ppt4.pptx"]
    scripts = [
         """In analyzing Player A's potential for success in the upcoming match, we first look at his recent form. With a form index of 80 and an impressive batting average of 50.0, it's evident that he is currently in good touch with the bat. His previous runs of 400 in 10 innings, along with a strike rate of 114.29, indicate a strong ability to score quickly and consistently.

Moreover, when considering Player A's history of performance, his consistency index of 70 highlights his ability to deliver solid results match after match. With 40 boundaries and 10 sixes in his last few innings, he has shown the capability to score runs in various ways, showcasing his versatility as a batter.

Lastly, an important aspect to consider is the analysis of the opposition team. Facing Team B, Player A has an opposition performance index of 60. By examining the bowlers he has previously faced and their stats, we can determine the best strategies for him to succeed against them in the upcoming match.
""",
    "This is the script for slide 2.",
    """In analyzing Player A's potential for success in the upcoming match, we first look at his recent form. With a form index of 80 and an impressive batting average of 50.0, it's evident that he is currently in good touch with the bat. His previous runs of 400 in 10 innings, along with a strike rate of 114.29, indicate a strong ability to score quickly and consistently.

Moreover, when considering , an important aspect to consider is the analysis of the opposition team. Facing Team B, Player A has an opposition performance index of 60. By examining the bowlers he has previously faced and their stats, we can determine the best strategies for him to succeed against them in the upcoming match.
""",
    "This is the script for slide 4."
    ]

    png_files, audio_files = process_files(pptx_files, scripts)

    try:
        create_video(png_files, audio_files)
    except Exception as e:
        print(f"Error during video creation: {e}")
    finally:
        cleanup_temp_files(png_files + audio_files)

if __name__ == "__main__":
    main()