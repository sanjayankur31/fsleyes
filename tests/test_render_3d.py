#!/usr/bin/env python
#
# test_render_3d.py -
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#

import pytest

from . import run_cli_tests


pytestmark = pytest.mark.clitest


cli_tests = """
-z 25   3d.nii.gz
-z 50   3d.nii.gz
-z 100  3d.nii.gz
-z 1500 3d.nii.gz
-he     3d.nii.gz

-cb -fs 20 3d.nii.gz

     3d.nii.gz  3d.nii.gz -cr 6300 8000 -cm red-yellow
-noc 3d.nii.gz  3d.nii.gz -cr 6300 8000 -cm red-yellow

                  gifti/white.surf.gii -mc 1 0 0
-dl               gifti/white.surf.gii -mc 1 0 0
-lp  200  0   0   gifti/white.surf.gii -mc 1 0 0
-lp -200  0   0   gifti/white.surf.gii -mc 1 0 0
-lp  0    200 0   gifti/white.surf.gii -mc 1 0 0
-lp  0   -200 0   gifti/white.surf.gii -mc 1 0 0
-lp  0    0   200 gifti/white.surf.gii -mc 1 0 0
-lp  0    0  -200 gifti/white.surf.gii -mc 1 0 0

-off  0    0   mesh_l_thal.vtk -mc 1 0 0
-off  0.5  0.5 mesh_l_thal.vtk -mc 1 0 0
-off  0.5 -0.5 mesh_l_thal.vtk -mc 1 0 0
-off -0.5  0.5 mesh_l_thal.vtk -mc 1 0 0
-off -0.5 -0.5 mesh_l_thal.vtk -mc 1 0 0

-rot  45   0   0 gifti/white.surf.gii -mc 1 0 0
-rot -45   0   0 gifti/white.surf.gii -mc 1 0 0
-rot   0  45   0 gifti/white.surf.gii -mc 1 0 0
-rot   0 -45   0 gifti/white.surf.gii -mc 1 0 0
-rot   0   0  45 gifti/white.surf.gii -mc 1 0 0
-rot   0   0 -45 gifti/white.surf.gii -mc 1 0 0

-rot  45  45   0 gifti/white.surf.gii -mc 1 0 0
-rot  45 -45   0 gifti/white.surf.gii -mc 1 0 0
-rot -45 -45  45 gifti/white.surf.gii -mc 1 0 0
-rot -45 -45 -45 gifti/white.surf.gii -mc 1 0 0
"""


def test_render_3d():
    extras = {
    }
    run_cli_tests('test_render_3d', cli_tests, extras=extras, scene='3d')
