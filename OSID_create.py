from pydub import AudioSegment
from pydub.silence import split_on_silence
import random
import pandas as pd
from itertools import combinations, combinations_with_replacement
from tqdm import tqdm

def clear_silence(audio):
    audio_data = 0
    dBFS = audio.dBFS
    chunks = split_on_silence(audio,
        min_silence_len = 150,
        silence_thresh = dBFS-16,
        keep_silence = 50
    )
    for chunk in chunks:
        audio_data+=chunk
    return audio_data

def get_position_and_percent_Overlay(dur):
    percent_overlay = random.randint(5, 10)
    position = dur * percent_overlay * 0.01
    return percent_overlay, position

def get_naming(wav1, wav2, percent_overlay):
    ### Example input naming -> wav48/p265/p265_005.wav
    ### Example output naming -> p265
    name_1 = wav1.split('/')[1]
    name_2 = wav2.split('/')[1]
    return 'spekaers-{}_{}_percentOverlay-{}'.format(name_1, name_2, percent_overlay)

def get_path_for_speaker(data, speaker):
    ### Example data file ->        0                1
    ###                     'audio_wav_path' | name_speaker
    ### Example output list -> [path1, path2]
    data = data[data[1] == speaker] 
    wav_path_array = data[0].unique()
    return list(wav_path_array)
    
def mix_audio(wav1, wav2):    
    ### Get_duration and clear silence
    sound1 = clear_silence(AudioSegment.from_file(wav1))
    sound2 = clear_silence(AudioSegment.from_file(wav2))
    dur_1 = sound1.frame_count() / sound1.frame_rate * 1000
    dur_2 = sound2.frame_count() / sound2.frame_rate * 1000
    
    ### Get position and percent overlay
    percent_overlay, get_position = get_position_and_percent_Overlay(dur_1)
    
    ### Create audio with final duration
    silence = AudioSegment.silent(duration = dur_1 + dur_2 - get_position)
    
    ### Get naming audio
    save_name_audio = get_naming(wav1, wav2, percent_overlay)
    
    ### Save overlay audio
    output = silence.overlay(sound1).overlay(sound2, position = dur_1 - get_position)
    output.export('wavs_overlay/' + save_name_audio + '.wav', format='wav')
    
    ### metadata about overlay audio
    data = {}
    data['audioname'] = save_name_audio
    data['first_audio_timestamp'] = [0, dur_1]
    data['second_audio_timestamp'] = [dur_1 - get_position, dur_1 - get_position + dur_2]
    data['percent_overlay'] = percent_overlay
    return data

### Load source metadata  
data = pd.read_csv('all_speaker_2wavs_file_more5sec.csv', header=None, sep='|')

### Create new audios and metadata
full_speaker_pairs = list(combinations(data[1].unique(), 2))
metadata = []
for i in tqdm(full_speaker_pairs):
    wavs_1st_speaker = get_path_for_speaker(data, i[0])
    wavs_2nd_speaker = get_path_for_speaker(data, i[1])
    ### HardCode
    metadata.append(mix_audio( wavs_1st_speaker[0], wavs_2nd_speaker[0] ))
    metadata.append(mix_audio( wavs_1st_speaker[0], wavs_2nd_speaker[1] ))
    metadata.append(mix_audio( wavs_1st_speaker[1], wavs_2nd_speaker[0] ))
    metadata.append(mix_audio( wavs_1st_speaker[1], wavs_2nd_speaker[1] ))
    
data = pd.DataFrame(data=metadata)
data['audioname'] = data['audioname'].apply(lambda x: 'wavs_overlay/' + x + '.wav')
data.to_csv('OSID.csv', sep='|', index=False)
