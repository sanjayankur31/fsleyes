#!/usr/bin/env python
#
# __init__.py - Functions for OpenGL 2.1 rendering.
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#
"""This package contains modules for rendering various :class:`.GLObject`
types in an OpenGL 2.1 compatible manner. The following modules currently
exist:

.. autosummary::

   ~fsl.fsleyes.gl.gl21.glvolume_funcs
   ~fsl.fsleyes.gl.gl21.glrgbvector_funcs
   ~fsl.fsleyes.gl.gl21.gllinevector_funcs
   ~fsl.fsleyes.gl.gl21.glmodel_funcs
   ~fsl.fsleyes.gl.gl21.gllabel_funcs
   ~fsl.fsleyes.gl.gl21.gltensor_funcs
"""


from . import glvolume_funcs
from . import glrgbvector_funcs
from . import gllinevector_funcs
from . import glmodel_funcs
from . import gllabel_funcs
from . import gltensor_funcs
