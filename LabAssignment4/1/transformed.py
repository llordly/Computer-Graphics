import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

keyList = []

def render():
    glClear(GL_COLOR_BUFFER_BIT)

    glLoadIdentity()
    # draw cooridnates
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0., 0.]))
    glVertex2fv(np.array([1., 0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0., 0.]))
    glVertex2fv(np.array([0., 1.]))
    glEnd()
    glColor3ub(255, 255, 255)

    ###########################
    # implement here
    ###########################
    for i in keyList[::-1]:
        if i == 'Q':
            glTranslatef(-0.1, 0., 0.)
        elif i == 'E':
            glTranslatef(0.1, 0., 0.)
        elif i == 'A':
            glRotatef(10, 0, 0, 1)
        elif i == 'D':
            glRotatef(-10, 0, 0, 1)
        elif i == '1':
            keyList.clear()
            glLoadIdentity()

    drawTriangle()

def drawTriangle():
    glBegin(GL_TRIANGLES)
    glVertex2fv(np.array([0., .5]))
    glVertex2fv(np.array([0., 0.]))
    glVertex2fv(np.array([.5, 0.]))
    glEnd()

def key_callback(window, key, scancode, action, mods):
    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_Q:
            keyList.append('Q')
        elif key == glfw.KEY_E:
            keyList.append('E')
        elif key == glfw.KEY_A:
            keyList.append('A')
        elif key == glfw.KEY_D:
            keyList.append('D')
        elif key == glfw.KEY_1:
            keyList.append('1')

def main():
    if not glfw.init():
        return
    window = glfw.create_window(480, 480, '2017029589', None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()