'''
utility functions to read wav audio files
'''
import os.path as ospath
import scipy.io.wavfile as spwav


def read_single_wav(file_path, orig_file_path=None):
    '''
    reads wav file at file_path using the scipy.io.wavfile package

    @params: file_path
    @returns: dict{"abs_file_path": "",
                   "sampling_freq": int,
                   "data": numpy array}
    '''
    try:
        [Fs, data] = spwav.read(file_path)
        file_path_ = file_path if orig_file_path is None else orig_file_path
        return {"abs_file_path": ospath.abspath(file_path_),
                "sampling_frequency": Fs,
                "data": data}
    except IOError:
        print("ERROR read_single_wav(): File not found or other IOError")
        print("Given filename: " + file_path)
        raise
    except ValueError:
        print("ERROR read_single_wav(): " +
              "file at path not a wav file, or other ValueError")
        # TODO: @motjuste: check file extension itself?
        print("Given filename: " + file_path)
        raise


def iter_list_wav(file_paths):
    return map(read_single_wav, file_paths)


def read_list_wav(file_paths):
    return list(iter_list_wav(file_paths))
