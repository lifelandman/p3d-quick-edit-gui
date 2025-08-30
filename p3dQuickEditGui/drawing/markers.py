'''
Tools useful for displaying markers or draggable points.
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
triStrip.add_vertex(4)
triStrip.close_primitive()

markerGeom = Geom(markercardvert)
markerGeom.add_primitive(triStrip)

markerGeomNode = GeomNode('marker_gnode')
markerGeomNode.add_geom(markerGeom)
del markercardvert
del triStrip

#Define shaders for markers
markerVertShader = """
##version 150

uniform mat4 p3d_ModelViewProjectionMatrix;

in vec4 p3d_Vertex;
in vec2 p3d_MultiTexCoord0;

uniform in float markerScale;

out vec2 texCoord;

void main()
{
  vec4 newPosition;
  newPosition = p3d_Vertex * markerScale;
  gl_Position = p3d_ModelViewProjectionMatrix * newPosition;
  texCoord = p3d_MultiTexCoord0 - 0.5;
}
"""

markerFragShader = """
#version 150

in vec2 texCoord;

out vec4 fragColor;

void main() {
  if ((abs(texCoord.u) > 0.4) || (abs(texCoord.v) > 0.4))
  {
  fragColor = vec4(0.9, 0.8, 0.8, 1);
  }
  else
  {
  fragColor = vec4(0.1,0.1,0.1,1);
  }
  
}
"""

from panda3d.core import NodePath, Shader
markerShader = Shader.make(Shader.SL_GLSL, vertex = markerVertShader, fragment = markerFragShader)
def getMarkerGeomNodePath(scale:float = 1):
    newGeomNP = NodePath(markerGeomNode)
    newGeomNP.set_shader_input("markerScale", scale)
    newGeomNP.set_billboard_point_eye(-10, fixed_depth = True)
    newGeomNP.set_shader(markerShader)
    return newGeomNP

__all__ = ["getMarkerGeomNodePath", "markerFragShader", "markerVertShader"]