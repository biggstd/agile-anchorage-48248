import json

from isatools.isajson import ISAJSONEncoder
from isatools.model import Sample


def build_isa_sample(value_dict):
    '''Creates an ISA Sample object.'''
    new_sample = Sample(**value_dict)
    return new_sample


def jsonify_isa_object(isa_object):
    """Converts an ISA object object to a .json string.
    """
    return json.dumps(
        isa_object,
        cls=ISAJSONEncoder,
        sort_keys=True,
        indent=4,
        separators=(',', ': ')
    )


