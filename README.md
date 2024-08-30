## Описание

Этот скрипт автоматически объединяет видео, аудио и субтитры в один файл формата `.mkv`, используя утилиту `ffmpeg`. Скрипт был специально разработан для работы с файлами, загруженными с [Магия дружбы](https://xn--80acfekkz0b1a6ftb.xn--p1ai/%D1%81%D1%82%D0%B0%D1%84%D1%84/%D0%B2%D0%B8%D0%B4%D0%B5%D0%BE/MLP-FiM/), но может быть использован для любых других совместимых файлов.

## Важно

Скрипт работает только с исходными .webm видео. Видео в этом формате на сайте доступны только для 2K и 4K качества. Также учитывайте, что субтитры и аудио должны быть только в форматах .ass и .opus соответственно. Однако, вы можете изменить скрипт под себя

## Требования

- Установленный [FFmpeg](https://ffmpeg.org/download.html).

## Как использовать?
### 1. Скачивание файлов

1) Переходим на сайт [Магия дружбы](https://xn--80acfekkz0b1a6ftb.xn--p1ai/%D1%81%D1%82%D0%B0%D1%84%D1%84/%D0%B2%D0%B8%D0%B4%D0%B5%D0%BE/MLP-FiM/). Выбираем нужный сезон и серию
2) В инструментах разработчика (F12) с помощью указателя жмем на плеер
![](1.png)
3) В инструментах разработчика в панели элементов появится часть кода. Из него нам нужны несколько строк со ссылками на видео и аудио ![](2.png)

4) Копируем ссылки после src=. Важно заранее выбрать качество и озвучку, в которых вы хотите скачать эпизод.
5) Вставляем ссылки поочередно в браузер, скачивание должно начаться само. Либо можете воспользоваться программой IDM
6) Для скачивания субтитров можно перейти на [TDT](https://thedoctorteam.ru/project/mlp), где из нужной серии скачать субтитры в формате .ass на нужном вам языке. 
7) Для скачивания субтитров можно воспользоваться альтернативным способом, оставаясь на сайте магия дружбы:
	- Переходим в вкладку Network в инструментах разработчика, затем в плеере выбираем нужные субтитры. У вас сразу появится в списке файл с расширением .ass. Если возникают проблемы с поиском, воспользуйтесь сочетанием клавиш Ctrl + F и найдите файл с этим расширением
	- Жмем на наши субтитры и переходим в раздел Prewiev, откуда все копируем и вставляем в текстовый файл на нашем компьютере. Называем файл как хотим и ставим расширение .ass
### 2. Настройка скрипта

1) Помещаем все файлы в одну папку для удобства, копируем ее путь и вставляем его в Batch файл вместо моего "D:\Поняший архив" в строке 6:
   `cd /d "D:\Поняший архив"`
2) Вам также нужно иметь установленный ffmpeg. Если не меняли папку при его установке, то все сработает правильно. Однако вы можете поменять путь для ffmpeg в строке 5:
   `set "FFMPEG_PATH=C:\Program Files (x86)\FFmpeg\bin"`
### 3. Использование Batch файла

1. При запуске скрипт попросит вас выбрать файлы видео, аудио и субтитров из указанной папки.
2. После выбора файлов, скрипт предложит склеить их в один `.mkv` файл. Подтвердите действие, набрав `y` и нажав Enter.
3. По завершении склеивания будет предложено удалить исходные файлы. Если вы хотите их сохранить, выберите `n`.


