import numpy as np
from skimage.feature import peak_local_max
from scipy.signal import spectrogram


TGT_ZONE = {
    "height_minus": 25,
    "height_plus": 25,
    "width": 50,
    "displacement": 50
}

PEAK_MIN_DIST = 2


def fingerprint(data, sampling_frequency, song_id):
    '''
    function returns a dictionary with fingerprints as keys,
    and values as another dictionary, which has song_id as keys and
    {channel:timestamps} as values.

    The fingerprints are tuples (f1, f2, (t2 - t1))

    The fingerprints are generated by finding constellations in the
    peak_local_max result of the spectogram analysis. The constellations
    are found in target zones defined by TGT_ZONE dict defined as a global,
    per local maxima.

    TODO: @motjuste: depending a lot on the default params for the
    library functions being called.

    '''
    n_channels = data.shape[1]

    fingerprints = dict(dict(dict(list())))

    for c in range(n_channels):
        f = fingerprint_channel(data[:, c], sampling_frequency)
        for k in f.keys():

            # TODO: @motjuste: potential bug
            # since it is the same song
            # and this channel is definitely not there
            fingerprints.setdefault(k, {song_id: {c: []}})
            fingerprints[k][song_id][c] = f[k]

    return fingerprints


def fingerprint_channel(dc, fs):
    [f_spec, t_spec, spec] = spectrogram(dc, fs=fs, scaling='spectrum')
    t_diff = t_spec[1] - t_spec[0]

    lmx_2d = peak_local_max(spec, min_distance=PEAK_MIN_DIST,
                            exclude_border=False, threshold_rel=0,
                            indices=False)

    lmx_loc = np.transpose(np.nonzero(lmx_2d))

    # pad the lmx_2d for later target zoning
    # use the max TGT_ZONE properties
    padding = max(TGT_ZONE.values()) + (TGT_ZONE["displacement"])
    lmx_2d = np.pad(lmx_2d, padding,
                    mode='constant', constant_values=0)

    tgt_Y, tgt_X = np.ogrid[-TGT_ZONE["height_minus"]:TGT_ZONE["height_plus"],
                            TGT_ZONE["displacement"]:
                            TGT_ZONE["displacement"] + TGT_ZONE["width"]]

    fingerprints = dict(list())

    for (y, x) in lmx_loc:
        zone_Y = tgt_Y + (y + padding - 1)
        zone_X = tgt_X + (x + padding - 1)
        zone = lmx_2d[zone_Y, zone_X]

        nonzero_loc = np.transpose(np.nonzero(zone))
        nonzero_loc[:, 0] += (y - TGT_ZONE["height_minus"] - 1)  # f2
        nonzero_loc[:, 1] += TGT_ZONE["displacement"]  # t2-t1

        for i, (f2, t21) in enumerate(nonzero_loc):
            fingerprint = (f_spec[y], f_spec[f2], t21 * t_diff)
            value = t_spec[x]

            fingerprints.setdefault(fingerprint, []).append(value)

    return fingerprints
