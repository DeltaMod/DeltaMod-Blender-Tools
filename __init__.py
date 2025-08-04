#
bl_info = {
    "name": "DeltaMod Blender Tools",
    "author": "Vidar Flodgren",
    "location": "View 3D > Sidebar > DMBT",
    "description": "Collection of tools developed to fill missing needs to the core of blender",
    "version": (1, 0),
    "blender": (2, 93, 0),
    "doc_url": "https://github.com/DeltaMod/DeltaMod-Blender-Tools",
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
    bl_category = "DMBT"
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

class BoneChain_Renamer_Props(PropertyGroup):
    root_name: StringProperty(name="New Chain Name", default="Chain")
    apply_mirror: BoolProperty(name="Apply Mirror", default=False)
    bone_side: EnumProperty(
        name="Active Bone Side",
        description="Used to control mirroring behaviour",
        items=[
            ('Guess', 'Guess from Bone Name', ''),
            ('L', 'Left (.L)', ''),
            ('R', 'Right (.R)', ''),
            ('None', 'No Side / Do Not Mirror', '')
        ],
        default='Guess'
    )


class UFUNC_OT_RENAME_BONE_CHAIN(Operator):
    bl_idname = "ufunc.rename_bone_chain"
    bl_label = "Rename Bone Chain"

    def execute(self, context):
        obj = context.object
        props = context.scene.DeltaMod_Tool_Props.BoneChain_Renamer_Props
        new_name = props.root_name.strip()
        apply_mirror = props.apply_mirror
        side_selection = props.bone_side

        if not obj or obj.type != 'ARMATURE':
            self.report({'WARNING'}, "No armature selected")
            return {'CANCELLED'}

        bones = obj.data.edit_bones if obj.mode == 'EDIT' else obj.pose.bones
        active = bones.active if hasattr(bones, "active") else None

        if not active:
            self.report({'WARNING'}, "No active bone selected")
            return {'CANCELLED'}
        original_root_name = active.name
        
        def chain_from(bone):
            yield bone
            children = list(bone.children) if hasattr(bone, "children") else bone.bone.children
            if children:
                yield from chain_from(children[0])
        
        # Determine mirror side
        active_side = None
        if side_selection == 'Guess':
            if '.L' in active.name:
                active_side = 'L'
            elif '.R' in active.name:
                active_side = 'R'
        elif side_selection in {'L', 'R'}:
            active_side = side_selection
            
        # Rename main chain
        if active_side:
            for i, b in enumerate(chain_from(active), 1):
                b.name = f"{new_name}.{active_side}.{str(i).zfill(3)}"
        else:
            for i, b in enumerate(chain_from(active), 1):
                b.name = f"{new_name}.{str(i).zfill(3)}"

        if apply_mirror and active_side:
            mirror_side = 'R' if active_side == 'L' else 'L'
            suffixes = { 'source': f".{active_side}", 'mirror': f".{mirror_side}" }

            mirror_root_name = original_root_name.replace(suffixes['source'], suffixes['mirror'])
            mirror_root = bones.get(mirror_root_name)

            if mirror_root:
                mirror_base_name = new_name + suffixes['mirror']
                for i, b in enumerate(chain_from(mirror_root), 1):
                    b.name = f"{mirror_base_name}.{str(i).zfill(3)}"

        self.report({'INFO'}, "Renaming complete")
        return {'FINISHED'}


class OBJECT_PT_RenameBoneChains(Panel):
    bl_label = "Rename Bone Chains"
    bl_idname = "OBJECT_PT_rename_bone_chains"
    bl_category = "DMBT"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        props = context.scene.DeltaMod_Tool_Props.BoneChain_Renamer_Props
        obj = context.object
        box = layout.box()

        if not obj or obj.type != 'ARMATURE':
            box.label(text="No Armature Selected", icon="ERROR")
            return

        active_bone = None
        if obj.mode == 'EDIT':
            active_bone = obj.data.edit_bones.active
        elif obj.mode == 'POSE':
            active_bone = obj.pose.bones.active

        name = active_bone.name if active_bone else "None"
        box.label(text=f"Active Root Bone: {name}")
        box.prop(props, "root_name", text="Name")
        box.prop(props, "apply_mirror")
        box.prop(props, "bone_side", text="Side")
        box.operator("ufunc.rename_bone_chain", text="Rename Chain")


class DeltaMod_Tool_Props(PropertyGroup):
    Weight_Select_Props: PointerProperty(type=Weight_Select_Props)
    BoneChain_Renamer_Props: PointerProperty(type=BoneChain_Renamer_Props)


register_classes = [
    Weight_Select_Props,
    BoneChain_Renamer_Props,
    DeltaMod_Tool_Props,
    UFUNC_OT_WEIGHT_SELECT,
    UFUNC_OT_RENAME_BONE_CHAIN,
    OBJECT_PT_Weight_Selection_Panel,
    OBJECT_PT_RenameBoneChains,
]

def register():
    for cls in register_classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.DeltaMod_Tool_Props = PointerProperty(type=DeltaMod_Tool_Props)

def unregister():
    for cls in reversed(register_classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.DeltaMod_Tool_Props

if __name__ == "__main__":
    register()