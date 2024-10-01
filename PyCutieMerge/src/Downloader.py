import requests
import logging
import os
import re

from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from time import sleep

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.join(SCRIPT_DIR, ".temp")

BASE_URL = "https://база.магиядружбы.рф/"

def sanitize_filename(filename):
    """
    Удаляет недопустимые символы из имени файла.

    Args:
        filename (str): Имя файла.

    Returns:
        str: Очищенное имя файла.
    """
    invalid_chars = r'[\\/:*?"<>|]'  # Запрещенные символы в Windows
    sanitized_filename = re.sub(invalid_chars, '', filename)

    if sanitized_filename != filename:
        logging.info(f"Из названия серии удалены недопустимые символы: '{filename}' -> '{sanitized_filename}'")

    return sanitized_filename


def DownloadFile(url, filename): # фикс
    """
    Скачивает файл по заданному URL и сохраняет его с указанным именем,
    используя многопоточную загрузку.

    Args:
        url (str): URL файла для скачивания.
        filename (str): Имя файла для сохранения.
        num_threads (int, optional): Количество потоков для загрузки. Defaults to 4.
    """

    from Config import max_retries, num_threads, timeout

    try:
        logging.info(f"Максимальное количество повторных попыток при ошибке загрузки: {max_retries}")
        logging.info(f"Число потоков для скачивания: {num_threads}")
        with requests.Session() as session:
            response = session.head(url, timeout=timeout)
            response.raise_for_status()
            file_size = int(response.headers.get('content-length', 0))

            chunk_size = file_size // num_threads
            chunks = [(i * chunk_size, (i + 1) * chunk_size - 1) for i in range(num_threads - 1)]
            chunks.append(((num_threads - 1) * chunk_size, file_size - 1))

            with ThreadPoolExecutor(max_workers=num_threads) as executor, open(filename, 'wb') as f:
                futures = []
                t = tqdm(total=file_size, unit='iB', unit_scale=True, desc=filename)

                def download_chunk(start, end, retry_count=0):
                    try:
                        headers = {'Range': f'bytes={start}-{end}'}
                        response = session.get(url, headers=headers, stream=True)
                        response.raise_for_status()
                        for data in response.iter_content(chunk_size=1024):
                            t.update(len(data))
                            f.seek(start)
                            f.write(data)
                            start += len(data)
                    except requests.exceptions.RequestException as e:
                        logging.error(f"Ошибка при загрузке фрагмента: {e}")
                        if retry_count < max_retries:
                            logging.info(f"Повторная попытка загрузки фрагмента (попытка {retry_count + 1})...")
                            sleep(1)  # Пауза перед повторной попыткой
                            download_chunk(start, end, retry_count + 1)
                        else:
                            logging.error(f"Не удалось загрузить фрагмент после {max_retries} попыток.")
                            raise  # Передать исключение дальше

                for start, end in chunks:
                    futures.append(executor.submit(download_chunk, start, end))

                for future in futures:
                    future.result()

                t.close()

        logging.info(f"Файл '{filename}' успешно скачан.")
        return True

    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при скачивании файла '{filename}': {e}")
        return False


def download_video(season, episode, quality):
    if int(quality) <= 1080:
        ext = "mp4"
    else:
        ext = "webm"
    url = f"{BASE_URL}video/G4/FiM/media/s{season}/e{episode}/{quality}.{ext}"
    filename = os.path.join(TEMP_DIR, f"video.{ext}")
    logging.info("Скачивание видео...")
    return DownloadFile(url, filename)


def download_audio(season, episode, dub_code):
    url = f"{BASE_URL}video/G4/FiM/media/s{season}/e{episode}/{dub_code}.opus"
    filename = os.path.join(TEMP_DIR, "audio.opus")
    logging.info("Скачивание аудио...")
    return DownloadFile(url, filename)


def download_subs(season, episode, subs_code):
    url = f"{BASE_URL}video/G4/FiM/media/s{season}/e{episode}/{subs_code}.ass"
    filename = os.path.join(TEMP_DIR, "subs.ass")
    logging.info("Скачивание субтитров...")
    return DownloadFile(url, filename)