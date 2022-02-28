# O3MS_OSID_datasets

## OSID

Датасет представляет из себя аудиодорожки двух спикеров, наложенные друг на друга с рандомным процентом наложения ( от 5 до 10 )

Имя датасета - Overlay_speakerID_dataset

Датасет строился на основе VCTK. 

Для каждого спикера брались 2 аудиофайла длительностью > 5 секунд

Количество получившихся аудиофайлов - 21012

Характеристика аудиофайлов:
* channels = 1
* sample_rate = 16000
* 
Пример метадаты для одной дорожки:
* audioname = str
* first_audio_timestamp = []
* second_audio_timestamp = []
* percent_overlay = int

Структура датасета

* OSID
  - OSID_create.py
  - OSID_create.ipynb
  - metadatas/
    - OSID.csv
  - wavs_overlay/
    *  first.wav
   ...
    *  last.wav


## O3MS


Датасет представляет из себя аудиодорожки трех спикеров, наложенные друг на друга с рандомным процентом наложения ( от 10 до 90 )

Имя датасета - ?

Датасет строился на основе VCTK. 

Было взято 20 мужских и 20 женских спикеров.

Были составлены тройки разных спикеров. Для каждого спикера была случайным образом выбрана аудиодорожка, которые были склеены с различными процентами overlap/overlay.

Количество получившихся аудиофайлов - 59280

Характеристика аудиофайлов:
* channels = 1
* sample_rate = 16000

Пример метадаты для одной дорожки:
* audioname = str
* first_audio_timestamp = []
* second_audio_timestamp = []
* third_audio_timestamp = []
* percent_overlay_1 = int
* percent_overlay_2 = int

Структура датасета
* O3MS
  - O3MS_create.py
  - O3MS_create.ipynb
  - metadatas/
    - O3MS.csv
  - wavs_overlay_3speakers/
    - first.wav
    ...
    - last.wav
  - spk1/
    - first.wav
    ...
    - last.wav
  - spk2/
    - first.wav
    ...
    - last.wav
  - spk3/
    - first.wav
    ...
    - last.wav
