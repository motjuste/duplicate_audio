import pytest
import duplicate_audio.wavBasicRead as wbr


EXISTING_SINGLE_WAV = \
    "./resources/Aina_Haina_-_Foolin_Around_Mix_Instrumental.wav"
NON_EXISTING_SINGLE_WAV = \
    "./resources/NOT_Aina_Haina_-_Foolin_Around_Mix_Instrumental.wav"
EXISTING_SINGLE_MP3 = \
    "./resources/Aina_Haina_-_Foolin_Around_Mix_Instrumental.mp3"


def test_read_existing_single_wav():
    '''
    reading an existing wav file through the read_single_wav
    should not raise exception
    '''
    wbr.read_single_wav(EXISTING_SINGLE_WAV)


def test_read_nonexisting_single_wav():
    '''
    reading a non-existing wav file through the read_single_wav
    should raise IOError
    '''
    with pytest.raises(FileNotFoundError):
        wbr.read_single_wav(NON_EXISTING_SINGLE_WAV)


def test_read_existing_single_mp3():
    '''
    reading an existing MP3 through the read_single_wav
    should raise ValueError
    '''
    with pytest.raises(ValueError):
        wbr.read_single_wav(EXISTING_SINGLE_MP3)


def test_read_single_wav_samplingFreq():
    '''
    result of reading an existing WAV has sampling frequency
    EXISTING_SINGLE_WAV above has known sampling freq of 44100
    '''
    result = wbr.read_single_wav(EXISTING_SINGLE_WAV)

    assert result["sampling_frequency"] == 44100
