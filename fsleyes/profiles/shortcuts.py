#!/usr/bin/env python
#
# shortcuts.py - Keyboard shortcuts
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#
"""This module defines keyboard shortcuts used throughout FSLeyes.
"""

import fsl.utils.typedict as td


actions = td.TypeDict({
    
    'LoadOverlayAction'        : 'Ctrl-O',
    'LoadOverlayFromDirAction' : 'Ctrl-D',
    'LoadStandardAction'       : 'Ctrl-S',
    'CopyOverlayAction'        : 'Ctrl-Alt-C',
    'SaveOverlayAction'        : 'Ctrl-Alt-S',
    'CorrelateAction'          : 'Ctrl-Alt-P',
    'ReloadOverlayAction'      : 'Ctrl-Alt-R',
    'RemoveOverlayAction'      : 'Ctrl-Alt-W',

    'FSLeyesFrame.closeFSLeyes'           : 'Ctrl-Q',
    'FSLeyesFrame.openHelp'               : 'Ctrl-H',
    'FSLeyesFrame.removeFocusedViewPanel' : 'Ctrl-W',
    
    'FSLeyesFrame.perspectives.default'   : 'Ctrl-D',

    'FSLeyesFrame.addOrthoPanel'          : 'Ctrl-1',
    'FSLeyesFrame.addLightBoxPanel'       : 'Ctrl-2',
    'FSLeyesFrame.addTimeSeriesPanel'     : 'Ctrl-3',
    'FSLeyesFrame.addHistogramPanel'      : 'Ctrl-4',
    'FSLeyesFrame.addPowerSpectrumPanel'  : 'Ctrl-5',
    'FSLeyesFrame.addShellPanel'          : 'Ctrl-6',
    
    'FSLeyesFrame.selectNextOverlay'       : 'Ctrl-Up',
    'FSLeyesFrame.selectPreviousOverlay'   : 'Ctrl-Down',
    'FSLeyesFrame.toggleOverlayVisibility' : 'Ctrl-Z',
 

    # ViewPanel actions must use one
    # of CTRL, ALT or Shift due to
    # hacky things in FSLeyesFrame.

    'CanvasPanel.toggleOverlayList'         : 'Ctrl-Alt-1',
    'CanvasPanel.toggleLocationPanel'       : 'Ctrl-Alt-2',
    'CanvasPanel.toggleOverlayInfo'         : 'Ctrl-Alt-3',
    'CanvasPanel.toggleDisplayPanel'        : 'Ctrl-Alt-4',
    'CanvasPanel.toggleCanvasSettingsPanel' : 'Ctrl-Alt-5',
    'CanvasPanel.toggleAtlasPanel'          : 'Ctrl-Alt-6',

    'CanvasPanel.toggleDisplayToolBar'      : 'Ctrl-Alt-7',
    
    'OrthoPanel.toggleOrthoToolBar'         : 'Ctrl-Alt-8',

    'CanvasPanel.toggleMovieMode'           : 'Alt-M',
    'CanvasPanel.toggleDisplaySync'         : 'Alt-S',
    
    'OrthoPanel.toggleEditMode'             : 'Alt-E',
    'OrthoPanel.resetDisplay'               : 'Alt-R',
    'OrthoPanel.centreCursor'               : 'Alt-P',
    'OrthoPanel.centreCursorWorld'          : 'Alt-O',
    'OrthoPanel.toggleLabels'               : 'Alt-L',
    'OrthoPanel.toggleCursor'               : 'Alt-C',
    'OrthoPanel.toggleXCanvas'              : 'Alt-X',
    'OrthoPanel.toggleYCanvas'              : 'Alt-Y',
    'OrthoPanel.toggleZCanvas'              : 'Alt-Z',

    'LightBoxPanel.toggleLightBoxToolBar'   : 'Ctrl-Alt-8',

    'PlotPanel.toggleOverlayList'         : 'Ctrl-Alt-1',
    'PlotPanel.togglePlotList'            : 'Ctrl-Alt-2',
    'PlotPanel.importDataSeries'          : 'Alt-I',
    'PlotPanel.exportDataSeries'          : 'Alt-E',

    'TimeSeriesPanel.toggleTimeSeriesToolBar'       : 'Ctrl-Alt-3',
    'TimeSeriesPanel.toggleTimeSeriesControl'       : 'Ctrl-Alt-4',
    'HistogramPanel.toggleHistogramToolBar'         : 'Ctrl-Alt-3',
    'HistogramPanel.toggleHistogramControl'         : 'Ctrl-Alt-4',
    'PowerSpectrumPanel.togglePowerSpectrumToolBar' : 'Ctrl-Alt-3',
    'PowerSpectrumPanel.togglePowerSpectrumControl' : 'Ctrl-Alt-4', 
})
