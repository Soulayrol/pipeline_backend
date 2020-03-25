# -*- coding: utf-8 -*-
"""

This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.

"""
import functools
import os
from collections import OrderedDict

import six

# from spil libs
from spil.libs.util.log import debug, info, warn, error
from spil.libs.util.exception import SpilException

# from fs
from spil.libs.fs.core.fs_resolver import path_to_dict, dict_to_path

# from sid
from spil.libs.sid.core import sid_resolver
from spil.libs.sid.core.sid_helper import compare_by_template

# Sid config
from spil.conf.project_conf import projects, project_order
from spil.conf.fs_conf import path_templates, path_mapping  # FOR CACHE TEMP SMELL
from spil.conf.sid_conf import values_sorted, basetype_order
from spil.conf.sid_conf import values_defaults, optional_keys, force_keys
from spil.conf.sid_conf import sip, get_sidtype

from spil.libs.util import log

log.setLevel(log.INFO)

@functools.total_ordering
class BaseSid(object):
    """
    Base class for the Sid classes.
    Contains the functions.
    """
    def __init__(self):
        self.data = None
        self._keys = []

    def init_data(self, data):
        data = data.copy()
        self.data = OrderedDict()
        self._keys = sid_resolver.dict_to_keys(data)
        for key in self._keys:
            self.data[key] = data.get(key)

    # Utilities
    def is_shot(self):
        return self.basetype() == 'shot'

    def is_asset(self):
        return self.basetype() == 'asset'

    @property
    def project_long(self):
        """return long name project"""
        try:
            return projects[self.get('project')].get('long_name')
        except KeyError:
            raise SpilException('Sid malformed, project "{0}" unknown'.format(self.get('project')))

    @property
    def keys(self):
        return self._keys

    @property
    def path(self):
        """
        return the sid as a path
        """
        result = None
        try:
            result = dict_to_path(self.asdict())
        except SpilException as e:
            info('This Sid has no path. ({})'.format(e))
        return result

    def get_cache(self):  # Todo remove
        """
        get the cache path of the current sid
        """
        # project_root = path_templates['project_root'].format(project=self.project)
        for key, value in path_mapping['state'].items():
            if value == self.state:
                state = key
        for key, value in path_mapping['project'].items():
            if value == self.project:
                project = key
        if self.is_asset() and self.get_as("name"):
            return path_templates['asset_cache_file'].format(project=project, cat=self.cat, name=self.name, task=self.task,
                                                             subtask=self.subtask, state=state,
                                                             version=self.version)
        elif self.is_shot() and self.get_as("project"):
            return path_templates['shot_cache_file'].format(project=project, seq=self.seq, shot=self.shot, task=self.task,
                                                             subtask=self.subtask, state=state,
                                                             version=self.version)

    def conform(self):
        """
        looks to be used for CGWire connection
        """
        for key in self.data.keys():
            self.set(key, str(self.get(key)).lower().replace(' ', '_'))

    def get_stripped(self):
        """
        # TODO : useful ?
        Returns a copy with righter values stripped, into a valid form.
        :return:
        """
        stripped = self.copy(until=self.last_key())
        return stripped

    def get(self, attribute):
        if str(attribute) not in self.data.keys():
            warn('Attribute... "{}" not in Sid definition of {}. Return None'.format(attribute, self))
            return None
        return self.data.get(attribute)

    def set(self, attribute=None, value=None, **kwargs):
        if attribute:
            kwargs[attribute] = value

        self.data.update(kwargs)
        self.init_data(self.data)

    def set_defaults(self, attribute=None, force=None):
        """
        Sets the default values on empty fields, for this sid, as configured.

        If attributes is given, only the given attributes default are set.
        Else, all are set.

        If force is True, already set attributes are overriden with their defaults.
        Else, no attribute is overriden if exists.
        Defaults to False.

        :param attributes: a list or a single attribute to set to default value
        :param force: if attributes with values should be overriden to defaults
        :return:
        """
        # if attributes and not is_sequence(attributes): attributes = [attributes]

        attributes = [attribute] if attribute else list(values_defaults.get(self.basetype(), {}))
        for attribute in attributes:
            if force or not self.get(attribute):
                value = values_defaults.get(self.basetype()).get(attribute)
                self.set(attribute, value)
                debug('Set {} to default value {}'.format(attribute, value))

    def get_as(self, attribute):  # note : should be used as get_as "cache"
        """
        Returns a copy of the Sid as the given attribute.
        Calls copy(until=attribute).

        Example:
        sid.get_as('task')  # Returns a Sid of type task.

        :param attribute:
        :return:
        """
        if not self.has_a(attribute):
            warn('Asked for a "{}" sid, but sid is incomplete. Returning None'.format(attribute))
            return None
        return self.copy(until=attribute)

    def get_with(self, attribute=None, value=None, **kwargs):
        """
        Returns a Sid with the given attribute(s) changed.

        Can be called with an attribute / value pair (if attribute is set)
        Or via **kwargs to set multiple attributes
        Or both.

        :param attribute: an attribute name
        :param value: a value for attribute
        :param kwargs: a attribute/value dictionary
        :return:
        """
        sid_copy = self.asdict()
        if attribute:
            kwargs[attribute] = value
        sid_copy.update(kwargs)
        return Sid(data=sid_copy)
    '''
    def has_a(self, attribute):
        """
        Checks whether the Sid contains a complete Sid of given attribute.
        Calls is_complete(until=attribute)

        Example:
        sid.has_a('task')  # Returns True if all is set until task.

        :param attribute:
        :return:
        """
        return self.is_complete(until=attribute)
    '''
    def has_a(self, attribute):
        return self.data.get(attribute)

    def values(self):
        """
        Returns a list of all values.
        Empty values are included.

        :return:
        """
        return [self.data.get(p) for p in self.data.keys()]

    def parent(self, set_default=False):
        """
        Returns the parent sid.
        Does not return the parent value, but the full parent Sid.

        Sets defaults if set_default is True.
        Useful because the parent may have its last key empty, which might be unexpected.

        Example:
        Sid('demo|s|010|120|animation').parent()  # Will return the Shot Sid 'demo|s|010|120'
        sid.parent()

        Uses get_as().

        :param set_default:
        :return:
        """
        if len(self) <= 1:
            info('Sid {} has no parent. Copy is returned.'.format(self))
            return self.copy()
        parent_key = self.data.keys()[len(self) - 2]
        if set_default:
            self.set_defaults(parent_key)
        return self.get_as(parent_key)

    def copy(self, until=None):
        """
        Returns a copy of the current Sid.
        The copy is always of the same class as the copied.

        If until is given, parameters after until are nulled.

        :param until:
        :return:
        """
        # Full copy, identical class
        if not until:
            return self.__class__(data=self.asdict())

        # we make a dict copy, and empty the attributes after "until"
        sid_copy = self.asdict()

        try:
            index = self.data.keys().index(until) + 1
            for attribute in self.data.keys()[index:]:
                sid_copy[attribute] = None
        except ValueError as e:
            msg = 'Given "{}" is not in dict (Error: {})'.format(until, e)
            error(msg)
            raise SpilException(msg)

        return Sid(data=sid_copy)

    def get_filled(self, by, force=None, until=None):
        """
        Fills all empty attributes by the given "by"
        Optionally until a given attribute.

        :param by:
        :param until:
        :return:
        """
        temp = self.copy()
        for key in self.data.keys():
            if not temp.get(key) or (force and key not in force_keys):
                temp.set(key, by)
        return temp.copy(until=until)

    def is_complete(self, until='project'):
        """
        Checks if a Sid is complete - all keys have values (all attributes return True) - until a given attribute.

        Intermediate optional keys are ignored.

        @param until: the last attribute that is checked
        """
        for key in self.data.keys():
            if not self.data.get(key):
                if key not in optional_keys:
                    return False
            if key == until:
                return bool(self.data.get(key))
        warn('[Sid] could not verify completeness of self "{0}" until "{1}"'.format(self, until))
        return False  # malformed or until malformed?

    def last_key(self):
        if not self.data.keys():
            return None
        return self.data.keys()[len(self) - 1]

    def last_valid_key(self):
        last_key = ''
        for key, value in self.data.items():
            if value == '*':
                return last_key
            else:
                last_key = key
        return last_key

    def remove_key(self, key):
        if key in self.data.keys():
            del self.data[key]


    # overrides

    def __len__(self):
        """
        Returns the length of the sid, relying on is_complete.
        """
        index = len(self.data.keys())
        for p in reversed(self.data.keys()):
            if self.is_complete(until=p):
                return index
            else:
                index = index-1
        return 0

    def __str__(self):
        if not self.asdict():
            return ''
        return sid_resolver.dict_to_sid(self.asdict())

    def __repr__(self):
        return 'Sid("{0}")'.format(str(self))

    def __hash__(self, *args, **kwargs):
        return hash(repr(self))

    def __eq__(self, other):
        return self._compare(other) == 0

    def __lt__(self, other):
        return self._compare(other) < 0

    def __iter__(self):
        """
        Iterates over the Sids values.
        Stops at the first mandatory empty value.

        :return: Iterator
        """
        for x in [self.data.get(p) for p in self.data.keys()]:
            if x or x in optional_keys:
                yield x

    def __nonzero__(self):
        """
        Conversion to bool.
        At least the project needs to be defined for the sid to be "True"
        """
        return all([self.get('project')])

    def __add__(self, other):
        """
        Adds a value at the end of the Sid and returns the result.

        If the Sid is complete, a copy is returned without anything added.

        :param other:
        :return:
        """
        if len(self) == len(self.keys):
            warn('Sid {} is already complete. Concatenation impossible.'.format(self))
            return self.copy()
        other = str(other)
        if not other.startswith(sip):
            other = sip + other
        result = str(self) + other
        return Sid(result)

    def _compare(self, other):
        """
        Compares 2 sids hierarchically.

        First compares the projects, than the types.
        If they are not equal, as per configuration, the result is returned.

        If project and types are equal, each sid key is evaluated against the counterpart in the other sid.
        In case of equality, the next key is evaluated, until a greater value is found, and the result is returned.

        For each key, the comparison uses the configuration, or string comparison.

        Uses compare_by_template, where the template comes from the config.

        #IDEA : delegate this to an external comparing function, for example the FileSystem (by dates), or a database.
        In this case, the delegate must only be imported on-demand, since it would be slower than string comparisons.

        :param other: another Sid or Sid string
        :return:
        """
        if unicode(other) == unicode(self):
            return 0

        a = self

        # if b is a string, transform to Sid first.
        if isinstance(other, BaseSid):
            b = other
        else:
            b = Sid(other)

        # first compare projects
        compared = compare_by_template(a.get('project'), b.get('project'), project_order)
        if compared != 0:
            return compared

        # then compare the sid types
        compared = compare_by_template(a.basetype(), b.basetype(), basetype_order)
        if compared != 0:
            return compared

        # now looping of the sid keys, until discrimination
        sorted_values = values_sorted.get(a.basetype(), {})  # TODO: bad conf error handling (not just default to {})
        for i, (ia, ib) in enumerate(zip(a, b)):
            if not ia and ib:
                continue
            template = sorted_values.get(a.keys[i])
            compared = compare_by_template(ia, ib, template)
            if compared != 0:
                return compared
        return -1

    def asdict(self):
        """
        A dictionary representation of the current Sid.

        (Generated by attr)

        :return:
        """
        return self.data.copy()

    def sidtype(self):
        """
        Complete sid type as defined in sid_conf.get_sidtype()

        Example:
        "asset_task"  # is the type of a Sid that is complete until "task"

        :return: String sid type
        """
        return get_sidtype(self.asdict())

    def basetype(self):
        """
        Returns the first element of the Sid type

        Example:
        "asset" is the first element of "asset_task"

        :return:
        """
        return self.sidtype().split('_')[0]

    def endtype(self):
        """
        Returns the last element of the Sid type

        Example:
        "task" is the last element of "asset_task"

        :return:
        """
        return self.sidtype().split('_')[-1]


class Sid(BaseSid):

    def __init__(self, sid=None, data=None, path=None):
        """
        Sid Init method.

        If multiple parameters are given, data is overriden by path, which is overriden by sid.
        If no param is given, eg. Sid(), returns an empty Sid().

        :param sid: a Sid object or string
        :param data: a data dictionary
        :param path: a valid path
        :return:
        """

        self.data = OrderedDict()
        # self._keys = []  #  ['project']

        if path:
            # self.type, self.data = path_to_dict(path)
            __, data = path_to_dict(path)
            if not data:
                raise SpilException('[Sid] Path "{}" did not resolve to valid Sid data.'.format(path))

        if sid:
            sid_str = str(sid)
            data = sid_resolver.sid_to_dict(sid_str)
            if not data:
                raise SpilException('[Sid] Sid "{}" did not resolve to valid Sid data.'.format(sid))

        if data:
            data_tmp = data.copy()
            # self.data = data_tmp
            self.init_data(data_tmp)

        # Conform Project
        for key, value in path_mapping['project'].items():
            if key == self.data['project']:
                self.data['project'] = value
        # print 'Init done:', self

if __name__ == '__main__':

    import sys
    sid = Sid('demo/s/s010/p010/fx/main/v001/p/hip')
    info(sid)
    mov = sid.get_with(ext='mov')
    print "SID MOV : ", sid
    info(mov.path)
    exr = sid.get_with(ext='exr')
    exr.set('frame', '*')
    print "SID EXR : ", exr
    exr = exr.get_filled('*', True)
    print "SID EXR : ", exr

    sys.exit()

    info('Most tests are in the spil.tests package')

    from spil.libs.util.log import setLevel, DEBUG, INFO

    info('-'*20)
    info('Tests start')
    info('-'*20)

    setLevel(INFO)

    sid = Sid('demo/s/s010/p010/////ma')
    info(sid)
    info(sid.path)
    info(sid.get_stripped().path)
    info('-'*20)

    sid2 = Sid(sid)
    info(sid2)
    info(sid == sid2)
    info('-'*20)

    toto = Sid(path='i:/synologydrive/DEMO/03_work_pipe/01_ASSET_3D/characters/dragon')
    info(toto)
    info(toto.project_long)
    info(toto.basetype())
    info(toto.sidtype())
    info(toto.path)
    info(repr(toto))
    info('-'*20)

    info('Empty Sid:')
    info(type(Sid()))
    info(Sid())
    info(Sid().set('project', 'test'))
    info('-'*20)

    test = Sid('demo/a')
    info(test)
    info('-' * 20)

    test = Sid('demo/a/vehicles')
    print 'test', test
    test.set(name='voiture', task='modeling')
    test = test.get_with(ext='bla')

    print 'test with ext', test
    print 'filled', test.get_filled(by='*')
    print 'filled until name', test.get_filled(by='*', until='name')
    print test.get_as('project')

    for i in test.get_filled(by='*', until='name'):
        print i

    info('-'*20)


