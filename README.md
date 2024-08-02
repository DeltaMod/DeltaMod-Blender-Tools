# DeltaMod-Blender-Tools
A collection of UI Panel tools that I hope to continuously update that performs different tasks that are not included in the core of blender.

The addon is found in the side panel in the 3d view, in "View 3D > Sidebar > DMBT"

# Select By Weight 
This will select all vertices within a vertex group of your selected object. Simply choose the range of weights within the vertex group that you want to select, and it will select them for you. For instance, if you want to select all vertices that have weight zero, you can set min=0, max=0 and only those vertices will be selected. 
Note that currently, it will only select zero weights if they are included in the vertex group, since vertices can have no weight and not belong to a vertex group. In this case, you can either simply invert your vertex group selection, or add all vertices in your mesh with a weight zero.  
