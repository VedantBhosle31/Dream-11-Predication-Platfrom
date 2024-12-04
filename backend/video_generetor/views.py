from django.shortcuts import render
from django.http import FileResponse, HttpResponse, JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import os
import shutil
import json
from video_generetor.utils.ppt_generator import generate_ppts
from video_generetor.utils.scripts_generetor import get_explainable_data
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
        
@csrf_exempt
def generate_pptx_images_and_audio(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get("name", "Virat Kohli")
        match_date = data.get("match_date", "2024-12-14")
        format = data.get("format", "Odi")
        team = data.get("team", "India")
        predictions = data.get("predictions", {})
        player_type = data.get("player_type", "Batter")

        try:    
            try:
                ppts = generate_ppts(name, match_date, format, team, predictions)
            except Exception as e:
                return JsonResponse({"status": "Error in generating ppts", "message": str(e)}, status=500)
            pptx_files = [f"video_generetor/utils/pptx_out/ppt{i}" for i in range(1, 5)]
            scripts = get_explainable_data(name, match_date, format, player_type)
            png_files, audio_files = process_files(pptx_files, scripts)
            return JsonResponse({"status": "success", "png_files": png_files, "audio_files": audio_files})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)