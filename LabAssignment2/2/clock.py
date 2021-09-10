import glfw
import numpy as np
from OpenGL.GL import *

# B
v = np.linspace(0, ((2 * np.pi) / 12) * 11, 12)
hour = v[3]
def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glBegin(GL_LINE_LOOP)
    # C
    for i in v:
        glVertex2f(np.cos(i), np.sin(i))
    glEnd()

    glBegin(GL_LINES)
    glVertex2f(0, 0)
    glVertex2f(np.cos(hour), np.sin(hour))
    glEnd()

# F
key_list = [glfw.KEY_1, glfw.KEY_2, glfw.KEY_3, glfw.KEY_4,
            glfw.KEY_5, glfw.KEY_6, glfw.KEY_7, glfw.KEY_8,
            glfw.KEY_9, glfw.KEY_0, glfw.KEY_Q, glfw.KEY_W]

def key_callback(window, key, scancode, action, mods):
    global hour
    for i in range(12):
        if key == key_list[i] and action == glfw.PRESS:
            if i <= 2:
                hour = v[2 - i]
            else:
                hour = v[14 - i]

def main():
    if not glfw.init():
        return
    # A
    window = glfw.create_window(480, 480, "2017029589", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.set_key_callback(window, key_callback)

    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        render()

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()