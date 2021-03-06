import pytest
import os.path as ospath
import duplicate_audio.mp3BasicRead as mbr


EXISTING_SINGLE_MP3 = \
    "./resources/Aina_Haina_-_Foolin_Around_Mix_Instrumental.mp3"
EXISTING_SINGLE_MP3_2 = \
    "./resources/Aina_Haina_-_Foolin_Around_Mix_Instrumental 2.mp3"
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
    res = mbr.read_single_mp3(EXISTING_SINGLE_MP3)
    assert res["abs_file_path"] == ospath.abspath(EXISTING_SINGLE_MP3)


def test_read_list_mp3_nosave():
    res = mbr.read_list_mp3([EXISTING_SINGLE_MP3, EXISTING_SINGLE_MP3_2])
    assert len(res) == 2
