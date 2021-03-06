#!/usr/bin/env python
#
# test_resample.py -
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#

try:
    from unittest import mock
except ImportError:
    import mock

import numpy as np

import wx

import fsl.data.image as fslimage

import fsleyes.actions.resample as resample

from . import (run_with_fsleyes,
               run_with_orthopanel,
               realYield,
               simtext,
               simclick)


def test_resample():
    run_with_orthopanel(_test_resample)


def _test_resample(panel, overlayList, displayCtx):


    class ResampleDialog(object):
        ShowModal_return        = None
        GetVoxels_return        = None
        GetPixdims_return       = None
        GetInterpolation_return = None
        GetDataType_return      = None
        GetSmoothing_return     = None
        GetAllVolumes_return    = None
        def __init__(self, *args, **kwargs):
            pass
        def ShowModal(self):
            return ResampleDialog.ShowModal_return

        def GetVoxels(self):
            return ResampleDialog.GetVoxels_return
        def GetInterpolation(self):
            return ResampleDialog.GetInterpolation_return
        def GetDataType(self):
            return ResampleDialog.GetDataType_return
        def GetSmoothing(self):
            return ResampleDialog.GetSmoothing_return
        def GetAllVolumes(self):
            return ResampleDialog.GetAllVolumes_return
        def GetPixdims(self):
            return ResampleDialog.GetPixdims_return


    act = resample.ResampleAction(overlayList, displayCtx, panel.frame)

    with mock.patch('fsleyes.actions.resample.ResampleDialog', ResampleDialog):

        img = fslimage.Image(np.random.randint(1, 255, (20, 20, 20)))
        overlayList.append(img)

        ResampleDialog.ShowModal_return = wx.ID_CANCEL
        act()
        assert len(overlayList) == 1

        ResampleDialog.ShowModal_return        = wx.ID_OK
        ResampleDialog.GetVoxels_return        = (10, 10, 10)
        ResampleDialog.GetInterpolation_return = 'linear'
        ResampleDialog.GetDataType_return      = np.int32
        ResampleDialog.GetSmoothing_return     = True
        ResampleDialog.GetAllVolumes_return    = True
        ResampleDialog.GetPixdims_return       = (2, 2, 2)
        act()
        assert len(overlayList) == 2
        resampled = overlayList[1]
        assert tuple(resampled.shape)  == (10, 10, 10)
        assert tuple(resampled.pixdim) == (2, 2, 2)
        assert resampled.dtype         == np.int32

        img = fslimage.Image(np.random.randint(1, 255, (20, 20, 20, 15)))
        overlayList.clear()
        overlayList.append(img)
        act()
        assert len(overlayList) == 2
        resampled = overlayList[1]
        assert tuple(resampled.shape)  == (10, 10, 10, 15)
        assert tuple(resampled.pixdim) == (2, 2, 2, 1)
        assert resampled.dtype         == np.int32

        overlayList.clear()
        overlayList.append(img)
        ResampleDialog.GetAllVolumes_return = False
        act()
        assert len(overlayList) == 2
        resampled = overlayList[1]
        assert tuple(resampled.shape)  == (10, 10, 10)
        assert tuple(resampled.pixdim) == (2, 2, 2)
        assert resampled.dtype         == np.int32


def test_ResampleDialog():
    run_with_fsleyes(_test_ResampleDialog)

def _test_ResampleDialog(frame, overlayList, displayCtx):

    sim = wx.UIActionSimulator()

    # click ok
    dlg = resample.ResampleDialog(frame,
                                  'title',
                                  (10, 10, 10),
                                  (1, 1, 1))
    wx.CallLater(500, simclick, sim, dlg.okButton)
    assert dlg.ShowModal() == wx.ID_OK

    # click cancel
    dlg = resample.ResampleDialog(frame,
                                  'title',
                                  (10, 10, 10),
                                  (1, 1, 1))
    wx.CallLater(500, simclick, sim, dlg.cancelButton)
    assert dlg.ShowModal() == wx.ID_CANCEL

    # set voxel dims
    dlg = resample.ResampleDialog(frame,
                                  'title',
                                  (10, 10, 10),
                                  (1, 1, 1))
    wx.CallLater(300,  simtext,  sim, dlg.voxXCtrl.textCtrl, '20')
    wx.CallLater(400,  simtext,  sim, dlg.voxYCtrl.textCtrl, '40')
    wx.CallLater(500,  simtext,  sim, dlg.voxZCtrl.textCtrl, '80')
    wx.CallLater(1000, simclick, sim, dlg.okButton)
    dlg.ShowModal()
    assert dlg.GetVoxels()  == (20,  40,   80)
    assert dlg.GetPixdims() == (0.5, 0.25, 0.125)
    dlg.Destroy()


    # set pixdims
    dlg = resample.ResampleDialog(frame,
                                  'title',
                                  (10, 10, 10),
                                  (1, 1, 1))

    wx.CallLater(300,  simtext,  sim, dlg.pixXCtrl.textCtrl, '0.5')
    wx.CallLater(400,  simtext,  sim, dlg.pixYCtrl.textCtrl, '0.25')
    wx.CallLater(500,  simtext,  sim, dlg.pixZCtrl.textCtrl, '0.125')
    wx.CallLater(1000, simclick, sim, dlg.okButton)
    dlg.ShowModal()
    assert dlg.GetVoxels()  == (20,  40,   80)
    assert dlg.GetPixdims() == (0.5, 0.25, 0.125)
    dlg.Destroy()

    # reset
    dlg = resample.ResampleDialog(frame,
                                  'title',
                                  (10, 10, 10),
                                  (1, 1, 1))
    wx.CallLater(300,  simtext,  sim, dlg.pixXCtrl.textCtrl, '0.5')
    wx.CallLater(400,  simtext,  sim, dlg.pixYCtrl.textCtrl, '0.25')
    wx.CallLater(500,  simtext,  sim, dlg.pixZCtrl.textCtrl, '0.125')
    wx.CallLater(1000, simclick, sim, dlg.resetButton)
    wx.CallLater(1500, simclick, sim, dlg.okButton)
    dlg.ShowModal()
    assert dlg.GetVoxels()  == (10, 10, 10)
    assert dlg.GetPixdims() == (1, 1, 1)
    dlg.Destroy()

    # set options
    dlg = resample.ResampleDialog(frame,
                                  'title',
                                  (10, 10, 10, 10),
                                  (1, 1, 1))

    dlg.interpCtrl.SetSelection(1)
    dlg.dtypeCtrl .SetSelection(1)

    origSmooth  = dlg.GetSmoothing()
    origAllVols = dlg.GetAllVolumes()

    wx.CallLater(500,  simclick, sim, dlg.smoothCtrl)
    wx.CallLater(1000, simclick, sim, dlg.allVolumesCtrl)
    wx.CallLater(1500, simclick, sim, dlg.okButton)
    dlg.ShowModal()
    assert dlg.GetSmoothing()     == (not origSmooth)
    assert dlg.GetAllVolumes()    == (not origAllVols)
    assert dlg.GetInterpolation() == 'nearest'
    assert dlg.GetDataType()      == np.uint8
    dlg.Destroy()
