import sys
from PySide2 import QtWidgets, QtGui, QtCore
import bpy
from bl_ui.space_toolsystem_toolbar import VIEW3D_PT_tools_active, ToolDef, _defs_sculpt


class Ui_Form(QtWidgets.QDialog):
    label = None
    size = QtCore.QSize(160, 100)

    def __init__(self, parent=None):
        super(Ui_Form, self).__init__(parent)
        self.setAnimatedGif('Clay.gif', QtCore.QPoint(0, 0))
        self.setAnimatedGifLayout()

    def setAnimatedGif(self, gif_path, _qpoint):
        self.pixel = QtGui.QMovie(
            '/home/mateus/Documents/Blender Projects/preview_animated/gifs/'+gif_path)
        self.pixel.setScaledSize(self.size)

        self.setFixedSize(160, 100)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.label = QtWidgets.QLabel()
        self.label.setStyleSheet("""
        QWidget{
           background: transparent;
        }
        QFrame{
            border-style: solid;
            border-color: #FE9618;
            border-width: 2px;
            border-radius: 3px;
            background-color: rgba(55, 55, 55, 255);
        }
        """)

        self.label.setMovie(self.pixel)
        self.pixel.start()

        self.label.unsetCursor()
        self.label.clearFocus()

        self.label.setWindowFlags(
            QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.label.setAttribute(QtCore.Qt.WA_ShowWithoutActivating)
        self.label.setParent(None)
        self.label.show()
        self.label.setVisible(True)
        self.label.move(_qpoint)

    def setAnimatedGifLayout(self):
        #layout = QtWidgets.QVBoxLayout()
        # layout.setMargin(0)
        # layout.addWidget(self.label)
        # self.setLayout(layout)
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # self.show()
        print("showing window")
