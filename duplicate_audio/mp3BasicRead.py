'''
Utility functions to read mp3 files

USES ffmpeg for mp3 to wav conversions
'''
import os
import ntpath
import subprocess

FFMPEG_BIN = "ffmpeg" if os.name == 'posix' else "ffmpeg.exe"


def convert_single_mp3ToWav(file_path, save_to_dir=None):
    '''
    reads a single mp3 file, converts and saves as WAV
    new file is saved in a sub directory called 'wav' if save_to_dir is None.
    saved file has same file name, except the extension
    name clashes are ignored and overwritten, for now
    '''
    # TODO: @motjuste: handle name clashes better in mp3ToWav?
    # extract filename and extension, and check if mp
    file_name, file_ext = os.path.splitext(os.path.basename(file_path))
    assert file_ext == ".mp3", "File is not an MP3"

    # Set save_to_dir if not given
    if save_to_dir is None:
        save_to_dir = os.path.dirname(file_path) + os.sep + "wav"

    if not os.path.isdir(save_to_dir):
        print(save_to_dir, "does not exit, creating one")
        os.makedirs(save_to_dir)

    new_wav_file_path = save_to_dir + os.sep + file_name + ".wav"
    if os.path.exists(new_wav_file_path):
        print(new_wav_file_path, "already exists, will be replaced")

    # Convert mp3 to wav using ffmpeg
    command = [FFMPEG_BIN,
               '-i', os.path.abspath(file_path),  # Input file
               '-y',  # overwrite if already exists
               os.path.abspath(new_wav_file_path)]
    subprocess.call(command, stderr=subprocess.STDOUT)
    # TODO: @motjuste: handle any errors while using ffmpeg
