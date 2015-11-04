'''
Utility functions to read mp3 files

USES ffmpeg for mp3 to wav conversions
'''
import os
import ntpath
import subprocess
import duplicate_audio.wavBasicRead as wbr

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
    ret = subprocess.call(command, stderr=subprocess.STDOUT)
    if ret > 0:
        print("There was an error with ffmpeg")
        print("file: ", file_path)
    # TODO: @motjuste: handle any errors while using ffmpeg
    return new_wav_file_path


# def convert_iter_mp3ToWav(file_paths, save_to_dir=None):
#     return map(convert_single_mp3ToWav, file_paths)
# def convert_list_mp3ToWav(file_paths):
#     return list(convert_iter_mp3ToWav(file_paths))


def read_single_mp3(file_path, save_to_dir=None):
    '''
    Reads single mp3, converts to wav, then reads it using wavBasicRead
    if save_to_dir is None, the intermediate wav file is deleted
    '''
    delete_intermediate = False
    if save_to_dir is None:
        delete_intermediate = True
        save_to_dir = os.path.dirname(file_path) + os.sep + "wav_temp"

    path_to_wav = convert_single_mp3ToWav(file_path, save_to_dir)
    read_wav = wbr.read_single_wav(path_to_wav, orig_file_path=file_path)

    if delete_intermediate:
        os.remove(path_to_wav)
        try:
            os.rmdir(save_to_dir)
        except OSError:
            print(save_to_dir, " was not deleted")
            print("Probably existing from previous run")
            print("Delete Manually")

    return read_wav


def iter_list_mp3(file_paths, save_to_dir=None):
    '''
    if save_to_dir is None, the intermediates will be deleted,
        after the list has been iterated over
    '''
    delete_intermediates = False
    if save_to_dir is None:
        delete_intermediates = True
        save_to_dir = os.path.dirname(file_paths[0]) + os.sep + "wav_temp"
        # FIXME: @motjuste: if the first file in the list does not exist

    paths_to_wavs = []

    for fp in file_paths:
        paths_to_wavs.append(convert_single_mp3ToWav(fp, save_to_dir))
        yield wbr.read_single_wav(paths_to_wavs[-1], orig_file_path=fp)

    if delete_intermediates:
        for w in paths_to_wavs:
            os.remove(w)
        try:
            os.rmdir(save_to_dir)
        except OSError:
            print(save_to_dir, " was not deleted")
            print("Probably existing from previous run")
            print("Delete Manually")


def read_list_mp3(file_paths, save_to_dir=None):
    return list(iter_list_mp3(file_paths, save_to_dir))
