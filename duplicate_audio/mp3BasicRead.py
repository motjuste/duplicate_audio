'''
Utility functions to read mp3 files

USES ffmpeg for mp3 to wav conversions
'''
import os


def convert_single_mp3ToWav(file_path, save_to_dir=None):
    '''
    reads a single mp3 file, converts and saves as WAV
    new file is saved in a sub directory called 'wav' if save_to_dir is None.
    saved file has same file name, except the extension
    name clashes are ignored and overwritten, for now
    '''
    # TODO: @motjuste: handle name clashes better in mp3ToWav?
    pass
