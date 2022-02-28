from pydub import AudioSegment
from pydub.silence import split_on_silence
import random
import pandas as pd
from itertools import combinations, combinations_with_replacement
from tqdm import tqdm
from multiprocessing import Pool

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
    percent_overlay = random.randint(10, 90)
    position = dur * percent_overlay * 0.01
    return percent_overlay, position

def get_naming(wav1, wav2, wav3, percent_overlay1, percent_overlay2):
    ### Example input naming -> wav48/p265/p265_005.wav
    ### Example output naming -> p265
    name_1 = wav1.split('/')[1]
    name_2 = wav2.split('/')[1]
    name_3 = wav3.split('/')[1]
    return 'spekaers-{}_{}_{}-First_percentOverlay-{}-Second_percentOverlay-{}'.format(name_1, name_2, name_3, percent_overlay1, percent_overlay2)

def get_path_for_speaker(data, speaker):
    ### Example data file ->        0                1
    ###                     'audio_wav_path' | name_speaker
    ### Example output list -> [path1, path2]
    data = data[data[1] == speaker] 
    wav_path_array = data[0].unique()
    return list(wav_path_array)

def mix_audio(wav1, wav2, wav3):
    ### Get_duration and clear silence
    sound1 = clear_silence(AudioSegment.from_file(wav1))
    sound2 = clear_silence(AudioSegment.from_file(wav2))
    dur_1 = sound1.frame_count() / sound1.frame_rate * 1000
    dur_2 = sound2.frame_count() / sound2.frame_rate * 1000
    sound3 = clear_silence(AudioSegment.from_file(wav3))
    dur_3 = sound3.frame_count() / sound3.frame_rate * 1000


    ### Get position and percent overlay
    percent_overlay_1, get_position_1 = get_position_and_percent_Overlay(dur_1)
    percent_overlay_2, get_position_2 = get_position_and_percent_Overlay(dur_1 + dur_2 - get_position_1)

    ### Create audio with final duration
    silence = AudioSegment.silent(duration = (dur_1 + dur_2 - get_position_1) + dur_3 - get_position_2)

    ### Get naming audio
    save_name_audio = get_naming(wav1, wav2, wav3, percent_overlay_1, percent_overlay_2)

    ### Save overlay audio
    output = silence.overlay(sound1).overlay(sound2, position = dur_1 - get_position_1).overlay(sound3, dur_1 + dur_2 - get_position_1 - get_position_2)
    output.set_frame_rate(16000).set_channels(1).export('wavs_overlay_3speakers/' + save_name_audio + '.wav', format='wav')
    silence.overlay(sound1).set_frame_rate(16000).set_channels(1).export('spk1/' + save_name_audio + '.wav', format='wav')
    silence.overlay(sound2, position = dur_1 - get_position_1).set_frame_rate(16000).set_channels(1).export('spk2/' + save_name_audio + '.wav', format='wav')
    silence.overlay(sound3, dur_1 + dur_2 - get_position_1 - get_position_2).set_frame_rate(16000).set_channels(1).export('spk3/' + save_name_audio + '.wav', format='wav')
    

    ### metadata about overlay audio
    data = {}
    data['audioname'] = save_name_audio
    data['first_audio_timestamp'] = [0, dur_1]
    data['second_audio_timestamp'] = [dur_1 - get_position_1, dur_1 - get_position_1 + dur_2]
    data['third_audio_timestamp'] = [dur_1 - get_position_1 + dur_2 - get_position_2, dur_1 - get_position_1 + dur_2 - get_position_2 + dur_3]
    data['percent_overlay_1'] = percent_overlay_1
    data['percent_overlay_2'] = percent_overlay_2
    return data

metadata = []
items = list(combinations(data[1].unique(), 3))
pool = Pool(processes=12)

processes = []
for item in tqdm(items[:50000]):
    wavs_1st_speaker = random.choice(get_path_for_speaker(data, item[0]))
    wavs_2nd_speaker = random.choice(get_path_for_speaker(data, item[1]))
    wavs_3rd_speaker = random.choice(get_path_for_speaker(data, item[2]))
    processes.append(pool.apply_async(mix_audio, (wavs_1st_speaker, wavs_2nd_speaker, wavs_3rd_speaker)))

results = []
for process in tqdm(processes):
    results.append(process.get())
    
data = pd.DataFrame(data=results)
data.to_csv('O3MS.csv', index=False, sep='|')
