# from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
# from moviepy.editor import VideoFileClip
#
# # Путь к исходному видеофайлу
# source_video = 'C:\\scrap_tutorial-master\\Temp\\video\\Kubernetes.mp4'
#
# # Определение длины видео
# clip = VideoFileClip(source_video)
# duration = clip.duration
# clip.close()
#
# # Определение длительности каждого маленького файла
# segment_duration = 15  # 15 секунд
#
# # Разделение видео на маленькие части
# for start_time in range(0, int(duration), segment_duration):
#     end_time = start_time + segment_duration
#     if end_time > duration:
#         end_time = duration
#     output_file = f"output_{start_time}_{end_time}.mp4"
#     ffmpeg_extract_subclip(source_video, start_time, end_time, targetname=output_file)
#     print(f"Создан файл: {output_file}")
#
# print("Завершено!")
from moviepy.editor import VideoFileClip

# Путь к исходному видеофайлу
source_video = 'C:\\scrap_tutorial-master\\Temp\\video\\Kubernetes.mp4'

# Определение длины видео
clip = VideoFileClip(source_video)
duration = clip.duration

# Определение длительности каждого маленького файла
segment_duration = 15  # 15 секунд

# Разделение видео на маленькие части
for start_time in range(0, int(duration), segment_duration):
    end_time = start_time + segment_duration
    if end_time > duration:
        end_time = duration
    output_file = f"output_{start_time}_{end_time}.mp4"
    subclip = clip.subclip(start_time, end_time)
    subclip.write_videofile(output_file, codec="libx264")
    print(f"Создан файл: {output_file}")

clip.close()
print("Завершено!")
