# DeltaMod-Blender-Tools
A collection of UI Panel tools that I hope to continuously update that performs different tasks that are not included in the core of blender.

The addon is found in the side panel in the 3d view, in "View 3D > Sidebar > DMBT"

# Select By Weight 
This will select all vertices within a vertex group of your selected object whose weight is within the range you specify. Simply choose the range of weights within the vertex group that you want to select, and it will select them for you. For instance, if you want to select all vertices that have weight zero, you can set min=0, max=0 and only those vertices will be selected. 
Note that currently, it will only select zero weights if they are included in the vertex group, since vertices can have no weight and not belong to a vertex group. In this case, you can either simply invert your vertex group selection, or add all vertices in your mesh with a weight zero.  

# Rename bone chains
A simple tool that allows you to rename an entire bone chain (from the selected parent to its children) in correct numerical order (intended for rigify)

How to use:
- Select a single bone in a bone chain to use as the root bone for child-name propogation. 
- In the Rename bone chains panel in DMBT, verify that the correct active bone is selected and write a new name for the chain.
- If the active root bone name already has a L.00x/R.00x in its name, or is meant to be central or unique, then you can leave the Side as "Guess" and this will be preserved without the new name needing to include it. For example, if the bone is called Bone.L.001 and you want to call it Arm.L.001 then you enter the name "Arm" into the field and leave the option as "Guess"
- If the bone chain has no side, or you want to enfore a new side, you may select "L" or "R" in the side dropdown, and this will reflect accurately.
- If there already is named symmetry (so, you have bones Bone.L.001 and Bone.R.001) you can use "Apply symmetry" to automatically rename any bone chains whose mirror name exists (So both sides will rename to your new one) 
- Your bone chain is now in correct order.
