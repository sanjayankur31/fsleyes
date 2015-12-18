/*
 * OpenGL vertex shader used for rendering GLVolume instances.
 * All this shader does is set the vertex position, and pass the
 * voxel and texture coordinates through to the fragment shader.
 *
 * Author: Paul McCarthy <pauldmccarthy@gmail.com>
 */
#version 120

attribute vec3 vertex;
attribute vec3 voxCoord;
attribute vec3 texCoord;

varying vec3 fragVoxCoord;
varying vec3 fragTexCoord;
varying vec4 fragColourFactor;

void main(void) {

  fragVoxCoord     = voxCoord;
  fragTexCoord     = texCoord;
  fragColourFactor = vec4(1, 1, 1, 1);

  gl_Position = gl_ModelViewProjectionMatrix * vec4(vertex, 1);
}
