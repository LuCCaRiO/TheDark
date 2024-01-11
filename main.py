import moderngl
import pygame as pg

pg.init()
pg.mixer.init()

import sys
import array

from settings import *
from map import Map
from user_interface import HealthBar, MagicBar, UI, Dialogue
from camera import Camera
from cutscene import CutSceneManager, StoryCutScene


class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((WIDTH,
                                           HEIGHT), pg.FULLSCREEN | pg.OPENGL | pg.DOUBLEBUF)
        self.display = pg.Surface((WIDTH,
                                   HEIGHT))
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
            // Define the size of each "pixel"
            vec2 pixelSize = vec2(1 / 360.0); // Adjust the size to control pixelation
        
            // Calculate the texture coordinates for the current fragment
            vec2 coord = floor(uvs / pixelSize) * pixelSize + pixelSize * 0.5; // Adding half a pixel for centering
        
            // Perform bilinear filtering for smoother edges
            vec4 color = vec4(-0.2);
            int samples = 0; // Counter for the number of samples taken
        
            // Increase the range for sampling by considering a larger area
            for (float x = -1.0; x <= 1.0; x += 1.0) {
                for (float y = -1.0; y <= 1.0; y += 1.0) {
                    vec2 sampleCoord = coord + pixelSize * vec2(x, y);
                    color += texture(tex, sampleCoord);
                    samples++;
                }
            }
        
            color /= float(samples); // Average the colors based on the number of samples taken
        
            // Output the final color
            f_color = color;
        }

        '''

        self.program = self.ctx.program(vertex_shader=vert_shader, fragment_shader=frag_shader)
        self.render_object = self.ctx.vertex_array(self.program, [(quad_buffer, "2f 2f", "vert", "texcoord")])

        self.camera = Camera(self.display)

        self.level = 0

        self.cut_scene_manager = CutSceneManager(self.display)
        story_cut_scene = StoryCutScene()
        self.cut_scene_manager.start_cut_scene(story_cut_scene)

        self.map = Map(f"levels/level_{self.level}.csv", self.camera)

        self.health_bar = None
        self.magic_bar = None
        self.dialogue = None

        self.time = NORMAL_TIME
        self.ability_on = False

        self.pause = False

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

            self.handle_events()
            if not self.cut_scene_manager.cut_scene_running:
                self.ability_mode(delta_time)
                delta_time *= self.time

                if self.ability_on:
                    self.display.fill(ABILITY_COLOR)
                else:
                    self.display.fill(NORMAL_COLOR)

                if self.dialogue.running:
                    self.pause = True
                else:
                    self.pause = False

                self.map.update(delta_time, self.pause)

                self.user_interface.update(delta_time)
                self.health_bar.set_value(self.map.player.health)
                self.magic_bar.set_value(self.map.player.magic)
                self.user_interface.draw(self.display)
            else:
                self.display.fill(NORMAL_COLOR)
                self.cut_scene_manager.update(delta_time)
                self.cut_scene_manager.draw()

            frame_tex = Game.surf_to_tex(self.ctx, self.display)
            frame_tex.use(0)
            self.program["tex"] = 0
            self.render_object.render(mode=moderngl.TRIANGLE_STRIP)

            pg.display.flip()

            frame_tex.release()

    def load_level(self, file):
        self.map.kill()
        self.camera.offset = pg.math.Vector2(0, 0)
        self.map = Map(file, self.camera)

    def next_level(self):
        self.level += 1
        self.load_level(f"levels/level_{self.level}.csv")

    def ability_mode(self, delta_time):
        if self.map.player.magic <= 0 or not self.map.player.ABILITIES["slowness"]:
            self.ability_on = False
            self.time = NORMAL_TIME
        elif self.ability_on:
            self.map.player.set_magic(self.map.player.magic - (delta_time / RELATION_DELTA_TIME) * 0.15)

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                match event.key:
                    case pg.K_SPACE:
                        self.map.player.jump()
                    case pg.K_LSHIFT:
                        if not self.ability_on:
                            self.ability_on = True
                            self.time = ABILITY_TIME
                        else:
                            self.ability_on = False
                            self.time = NORMAL_TIME
                    case pg.K_w:
                        self.map.player.dash()

    def get_player(self):
        return self.map.player

    def create_ui(self):
        self.health_bar = HealthBar((10, 10), [self.user_interface])
        self.magic_bar = MagicBar((10, 100), [self.user_interface])
        self.dialogue = Dialogue(["Where am I?", "Who am I?"], (0, 0), [self.user_interface])


if __name__ == "__main__":
    game = Game()

    from scene_loader import SceneLoader
    SceneLoader(game)

    game.run()
