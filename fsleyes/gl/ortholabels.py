#!/usr/bin/env python
#
# ortholabels.py - The OrthoLabels class.
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#
"""This module provides the :class:`OrthoLabels` class, which manages
anatomical orientation labels for an :class:`.OrthoPanel`.

This logic is independent from the :class:`.OrthoPanel` so it can be used in
off-screen rendering (see :mod:`.render`).
"""


import fsl.data.constants as constants
import fsleyes.strings    as strings


class OrthoLabels(object):
    """The ``OrthoLabels`` class manages anatomical orientation labels which 
    are displayed on a set of three :class:`.SliceCanvas` instances, one for 
    each plane in the display coordinate system, typically within an
    :class:`.OrthoPanel`.

    The ``OrthoLabels`` class uses :class:`.annotations.Text` annotations,
    showing the user the anatomical orientation of the display on each
    canvas. These labels are only shown if the currently selected overlay (as
    dicated by the :attr:`.DisplayContext.selectedOverlay` property) is a
    :class:`.Image` instance, **or** the
    :meth:`.DisplayOpts.getReferenceImage` method for the currently selected
    overlay returns an :class:`.Image` instance.
    """


    def __init__(self,
                 overlayList,
                 displayCtx,
                 orthoOpts,
                 xcanvas,
                 ycanvas,
                 zcanvas):
        """Create an ``OrthoLabels`` instance.

        :arg overlayList: The :class:`.OverlayList`.
        :arg displayCtx:  The :class:`.DisplayContext`.
        :arg orthoOpts:   :class:`.OrthoOpts` instance which contains
                          display settings.
        :arg xcanvas:     :class:`.SliceCanvas` for the X plane, or ``None``.
        :arg ycanvas:     :class:`.SliceCanvas` for the Y plane, or ``None``.
        :arg zcanvas:     :class:`.SliceCanvas` for the Z plane, or ``None``.
        """

        self.__name        = '{}_{}'.format(type(self).__name__, id(self))
        self.__orthoOpts   = orthoOpts
        self.__displayCtx  = displayCtx
        self.__overlayList = overlayList

        # Any of the canvases may be None,
        # so we store a list of the ones
        # that are not None.
        # 
        # labels is a list of dicts, one
        # for each canvas, containing Text
        # annotations to show anatomical
        # orientation
        canvases  = [xcanvas, ycanvas, zcanvas]
        canvases  = [c  for c in canvases if c is not None]
        annots    = [{} for c in canvases]

        self.__canvases = canvases
        self.__annots   = annots

        # Create the Text annotations
        for side in ('left', 'right', 'top', 'bottom'):
            for canvas, cannots in zip(canvases, annots):
                annot         = canvas.getAnnotations()
                cannots[side] = annot.text('', 0, 0, width=2, hold=True)

        # Initialise the display properties 
        # of each Text annotation
        for cannots in annots:
            cannots['left']  .halign = 'left'
            cannots['right'] .halign = 'right'
            cannots['top']   .halign = 'centre'
            cannots['bottom'].halign = 'centre'

            cannots['left']  .valign = 'centre'
            cannots['right'] .valign = 'centre'
            cannots['top']   .valign = 'top'
            cannots['bottom'].valign = 'bottom'

            cannots['left']  .xpos = 0
            cannots['left']  .ypos = 0.5
            cannots['right'] .xpos = 1.0
            cannots['right'] .ypos = 0.5
            cannots['bottom'].xpos = 0.5
            cannots['bottom'].ypos = 0
            cannots['top']   .xpos = 0.5
            cannots['top']   .ypos = 1.0

            # Keep cannots 5 pixels away
            # from the canvas edges
            cannots['left']  .xoff =  5
            cannots['right'] .xoff = -5
            cannots['top']   .yoff = -5
            cannots['bottom'].yoff =  5

        # Add listeners to properties
        # that need to trigger a label
        # refresh.
        name = self.__name
 
        # Make immediate so the label
        # annotations get updated before
        # a panel refresh occurs (where
        # the latter is managed by the
        # OrthoPanel).
        refreshArgs = {
            'name'      : name,
            'callback'  : self.__refreshLabels,
            'immediate' : True
        }

        for c in canvases:
            c.addListener('invertX', **refreshArgs)
            c.addListener('invertY', **refreshArgs)

        orthoOpts  .addListener('showLabels',       **refreshArgs)
        orthoOpts  .addListener('labelSize',        **refreshArgs)
        orthoOpts  .addListener('labelColour',      **refreshArgs)
        displayCtx .addListener('selectedOverlay',  **refreshArgs)
        displayCtx .addListener('displaySpace',     **refreshArgs)
        displayCtx .addListener('radioOrientation', **refreshArgs)
        overlayList.addListener('overlays', name, self.__overlayListChanged)

        
    def destroy(self):
        """Must be called when this ``OrthoLabels`` instance is no longer
        needed.
        """

        name        = self.__name
        overlayList = self.__overlayList
        displayCtx  = self.__displayCtx
        orthoOpts   = self.__orthoOpts
        canvases    = self.__canvases
        annots      = self.__annots

        self.__overlayList = None
        self.__displayCtx  = None
        self.__orthoOpts   = None
        self.__canvases    = None
        self.__annots      = None
        
        orthoOpts  .removeListener('showLabels',       name)
        orthoOpts  .removeListener('labelSize',        name)
        orthoOpts  .removeListener('labelColour',      name)
        displayCtx .removeListener('selectedOverlay',  name)
        displayCtx .removeListener('displaySpace',     name)
        displayCtx .removeListener('radioOrientation', name)
        overlayList.removeListener('overlays',         name)

        for c in canvases:
            c.removeListener('invertX', name)
            c.removeListener('invertY', name)

        # The _overlayListChanged method adds
        # listeners to individual overlays,
        # so we have to remove them too
        for ovl in overlayList:
            opts = displayCtx.getOpts(ovl)
            opts.removeListener('bounds', name)

        # Destroy the Text annotations
        for a in annots:
            for side, text in a.items():
                text.destroy()


    def __overlayListChanged(self, *a):
        """Called when the :class:`.OverlayList` changes. Registers a listener
        on the attr:.DisplayOpts.bounds` property of every overlay in the list,
        so the labels are refreshed when any overlay bounds change.
        """
        
        for i, ovl in enumerate(self.__overlayList):

            opts = self.__displayCtx.getOpts(ovl)

            # Update anatomy labels when 
            # overlay bounds change
            opts.addListener('bounds',
                             self.__name,
                             self.__refreshLabels,
                             overwrite=True)

        # When the list becomes empty, or
        # an overlay is added to an empty
        # list, the DisplayContext.selectedOverlay
        # will not change, and __refreshLabels
        # will thus not get called. So we call
        # it here.
        if len(self.__overlayList) in (0, 1):
            self.__refreshLabels()


    def __refreshLabels(self, *a):
        """Updates the attributes of the :class:`.Text` anatomical orientation
        annotations on each :class:`.SliceCanvas`.
        """

        displayCtx = self.__displayCtx
        sopts      = self.__orthoOpts
        overlay    = displayCtx.getSelectedOverlay()
        ref        = displayCtx.getReferenceImage(overlay)

        canvases = self.__canvases
        annots   = self.__annots

        for cannots in annots:
            for text in cannots.values():
                text.enabled = sopts.showLabels and (overlay is not None)

        if not sopts.showLabels or overlay is None:
            return

        # Calculate all of the xyz
        # labels for this overlay
        labels, orients, vertOrient  = self.__getLabels(ref)
        xlo, ylo, zlo, xhi, yhi, zhi = labels

        fontSize = sopts.labelSize
        bgColour = tuple(sopts.bgColour)
        fgColour = tuple(sopts.labelColour)

        # If any axis orientation is unknown, and the
        # the background colour is black or white,
        # make the foreground colour red, to highlight
        # the unknown orientation. It's too difficult
        # to do this for any background colour.
        if constants.ORIENT_UNKNOWN in orients and \
           bgColour in ((0, 0, 0, 1), (1, 1, 1, 1)):
            fgColour = (1, 0, 0, 1) 

        # A list, with one entry for each canvas,
        # and with each entry of the form:
        #
        #   [[xlo, xhi], [ylo, yhi]]
        # 
        # containing the low/high labels for the
        # horizontal (x) and vertical (y) canvas
        # axes.
        canvasLabels = []
        for canvas in canvases:

            cax = 'xyz'[canvas.zax]
            
            if   cax == 'x': clabels = [[ylo, yhi], [zlo, zhi]]
            elif cax == 'y': clabels = [[xlo, xhi], [zlo, zhi]]
            elif cax == 'z': clabels = [[xlo, xhi], [ylo, yhi]]

            if canvas.invertX: clabels[0] = [clabels[0][1], clabels[0][0]]
            if canvas.invertY: clabels[1] = [clabels[1][1], clabels[1][0]]

            canvasLabels.append(clabels)

        # Update the text annotation properties
        for canvas, cannots, clabels in zip(canvases, annots, canvasLabels):

            cax = 'xyz'[canvas.zax]

            cannots['left']  .text = clabels[0][0]
            cannots['right'] .text = clabels[0][1]
            cannots['bottom'].text = clabels[1][0]
            cannots['top']   .text = clabels[1][1]

            if   cax == 'x': show = sopts.showXCanvas
            elif cax == 'y': show = sopts.showYCanvas
            elif cax == 'z': show = sopts.showZCanvas

            for side in ['left', 'right', 'bottom', 'top']:
                
                cannots[side].enabled  = show
                cannots[side].fontSize = fontSize
                cannots[side].colour   = fgColour

            if vertOrient:
                cannots['left'] .angle = 90
                cannots['right'].angle = 90

        
    def __getLabels(self, refImage):
        """Generates some orientation labels to use for the given reference
        image (assumed to be a :class:`.Nifti` overlay, or ``None``).

        Returns a tuple containing:

          - The ``(xlo, ylo, zlo, xhi, yhi, zhi)`` bounds
          - The ``(xorient, yorient, zorient)`` orientations (see
            :meth:`.Image.getOrientation`)
          - A boolean flag which indicates whether the label should be oriented
            vertically (``True``), or horizontally (``False``).
        """

        if refImage is None:
            return ('??????', [constants.ORIENT_UNKNOWN] * 3, False) 
        
        opts = self.__displayCtx.getOpts(refImage)

        vertOrient = False
        xorient    = None
        yorient    = None
        zorient    = None
        
        # If we are displaying in voxels/scaled voxels,
        # and this image is not the current display
        # image, then we do not show anatomical
        # orientation labels, as there's no guarantee
        # that all of the loaded overlays are in the
        # same orientation, and it can get confusing.
        if opts.transform in ('id', 'pixdim', 'pixdim-flip') and \
           self.__displayCtx.displaySpace != refImage:
            xlo        = 'Xmin'
            xhi        = 'Xmax'
            ylo        = 'Ymin'
            yhi        = 'Ymax'
            zlo        = 'Zmin'
            zhi        = 'Zmax'
            vertOrient = True

        # Otherwise we assume that all images
        # are aligned to each other, so we
        # estimate the current image's orientation
        # in the display coordinate system
        else:

            xform      = opts.getTransform('display', 'world')
            xorient    = refImage.getOrientation(0, xform)
            yorient    = refImage.getOrientation(1, xform)
            zorient    = refImage.getOrientation(2, xform)

            xlo        = strings.anatomy['Nifti', 'lowshort',  xorient]
            ylo        = strings.anatomy['Nifti', 'lowshort',  yorient]
            zlo        = strings.anatomy['Nifti', 'lowshort',  zorient]
            xhi        = strings.anatomy['Nifti', 'highshort', xorient]
            yhi        = strings.anatomy['Nifti', 'highshort', yorient]
            zhi        = strings.anatomy['Nifti', 'highshort', zorient]

        return ((xlo, ylo, zlo, xhi, yhi, zhi), 
                (xorient, yorient, zorient),
                vertOrient)