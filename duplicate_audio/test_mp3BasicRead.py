import pytest
import duplicate_audio.mp3BasicRead as mbr


EXISTING_SINGLE_MP3 = \
    "./resources/Aina_Haina_-_Foolin_Around_Mix_Instrumental.mp3"
NON_EXISTING_SINGLE_MP3 = \
    "./resources/NOT_Aina_Haina_-_Foolin_Around_Mix_Instrumental.mp3"
EXISTING_SINGLE_NOT_MP3 = \
    "./resources/Aina_Haina_-_Foolin_Around_Mix_Instrumental.wav"


def test_convert_existing_single_mp3ToWav():
    '''
    calling convert_single_mp3ToWav for existing file
    should not raise an exception
    '''
    mbr.convert_single_mp3ToWav(EXISTING_SINGLE_MP3)


def test_read_single_mp3_nosave():
    mbr.read_single_mp3(EXISTING_SINGLE_MP3)
