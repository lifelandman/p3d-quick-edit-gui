from panda3d.core import NodePath, LineSegs, LColorf

##Draw a cube
def _cube_xz_axis(seg, x, ypos, z):
    seg.move_to(-x,ypos,z)
    seg.draw_to(x,ypos,z)
    seg.draw_to(x,ypos,-z)
    seg.draw_to(-x,ypos,-z)
    seg.draw_to(-x,ypos,z)

def _cube_y_axis(seg, x, y, z):
    seg.move_to(-x,-y,z)
    seg.draw_to(-x,y,z)
    seg.move_to(-x,-y,-z)
    seg.draw_to(-x,y,-z)
    seg.move_to(x,-y,z)
    seg.draw_to(x,y,z)
    seg.move_to(x,-y,-z)
    seg.draw_to(x,y,-z)

def drawBox(scale_x,scale_y,scale_z, thickness:float = 1, color:LColorf = LColorf(1,1,1,1)):
    '''
    Returns a NodePath that shows a box made out of lines of a specified thickness, or 1 px otherwise.
    The line can be set to any color.
    '''
    x, y, z = (abs(val)/2 for val in (scale_x,scale_y,scale_z))

    _linesegs = LineSegs("Default Box LineSegs")
    _linesegs.set_color(color)
    _linesegs.set_thickness(thickness)

    #Make front and back
    _cube_xz_axis(_linesegs,x,y,z)
    _cube_xz_axis(_linesegs,x,-y,z)
    #Make lines connecting front and back
    _cube_y_axis(_linesegs, x,y,z)

    return NodePath(_linesegs.create())

