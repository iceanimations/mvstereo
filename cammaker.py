import pymel.core as pc

import re

from . import utilities
reload(utilities)
from .utilities import clamp, lockAndHide

from . import multExpression
reload(multExpression)
from .multExpression import getMultStereoExpression


__all__ = ['createMultiRig', 'attachToCameraSet', 'registerMultiRig',
'UnregisterMultiRig']

__multiRigTypeName = 'MultiStereoRig'

optimalDistance = 350.0
screenSizeWidth = 146.038079067483
origFov = 23.568699088151078

endnumPattern = re.compile(r'^.*?(\d*)$')


def createMultiStereoCamera(root, rootShape, camIndex, nStereoCams=9):
    cam, camShape = pc.camera()
    pc.parent(cam, root)
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

    for attr in [ 'visibility', 'centerOfInterest' ] :
        cam.attr(attr).set(keyable=False)

    #stereoOffset = stereoEyeSeparation * (camIndex - nCams/2.0 + 0.5)
    #shift = -stereoOffset * (fl/10.0) / imageZ * p / (INCHES_TO_MM/10)
    mult = camIndex - nStereoCams / 2.0 + 0.5
    offsetAttr = 'stereoRightOffset'
    rotAttr = 'stereoRightAngle'
    hfoAttr = 'filmBackOutputRight'
    if mult < 0:
        offsetAttr = 'stereoLeftOffset'
        rotAttr = 'stereoLeftAngle'
        hfoAttr = 'filmBackOutputLeft'
        mult = abs(mult)
    offsetAttr = root.attr(offsetAttr)
    rotAttr = root.attr(rotAttr)
    hfoAttr = root.attr(hfoAttr)

    expression = getMultStereoExpression(
            mult,
            hfoAttr,
            offsetAttr,
            rotAttr,
            rootShape.zeroParallax,
            cam.translateX,
            camShape.hfo,
            cam.rotateX
            )
    exprNode = pc.expression(s=expression)
    exprNode.rename(cam.name() + '_expression')

    lockAndHide(cam)
    return cam


def createMainCam(basename='multiStereoCamera'):
    ''' create the main stereoRig Root Cam'''

    root = pc.createNode( 'stereoRigTransform', name=basename )

    numstr = ''
    nummatch = endnumPattern.match(root.name())
    if nummatch:
        numstr = nummatch.group(1)

    rootShape = pc.createNode('stereoRigCamera',
            name=basename + 'Shape' + numstr,
            parent=root)

    return root, rootShape


def createMultiRig(basename='multiStereoCamera', nStereoCams=9):
    ''' Creates a Simple Multi Stereo camera rig to be used in autostereoscopic
    displays '''

    try:
        nStereoCams = clamp(2, 16, nStereoCams)

        # create Main Central Cam
        root, rootShape = createMainCam(basename)

        # create Stereo Cams
        stereoCams = [
                createMultiStereoCamera(root, rootShape, i, nStereoCams)
                for i in range( nStereoCams )]

        camarray = [root, stereoCams[nStereoCams/2], stereoCams[nStereoCams/2+1]]

        pc.select(root)
        return [node.name() for node in camarray]

    except Exception as e:
        import traceback
        traceback.print_exc()
        print e
        raise


def attachToCameraSet(*args, **keywords):
    pass


def registerMultiRig():
    pc.loadPlugin('stereoCamera', quiet=True)
    UnregisterMultiRig()
    pc.stereoRigManager(add=[__multiRigTypeName, 'Python',
        'mvstereo.createMultiRig'])

def UnregisterMultiRig():
    try:
        pc.stereoRigManager(delete=__multiRigTypeName)
    except:
        pass


