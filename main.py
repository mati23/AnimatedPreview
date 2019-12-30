import sys
from PySide2 import QtWidgets, QtGui, QtCore
import bpy
from bl_ui.space_toolsystem_toolbar import VIEW3D_PT_tools_active, ToolDef, _defs_sculpt


class Ui_Form(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(Ui_Form, self).__init__(parent)
        self.size = QtCore.QSize(160, 100
                                 )
        self.pixel = QtGui.QMovie(
            '/home/mateus/Documents/Blender Projects/preview_animated.gif')
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

        layout = QtWidgets.QVBoxLayout()
        layout.setMargin(0)
        layout.addWidget(self.label)

        self.unsetCursor()

        # ----------------------------
        """
        tools = VIEW3D_PT_tools_active._tools

        sculpt_tools = tools['SCULPT']

        # Custom tooltip must have 3 parameters and return a string
        # Called when tool is hovered
        def tooltip(context, tool, keymap):
            print(tool.label)
            return ""

        # Get all tooldefs for builtin brushes
        brushes = list(_defs_sculpt.generate_from_brushes(bpy.context))

        for idx, tool in enumerate(brushes):
            new_tool_dict = tool._asdict()
            new_tool_dict['description'] = tool
        print("--------------------------------------------------------------")
        print(new_tool_dict)
        print("--------------------------------------------------------------")
        """
        # ---------------------------

        self.setLayout(layout)
        self.show()
