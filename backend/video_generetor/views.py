from django.shortcuts import render
from django.http import FileResponse, HttpResponse
from django.conf import settings
import os
import shutil
from utils.video_generetor import process_files, create_video, cleanup_temp_files

def generate_video(request):
    if request.method == 'GET':
        try:
            pptx_files = ["video_generetor/utils/pptx_template/batting1.pptx", "video_generetor/utils/pptx_template/batting2.pptx", "video_generetor/utils/pptx_template/batting3.pptx", "video_generetor/utils/pptx_template/batting4.pptx"]
            scripts = [
                """In analyzing Player A's potential...""",  
                "This is the script for slide 2.",
                """In analyzing Player A's potential...""",
                "This is the script for slide 4."
            ]
            png_files, audio_files = process_files(pptx_files, scripts)
            # print(png_files)
            # print(audio_files)
            create_video(png_files, audio_files)
            video_path = os.path.join("videos", "final_video.mp4")
            
            if not os.path.exists(video_path):
                return HttpResponse("Video generation failed", status=500)
            video = open(video_path, 'rb')
            response = FileResponse(video, content_type='video/mp4')
            response['Content-Disposition'] = 'attachment; filename="final_video.mp4"'
            def cleanup():
                video.close()
                if os.path.exists("videos"):
                    shutil.rmtree("videos")
                cleanup_temp_files(png_files + audio_files)
            response.close = cleanup
            return response
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}", status=500)
        

