"""Shared definition of relative runtime profiles for overview and detailed figures."""
import numpy as np

PROFILE_METHODS = ['far', 'event_descending', 'delta_merge', 'trace_range',
                   'bounded_merge', 'bounded_frontier']


def centered_log_profiles(medians):
    log = np.log(medians[PROFILE_METHODS])
    return log.sub(log.mean(axis=1), axis=0)
