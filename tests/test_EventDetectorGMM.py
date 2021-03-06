""" Unit tests for SceneClassifierGMM """

import nose.tools
import sys
sys.path.append('..')
import json
import os
from dcase_framework.features import FeatureContainer, FeatureExtractor
from dcase_framework.metadata import MetaDataContainer, MetaDataItem
from dcase_framework.learners import EventDetectorGMM
import tempfile
from IPython import embed


def test_learn():
    FeatureExtractor(store=True, overwrite=True).extract(
        audio_file=os.path.join('material', 'test.wav'),
        extractor_name='mfcc',
        extractor_params={
            'mfcc': {
                'n_mfcc': 10
            }
        },
        storage_paths={
            'mfcc': os.path.join('material', 'test.mfcc.cpickle')
        }
    )
    feature_container = FeatureContainer(filename=os.path.join('material', 'test.mfcc.cpickle'))

    data = {
        'file1.wav': feature_container,
        'file2.wav': feature_container,
    }

    annotations = {
        'file1.wav': MetaDataContainer([
                {
                    'file': 'file1.wav',
                    'scene_label': 'scene1',
                    'event_onset': 0.0,
                    'event_offset': 1.0,
                    'event_label': 'event1',
                    'location_identifier': 'a',
                },
                {
                    'file': 'file1.wav',
                    'scene_label': 'scene1',
                    'event_onset': 1.0,
                    'event_offset': 2.0,
                    'event_label': 'event2',
                    'location_identifier': 'a',
                },
                {
                    'file': 'file1.wav',
                    'scene_label': 'scene1',
                    'event_onset': 2.0,
                    'event_offset': 3.0,
                    'event_label': 'event2',
                    'location_identifier': 'a',
                },
                {
                    'file': 'file1.wav',
                    'scene_label': 'scene1',
                    'event_onset': 4.0,
                    'event_offset': 5.0,
                    'event_label': 'event1',
                    'location_identifier': 'a',
                },
                {
                    'file': 'file1.wav',
                    'scene_label': 'scene1',
                    'event_onset': 1.0,
                    'event_offset': 2.0,
                    'event_label': 'event1',
                    'location_identifier': 'a',
                }
            ]
        ),
        'file2.wav': MetaDataContainer([
                {
                    'file': 'file2.wav',
                    'scene_label': 'scene1',
                    'event_onset': 0.0,
                    'event_offset': 1.0,
                    'event_label': 'event2',
                    'location_identifier': 'b',
                },
                {
                    'file': 'file2.wav',
                    'scene_label': 'scene1',
                    'event_onset': 1.0,
                    'event_offset': 2.0,
                    'event_label': 'event1',
                    'location_identifier': 'b',
                },
                {
                    'file': 'file2.wav',
                    'scene_label': 'scene1',
                    'event_onset': 2.0,
                    'event_offset': 3.0,
                    'event_label': 'event2',
                    'location_identifier': 'b',
                },
                {
                    'file': 'file2.wav',
                    'scene_label': 'scene1',
                    'event_onset': 3.0,
                    'event_offset': 4.0,
                    'event_label': 'event2',
                    'location_identifier': 'b',
                }
            ]
        )
    }

    ed = EventDetectorGMM(
        method='gmm',
        class_labels=['event1', 'event2'],
        params={
            'hop_length_seconds': 0.02,
            'parameters':{
                'n_components': 6,
                'covariance_type': 'diag',
                'tol': 0.001,
                'reg_covar': 0,
                'max_iter': 40,
                'n_init': 1,
                'init_params': 'kmeans',
                'random_state': 0,
            }
        },
        filename=os.path.join('material', 'test.model.cpickle'),
        disable_progress_bar=True,
    )

    ed.learn(data=data, annotations=annotations)
    # Test model count
    nose.tools.eq_(len(ed.model), 2)

    # Test model dimensions
    nose.tools.eq_(ed.model['event1']['positive'].means_.shape[0], 6)


def test_predict():
    FeatureExtractor(store=True, overwrite=True).extract(
        audio_file=os.path.join('material', 'test.wav'),
        extractor_name='mfcc',
        extractor_params={
            'mfcc': {
                'n_mfcc': 10
            }
        },
        storage_paths={
            'mfcc': os.path.join('material', 'test.mfcc.cpickle')
        }
    )
    feature_container = FeatureContainer(filename=os.path.join('material', 'test.mfcc.cpickle'))

    data = {
        'file1.wav': feature_container,
        'file2.wav': feature_container,
    }

    annotations = {
        'file1.wav': MetaDataContainer([
                {
                    'file': 'file1.wav',
                    'scene_label': 'scene1',
                    'event_onset': 0.0,
                    'event_offset': 1.0,
                    'event_label': 'event1',
                    'location_identifier': 'a',
                },
                {
                    'file': 'file1.wav',
                    'scene_label': 'scene1',
                    'event_onset': 1.0,
                    'event_offset': 2.0,
                    'event_label': 'event2',
                    'location_identifier': 'a',
                },
                {
                    'file': 'file1.wav',
                    'scene_label': 'scene1',
                    'event_onset': 2.0,
                    'event_offset': 3.0,
                    'event_label': 'event2',
                    'location_identifier': 'a',
                },
                {
                    'file': 'file1.wav',
                    'scene_label': 'scene1',
                    'event_onset': 4.0,
                    'event_offset': 5.0,
                    'event_label': 'event1',
                    'location_identifier': 'a',
                },
                {
                    'file': 'file1.wav',
                    'scene_label': 'scene1',
                    'event_onset': 1.0,
                    'event_offset': 2.0,
                    'event_label': 'event1',
                    'location_identifier': 'a',
                }
            ]
        ),
        'file2.wav': MetaDataContainer([
                {
                    'file': 'file2.wav',
                    'scene_label': 'scene1',
                    'event_onset': 0.0,
                    'event_offset': 1.0,
                    'event_label': 'event2',
                    'location_identifier': 'b',
                },
                {
                    'file': 'file2.wav',
                    'scene_label': 'scene1',
                    'event_onset': 1.0,
                    'event_offset': 2.0,
                    'event_label': 'event1',
                    'location_identifier': 'b',
                },
                {
                    'file': 'file2.wav',
                    'scene_label': 'scene1',
                    'event_onset': 2.0,
                    'event_offset': 3.0,
                    'event_label': 'event2',
                    'location_identifier': 'b',
                },
                {
                    'file': 'file2.wav',
                    'scene_label': 'scene1',
                    'event_onset': 3.0,
                    'event_offset': 4.0,
                    'event_label': 'event2',
                    'location_identifier': 'b',
                }
            ]
        )
    }

    ed = EventDetectorGMM(
        method='gmm',
        class_labels=['event1', 'event2'],
        params={
            'hop_length_seconds': 0.02,
            'parameters':{
                'n_components': 6,
                'covariance_type': 'diag',
                'tol': 0.001,
                'reg_covar': 0,
                'max_iter': 40,
                'n_init': 1,
                'init_params': 'kmeans',
                'random_state': 0,
            }
        },
        filename=os.path.join('material', 'test.model.cpickle'),
        disable_progress_bar=True,
    )

    ed.learn(data=data, annotations=annotations)

    recognizer_params = {
        'frame_accumulation': {
            'enable': False,
            'type': 'sliding_sum',
            'window_length_frames': 2,
        },
        'frame_binarization': {
            'enable': True,
            'type': 'global_threshold',
            'threshold': 10,
        }
    }
    result = ed.predict(
        feature_data=feature_container,
        recognizer_params=recognizer_params
    )

    # Test result
    nose.tools.eq_(len(result) > 5, True)

    # Test errors
    recognizer_params['frame_binarization']['type'] = 'test'
    nose.tools.assert_raises(AssertionError, ed.predict, feature_container, recognizer_params)
