import numpy as np
import wx.adv
import sys, wx

if sys.version_info[0]==2:memoryview=np.getbuffer
class CMapSelCtrl(wx.adv.OwnerDrawnComboBox):
    def __init__(self, parent):
        wx.adv.OwnerDrawnComboBox.__init__(self, parent, choices=[], 
            style=wx.CB_READONLY, pos=(20,40), size=(256, 30))

    def SetItems(self, kvs):
        self.Clear()
        ks, vs = list(kvs.keys()), list(kvs.values())
        if 'Grays' in ks:
            i = ks.index('Grays')
            ks.insert(0, ks.pop(i))
            vs.insert(0, vs.pop(i))
        self.AppendItems(ks)
        self.Select(0)
        self.ks, self.vs = ks, vs

    def SetValue(self, x):
        n = self.ks.index(x) if x in self.ks else 0
        self.SetSelection(n)

    def GetValue(self):
        return self.ks[self.GetSelection()]

    # Overridden from OwnerDrawnComboBox, called to draw each
    # item in the list
    def OnDrawItem(self, dc, rect, item, flags):
        if item == wx.NOT_FOUND:
            # painting the control, but there is no valid item selected yet
            return
        r = wx.Rect(*rect)  # make a copy
        r.Deflate(3, 5)
        cmap = None


        pen = wx.Pen(dc.GetTextForeground(), 3)
        dc.SetPen(pen)

        # for painting the items in the popup
        dc.DrawText(self.GetString( item),
                    r.x + 3,
                    (r.y + 0) + ( (r.height/2) - dc.GetCharHeight() )/2
                    )
        #dc.DrawLine( r.x+5, r.y+((r.height/4)*3)+1, r.x+r.width - 5, r.y+((r.height/4)*3)+1 )
        arr = np.zeros((10,256,3),dtype=np.uint8)
        arr[:] = self.vs[item]
        bmp = wx.Bitmap.FromBuffer(256,10, memoryview(arr))
        dc.DrawBitmap(bmp, r.x, r.y+15)

    # Overridden from OwnerDrawnComboBox, called for drawing the
    # background area of each item.
    def OnDrawBackground(self, dc, rect, item, flags):
        # If the item is selected, or its item # iseven, or we are painting the
        # combo control itself, then use the default rendering.
        if (item & 1 == 0 or flags & (wx.adv.ODCB_PAINTING_CONTROL |
                                      wx.adv.ODCB_PAINTING_SELECTED)):
            wx.adv.OwnerDrawnComboBox.OnDrawBackground(self, dc, rect, item, flags)
            return

    # Overridden from OwnerDrawnComboBox, should return the height
    # needed to display an item in the popup, or -1 for default
    def OnMeasureItem(self, item):
        return 30
        # Simply demonstrate the ability to have variable-height items
        if item & 1:
            return 36
        else:
            return 24

    # Overridden from OwnerDrawnComboBox.  Callback for item width, or
    # -1 for default/undetermined
    def OnMeasureItemWidth(self, item):
        return -1; # default - will be measured from text width

class CMapSelPanel(wx.Panel):
    def __init__( self, parent, title):
        wx.Panel.__init__(self, parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        lab_title = wx.StaticText( self, wx.ID_ANY, title,
                                   wx.DefaultPosition, wx.DefaultSize)
        lab_title.Wrap( -1 )
        sizer.Add( lab_title, 0, wx.ALL, 5 )
        self.ctrl = CMapSelCtrl(self)
        sizer.Add( self.ctrl, 0, wx.ALL|wx.EXPAND, 0 )
        self.SetSizer(sizer)
        self.GetValue = self.ctrl.GetValue
        self.SetValue = self.ctrl.SetValue
        self.SetItems = self.ctrl.SetItems
        self.ctrl.Bind( wx.EVT_COMBOBOX, self.on_sel)
                
    def Bind(self, z, f): self.f = f

    def on_sel(self, event):
        self.f(event)