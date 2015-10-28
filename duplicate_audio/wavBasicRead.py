'''
utility functions to read wav audio files
'''
import scipy.io.wavfile as spwav


def read_single_wav(file_path):
    '''
    reads wav file at file_path using the scipy.io.wavfile package

    @params: file_path
    @returns: Tuple(sampling_rate, data)
    '''
    try:
        single_wav = spwav.read(file_path)
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
