# -*- coding: utf-8 -*-
"""

This file is part of SPIL, The Simple Pipeline Lib.

(C) copyright 2019 Michael Haussmann, spil@xeo.info

SPIL is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

SPIL is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with SPIL.
If not, see <https://www.gnu.org/licenses/>.


Sid resolver

Is the low level under the Sid object.

Transforms the sid string into a valid sid dict, and reverse.

"""

# TODO : refacto into class
# TODO : use explicit project in resolve process, so we can have one configuration per project.

import six

if six.PY3:
    import spil.vendor
import lucidity
from lucidity import Template

from spil.libs.util.log import debug, warn
from spil.libs.util.exception import SpilException

# sid conf
from spil.conf.sid_conf import sip, values_sorted
from spil.conf.sid_conf import sid_templates, sid_filters, get_sidtype, meta_items

def parse_sid(sid, pattern, name='template'):

    template = lucidity.Template(name, pattern,
                                 default_placeholder_expression='[^/]*',  # allows for empty keys // should it be '[^|]*' ?
                                 anchor=lucidity.Template.ANCHOR_BOTH)

    diff = template.pattern.count(sip) - sid.count(sip)  # allowing sids to be open at the end
    if diff > 0:
        sid = sid + sip * diff

    try:
        data = template.parse(sid)
        debug('{} matched template "{}"'.format(sid, name))
        return data

    except Exception as e:
        debug('{} did not match template "{}" (error:{})'.format(sid, name, e))
        return None


def validate_sid(data, filters):  # FIXME : not used since refacto
    """
    Validates the data via filters.
    meta_items are not filtered.

    :param data:
    :param filters:
    :return:
    """
    if not filters:
        debug('No filter was given, data auto validated : {}'.format(data))
        return True

    if not data:
        return False

    if not data.keys():
        return False

    data = data.copy()

    for key, value in six.iteritems(data.copy()):
        if value in meta_items:
            continue
        if value and filters.get(key):
            if not filters.get(key)(value):
                return False
        if not value:
            data.pop(key)

    return True


def sid_to_dict(sid):

    templates = []

    for name, pattern in six.iteritems(sid_templates):
        template = Template(name, pattern,
                            anchor=lucidity.Template.ANCHOR_BOTH,
                            default_placeholder_expression='[^/]*',  # allows for empty keys // should it be '[^|]*' ?
                            duplicate_placeholder_mode=lucidity.Template.STRICT)
        # template.template_resolver = resolvers
        templates.append(template)

    try:
        """
        if len(sid.split('/')) >= 8:
            data = []
            for ext in sid.split('/')[-1].split(','):
                sid_copy = sid
                sid_copy = sid_copy.replace(sid_copy.split('/')[-1], ext)
                data.extend(lucidity.parse(str(sid_copy), templates)[0])
        else:
        """
        data, template = lucidity.parse(str(sid), templates)

        # print 'found', data, template
    except Exception as e:
        warn(e)
        return None

    if not data:
        return None

    '''
    for key in list(data.keys()):
        if key not in shot_keys + asset_keys:
            data.pop(key)
    '''
    # return template.name, data  # need the name ?
    return data


def dict_to_sid(data):

    data = data.copy()

    if not data:
        raise SpilException('[dict_to_sid] Data is empty')
    _type = get_sidtype(data)
    pattern = sid_templates.get(_type)

    if not pattern:
        raise SpilException(
            '[dict_to_sid] Unable to find pattern for sidtype: "{}" \nGiven data: "{}"'.format(_type, data))

    template = lucidity.Template(_type, pattern)

    if not template:
        raise SpilException('toe')
    sid = template.format(data).rstrip(sip)
    return sid


def dict_to_keys(data):
    """
    Returns a list of the keys for this pattern.
    The list is sorted by appearance in the pattern.

    This list is used to sort the data dict as the sid pattern.

    :param data:
    :return:
    """

    data = data.copy()

    if not data:
        raise SpilException('[dict_to_keys] Data is empty')
    _type = get_sidtype(data)
    basetype = _type.split('_')[0]
    pattern = sid_templates.get(_type)

    if not pattern:
        raise SpilException(
            '[dict_to_keys] Unable to find pattern for sidtype: "{}" \nGiven data: "{}"'.format(_type, data))

    template = lucidity.Template(_type, pattern)

    if not template:
        raise SpilException('toe')

    keys = values_sorted.get(basetype).get('keys')
    keys = filter(lambda x: x in template.keys(), keys)
    return keys


if __name__ == '__main__':

    from spil.libs.util.log import setLevel, DEBUG, INFO, info

    info('Tests start')

    setLevel(INFO)
    # setLevel(DEBUG)  # In case of problems, use DEBUG mode

    from spil.conf.sid_conf import test_sids as tests

    # tests = ['demo/*']

    for test in tests:

        info('Testing : {}'.format(test))

        _dict = sid_to_dict(test)
        info('sid {} ---> \n{}'.format(test, _dict))

        _type = get_sidtype(_dict)
        info('type : ' + _type)

        # info('------ keys : {}'.format(dict_to_keys(_dict)))

        retour = dict_to_sid(_dict)
        info('retour: ' + retour)

        assert(test == retour)

        info('*'*15)

    info('*' * 30)
    info('*' * 30)
