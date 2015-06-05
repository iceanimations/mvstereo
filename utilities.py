import math

INCHES_TO_MM = 25.4

# utility functions
def clamp(min, max, value):
    return sorted((min, value, max))[1]

def fovToFocalLength(fov, filmBackWidth=1.417):
    ''' filmBackWidth is in mm '''
    return filmBackWidth * INCHES_TO_MM / ( 2 * math.tan(fov/2.0) )

def focalLengthToFov(focalLength, filmBackWidth=1.417):
    ''' filmBackWidth is in mm '''
    return 2 * math.atan( filmBackWidth * INCHES_TO_MM / (2.0 * focalLength) )

def lockAndHide(node, tr=True, ro=True, scale=True):
    if scale:
        node.scaleX.set(l=True)
        node.scaleY.set(l=True)
        node.scaleZ.set(l=True)
        node.scaleX.setKeyable(False)
        node.scaleY.setKeyable(False)
        node.scaleZ.setKeyable(False)
    if ro:
        node.rotateX.set(l=True)
        node.rotateY.set(l=True)
        node.rotateZ.set(l=True)
        node.rotateX.setKeyable(False)
        node.rotateY.setKeyable(False)
        node.rotateZ.setKeyable(False)
    if tr:
        node.translateX.set(l=True)
        node.translateY.set(l=True)
        node.translateZ.set(l=True)
        node.translateX.setKeyable(False)
        node.translateY.setKeyable(False)
        node.translateZ.setKeyable(False)

def testFocalLengthToFov():
    assert focalLengthToFov(35) == 0.9500215125301936

def testFovToFocalLength():
    assert fovToFocalLength(0.9500215125301936) == 35

if __name__ == '__main__':
    testFocalLengthToFov()
    testFovToFocalLength()
