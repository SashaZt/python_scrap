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

"""Режет видео на куски"""
# from moviepy.editor import VideoFileClip
#
# # Путь к исходному видеофайлу
# source_video = 'C:\\scrap_tutorial-master\\Temp\\video\\Kubernetes.mp4'
#
# # Определение длины видео
# clip = VideoFileClip(source_video)
# duration = clip.duration
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
#     subclip = clip.subclip(start_time, end_time)
#     subclip.write_videofile(output_file, codec="libx264")
#     print(f"Создан файл: {output_file}")
#
# clip.close()
# print("Завершено!")

import os
from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip, concatenate_audioclips

video_folder = 'c:\\scrap_tutorial-master\\Temp\\video\\Git.mp4'
audio_folder = 'c:\scrap_tutorial-master\\Temp\\mp3\\'
image_folder = 'c:\\scrap_tutorial-master\\Temp\\img\\'
chunk_duration = 15  # В секундах

audio_file = os.path.join(audio_folder, os.listdir(audio_folder)[0])
image_file = os.path.join(image_folder, os.listdir(image_folder)[0])

# Определение длины видео
clip = VideoFileClip(video_folder)
duration = clip.duration

# Разделение видео на маленькие части
for start_time in range(0, int(duration), chunk_duration):
    end_time = start_time + chunk_duration
    if end_time > duration:
        end_time = duration

    subclip = clip.subclip(start_time, end_time)

    # Настроим аудио в соответствии с длительностью видео
    audio = AudioFileClip(audio_file)
    while audio.duration < subclip.duration:
        audio = concatenate_audioclips([audio, AudioFileClip(audio_file)])
    audio = audio.subclip(0, subclip.duration)
    subclip = subclip.set_audio(audio)

    # Размеры исходного видео
    video_width, video_height = subclip.size
    # Проверка, нужно ли преобразовать видео в вертикальный формат
    if video_width > video_height:
        # Преобразование в вертикальный формат, если исходное видео горизонтальное
        new_height = video_width  # Высота станет такой же, как была ширина
        new_width = int(
            video_width * video_height / video_width)  # Ширина будет меньше, чтобы сохранить соотношение сторон
        clip = clip.resize((new_width, new_height)).crop(x_center=new_width / 2, width=video_width, height=video_height)
    # Вычисляем размер изображения как 30% от площади видео
    target_width = int(video_width * (0.3 ** 0.5))
    target_height = int(video_height * (0.3 ** 0.5))

    # Накладываем изображение (водяной знак)
    logo = ImageClip(image_file).set_duration(subclip.duration).resize(width=target_width, height=target_height)

    # Установка положения изображения (если вы хотите его в центре, например)
    center_x = (video_width - target_width) // 2
    center_y = (video_height - target_height) // 2
    logo_position = (center_x, center_y)
    """устанавливает прозрачность для изображения (вашего "водяного знака") на 50%. 
    Значение 1.0 будет соответствовать полной непрозрачности, а 0.0 – полной прозрачности. 
    Таким образом, значение 0.5 делает изображение полупрозрачным."""
    final_clip = CompositeVideoClip([subclip, logo.set_position(logo_position).set_opacity(0.5)])
    # Сохраняем результат
    output_file = os.path.join('C:\scrap_tutorial-master\Temp', f"output_{start_time}_{end_time}.mp4")
    final_clip.write_videofile(output_file, codec="libx264")
    print(f"Создан файл: {output_file}")
