#
bl_info = {
    "name": "Select By Weight",
    "author": "Vidar Flodgren",
    "location": "View 3D > Sidebar > Selection Tools",
    "description": "Small tools to select by Weight",
    "version": (1, 0),
    "blender": (2, 93, 0),
    "doc_url": "https://github.com/DeltaMod",
    "category": "Object",}


import bpy

from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       CollectionProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Operator,
                       AddonPreferences,
                       PropertyGroup,
                       )




            
class Weight_Select_Props(PropertyGroup):
    minWeight:   FloatProperty(name="Minimum Weight", default=0.0, min=0.0, max=1.0)
    maxWeight:   FloatProperty(name="Maximum Weight", default=1.0, min=0.0, max=1.0)

    
class UFUNC_OT_WEIGHT_SELECT(bpy.types.Operator):
    bl_idname = "ufunc.weight_select"
    bl_label = "Weight Select"

    def execute(self, context):
        obj = context.object
        scene = context.scene
        DMT    = scene.DeltaMod_Tool_Props
        props  = DMT.Weight_Select_Props   
        initial_mode  = context.object.mode
        
        
        minWeight = props.minWeight
        maxWeight = props.maxWeight        
        vertexGroupIndex = obj.vertex_groups.active_index
        
        if initial_mode == "EDIT":
            bpy.ops.mesh.select_mode(type="VERT")
            
        if initial_mode not in ["OBJECT"]:
            bpy.ops.object.mode_set(mode = "OBJECT")

        for vertID,vert in enumerate(obj.data.vertices):
            try:
                if (vert.groups[vertexGroupIndex].weight <=maxWeight and vert.groups[vertexGroupIndex].weight >=minWeight):
                    obj.data.vertices[vertID].select=True
            except:
                None
            
        if initial_mode == "WEIGHT_PAINT":
            bpy.ops.object.mode_set(mode = "WEIGHT_PAINT")
            bpy.context.object.data.use_paint_mask_vertex = True
                        
        elif initial_mode == "EDIT":
            bpy.ops.object.mode_set(mode = "EDIT")
            bpy.ops.mesh.select_mode(type="VERT")
            
        
                
        self.report({'INFO'}, f"Selected Weights in Range")
        return {'FINISHED'}

                      
class OBJECT_PT_Weight_Selection_Panel(Panel):
    bl_label = "Select by Weight"
    bl_idname = "selweight"
    bl_category = "Weight Selection"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}
    
    
    def draw(self, context):
        layout = self.layout
        scene  = context.scene
        DMT    = scene.DeltaMod_Tool_Props
        props  = DMT.Weight_Select_Props   
        
        try:
            ActiveGroup = context.object.vertex_groups.active.name
        except:
            ActiveGroup = "No Object Selected"
        
        box = layout.box()
        row  = box.row()
        row.label(text="Active Group: " + ActiveGroup)
        row = box.row()
        row.prop(props, "minWeight", text="Min")
        row.prop(props, "maxWeight", text="Max")
        row = box.row()
        row.operator(UFUNC_OT_WEIGHT_SELECT.bl_idname,text="Select Weights")




#Here, we create the nested property group by assigning pointers to each property group in the master class
class DeltaMod_Tool_Props(PropertyGroup):
    Weight_Select_Props: PointerProperty(type=Weight_Select_Props)

register_classes = [UFUNC_OT_WEIGHT_SELECT,OBJECT_PT_Weight_Selection_Panel,Weight_Select_Props,DeltaMod_Tool_Props]
    
def register():
    for cls in register_classes:
        bpy.utils.register_class(cls)
    
    bpy.types.Scene.DeltaMod_Tool_Props = bpy.props.PointerProperty(type=DeltaMod_Tool_Props)
    
def unregister():
    for cls in register_classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()