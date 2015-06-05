import pymel.core as pc

import re

from . import utilities
from .utilities import clamp, fovToFocalLength, lockAndHide

__all__ = ['createMultiRig', 'attachToCameraSet', 'registerMultiRig']
__multiRigTypeName = 'MultiStereoRig'

optimalDistance = 350.0
screenSizeWidth = 146.038079067483
origFov = 23.568699088151078

endnumPattern = re.compile(r'^.*?(\d*)$')


def createMultiStereoCamera(root, rootShape, camIndex, nStereoCams=9):
    cam, camShape = pc.camera()
    cam.parent(root)
    name = str(root) + '_StereoCam%02d' % camIndex
    cam.rename(name)

    camShape.renderable.set(False)

    # Connect the camera attributes from the master, hide them
    #
    for attr in [ 'horizontalFilmAperture',
                    'verticalFilmAperture',
                    'focalLength',
                    'lensSqueezeRatio',
                    'fStop',
                    'focusDistance',
                    'shutterAngle',
                    'cameraPrecompTemplate',
                    'filmFit',
                    'displayFilmGate',
                    'displayResolution',
                    'nearClipPlane',
                    'farClipPlane' ] :
        camShapeAttr = camShape.attr(attr)
        rootShape.attr(attr) >> camShapeAttr
        camShapeAttr.set(keyable=False)

    for attr in [ 'scaleX', 'scaleY', 'scaleZ',
                    'visibility',
                    'centerOfInterest' ] :
        cam.attr(attr).set(keyable=False)

    return cam


def createMultiRig(basename='multiStereoCamera', nStereoCams=9):
    ''' Creates a Simple Multi Stereo camera rig to be used in autostereoscopic
    displays '''
    if nStereoCams < 2:
        nStereoCams = 2

    root = pc.createNode( 'stereoRigTransform', name=basename )

    numstr = ''
    nummatch = endnumPattern.match(root)
    if nummatch:
        numstr = nummatch.group(1)

    rootShape = pc.createNode('stereoRigCamera', name=basename + 'Shape' + numstr)

    stereoCams = [createMultiStereoCamera(root, rootShape, i, nStereoCams) for
            i in nStereoCams]

    return [root, stereoCams[nStereoCams/2], stereoCams[nStereoCams/2+1]]


def attachToCameraSet(*args, **keywords):
    pass


def registerMultiRig():
    pc.loadPlugin('stereoCamera', quiet=True)
    pc.stereoRigManager(add=[__multiRigTypeName, 'Python',
        'mvstereo.cammaker.createMultiRig'])

