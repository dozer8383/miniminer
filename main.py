import pyray as pr
from noise import snoise3

pr.set_config_flags(pr.FLAG_MSAA_4X_HINT);
pr.init_window(1920, 1080, "Miniminer")
pr.set_target_fps(144)
pr.disable_cursor()

camera = pr.Camera3D()
camera.position = pr.Vector3(10, 10, 10)
camera.up = pr.Vector3(0, 1, 0)
camera.fovy = 85.0
speed = 0.1
rotspeed = 0.5

groundtex = pr.load_texture("assets/ground.png")

shader = pr.load_shader("assets/vertex.vs", "assets/fragment.fs")
shader.locs[pr.ShaderLocationIndex.SHADER_LOC_MATRIX_MVP] = pr.get_shader_location(shader, "mvp")

block = pr.gen_mesh_cube(1.0, 1.0, 1.0)

ground = pr.load_material_default()
ground.maps[pr.MATERIAL_MAP_DIFFUSE].texture = groundtex

worldwidth = 20
worldheight = 20
worlddepth = 20
world = []

for iz in range(worlddepth):
    world.append([])
    for iy in range(worldheight):
        world[iz].append([])
        for ix in range(worldwidth):
            world[iz][iy].append([])
            if snoise3(ix/10,iy/10,iz/10,1) > 0.1:
                world[iz][iy][ix] = 1
            else:
                world[iz][iy][ix] = 0

while not pr.window_should_close():
    # pr.update_camera(camera, pr.CAMERA_FIRST_PERSON)
    pr.update_camera_pro(camera,
                         pr.Vector3(pr.is_key_down(pr.KEY_W)*speed - pr.is_key_down(pr.KEY_S)*speed,
                                    pr.is_key_down(pr.KEY_D)*speed - pr.is_key_down(pr.KEY_A)*speed,
                                    pr.is_key_down(pr.KEY_SPACE)*speed - pr.is_key_down(pr.KEY_LEFT_SHIFT)*speed),
                         pr.Vector3(pr.get_mouse_delta().x*rotspeed,
                                    pr.get_mouse_delta().y*rotspeed,
                                    0),
                         0)
                        
    pr.begin_drawing()
    pr.clear_background([25,12,10])
    pr.begin_mode_3d(camera)

    # pr.draw_grid(50, 1)
    for iz in range(worlddepth):
        for iy in range(worldheight):
            for ix in range(worldwidth):
                if world[ix][iy][iz] == 1:
                    pr.draw_mesh(block,ground,pr.matrix_translate(ix,iy+0.8,iz))

    pr.end_mode_3d()
    pr.draw_text(f"X:{round(camera.position.x)}, Y:{round(camera.position.y)}, Z:{round(camera.position.z)}", 3, 20, 20, pr.WHITE)
    pr.draw_fps(3, 3)
    pr.end_drawing()

    # if pr.is_key_down(pr.KEY_SPACE):
    #     camera.position.y += 1
    #     camera.tar = pr.Vector3(0, 1, 0)

    # if pr.is_key_down(pr.KEY_LEFT_SHIFT):
    #     camera.position.y -= 1
    #     camera.up = pr.Vector3(0, 1, 0)
    
pr.close_window()
