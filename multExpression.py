import os
from string import Template


__all__ = ['getMultStereoExpression']

expPath = os.path.join(os.path.dirname(__file__), 'multExpression.mel')
multExpression = ''
with open(expPath) as expFile:
    multExpression = expFile.read()
multExpressionTemplate = Template(multExpression)

def getMultStereoExpression(
        mult,
        hfoAttr,
        offsetAttr,
        rotAttr,
        zeroAttr,
        camTranslateXAttr,
        camHfoAttr,
        camRotXAttr
        ):
    data = {}
    data['s_mult']=str(mult)
    data['s_hfoAttr']=str(hfoAttr)
    data['s_offsetAttr']=str(offsetAttr)
    data['s_rotAttr']=str(rotAttr)
    data['s_zeroParallaxPlaneAttr']=str(zeroAttr)
    data['s_camTranslateXAttr']=str(camTranslateXAttr)
    data['s_camHfoAttr']=camHfoAttr
    data['s_camRotXAttr']=camRotXAttr
    expression = multExpressionTemplate.safe_substitute(data)
    return expression

