import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from OpenGL.arrays import vbo

gCamAng = 0.
gCamHeight = 1.


def createVertexAndIndexArrayIndexed():
    varr = np.array([
        (-0.5773502691896258, 0.5773502691896258, 0.5773502691896258),
        (-1, 1, 1),  # v0
        (0.8164965809277261, 0.4082482904638631, 0.4082482904638631),
        (1, 1, 1),  # v1
        (0.4082482904638631, -0.4082482904638631, 0.8164965809277261),
        (1, -1, 1),  # v2
        (-0.4082482904638631, -0.8164965809277261, 0.4082482904638631),
        (-1, -1, 1),  # v3
        (-0.4082482904638631, 0.4082482904638631, -0.8164965809277261),
        (-1, 1, -1),  # v4
        (0.4082482904638631, 0.8164965809277261, -0.4082482904638631),
        (1, 1, -1),  # v5
        (0.5773502691896258, -0.5773502691896258, -0.5773502691896258),
        (1, -1, -1),  # v6
        (-0.8164965809277261, -0.4082482904638631, -0.4082482904638631),
        (-1, -1, -1),  # v7
    ], 'float32')
    iarr = np.array([
        (0, 2, 1),
        (0, 3, 2),
        (4, 5, 6),
        (4, 6, 7),
        (0, 1, 5),
        (0, 5, 4),
        (3, 6, 2),
        (3, 7, 6),
        (1, 2, 6),
        (1, 6, 5),
        (0, 7, 3),
        (0, 4, 7),
    ])
    return varr, iarr


def drawCube_glDrawElements():
    global gVertexArrayIndexed, gIndexArray
    varr = gVertexArrayIndexed
    iarr = gIndexArray
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 6 * varr.itemsize, varr)
    glVertexPointer(3, GL_FLOAT, 6 * varr.itemsize, ctypes.c_void_p(varr.ctypes.data + 3 * varr.itemsize))
    glDrawElements(GL_TRIANGLES, iarr.size, GL_UNSIGNED_INT, iarr)


def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0., 0., 0.]))
    glVertex3fv(np.array([3., 0., 0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0., 0., 0.]))
    glVertex3fv(np.array([0., 3., 0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0., 0., 0]))
    glVertex3fv(np.array([0., 0., 3.]))
    glEnd()

def l2norm(v):
    return np.sqrt(np.dot(v, v))


def normalized(v):
    l = l2norm(v)
    return 1/l * np.array(v)


def exp(rv):
    th = l2norm(rv)
    rv = normalized(rv)
    x = rv[0]
    y = rv[1]
    z = rv[2]
    R = np.array([[np.cos(th) + x * x * (1 - np.cos(th)), x * y * (1 - np.cos(th)) - z * np.sin(th),
                   x * z * (1 - np.cos(th)) + y * np.sin(th)],
                  [y * x * (1 - np.cos(th)) + z * np.sin(th), np.cos(th) + y * y * (1 - np.cos(th)),
                   y * z * (1 - np.cos(th)) - x * np.sin(th)],
                  [z * x * (1 - np.cos(th)) - y * np.sin(th), z * y * (1 - np.cos(th)) + x * np.sin(th),
                   np.cos(th) + z * z * (1 - np.cos(th))]])
    return R


def log(R):
    th = np.arccos((R[0][0] + R[1][1] + R[2][2] - 1) / 2)
    v = np.array([(R[2][1] - R[1][2]) / (2 * np.sin(th)),
                  (R[0][2] - R[2][0]) / (2 * np.sin(th)),
                  (R[1][0] - R[0][1]) / (2 * np.sin(th))])
    return v * th


def slerp(R1, R2, t):
    return R1 @ exp(t * log(R1.T @ R2))


def XYZEulerToRotMat(euler):
    xang, yang, zang = euler
    xang = np.radians(xang)
    yang = np.radians(yang)
    zang = np.radians(zang)

    Rx = np.array([[1, 0, 0],
                   [0, np.cos(xang), -np.sin(xang)],
                   [0, np.sin(xang), np.cos(xang)]])
    Ry = np.array([[np.cos(yang), 0, np.sin(yang)],
                   [0, 1, 0],
                   [-np.sin(yang), 0, np.cos(yang)]])
    Rz = np.array([[np.cos(zang), -np.sin(zang), 0],
                   [np.sin(zang), np.cos(zang), 0],
                   [0, 0, 1]])
    return Rx @ Ry @ Rz

frame = 0

def render():
    global gCamAng, gCamHeight, frame
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1, 1, 10)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(5 * np.sin(gCamAng), gCamHeight, 5 * np.cos(gCamAng), 0, 0, 0, 0, 1, 0)

    # draw global frame
    drawFrame()

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glEnable(GL_RESCALE_NORMAL)

    lightPos = (3., 4., 5., 1.)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)

    lightColor = (1., 1., 1., 1.)
    ambientLightColor = (.1, .1, .1, 1.)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)

    objectColor = (1., 1., 1., 1.)
    specularObjectColor = (1., 1., 1., 1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)


    R1 = np.identity(4)
    R1[:3, :3] = XYZEulerToRotMat((20., 30., 30.))
    R2 = np.identity(4)
    R2[:3, :3] = XYZEulerToRotMat((15., 30., 25.))
    T1 = np.identity(4)
    T1[0][3] = 1.

    f = frame % 61
    t = (f % 20) / 20

    if f < 20:
        R1[:3, :3] = slerp(XYZEulerToRotMat((20., 30., 30.)), XYZEulerToRotMat((45., 60., 40.)), t)
        R2[:3, :3] = slerp(XYZEulerToRotMat((15., 30., 25.)), XYZEulerToRotMat((25., 40., 40.)), t)
    elif f < 40:
        R1[:3, :3] = slerp(XYZEulerToRotMat((45., 60., 40.)), XYZEulerToRotMat((60., 70., 50.)), t)
        R2[:3, :3] = slerp(XYZEulerToRotMat((25., 40., 40.)), XYZEulerToRotMat((40., 60., 50.)), t)
    elif f < 60:
        R1[:3, :3] = slerp(XYZEulerToRotMat((60., 70., 50.)), XYZEulerToRotMat((80., 85., 70.)), t)
        R2[:3, :3] = slerp(XYZEulerToRotMat((40., 60., 50.)), XYZEulerToRotMat((55., 80., 65.)), t)
    elif f == 60:
        R1[:3, :3] = XYZEulerToRotMat((80., 85., 70.))
        R2[:3, :3] = XYZEulerToRotMat((55., 80., 65.))
    frame += 1

    J1 = R1
    J2 = R1 @ T1 @ R2

    glPushMatrix()
    glMultMatrixf(J1.T)
    glPushMatrix()
    glTranslatef(0.5, 0, 0)
    glScalef(0.5, 0.05, 0.05)
    drawCube_glDrawElements()
    glPopMatrix()
    glPopMatrix()

    glPushMatrix()
    glMultMatrixf(J2.T)
    glPushMatrix()
    glTranslatef(0.5, 0, 0)
    glScalef(0.5, 0.05, 0.05)
    drawCube_glDrawElements()
    glPopMatrix()
    glPopMatrix()

    R1[:3, :3] = XYZEulerToRotMat((20., 30., 30.))
    R2[:3, :3] = XYZEulerToRotMat((15., 30., 25.))
    J1 = R1
    J2 = R1 @ T1 @ R2
    objectColor = (1., 0., 0., 1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)

    glPushMatrix()
    glMultMatrixf(J1.T)
    glPushMatrix()
    glTranslatef(0.5, 0, 0)
    glScalef(0.5, 0.05, 0.05)
    drawCube_glDrawElements()
    glPopMatrix()
    glPopMatrix()


    glPushMatrix()
    glMultMatrixf(J2.T)
    glPushMatrix()
    glTranslatef(0.5, 0, 0)
    glScalef(0.5, 0.05, 0.05)
    drawCube_glDrawElements()
    glPopMatrix()
    glPopMatrix()


    R1[:3, :3] = XYZEulerToRotMat((45., 60., 40.))
    R2[:3, :3] = XYZEulerToRotMat((25., 40., 40.))
    J1 = R1
    J2 = R1 @ T1 @ R2
    objectColor = (1., 1., 0., 1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)

    glPushMatrix()
    glMultMatrixf(J1.T)
    glPushMatrix()
    glTranslatef(0.5, 0, 0)
    glScalef(0.5, 0.05, 0.05)
    drawCube_glDrawElements()
    glPopMatrix()
    glPopMatrix()

    glPushMatrix()
    glMultMatrixf(J2.T)
    glPushMatrix()
    glTranslatef(0.5, 0, 0)
    glScalef(0.5, 0.05, 0.05)
    drawCube_glDrawElements()
    glPopMatrix()
    glPopMatrix()

    R1[:3, :3] = XYZEulerToRotMat((60., 70., 50.))
    R2[:3, :3] = XYZEulerToRotMat((40., 60., 50.))
    J1 = R1
    J2 = R1 @ T1 @ R2
    objectColor = (0., 1., 0., 1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)

    glPushMatrix()
    glMultMatrixf(J1.T)
    glPushMatrix()
    glTranslatef(0.5, 0, 0)
    glScalef(0.5, 0.05, 0.05)
    drawCube_glDrawElements()
    glPopMatrix()
    glPopMatrix()

    glPushMatrix()
    glMultMatrixf(J2.T)
    glPushMatrix()
    glTranslatef(0.5, 0, 0)
    glScalef(0.5, 0.05, 0.05)
    drawCube_glDrawElements()
    glPopMatrix()
    glPopMatrix()

    R1[:3, :3] = XYZEulerToRotMat((80., 85., 70.))
    R2[:3, :3] = XYZEulerToRotMat((55., 80., 65.))
    J1 = R1
    J2 = R1 @ T1 @ R2
    objectColor = (0., 0., 1., 1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)

    glPushMatrix()
    glMultMatrixf(J1.T)
    glPushMatrix()
    glTranslatef(0.5, 0, 0)
    glScalef(0.5, 0.05, 0.05)
    drawCube_glDrawElements()
    glPopMatrix()
    glPopMatrix()

    glPushMatrix()
    glMultMatrixf(J2.T)
    glPushMatrix()
    glTranslatef(0.5, 0, 0)
    glScalef(0.5, 0.05, 0.05)
    drawCube_glDrawElements()
    glPopMatrix()
    glPopMatrix()


    glDisable(GL_LIGHTING)


def key_callback(window, key, scancode, action, mods):
    global gCamAng, gCamHeight
    # rotate the camera when 1 or 3 key is pressed or repeated
    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_1:
            gCamAng += np.radians(-10)
        elif key == glfw.KEY_3:
            gCamAng += np.radians(10)
        elif key == glfw.KEY_2:
            gCamHeight += .1
        elif key == glfw.KEY_W:
            gCamHeight += -.1


gVertexArrayIndexed = None
gIndexArray = None


def main():
    global gVertexArrayIndexed, gIndexArray
    if not glfw.init():
        return
    window = glfw.create_window(640, 640, '2017029589', None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.swap_interval(1)

    gVertexArrayIndexed, gIndexArray = createVertexAndIndexArrayIndexed()

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()

        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()
