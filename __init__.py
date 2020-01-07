bl_info = {
    "name": "Animated Preview",
    "author": "Mateus Arruda de Medeiros",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D",
    "description": "Adds a new Mesh Object",
    "warning": "",
    "wiki_url": "",
    "category": "Object",
}

import sys
import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector
from bl_ui.space_toolsystem_toolbar import VIEW3D_PT_tools_active, ToolDef, _defs_sculpt
from bpy.app.handlers import persistent
from .main import Ui_Form
import os
import logging
from PySide2 import QtWidgets, QtCore, QtGui
import time
tools = VIEW3D_PT_tools_active._tools

sculpt_tools = tools['SCULPT']

brushes = list(_defs_sculpt.generate_from_brushes(bpy.context))
tooltip_active = {"active": False, "brush": "Clay", "step":0}
active_tooltip_brush = ""

class AnimatedPreview(bpy.types.Operator):
    """Create a new Mesh Object"""
    bl_idname = "wm.animated_preview"
    bl_label = "Animated Preview"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tool"
    bl_options = {'REGISTER','UNDO'}
    
    active_ = False

    
    #bl_space_type = "VIEW_3D"
    def __init__(self):
        print('initiated')          

    def __del__(self):
        print("End--")

    x: bpy.props.IntProperty()
    y: bpy.props.IntProperty()


    def execute(self, context):
        print('executed')
        self.current_time = time.time()

        self.app = QtWidgets.QApplication.instance()
        
        if not self.app:
            self.app = QtWidgets.QApplication(sys.argv)
        
        
        
        self.widget = Ui_Form()   
        
        #self.widget.setVisible(False)
        self.event_loop = QtCore.QEventLoop()
        self.widget.hide()

        wm = context.window_manager
        self._timer = wm.event_timer_add(1 / 120, window = context.window)
        context.window_manager.modal_handler_add(self)
        print('running modal')
        

        return {'RUNNING_MODAL'}

    def modal(self,context,event):
        #wm = context.window_manager
        global tooltip_active
        global active_tooltip_brush
        wm = context.window_manager
        
        self.qpoint = QtCore.QPoint(event.mouse_x+10, (-event.mouse_y)+730)
        self.widget.move(self.qpoint)
        
        if tooltip_active["active"] is True and active_tooltip_brush == tooltip_active["brush"]:
            if tooltip_active["step"] == 1:
                if (time.time() - self.current_time) > 3:
                    self.current_time = time.time()                    
                    self.set_active_tooltip(False, "")
                else:
                    pass
                    #print(self.widget.pos())
            else:
                tooltip_active["step"] = 1
                self.show_widget(self.qpoint)
                if (time.time() - self.current_time) > 3:
                    self.current_time = time.time()
                    self.set_active_tooltip(False, "")
                else:
                    pass
                    #print(self.qpoint)           
            
        #if not self.widget.isVisible():                        
        #    wm.event_timer_remove(self._timer)            
        #    return {'FINISHED'}
        else:
            tooltip_active["step"] = 0
            self.widget.label.hide()            
        #self.widget.show()         
        self.event_loop.processEvents()
        self.app.sendPostedEvents(None,0)      
        
        return {'PASS_THROUGH'}

    
    @staticmethod
    def set_active_tooltip(_boolean, label):
        global tooltip_active
        tooltip_active["active"] = _boolean
        tooltip_active["brush"] = label
    
    @staticmethod
    def set_active_brush(_label):        
        global active_tooltip_brush  
        active_tooltip_brush = _label

    def show_widget(self,_qpoint):
        self.widget.setAnimatedGif('Clay.gif', _qpoint)
        self.widget.setAnimatedGifLayout()           
        time.sleep(1)
def tooltip(context, tool, keymap):
    global active_tooltip_brush  
    print(tool.label)
    AnimatedPreview.set_active_brush(tool.label)
    AnimatedPreview.set_active_tooltip(True, tool.label)    
    return ""

for idx, tool in enumerate(brushes):
    new_tool_dict = tool._asdict()
    new_tool_dict['description'] = tooltip
    new_tool = ToolDef(*new_tool_dict.values())
    brushes[idx] = new_tool

def brush_tooldefs_get(context):
        return tuple(brushes)

sculpt_tools[0] = brush_tooldefs_get



def menu_func(self,context):
    self.layout.operator(AnimatedPreview.bl_idname)

def register():    
    bpy.utils.register_class(AnimatedPreview)  
    bpy.types.VIEW3D_MT_mask.append(menu_func)
def unregister():
    bpy.utils.unregister_class(AnimatedPreview)
    bpy.types.VIEW3D_MT_mask.remove(menu_func)

if __name__ == "__main__":  
    register()    

