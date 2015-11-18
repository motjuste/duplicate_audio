'''
@motjuste
NO TESTS!!!
'''
# TODO: @motjuste: test searching


import numpy as np
import duplicate_audio.fingerprinting as fgr

MIN_TIME_RESOLUTION = 0.01


def search_1channel_in_dictdb(qdata, sampling_freq, dict_db):
    '''
    returns tuple(votes, song_id, channel, timestamp)
    '''
    # get the fingerprints for the query data
    q_fingerprints = fgr.fingerprint_channel(qdata, sampling_freq)

    matches = get_matches_in_dictdb(q_fingerprints, dict_db)

    best_match = get_best_match(matches)

    return best_match


def get_matches_in_dictdb(q_fingerprints, dict_db):
    '''
    depends heavily on the kind of db in my mind
    returns all songs, and channels, and relative time-diff
    that match the fingerprints
    '''
    matches = dict(dict(list()))

    for (f, q_timestamps) in q_fingerprints.items():
        if f in dict_db.keys():
            for (s, channels_dict) in dict_db[f].items():
                matches.setdefault(s, dict(list()))
                for (c, timestamps) in channels_dict.items():
                    matches[s].setdefault(c, [])
                    for t in timestamps:
                        for q_t in q_timestamps:
                            matches[s][c].append(t - q_t)

    return matches


def get_best_match(m):
    '''
    expecting a particular type of dict
    Sorry. More documentation to be added
    returns a tuple(votes, song_id, channel, best_timestamp)
    '''
    # find best time matches and channels for all songs
    best_matches = []
    for (s, channels_dict) in m.items():
        for (c, time_diffs) in channels_dict.items():
            bins_ = np.arange(min(time_diffs), max(time_diffs),
                              MIN_TIME_RESOLUTION)
            hist, bins = np.histogram(time_diffs,
                                      bins=bins_)
            best_timestamp = bins[np.argmax(hist)]
            votes = hist.max()

            best_matches.append((votes, s, c, best_timestamp))

    # trick that max checks only the first entry of the tuples
    # TODO: @motjuste: potential bug
    return max(best_matches)
