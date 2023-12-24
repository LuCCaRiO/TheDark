import pygame as pg
pg.mixer.init()

import moderngl
import array

from settings import *
from map import Map
from user_interface import HealthBar, MagicBar, UI
from camera import Camera


class Game:
    def __init__(self):

        monitor_size = pg.display.Info()
        self.screen = pg.display.set_mode((monitor_size.current_h * TARGET_ASPECT_RATIO,
                                           monitor_size.current_h), pg.OPENGL | pg.DOUBLEBUF)
        self.display = pg.Surface((monitor_size.current_h * TARGET_ASPECT_RATIO,
                                   monitor_size.current_h))
        self.ctx = moderngl.create_context()
        quad_buffer = self.ctx.buffer(data=array.array('f', [
            -1.0, 1.0, 0.0, 0.0,
            1.0, 1.0, 1.0, 0.0,
            -1.0, -1.0, 0.0, 1.0,
            1.0, -1.0, 1.0, 1.0
        ]))

        vert_shader = '''
        #version 330 core
        
        in vec2 vert;
        in vec2 texcoord;
        out vec2 uvs;
        
        void main() {
            uvs = texcoord;
            gl_Position = vec4(vert, 0.0, 1.0);
        }
        '''

        frag_shader = '''
        #version 330 core
        
        uniform sampler2D tex;
        
        in vec2 uvs;
        out vec4 f_color;
        
        void main() {
            vec4 color = texture(tex, uvs);
            vec2 pixel = vec2(1.0/448.0, 1.0/264.0); // assuming 512x512 texture size   14 8
            vec2 coord = floor(uvs / pixel) * pixel;
            vec4 new_color = texture(tex, coord);
            f_color = vec4(new_color.rgb, color.a);
        }
        '''

        self.program = self.ctx.program(vertex_shader=vert_shader, fragment_shader=frag_shader)
        self.render_object = self.ctx.vertex_array(self.program, [(quad_buffer, "2f 2f", "vert", "texcoord")])

        self.camera_sprites = Camera(self.display)

        self.level = 0

        self.map = Map(f"levels/level_{self.level}.csv", self.camera_sprites)

        self.health_bar = None
        self.magic_bar = None

        self.time = NORMAL_TIME
        self.ability_on = False

        self.user_interface = pg.sprite.Group()
        self.create_ui()

    @staticmethod
    def surf_to_tex(ctx, surf):
        tex = ctx.texture(surf.get_size(), 4)
        tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
        tex.swizzle = "BGRA"
        tex.write(surf.get_view("1"))
        return tex

    def run(self):
        clock = pg.time.Clock()
        while True:
            delta_time = clock.tick(FPS)
            print(clock.get_fps())
            if self.ability_on:
                self.display.fill(ABILITY_COLOR)
            else:
                self.display.fill(NORMAL_COLOR)

            self.handle_events()

            self.ability_mode(delta_time)
            delta_time *= self.time
            self.map.update(delta_time)

            self.user_interface.update(delta_time)
            self.health_bar.set_value(self.map.player.health)
            self.magic_bar.set_value(self.map.player.magic)
            self.user_interface.draw(self.display)

            frame_tex = Game.surf_to_tex(self.ctx, self.display)
            frame_tex.use(0)
            self.program["tex"] = 0
            self.render_object.render(mode=moderngl.TRIANGLE_STRIP)

            pg.display.flip()

            frame_tex.release()

    def load_level(self, file):
        self.map.kill()
        self.map = Map(file, self.camera_sprites)

    def next_level(self):
        self.level += 1
        self.map.kill()
        self.map = Map(f"levels/level_{self.level}.csv", self.camera_sprites)

    def ability_mode(self, delta_time):
        if self.map.player.magic <= 0:
            self.ability_on = False
            self.time = NORMAL_TIME
        elif self.ability_on:
            self.map.player.set_magic(self.map.player.magic - (delta_time / RELATION_DELTA_TIME) * 0.33)

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.map.player.jump()
                if event.key == pg.K_LSHIFT:
                    if not self.ability_on:
                        self.ability_on = True
                        self.time = ABILITY_TIME
                    else:
                        self.ability_on = False
                        self.time = NORMAL_TIME

    def get_player(self):
        return self.map.player

    def create_ui(self):
        screen_width, screen_height = self.screen.get_size()

        #dark = pg.Surface(self.screen.get_size(), pg.SRCALPHA)
        #dark.fill(NORMAL_COLOR)

        #self.dark = UI([dark], (0, 0), [self.user_interface])
        #Light((screen_width // 2 - 200, 0), [self.user_interface], 200, self.get_player)

        self.health_bar = HealthBar((10, 10), [self.user_interface])
        self.magic_bar = MagicBar((10, 100), [self.user_interface])


if __name__ == "__main__":
    pg.init()
    game = Game()

    from scene_loader import SceneLoader
    SceneLoader(game)

    game.run()
