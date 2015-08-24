#!/usr/bin/env python
#
# lightboxtoolbar.py -
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#


import wx

import props

import fsl.fsleyes.toolbar  as fsltoolbar
import fsl.fsleyes.actions  as actions
import fsl.fsleyes.icons    as fslicons
import fsl.fsleyes.tooltips as fsltooltips
import fsl.data.strings     as strings


class LightBoxToolBar(fsltoolbar.FSLEyesToolBar):

    def __init__(self, parent, overlayList, displayCtx, lb):

        actionz = {'more' : self.showMoreSettings}
        
        fsltoolbar.FSLEyesToolBar.__init__(
            self, parent, overlayList, displayCtx, 24, actionz)
        self.lightBoxPanel = lb

        lbOpts = lb.getSceneOptions()
        
        icons = {
            'screenshot'  : fslicons.findImageFile('camera24'),
            'movieMode'   : fslicons.findImageFile('movie24'),
            'more'        : fslicons.findImageFile('gear24'),

            'zax' : {
                0 : fslicons.findImageFile('sagittalSlice24'),
                1 : fslicons.findImageFile('coronalSlice24'),
                2 : fslicons.findImageFile('axialSlice24'),
            }
        }

        tooltips = {

            'more'         : fsltooltips.actions[   self,    'more'],
            'screenshot'   : fsltooltips.actions[   lb,      'screenshot'],
            'movieMode'    : fsltooltips.properties[lb,      'movieMode'],
            'zax'          : fsltooltips.properties[lbOpts,  'zax'],
            'sliceSpacing' : fsltooltips.properties[lbOpts,  'sliceSpacing'],
            'zrange'       : fsltooltips.properties[lbOpts,  'zrange'],
            'zoom'         : fsltooltips.properties[lbOpts,  'zoom'],
        }
        
        specs = {
            
            'more'       : actions.ActionButton(
                'more',
                icon=icons['more'],
                tooltip=tooltips['more']),
            'screenshot' : actions.ActionButton(
                'screenshot',
                icon=icons['screenshot'],
                tooltip=tooltips['screenshot']),

            'movieMode'    : props.Widget(
                'movieMode',
                icon=icons['movieMode'],
                tooltip=tooltips['movieMode']), 
            
            'zax'          : props.Widget(
                'zax',
                icons=icons['zax'],
                tooltip=tooltips['zax']),
            
            'sliceSpacing' : props.Widget(
                'sliceSpacing',
                spin=False,
                showLimits=False,
                tooltip=tooltips['sliceSpacing']),
            
            'zrange'       : props.Widget(
                'zrange',
                spin=False,
                showLimits=False,
                tooltip=tooltips['zrange'],
                labels=[strings.choices[lbOpts, 'zrange', 'min'],
                        strings.choices[lbOpts, 'zrange', 'max']]),
            
            'zoom'         : props.Widget(
                'zoom',
                spin=False,
                showLimits=False,
                tooltip=tooltips['zoom']),
        }

        # Slice spacing and zoom go on a single panel
        panel = wx.Panel(self)
        sizer = wx.FlexGridSizer(2, 2)
        panel.SetSizer(sizer)

        more         = props.buildGUI(self,  self,   specs['more'])
        screenshot   = props.buildGUI(self,  lb,     specs['screenshot'])
        movieMode    = props.buildGUI(self,  lb,     specs['movieMode'])
        zax          = props.buildGUI(self,  lbOpts, specs['zax'])
        zrange       = props.buildGUI(self,  lbOpts, specs['zrange'])
        zoom         = props.buildGUI(panel, lbOpts, specs['zoom'])
        spacing      = props.buildGUI(panel, lbOpts, specs['sliceSpacing'])
        zoomLabel    = wx.StaticText(panel)
        spacingLabel = wx.StaticText(panel)

        zoomLabel   .SetLabel(strings.properties[lbOpts, 'zoom'])
        spacingLabel.SetLabel(strings.properties[lbOpts, 'sliceSpacing'])

        sizer.Add(zoomLabel)
        sizer.Add(zoom,    flag=wx.EXPAND)
        sizer.Add(spacingLabel)
        sizer.Add(spacing, flag=wx.EXPAND)

        tools = [more, screenshot, zax, movieMode, zrange, panel]
        
        self.SetTools(tools) 

        
    def showMoreSettings(self, *a):
        import canvassettingspanel
        self.lightBoxPanel.togglePanel(
            canvassettingspanel.CanvasSettingsPanel,
            self.lightBoxPanel,
            floatPane=True) 
