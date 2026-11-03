"""
Retro-Diag FDD Master Tester - Standalone Desktop Emulator (wxPython + PIL)
Author: Alessio Iodice <alessio67@gmail.com>
License: CC BY-NC-SA 4.0

Eseguibile nativamente con l'interprete Python di KiCad 9:
"C:\\Program Files\\KiCad\\9.0\\bin\\python.exe" emulator_desktop.py
"""

import wx
import os
import webbrowser

class FddEmulatorFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="Retro-Diag FDD Master Tester - Digital Twin", size=(1040, 720))
        self.SetBackgroundColour(wx.Colour(15, 23, 42))

        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Title Banner
        title_box = wx.BoxSizer(wx.HORIZONTAL)
        title_lbl = wx.StaticText(panel, label="RETRO-DIAG FDD MASTER TESTER — DIGITAL TWIN")
        title_lbl.SetForegroundColour(wx.Colour(0, 228, 255))
        font = title_lbl.GetFont()
        font.SetPointSize(12)
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        title_lbl.SetFont(font)
        title_box.Add(title_lbl, 0, wx.ALL, 10)
        sizer.Add(title_box, 0, wx.ALIGN_CENTER)

        # Info Box
        info_lbl = wx.StaticText(panel, label="L'emulatore completo ad alta fedelta con WebAudio, grafica RGB565 a 60 FPS,\n"
                                               "sintetizzatore del buzzer piezoelettrico e fault injection e visualizzabile nel browser.")
        info_lbl.SetForegroundColour(wx.Colour(203, 213, 225))
        sizer.Add(info_lbl, 0, wx.ALIGN_CENTER | wx.BOTTOM, 15)

        # Open Webview Button
        btn_open = wx.Button(panel, label="LANCIA SIMULATORE DIGITALE INTERATTIVO", size=(400, 50))
        btn_open.SetBackgroundColour(wx.Colour(14, 116, 144))
        btn_open.SetForegroundColour(wx.Colour(255, 255, 255))
        btn_open.Bind(wx.EVT_BUTTON, self.on_open_browser)
        sizer.Add(btn_open, 0, wx.ALIGN_CENTER | wx.BOTTOM, 20)

        panel.SetSizer(sizer)
        self.Centre()

    def on_open_browser(self, event):
        html_path = os.path.abspath(r"C:\Users\aless\.gemini\antigravity\brain\7152b287-3ec0-4667-a9e8-ae933cabc426\fdd_tester_digital_twin_emulator.html")
        webbrowser.open(f"file:///{html_path}")

if __name__ == "__main__":
    app = wx.App()
    frame = FddEmulatorFrame()
    frame.Show()
    app.MainLoop()
