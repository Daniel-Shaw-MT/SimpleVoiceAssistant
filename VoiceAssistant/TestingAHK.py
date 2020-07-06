from ahk import AHK
import wx
app = wx.App(False)
width, height = wx.GetDisplaySize()
ahk = AHK()

win = ahk.active_window
win.hide()
while(False):
    ctrlstate = ahk.key_state('Control')  # Return True or False based on whether Control key is pressed down
    capstate = ahk.key_state('CapsLock', mode='T')  # Check toggle state of a key (like for NumLock, CapsLock, etc)
    print(ctrlstate)

    if(capstate==True):
        print('Capslock is toggled ')
    if(capstate==False):
        print('Capslock is not toggled on')


