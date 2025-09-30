import os
import subprocess
import logging
from celery import shared_task
from app.models import Sound
from app.downloader import download_and_convert, upload_to_telegram
from telepad.settings import MEDIA_ROOT


@shared_task
def download_sound(user_id: int, url: str):
    path = None
    try:
        path, title, duration = download_and_convert(url, user_id)

        file_id = upload_to_telegram("/media/" + path, title, duration)

        sound = Sound.objects.create(
            owner=user_id,
            name=title,
            file_id=file_id,
            duration=duration,
            is_private=True,
        )
        sound.saves.add(user_id)

        return {
            "status": "ok",
            "sound_id": sound.id,
            "name": sound.name,
        }
    except Exception as error:
        return {
            "status": "failed",
            "detail": str(error),
        }


@shared_task
def upload_sound(user_id: int, temp_file, filename):
    return
#     basename, _ = os.path.splitext(filename)
#     output_file = os.path.join(MEDIA_ROOT, f"{basename}.ogg")

#     command = [
#         "ffmpeg",
#         "-i",
#         temp_file,
#         "-c:a",
#         "libopus",
#         "-ar",
#         "48000",
#         "-ac",
#         "1",
#         "-b:a",
#         "48k",
#         output_file,
#     ]

#     try:
#         file_id = upload_to_telegram("/media/" + output_file, title, duration)

#         subprocess.run(command, check=True, capture_output=True, text=True)
#         sound = Sound.objects.create(
#             owner=user_id,
#             name=basename,
#             file=file_id,
#             duration=duration,
#             is_private=True,
#         )

#         return {
#             "status": "ok",
#             "sound_id": sound.id,
#             "name": sound.name,
#         }

#     except subprocess.CalledProcessError as error:
#         return {
#             "status": "failed",
#             "detail": str(error.stderr),
#         }

#     finally:
#         if os.path.exists(temp_file):
#             os.remove(temp_file)
#             logging.info("Cleaned up temp file.")
