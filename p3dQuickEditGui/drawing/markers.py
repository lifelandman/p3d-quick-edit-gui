'''
Tools useful for displaying markers or draggable points.
'''

from panda3d.core import CardMaker, Vec2

maker = CardMaker("marker creator")
maker.set_frame(-1,1,-1,1)
maker.set_has_uvs(True)

markerGeomNode = maker.generate()

'''
##Define the Geom for markers
from panda3d.core import GeomVertexData, GeomVertexFormat, Geom, GeomVertexWriter, GeomTristrips, GeomNode
markercardvert = GeomVertexData("markercard", GeomVertexFormat.get_v3t2(), Geom.UHStatic)

markercardvert.setNumRows(4)

vertex = GeomVertexWriter(markercardvert, 'vertex')
texcoord = GeomVertexWriter(markercardvert, 'texcoord')

#Vertex pos is zero'd on every one to save a shader input for center of marker.
vertex.addData3(-1, 0, 1)#0
texcoord.addData2(1, 0)
vertex.addData3(1, 0, 1)#1
texcoord.addData2(1, 1)
vertex.addData3(1, 0, -1)#2
texcoord.addData2(0, 1)
vertex.addData3(-1, 0, -1)#3
texcoord.addData2(0, 0)
del vertex
del texcoord

triStrip = GeomTristrips(Geom.UHStatic)
triStrip.add_vertex(0)
triStrip.add_vertex(1)
triStrip.add_vertex(2)
triStrip.add_vertex(3)
#triStrip.add_vertex(4)
triStrip.close_primitive()

markerGeom = Geom(markercardvert)
markerGeom.add_primitive(triStrip)

markerGeomNode = GeomNode('marker_gnode')
markerGeomNode.add_geom(markerGeom)
del markercardvert
del triStrip
'''

#Define shaders for markers
markerVertShader = """
#version 150

uniform mat4 p3d_ModelViewProjectionMatrix;
uniform mat4 p3d_ModelViewMatrix;

in vec4 p3d_Vertex;
in vec2 p3d_MultiTexCoord0;
in vec4 p3d_Color;

out vec2 texCoord;

out vec4 color;

void main()
{

  gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
  texCoord = p3d_MultiTexCoord0;
  color = p3d_Color;
}
"""

markerFragShader = """
#version 150

in vec2 texCoord;

in vec4 color;

out vec4 fragColor;

uniform in vec4 fillColor;

void main() {
  if ((0.9 > texCoord.x && texCoord.x > 0.1) && (0.9 > texCoord.y && texCoord.y > 0.1))
  {
  fragColor = color;
  }
  else
  {
  fragColor = vec4(0.1,0.1,0.1,1);
  }
  
}
"""

from panda3d.core import NodePath, Shader, Vec4
markerShader = Shader.make(Shader.SL_GLSL, vertex = markerVertShader, fragment = markerFragShader)
def getMarkerGeomNodePath(scale:float = 0.5, fill_color:Vec4 = Vec4(0.85,0.75,0.8,1) ):
    newGeomNP = NodePath(markerGeomNode)
    newGeomNP.set_scale(scale)
    newGeomNP.set_color(fill_color)
    newGeomNP.set_billboard_point_eye(-10, fixed_depth = True)
    newGeomNP.set_shader(markerShader)
    return newGeomNP

__all__ = ["getMarkerGeomNodePath", "markerFragShader", "markerVertShader"]


if __name__ == "__main__":
    import direct.directbase.DirectStart
    np = getMarkerGeomNodePath()
    np.reparent_to(base.render)
    np.set_pos(0,2,0)
    base.run()