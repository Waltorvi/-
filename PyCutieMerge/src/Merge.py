import subprocess
import logging
import os
import shutil

DOWNLOADS_DIR = os.path.join(os.path.expanduser("~"), "Downloads")
TEMP_DIR = os.path.join(DOWNLOADS_DIR, ".temp")

def merge_video_audio_subs(video_filename, audio_filename, subs_filename=None, output_filename="output.mkv"):
    """
    Объединяет видео, аудио и субтитры (опционально) с помощью ffmpeg.

    Args:
        video_filename (str): Путь к видеофайлу.
        audio_filename (str): Путь к аудиофайлу.
        subs_filename (str, optional): Путь к файлу субтитров. Defaults to None.
        output_filename (str, optional): Имя выходного файла. Defaults to "output.mkv".
    """
    try:
        command = [
            "ffmpeg",
            "-i", video_filename,
            "-i", audio_filename,
            "-c:v", "copy",  # Копирование видео без перекодирования
            "-c:a", "copy",  # Копирование аудио без перекодирования
            "-map", "0:v",
            "-map", "1:a",
        ]

        if subs_filename:
            command.extend([
                "-vf", f"subtitles='{subs_filename}'"
            ])

        command.append(output_filename)

        logging.info(f"Запуск ffmpeg: {' '.join(command)}")
        subprocess.run(command, check=True)
        logging.info(f"Видео успешно объединено: {output_filename}")
        return True

    except subprocess.CalledProcessError as e:
        logging.error(f"Ошибка при объединении видео: {e}")
        return False

def cleanup_temp_files():
    """
    Удаляет временные файлы из папки TEMP_DIR.
    """
    try:
        shutil.rmtree(TEMP_DIR)
        os.makedirs(TEMP_DIR)
        logging.info("Временные файлы успешно удалены.")
    except OSError as e:
        logging.error(f"Ошибка при удалении временных файлов: {e}")