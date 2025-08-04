from ursina import *
from ursina.shaders import *
from ursina.lights import DirectionalLight
import math
from noise import snoise3
app = Ursina(title='MiniMiner',render_mode="wireframe")

Sky(color=color.white)

soil = Texture("./assets/ground.png")

camera.fov = 100
camera.clip_plane_far = 20

# mouse.locked = True

world = []

for iz in range(20):
    world.append([])
    for iy in range(10):
        world[iz].append([])
        for ix in range(20):
            world[iz][iy].append([])
            # if iy < sin(iz) + sin(ix) + 5:
            if snoise3(ix/10,iy/10,iz/10,1) > -0.1:
                world[iz][iy][ix] = Entity(model='cube',texture=soil,x=ix,y=iy,z=iz)

def update():
    camera.x += held_keys['d'] * time.dt * 5
    camera.x -= held_keys['a'] * time.dt * 5
    camera.y += held_keys['space'] * time.dt * 5
    camera.y -= held_keys['shift'] * time.dt * 5
    camera.z += held_keys['w'] * time.dt * 5
    camera.z -= held_keys['s'] * time.dt * 5
    camera.rotation_y = mouse.x*200
    camera.rotation_x = -mouse.y*200

# def input(key):
#     if key == 'space':
#         camera.y += 1
#         invoke(setattr, camera, 'y', camera.y-1, delay=0.25)

app.run()