import sys
from PySide2 import QtWidgets, QtGui, QtCore
import bpy
from bl_ui.space_toolsystem_toolbar import VIEW3D_PT_tools_active, ToolDef, _defs_sculpt


class Ui_Form(QtWidgets.QDialog):
    label = None
    size = QtCore.QSize(160, 100)

    def __init__(self, parent=None):
        super(Ui_Form, self).__init__(parent)

        self.setAnimatedGif('Clay.gif')
        self.setAnimatedGifLayout()

    def setAnimatedGif(self, gif_path):
        self.pixel = QtGui.QMovie(
            '/home/mateus/Documents/Blender Projects/preview_animated/'+gif_path)
        self.pixel.setScaledSize(self.size)

        self.setFixedSize(160, 100)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setStyleSheet("""
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

        self.label = QtWidgets.QLabel()
        self.label.setMovie(self.pixel)
        self.pixel.start()
        self.label.show()

    def setAnimatedGifLayout(self):
        layout = QtWidgets.QVBoxLayout()
        layout.setMargin(0)
        layout.addWidget(self.label)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.unsetCursor()

        self.setLayout(layout)

    def change_gif_file(self, gif_path):
        self.pixel = QtGui.QMovie(
            '/home/mateus/Documents/Blender Projects/preview_animated/'+gif_path)
        self.label.setMovie(self.pixel)
        self.pixel.start()
        self.label.show()
