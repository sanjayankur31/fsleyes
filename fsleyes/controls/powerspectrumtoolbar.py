#!/usr/bin/env python
#
# powerspectrumtoolbar.py - The PowerSpectrumToolBar class.
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#
"""This module provides the :class:`PowerSpectrumToolBar`, a toolbar for use
with a :class:`.PowerSpectrumPanel`.
"""


import props

import fsleyes.icons    as icons
import fsleyes.tooltips as tooltips
import fsleyes.actions  as actions


from . import plottoolbar


class PowerSpectrumToolBar(plottoolbar.PlotToolBar):
    """The ``PowerSpectrumToolBar`` is a toolbar for use with a
    :class:`.PowerSpectrumPanel`. It extends :class:`.PlotToolBar`,
    and adds a few controls specific to the :class:`.PoweSpectrumPanel`.
    """

    def __init__(self, parent, overlayList, displayCtx, psPanel):
        """Create a ``PowerSpectrumToolBar``.

        :arg parent:      The :mod:`wx` parent object.
        :arg overlayList: The :class:`.OverlayList` instance.
        :arg displayCtx:  The :class:`.DisplayContext` instance.
        :arg psPanel:     The :class:`.PowerSpectrumPanel` instance.
        """
        
        plottoolbar.PlotToolBar.__init__(
            self, parent, overlayList, displayCtx, psPanel)

        togControl = actions.ToggleActionButton(
            'togglePowerSpectrumControl',
            actionKwargs={'floatPane' : True},
            icon=[icons.findImageFile('spannerHighlight24'),
                  icons.findImageFile('spanner24')],
            tooltip=tooltips.actions[psPanel, 'togglePowerSpectrumControl'])
 
        togList = actions.ToggleActionButton(
            'togglePowerSpectrumList',
            actionKwargs={'floatPane' : True},
            icon=[icons.findImageFile('listHighlight24'),
                  icons.findImageFile('list24')],
            tooltip=tooltips.actions[psPanel, 'togglePowerSpectrumList']) 

        togControl = props.buildGUI(self, psPanel, togControl)
        togList    = props.buildGUI(self, psPanel, togList)

        self.InsertTools([togControl, togList], 0) 