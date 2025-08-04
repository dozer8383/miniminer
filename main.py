import pyray as pr
from noise import snoise3

pr.init_window(1920, 1080, "Miniminer")
pr.set_target_fps(144)
pr.disable_cursor()

camera = pr.Camera3D([18.0, 1.0, 18.0], [0.0, 0.0, 0.0], [0.0, 1.0, 0.0], 45.0, 0)

groundtex = pr.load_texture_from_image(pr.load_image("assets/ground.png"));
groundtex = pr.load_texture_from_image(pr.load_image("assets/ground.png"));

block = pr.gen_mesh_cube(1.0, 1.0, 1.0)

ground.materials[0].maps[pr.MATERIAL_MAP_DIFFUSE].texture = groundtex

world = []

for iz in range(20):
    for iy in range(20):
        for ix in range(20):
            if snoise3(ix/10,iy/10,iz/10,1) > -0.1:
                world.append(pr.Transform([ix-10,iy,iz], [0,0,0], [1,1,1]))

while not pr.window_should_close():
    pr.update_camera(camera, pr.CAMERA_FIRST_PERSON)
    pr.begin_drawing()
    pr.clear_background(pr.BLACK)
    pr.begin_mode_3d(camera)

    pr.draw_grid(50, 0.5)
    pr.draw_mesh_instanced(block, ground.materials[0], world, 20*20*20)
    # pr.draw_cube([ix-10, iy-5, iz-5], 1.0, 1.0, 1.0, [int(150+10*(iy/3)), int(60+10*(iy/3)), 0, 255])
    
    pr.draw_cube([-0.5,-6,4.5],20, 1, 20, pr.DARKGRAY)

    pr.end_mode_3d()
    # pr.draw_text("Hello world", 190, 200, 20, pr.VIOLET)
    pr.draw_fps(3, 3)
    pr.end_drawing()
pr.close_window()