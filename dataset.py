def load_videos():
    datasetDir = '/run/media/john_tukey/download/datasets/5c1dataset/'

    tears_of_steel_end = { 'fname' : 'tears.of.steel.end.24.1280x534.420',
                           'show' : 'tears of steel end',
                           'fpath' : datasetDir,
                           'width' : '1280',
                           'height' : '534',
                           'framerate': '24/1'}

    tears_of_steel = {'fname': 'tears.of.steel.24.1280x534.420',
                      'show' : 'tears of steel',
                          'fpath': datasetDir,
                          'width': '1280',
                          'height': '534',
                          'framerate': '24/1'}

    waterWorld = {'fname': 'waterWorld.2997.1280x720.420',
                  'show': 'waterWorld',
                  'fpath': datasetDir,
                  'width': '1280',
                  'height': '720',
                  'framerate':'30000/1001'}

    basketball_1 = {'fname': 'basketball.1.2982.1280x720.420',
                    'show': 'basketball 1',
                    'fpath': datasetDir,
                    'width': '1280',
                    'height': '720',
                    'framerate': '2982/100' # who comes up with these numbers, really
                    }

    basketball_2 = {'fname': 'basketball.2.2982.1280x720.420',
                    'show' : 'basketball 2',
                    'fpath': datasetDir,
                    'width': '1280',
                    'height': '720',
                    'framerate': '2982/100'
                    }

    gameplay = {'fname': 'gameplay.30.1280x720.420',
                'show': 'gameplay',
                    'fpath': datasetDir,
                    'width': '1280',
                    'height': '720',
                    'framerate': '30/1' # who plays CS:GO at 30 fps?
                    }

    gameplay_2 = {'fname': 'gameplay.2.30.1280x720.420',
                  'show' : 'gameplay 2',
                'fpath': datasetDir,
                'width': '1280',
                'height': '720',
                'framerate': '30/1'
                }

    waves = {'fname': 'waves.30.1280x720.420',
             'show': 'waves',
                'fpath': datasetDir,
                'width': '1280',
                'height': '720',
                'framerate': '30/1'
                }
    flowers_1 = {'fname': 'flowers.1.30.1280x720.420',
                 'show': 'flowers',
                'fpath': datasetDir,
                'width': '1280',
                'height': '720',
                'framerate': '30/1'
                }

    flowers_2 = {'fname': 'flowers.2.30.1280x720.420',
                 'show': 'flowers 2',
                 'fpath': datasetDir,
                 'width': '1280',
                 'height': '720',
                 'framerate': '30/1'
                 }

    elon = {'fname': 'elon.2997.1280x720.420',
            'show' : 'elon',
                 'fpath': datasetDir,
                 'width': '1280',
                 'height': '720',
                 'framerate': '30000/1001'
                 }




    videos = (
            tears_of_steel_end,
              tears_of_steel,
              waterWorld,
              basketball_1,
              basketball_2,
              gameplay,
              gameplay_2,
              waves,
              flowers_1,
              flowers_2,
              elon
              )

    return videos