"""A TestCase that initializes the library with standard API methods."""



import unittest

import ee


class ApiTestCase(unittest.TestCase):

  def setUp(self):
    self.InitializeApi()

  def InitializeApi(self):
    """Initializes the library with standard API methods.

    This is normally invoked during setUp(), but subclasses may invoke
    it manually instead if they prefer.
    """
    self.last_download_call = None
    self.last_thumb_call = None

    def MockSend(path, params, unused_method=None, unused_raw=None):
      if path == '/algorithms':
        return BUILTIN_FUNCTIONS
      elif path == '/value':
        return {'value': 'fakeValue'}
      elif path == '/mapid':
        return {'mapid': 'fakeMapId'}
      elif path == '/download':
        # Hang on to the call arguments.
        self.last_download_call = {'url': path, 'data': params}
        return {'docid': '1', 'token': '2'}
      elif path == '/thumb':
        # Hang on to the call arguments.
        self.last_thumb_call = {'url': path, 'data': params}
        return {'thumbid': '3', 'token': '4'}
      else:
        raise Exception('Unexpected API call to %s with %s' % (path, params))
    ee.data.send_ = MockSend

    ee.Reset()
    ee.Initialize(None, '')


BUILTIN_FUNCTIONS = {
    'Image.constant': {
        'type': 'Algorithm',
        'args': [
            {
                'description': '',
                'name': 'value',
                'type': 'Number'
            }
        ],
        'description': '',
        'returns': 'Image'
    },
    'Image.load': {
        'type': 'Algorithm',
        'args': [
            {
                'description': '',
                'name': 'id',
                'type': 'String'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'version',
                'type': 'Long'
            }
        ],
        'description': '',
        'returns': 'Image'
    },
    'Image.addBands': {
        'type': 'Algorithm',
        'args': [
            {
                'description': '',
                'name': 'dstImg',
                'type': 'Image'
            },
            {
                'description': '',
                'name': 'srcImg',
                'type': 'Image'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'names',
                'type': 'List<String>'
            },
            {
                'default': False,
                'description': '',
                'optional': True,
                'name': 'overwrite',
                'type': 'boolean'
            }
        ],
        'description': '',
        'returns': 'Image'
    },
    'Image.clip': {
        'type': 'Algorithm',
        'args': [
            {
                'description': '',
                'name': 'input',
                'type': 'Image'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'geometry',
                'type': 'Object'
            }
        ],
        'description': '',
        'returns': 'Image'
    },
    'Image.select': {
        'type': 'Algorithm',
        'args': [
            {
                'description': '',
                'name': 'input',
                'type': 'Image'
            },
            {
                'description': '',
                'name': 'bandSelectors',
                'type': 'Array<Object>'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'newNames',
                'type': 'Array<String>'
            }
        ],
        'description': '',
        'returns': 'Image'
    },
    'Image.parseExpression': {
        'type': 'Algorithm',
        'args': [
            {
                'description': '',
                'name': 'expression',
                'type': 'String'
            },
            {
                'default': 'image',
                'description': '',
                'optional': True,
                'name': 'argName',
                'type': 'String'
            }
        ],
        'description': '',
        'returns': 'Algorithm'
    },
    'Feature': {
        'type': 'Algorithm',
        'args': [
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'geometry',
                'type': 'ProjGeometry'
            },
            {
                'default': {},
                'description': '',
                'optional': True,
                'name': 'metadata',
                'type': 'Dictionary<Object>'
            }
        ],
        'description': '',
        'returns': 'Feature'
    },
    'Collection': {
        'type': 'Algorithm',
        'args': [
            {
                'description': '',
                'name': 'features',
                'type': 'List<Feature>'
            }
        ],
        'description': '',
        'returns': 'FeatureCollection'
    },
    'Collection.loadTable': {
        'type': 'Algorithm',
        'args': [
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'tableId',
                'type': 'Object'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'geometryColumn',
                'type': 'String'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'version',
                'type': 'Long'
            }
        ],
        'description': '',
        'returns': 'FeatureCollection'
    },
    'Collection.filter': {
        'type': 'Algorithm',
        'args': [
            {
                'description': '',
                'name': 'collection',
                'type': 'FeatureCollection'
            },
            {
                'description': '',
                'name': 'filter',
                'type': 'Filter'
            }
        ],
        'description': '',
        'returns': 'FeatureCollection'
    },
    'Collection.limit': {
        'type': 'Algorithm',
        'args': [
            {
                'description': '',
                'name': 'collection',
                'type': 'FeatureCollection'
            },
            {
                'default': -1,
                'description': '',
                'optional': True,
                'name': 'limit',
                'type': 'int'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'key',
                'type': 'String'
            },
            {
                'default': True,
                'description': '',
                'optional': True,
                'name': 'ascending',
                'type': 'boolean'
            }
        ],
        'description': '',
        'returns': 'FeatureCollection'
    },
    'Collection.map': {
        'type': 'Algorithm',
        'args': [
            {
                'description': '',
                'name': 'collection',
                'type': 'FeatureCollection'
            },
            {
                'description': '',
                'name': 'baseAlgorithm',
                'type': 'Algorithm'
            },
            {
                'description': '',
                'name': 'dynamicArgs',
                'type': 'Dictionary<String>'
            },
            {
                'default': {},
                'description': '',
                'optional': True,
                'name': 'constantArgs',
                'type': 'Dictionary<Object>'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'destination',
                'type': 'String'
            }
        ],
        'description': '',
        'returns': 'TaskResult'
    },
    'ImageCollection.load': {
        'type': 'Algorithm',
        'args': [
            {
                'description': '',
                'name': 'id',
                'type': 'String'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'version',
                'type': 'Long'
            }
        ],
        'description': '',
        'returns': 'ImageCollection'
    },
    'ImageCollection.fromImages': {
        'type': 'Algorithm',
        'args': [
            {
                'description': '',
                'name': 'images',
                'type': 'List<Image>'
            }
        ],
        'description': '',
        'returns': 'ImageCollection'
    },
    'ImageCollection.mosaic': {
        'type': 'Algorithm',
        'args': [
            {
                'description': '',
                'name': 'collection',
                'type': 'ImageCollection'
            }
        ],
        'description': '',
        'returns': 'Image'
    },
    'Collection.geometry': {
        'type': 'Algorithm',
        'args': [
            {
                'description': '',
                'name': 'collection',
                'type': 'FeatureCollection'
            },
            {
                'default': {
                    'type': 'ErrorMargin',
                    'unit': 'meters',
                    'value': 0
                },
                'description': '',
                'optional': True,
                'name': 'maxError',
                'type': 'ErrorMargin'
            }
        ],
        'description': '',
        'returns': 'TaskResult'
    },
    'DrawVector': {
        'type': 'Algorithm',
        'args': [
            {
                'description': '',
                'name': 'collection',
                'type': 'FeatureCollection'
            },
            {
                'description': '',
                'name': 'color',
                'type': 'String'
            },
            {
                'default': 3,
                'description': '',
                'optional': True,
                'name': 'pointRadius',
                'type': 'int'
            },
            {
                'default': 2,
                'description': '',
                'optional': True,
                'name': 'strokeWidth',
                'type': 'int'
            }
        ],
        'description': '',
        'returns': 'Image'
    },
    'DateRange': {
        'type': 'Algorithm',
        'args': [
            {
                'description': '',
                'name': 'start',
                'type': 'Date'
            },
            {
                'description': '',
                'name': 'end',
                'type': 'Date'
            }
        ],
        'description': '',
        'returns': 'DateRange'
    },
    'ErrorMargin': {
        'type': 'Algorithm',
        'args': [
            {
                'description': '',
                'name': 'value',
                'type': 'Double'
            },
            {
                'default': 'meters',
                'description': '',
                'optional': True,
                'name': 'unit',
                'type': 'String'
            }
        ],
        'description': '',
        'returns': 'ErrorMargin'
    },
    'Filter.intersects': {
        'type': 'Algorithm',
        'args': [
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'leftField',
                'type': 'String'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'rightValue',
                'type': 'Object'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'rightField',
                'type': 'String'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'leftValue',
                'type': 'Object'
            },
            {
                'default': {
                    'type': 'ErrorMargin',
                    'unit': 'meters',
                    'value': 0.1
                },
                'description': '',
                'optional': True,
                'name': 'maxError',
                'type': 'ErrorMargin'
            }
        ],
        'description': '',
        'returns': 'Filter'
    },
    'Filter.dateRangeContains': {
        'type': 'Algorithm',
        'args': [
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'leftField',
                'type': 'String'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'rightValue',
                'type': 'Object'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'rightField',
                'type': 'String'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'leftValue',
                'type': 'Object'
            }
        ],
        'description': '',
        'returns': 'Filter'
    },
    'Filter.or': {
        'type': 'Algorithm',
        'args': [
            {
                'description': '',
                'name': 'filters',
                'type': 'List<Filter>'
            }
        ],
        'description': '',
        'returns': 'Filter'
    },
    'Filter.and': {
        'type': 'Algorithm',
        'args': [
            {
                'description': '',
                'name': 'filters',
                'type': 'List<Filter>'
            }
        ],
        'description': '',
        'returns': 'Filter'
    },
    'Filter.not': {
        'type': 'Algorithm',
        'args': [
            {
                'description': '',
                'name': 'filter',
                'type': 'Filter'
            }
        ],
        'description': '',
        'returns': 'Filter'
    },
    'Filter.equals': {
        'type': 'Algorithm',
        'args': [
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'leftField',
                'type': 'String'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'rightValue',
                'type': 'Object'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'rightField',
                'type': 'String'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'leftValue',
                'type': 'Object'
            }
        ],
        'description': '',
        'returns': 'Filter'
    },
    'Filter.lessThan': {
        'type': 'Algorithm',
        'args': [
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'leftField',
                'type': 'String'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'rightValue',
                'type': 'Object'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'rightField',
                'type': 'String'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'leftValue',
                'type': 'Object'
            }
        ],
        'description': '',
        'returns': 'Filter'
    },
    'Filter.greaterThan': {
        'type': 'Algorithm',
        'args': [
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'leftField',
                'type': 'String'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'rightValue',
                'type': 'Object'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'rightField',
                'type': 'String'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'leftValue',
                'type': 'Object'
            }
        ],
        'description': '',
        'returns': 'Filter'
    },
    'Filter.stringContains': {
        'type': 'Algorithm',
        'args': [
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'leftField',
                'type': 'String'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'rightValue',
                'type': 'Object'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'rightField',
                'type': 'String'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'leftValue',
                'type': 'Object'
            }
        ],
        'description': '',
        'returns': 'Filter'
    },
    'Filter.stringStartsWith': {
        'type': 'Algorithm',
        'args': [
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'leftField',
                'type': 'String'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'rightValue',
                'type': 'Object'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'rightField',
                'type': 'String'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'leftValue',
                'type': 'Object'
            }
        ],
        'description': '',
        'returns': 'Filter'
    },
    'Filter.stringEndsWith': {
        'type': 'Algorithm',
        'args': [
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'leftField',
                'type': 'String'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'rightValue',
                'type': 'Object'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'rightField',
                'type': 'String'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'leftValue',
                'type': 'Object'
            }
        ],
        'description': '',
        'returns': 'Filter'
    },
    'Filter.listContains': {
        'type': 'Algorithm',
        'args': [
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'leftField',
                'type': 'String'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'rightValue',
                'type': 'Object'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'rightField',
                'type': 'String'
            },
            {
                'default': None,
                'description': '',
                'optional': True,
                'name': 'leftValue',
                'type': 'Object'
            }
        ],
        'description': '',
        'returns': 'Filter'
    },
    'Image.mask': {
        'type': 'Algorithm',
        'args': [
            {
                'name': 'image',
                'type': 'Image',
                'description': ''
            },
            {
                'name': 'mask',
                'type': 'Image',
                'description': '',
                'optional': True,
                'default': None
            }
        ],
        'description': '',
        'returns': 'Image'
    },
    # These two functions (Dictionary.get and Image.reduceRegion) are here
    # to force the creation of the Dictionary class.
    'Dictionary.get': {
        'returns': 'Object',
        'args': [
            {
                'type': 'Dictionary<Object>',
                'description': '',
                'name': 'map'
                },
            {
                'type': 'String',
                'description': '',
                'name': 'property'
                }
            ],
        'type': 'Algorithm',
        'description': '',
    },
    'Image.reduceRegion': {
        'returns': 'Dictionary<Object>',
        'hidden': False,
        'args': [
            {
                'type': 'Image',
                'description': '',
                'name': 'image'
            },
            {
                'type': 'ReducerOld',
                'description': '',
                'name': 'reducer'
            },
            {
                'default': None,
                'type': 'ProjGeometry',
                'optional': True,
                'description': '',
                'name': 'geometry'
            },
            {
                'default': None,
                'type': 'Double',
                'optional': True,
                'description': '',
                'name': 'scale'
            },
            {
                'default': 'EPSG:4326',
                'type': 'String',
                'optional': True,
                'description': '',
                'name': 'crs'
            },
            {
                'default': None,
                'type': 'double[]',
                'optional': True,
                'description': '',
                'name': 'crsTransform'
            },
            {
                'default': False,
                'type': 'boolean',
                'optional': True,
                'description': '',
                'name': 'bestEffort'
            }
        ],
        'type': 'Algorithm',
        'description': ''
    },
}
