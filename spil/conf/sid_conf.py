# -*- coding: utf-8 -*-
"""
Example Sid resolver config

Some parts of the sid contain hard coded elements :
project, version, state, ext

This config uses the attr library.
(We should add the these later using a global config, using converter/validator functions

"""
import six

from spil.conf.project_conf import projects
from collections import OrderedDict
import conf

###########################################################################################
# SID BASE CONFIG / PARTS CONFIG
###########################################################################################

sip = '/'  # sid separator

# A sid template must contain a field only once.
# (if not the data cannot be sorted correctly, and the "key by placement" mechanism does not work.

sid_templates = OrderedDict([

    ('asset_file', '{project}/{type:a}/{cat}/{name}/{task}/{subtask}/{version}/{state}/{ext:(' + '|'.join(conf.extensions) + '|\*)}'),

    ('asset_image_frame_file', '{project}/{type:a}/{cat}/{name}/{task}/{subtask}/{version}/{state}/{frame}/{ext:(' + '|'.join(conf.extensions_image) + '|\*)}'),
    ('asset_image_file', '{project}/{type:a}/{cat}/{name}/{task}/{subtask}/{version}/{state}/{ext:(' + '|'.join(conf.extensions_image) + '|\*)}'),
    ('asset_movie_file', '{project}/{type:a}/{cat}/{name}/{task}/{subtask}/{version}/{state}/{ext:(' + '|'.join(conf.extensions_movie) + '|\*)}'),

    ('asset_cache_frame_file', '{project}/{type:a}/{cat}/{name}/{task}/{subtask}/{version}/{state}/{frame}/{ext:(' + '|'.join(conf.extensions_cache) + '|\*)}'),
    ('asset_cache_file', '{project}/{type:a}/{cat}/{name}/{task}/{subtask}/{version}/{state}/{ext:(' + '|'.join(conf.extensions_cache) + '|\*)}'),

    ('asset_state', '{project}/{type:a}/{cat}/{name}/{task}/{subtask}/{version}/{state}'),
    ('asset_version', '{project}/{type:a}/{cat}/{name}/{task}/{subtask}/{version}'),
    ('asset_subtask', '{project}/{type:a}/{cat}/{name}/{task}/{subtask}'),
    ('asset_task', '{project}/{type:a}/{cat}/{name}/{task}'),
    ('asset_name', '{project}/{type:a}/{cat}/{name}'),
    ('asset_cat', '{project}/{type:a}/{cat}'),
    ('asset', '{project}/{type:a}'),

    ('shot_file', '{project}/{type:(s)}/{seq}/{shot}/{task}/{subtask}/{version}/{state}/{ext:(' + '|'.join(conf.extensions) + '|\*)}'),

    ('shot_cache_frame_file', '{project}/{type:s}/{seq}/{shot}/{task}/{subtask}/{version}/{state}/{namespace}/{frame}/{ext:(' + '|'.join(conf.extensions_cache) + '|\*)}'),
    ('shot_cache_file', '{project}/{type:s}/{seq}/{shot}/{task}/{subtask}/{version}/{state}/{namespace}/{ext:(' + '|'.join(conf.extensions_cache) + '|\*)}'),

    ('shot_image_frame_file', '{project}/{type:s}/{seq}/{shot}/{task}/{subtask}/{version}/{state}/{frame}/{ext:(' + '|'.join(conf.extensions_image) + '|\*)}'),
    ('shot_image_file', '{project}/{type:s}/{seq}/{shot}/{task}/{subtask}/{version}/{state}/{ext:(' + '|'.join(conf.extensions_image) + '|\*)}'),
    ('shot_movie_file', '{project}/{type:s}/{seq}/{shot}/{task}/{subtask}/{version}/{state}/{ext:(' + '|'.join(conf.extensions_movie) + '|\*)}'),

    ('shot_state', '{project}/{type:s}/{seq}/{shot}/{task}/{subtask}/{version}/{state}'),
    ('shot_version', '{project}/{type:s}/{seq}/{shot}/{task}/{subtask}/{version}'),
    ('shot_subtask', '{project}/{type:s}/{seq}/{shot}/{task}/{subtask}'),
    ('shot_task', '{project}/{type:s}/{seq}/{shot}/{task}'),
    ('shot_shot', '{project}/{type:s}/{seq}/{shot}'),
    ('shot_seq', '{project}/{type:s}/{seq}'),

    ('shot_2d_file', '{project}/{type:s}/{seq}/{shot}/{task}/{subtask}/{version}/{state}/{ext:(' + '|'.join(conf.extensions) + '|\*)}'),

    ('shot_2d_image_file', '{project}/{type:s}/{seq}/{shot}/{task}/{subtask}/{version}/{state}/{frame}/{ext:(' + '|'.join(conf.extensions_image) + '|\*)}'),
    ('shot_2d_movie_file', '{project}/{type:s}/{seq}/{shot}/{task}/{subtask}/{version}/{state}/{ext:(' + '|'.join(conf.extensions_movie) + '|\*)}'),

    ('shot_2d_state', '{project}/{type:s}/{seq}/{shot}/{task}/{subtask}/{version}/{state}'),
    ('shot_2d_version', '{project}/{type:s}/{seq}/{shot}/{task}/{subtask}/{version}'),
    ('shot_2d_subtask', '{project}/{type:s}/{seq}/{shot}/{task}/{subtask}'),
    ('shot_2d_task', '{project}/{type:s}/{seq}/{shot}/{task}'),
    ('shot_2d_shot', '{project}/{type:s}/{seq}/{shot}'),
    ('shot_2d_seq', '{project}/{type:s}/{seq}'),

    ('shot', '{project}/{type:s}'),
    ('project', '{project}'),

])


###########################################################################################
# SID ATTRIBUTES CONFIG for attr library : validators and converters (need to be defined first)
###########################################################################################

"""
# Example code, not used
# validators and converters

#  validators
def x_smaller_than_y(instance, attribute, value):
    print('validating', instance, '-', attribute.name, '-', value)
    pass
    
# converters
def to_substr(value):
    if value:
        return SubStr(value)

Usage :
shot_config['shot'] = attr.ib(default=None, converter=to_substr, validator=[x_smaller_than_y], converter=biggy)

"""

# note : tasks are not filtered by a task list
sid_filters = {

    'asset': {
        'project': lambda x: x in list(projects),
        # 'cat': lambda x: x in allowed_categories,
        # 'task': lambda x: not six.text_type(x).isnumeric(),
        'state': lambda x: x in allowed_states,
        # 'ext': lambda x: x in allowed_extensions,
    },

    'shot': {
        'project': lambda x: x in list(projects),
        'state': lambda x: x in allowed_states,
        # 'ext': lambda x: x in allowed_extensions,

    },
    'project': {
        'project': lambda x: x in list(projects),
    }

}

###########################################################################################
# SID CONFIG
###########################################################################################

# SORTING ##################################################

asset_keys = ['project', 'type', 'cat', 'name', 'task', 'subtask', 'version', 'state', 'frame', 'ext']
shot_keys = ['project', 'type', 'seq', 'shot', 'task', 'subtask', 'namespace', 'version', 'state', 'frame', 'ext']

basetype_order = ['project', 'asset', 'shot']

values_sorted = {
    'asset': {
        'keys': ['project', 'type', 'cat', 'name', 'task', 'subtask', 'version', 'state', 'frame', 'ext'],
        'task': ['modeling', 'modeling_low', 'uvs', 'setup', 'gpu', 'surfacing', 'ass'],
        'state': ['w', 'p', '*'],
        'ext': ['ma', 'mb']
    },
    'shot': {
        'keys': ['project', 'type', 'seq', 'shot', 'task', 'subtask', 'namespace', 'version', 'state', 'frame', 'ext'],
        'task': ['layout', 'blocking', 'anim', 'animation', 'fx', 'render', 'comp'],
    },
    'project': {
        'keys': ['project']
    }
}

force_keys = ['project', 'type', 'state', 'ext']

optional_keys = ['subtask', 'namespace']

_2d_tasks = ['06_comp', 'comp', 'compo']

values_defaults = {
    'asset': {
        'state': 'w',
    },
    'shot': {
        'subtask': 'main',
        'state': 'w',
    }
}

# Validation / Type detection ##################################################

cache_extensions = ['abc', 'json', 'fur', 'grm']
image_extensions = ['jpg', 'png', 'exr']
# allowed_extensions = ['ma', 'mb', 'hip', 'hda'] + image_extensions + cache_extensions

allowed_states = ['w', 'p', '*']
multipass_tasks = ['render']

meta_items = ['*', '.', '^', '$', '?', '**']  # allowed items in search sids (# CBB this is part of the sid+fs conf)


###########################################################################################
# SID TYPE DEFINITION
###########################################################################################

def get_sidtype(data):
    """
    rules defining the sidtype, based on the data dict of the sid.
    The keys are always given.
    The values can be empty.

    :param data:
    :return:
    """
    # print "data : ", data

    if data.get('type') == 'a':
        subtype = 'asset'

        if data.get('cat'):
            subtype = 'asset_cat'

        if data.get('name'):
            subtype = 'asset_name'

        if data.get('task'):
            subtype = 'asset_task'

        if data.get('subtask'):
            subtype = 'asset_subtask'

        if data.get('version'):
            subtype = 'asset_version'

        if data.get('state'):
            subtype = 'asset_state'

        if data.get('ext'):
            subtype = 'asset_file'

            if data.get('ext').split(',')[0] in conf.extensions_image:
                subtype = 'asset_image_file'

            if data.get('ext').split(',')[0] in conf.extensions_cache:
                subtype = 'asset_cache_file'

            if data.get('ext').split(',')[0] in conf.extensions_movie:
                subtype = 'asset_movie_file'

        if data.get('frame'):
            subtype = subtype.replace('file', 'frame_file')

    elif data.get('type') == 's':
        subtype = 'shot'

        if data.get('seq'):
            subtype = 'shot_seq'

        if data.get('shot'):
            subtype = 'shot_shot'

        if data.get('task'):
            subtype = 'shot_task'

        if data.get('subtask'):
            subtype = 'shot_subtask'

        if data.get('version'):
            subtype = 'shot_version'

        if data.get('state'):
            subtype = 'shot_state'

        if data.get('ext'):
            subtype = 'shot_file'

            if data.get('ext').split(',')[0] in conf.extensions_image:
                subtype = 'shot_image_file'

            if data.get('ext').split(',')[0] in conf.extensions_cache:
                subtype = 'shot_cache_file'

            if data.get('ext').split(',')[0] in conf.extensions_movie:
                subtype = 'shot_movie_file'

        if data.get('frame'):
            subtype = subtype.replace('file', 'frame_file')

        if data.get('task') in _2d_tasks:
            subtype = subtype.replace('shot_', 'shot_2d_')
    else:
        subtype = 'project'

    # print subtype

    return subtype


###########################################################################################
# TEST DATA - TODO : add types for auto tests
###########################################################################################

test_sids = [

    'demo/a/*/*/*/*/*/*/ma,mb',

    'demo/a/01_characters/crab/modeling/maya/v002/p/ma',
    'demo/s/s010/master/01_layout/main/valid/p/ma',
    'demo',

    'demo/a/02_vehicles/race_car',
    'demo/a/03_props/barrel',
    'demo/a/sets/desert',
    'demo/a/sets/cyberpunk_roof_top',

    'demo/a/fx/smoke/setup/houdini/valid/p/hip',
    'demo/a/fx/fire/setup/houdini/valid/p/hip',
    'demo/a/03_props/barrel',

    'demo/a/01_characters/dragon/setup/houdini/valid/p/ma',
    'demo/a/01_characters/dragon/setup/houdini/v001/p/ma',
    'demo/a/01_characters/dragon/setup/houdini/v001/w/ma',
    'demo/a/01_characters/dragon/setup/houdini/v001',
    'demo/a/01_characters/dragon/setup/houdini',
    'demo/a/01_characters/dragon/setup',
    'demo/a/01_characters/dragon',

    'demo/a/01_characters/crab/modeling_lo',
    'demo/a/01_characters/crab/modeling/zbrush/v001/w',
    'demo/a/01_characters/crab/modeling/maya/valid/p/ma',
    'demo/a/01_characters/crab/modeling/maya/v001/p/ma',
    'demo/a/01_characters/crab/modeling/maya/v001/w/ma',
    'demo/a/01_characters/crab/modeling/maya/v001',
    'demo/a/01_characters/crab/modeling/maya',
    'demo/a/01_characters/crab/modeling',
    'demo/a/01_characters/crab',

    'demo/a/01_characters',

    'demo/s/s010/p040',

    'demo/s/s010/p030/03_anim/main/valid/p/ma',
    'demo/s/s010/p030/03_anim/main/v001/p/ma',
    'demo/s/s010/p030/03_anim/main/v001/w/ma',

    'demo/s/s010/p020/03_anim/main/v001/w/ma',

    'demo/s/s010/p010/04_fx/water/v001/w/hip',
    'demo/s/s010/p010/04_fx/pyro/v002/w/hip',
    'demo/s/s010/p010/04_fx/pyro/v001/w/hip',
    'demo/s/s010/p010/03_anim/main/v001/w/ma',

    'demo/s/s010/p010/06_comp/main/v001/w/nk',
    'demo/s/s010/p010/06_comp/main/v002/w/nk',
    'demo/s/s010/p010/06_comp/main/v002/p/nk',

    'demo/s/s010/p010/02_blocking/main/v001/w/ma',
    'demo/s/s010/p010/02_blocking/main/v001/w',
    'demo/s/s010/p010/02_blocking/main/v001',
    'demo/s/s010/p010/02_blocking/main',
    'demo/s/s010/p010/02_blocking',
    'demo/s/s010/p010',

    'demo/s/s010/master/01_layout/main/valid/p/ma',
    'demo/s/s010/master/01_layout/main/v002/p/ma',
    'demo/s/s010/master/01_layout/main/v002/w/ma',
    'demo/s/s010/master/01_layout/main/v001/w/ma',
    'demo/s/s010/master/01_layout',
    'demo/s/s010/master',
    'demo/s/s020',
    'demo/s/s010',
    'demo',

    #'aral/s/s010/p010',
    #'fyp/s/s010/p010',

]


if __name__ == '__main__':

    from pprint import pprint
    pprint(globals())