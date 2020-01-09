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
from Xlib.display import Display
import Xlib
from ewmh import EWMH

sculpt_tools = tools['SCULPT']

brushes = list(_defs_sculpt.generate_from_brushes(bpy.context))
tooltip_active = {"active": False, "brush": "Clay", "step":0}
active_tooltip_brush = ""

def animation():
    animation.block = getattr(animation, "block", False)

    if not animation.block:
        print("playing")
        return 0.1
    else:
        print("not playing")
        return 0.1

animation.block = True

class VIEW3D_OT_poll_region(bpy.types.Operator):
    bl_idname = "view3d.poll_region"
    bl_label = "Poll Region"
    bl_options = {'INTERNAL'}


    @classmethod
    def poll(cls, context):        
        if not animation.block:
            animation.block = True
        return False

    def execute(self, context):
        return {'CANCELLED'}

    def modal(self,context, event):
        
        return {'RUNNING_MODAL'}

class AnimatedPreview(bpy.types.Operator):
    """Create a new Mesh Object"""
    bl_idname = "wm.animated_preview"
    bl_label = "Animated Preview"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tool"
    bl_options = {'REGISTER','UNDO'}
    
    active_ = False
    blender = None
    ewmh = EWMH()
    wins = ewmh.getClientList()
    
    
    
    #display = Display()
    #root = display.screen().root  
    #NET_ACTIVE_WINDOW = display.intern_atom('_NET_ACTIVE_WINDOW')

    #win_id = root.get_full_property(NET_ACTIVE_WINDOW,Xlib.X.AnyPropertyType).value[0]


    
    #bl_space_type = "VIEW_3D"
    def __init__(self):
        print('initiated')          

    def __del__(self):
        print("End--")

    x: bpy.props.IntProperty()
    y: bpy.props.IntProperty()

    def printWindowHierrarchy(self,window, indent):
        children = window.query_tree().children
        for w in children:
            print(indent, w.get_wm_class())
            self.printWindowHierrarchy(w, indent+'-')

    def execute(self, context):
        for i in self.wins:            
            if (str(self.ewmh.getWmName(i)).find('Blender')) is not -1:
                self.blender = i
            

        self.current_time = time.time()
        
        self.app = QtWidgets.QApplication.instance()
        
        if not self.app:
            self.app = QtWidgets.QApplication(sys.argv)
        
        
        
        self.widget = Ui_Form()   
        
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
        if animation.block == False:            
            if tooltip_active["step"] == 1:                    
                pass
                
            else:
                tooltip_active["step"] = 1
                self.show_widget(tooltip_active["brush"], self.qpoint)                  
                #self.ewmh.setActiveWindow(self.blender)
                #self.ewmh.display.flush()
                #self.widget.label.show()
                #print(self.widget.label.isEnabled())
                
        else:
            tooltip_active["step"] = 0
            self.widget.label.hide()            
             
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

    def show_widget(self,_brush_name,_qpoint):
        self.widget.setAnimatedGif(_brush_name, _qpoint)
    
    

             
def tooltip(context, tool, keymap):  
    bpy.app.timers.register(animation)
    animation.block = False                  
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
    bpy.utils.register_class(VIEW3D_OT_poll_region)
    bpy.utils.register_class(AnimatedPreview)  
    bpy.types.VIEW3D_MT_mask.append(menu_func)
def unregister():
    bpy.utils.unregister_class(VIEW3D_OT_poll_region)
    bpy.utils.unregister_class(AnimatedPreview)
    bpy.types.VIEW3D_MT_mask.remove(menu_func)

if __name__ == "preview_animated":  
    register()    

    
    
    kc = bpy.context.window_manager.keyconfigs.addon
    km = kc.keymaps.get("3D View")

    if not km:
        km = kc.keymaps.new("3D View", space_type="VIEW_3D")

    kmi = km.keymap_items.get("view3d.poll_region")
    if not kmi:
        kmi = km.keymap_items.new("view3d.poll_region", 'MOUSEMOVE', 'ANY', head=1)

    