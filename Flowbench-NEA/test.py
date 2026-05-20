import taichi as ti
import numpy as np
import cv2  # pip install opencv-python

ti.init(arch=ti.cpu)

 # Intel Arc via Vulkan

# -----------------------------
# Parameters
# -----------------------------
DOMAIN_SIZE = 1.0
N = 128          # simulation resolution
dt = 0.02
visc = 0.0001
dx = DOMAIN_SIZE / (N - 1)

WIN_W, WIN_H = 2560, 1440  # GUI resolution

# -----------------------------
# Fields
# -----------------------------
vel = ti.Vector.field(2, ti.f32, shape=(N, N))
vel_prev = ti.Vector.field(2, ti.f32, shape=(N, N))
pressure = ti.field(ti.f32, shape=(N, N))
divergence = ti.field(ti.f32, shape=(N, N))
curl = ti.field(ti.f32, shape=(N, N))

# -----------------------------
# Helpers
# -----------------------------
@ti.func
def pos(i, j):
    return ti.Vector([i * dx, j * dx])

@ti.func
def bilerp(vf, p):
    x = p[0] / dx
    y = p[1] / dx
    x = ti.min(ti.max(x, 0.0), N - 1.001)
    y = ti.min(ti.max(y, 0.0), N - 1.001)

    i0 = int(x)
    j0 = int(y)
    i1 = i0 + 1
    j1 = j0 + 1

    sx = x - i0
    sy = y - j0

    i1 = ti.min(i1, N - 1)
    j1 = ti.min(j1, N - 1)

    v00 = vf[i0, j0]
    v10 = vf[i1, j0]
    v01 = vf[i0, j1]
    v11 = vf[i1, j1]

    v0 = v00 * (1 - sx) + v10 * sx
    v1 = v01 * (1 - sx) + v11 * sx
    return v0 * (1 - sy) + v1 * sy

# -----------------------------
# Kernels
# -----------------------------
@ti.kernel
def apply_forces(time: ti.f32):
    decay = max(2.0 - 0.5 * time, 0.0)
    for i, j in vel:
        x, y = pos(i, j)
        if 0.4 < x < 0.6 and 0.1 < y < 0.3:
            vel[i, j].y += dt * decay

@ti.kernel
def copy_vel():
    for i, j in vel:
        vel_prev[i, j] = vel[i, j]

@ti.kernel
def advect():
    for i, j in vel:
        p = pos(i, j)
        v = vel_prev[i, j]
        v = ti.min(ti.max(v, ti.Vector([-5.0, -5.0])), ti.Vector([5.0, 5.0]))
        back = p - dt * v
        back[0] = ti.min(ti.max(back[0], 0.0), DOMAIN_SIZE)
        back[1] = ti.min(ti.max(back[1], 0.0), DOMAIN_SIZE)
        vel[i, j] = bilerp(vel_prev, back)

@ti.kernel
def diffuse():
    for i, j in vel:
        if 0 < i < N - 1 and 0 < j < N - 1:
            lap = (
                vel_prev[i + 1, j] + vel_prev[i - 1, j] +
                vel_prev[i, j + 1] + vel_prev[i, j - 1] -
                4 * vel_prev[i, j]
            ) / (dx * dx)
            vel[i, j] = vel_prev[i, j] + visc * dt * lap
        else:
            vel[i, j] = ti.Vector([0.0, 0.0])

@ti.kernel
def compute_div():
    for i, j in divergence:
        if 0 < i < N - 1 and 0 < j < N - 1:
            vx = (vel[i + 1, j].x - vel[i - 1, j].x) / (2 * dx)
            vy = (vel[i, j + 1].y - vel[i, j - 1].y) / (2 * dx)
            divergence[i, j] = vx + vy
        else:
            divergence[i, j] = 0.0

@ti.kernel
def clear_pressure():
    for i, j in pressure:
        pressure[i, j] = 0.0

@ti.kernel
def pressure_jacobi():
    for i, j in pressure:
        if 0 < i < N - 1 and 0 < j < N - 1:
            pressure[i, j] = (
                pressure[i + 1, j] + pressure[i - 1, j] +
                pressure[i, j + 1] + pressure[i, j - 1] -
                divergence[i, j] * dx * dx
            ) * 0.25

@ti.kernel
def project():
    for i, j in vel:
        if 0 < i < N - 1 and 0 < j < N - 1:
            px = (pressure[i + 1, j] - pressure[i - 1, j]) / (2 * dx)
            py = (pressure[i, j + 1] - pressure[i, j - 1]) / (2 * dx)
            vel[i, j] -= ti.Vector([px, py])
        else:
            vel[i, j] = ti.Vector([0.0, 0.0])

@ti.kernel
def compute_curl():
    for i, j in curl:
        if 0 < i < N - 1 and 0 < j < N - 1:
            dvx_dy = (vel[i, j + 1].x - vel[i, j - 1].x) / (2 * dx)
            dvy_dx = (vel[i + 1, j].y - vel[i - 1, j].y) / (2 * dx)
            curl[i, j] = dvy_dx - dvx_dy
        else:
            curl[i, j] = 0.0

# -----------------------------
# Main (Taichi GUI)
# -----------------------------
def main():
    gui = ti.GUI("Fluid (Intel Arc)", res=(WIN_W, WIN_H))
    time = 0.0

    while gui.running:
        time += dt

        apply_forces(time)

        copy_vel()
        advect()

        copy_vel()
        diffuse()

        compute_div()
        clear_pressure()
        for _ in range(20):
            pressure_jacobi()
        project()

        compute_curl()
        curl_np = curl.to_numpy()
        m = np.max(np.abs(curl_np)) + 1e-6
        img = (curl_np / m * 0.5 + 0.5).astype(np.float32)

        # Get actual GUI resolution dynamically
        win_w, win_h = gui.res

        # Resize correctly (cv2 uses width, height)
        img_resized = cv2.resize(img, (win_w, win_h), interpolation=cv2.INTER_LINEAR)

        # Ensure shape matches Taichi GUI expectation (height, width)
        img_resized = img_resized.reshape(win_h, win_w)

        gui.set_image(img_resized)
        gui.show()




if __name__ == "__main__":
    main()
