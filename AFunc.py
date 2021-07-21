from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.graphics.texture import Texture
from math import sin, cos, tan, pi, log, log10, log2
from kivy.core.window import Window
from kivy.clock import Clock
from array import array

class MainScreen(Label):

    def main_loop_func(self, dt):
        if self.mode == 1:
            self.arr = []
            self.x = self.ids.starting_value.text
            result = self.run_function()
            n = 0
            for number in result:
                if number <= 3000 / int(self.ids.vertical_scale.text) and number >= 0:
                    try:
                        draw_canvas.texture_array[int((self.iteration + (int(number * int(self.ids.vertical_scale.text))) * 800) * 3)] = 255 - (n * 2 + 50)
                        draw_canvas.texture_array[int((self.iteration + (int(number * int(self.ids.vertical_scale.text))) * 800) * 3) + 2] = n * 2 + 50
                    except:
                        pass
                n += 1
            self.iteration += 1
            if self.iteration == 800:
                self.mode = 0
        draw_canvas.draw_canvas()
    
    def run_function(self):
        output = []
        for _ in range(100):
            try:
                x = self.x
                a = self.iteration / 200
                x = eval(self.ids.function.text)
                self.x = x
                if x <= 100000000 and x >= -100000000:
                    output.append(x)
                else:
                    break
            except:
                break
        return output
    
    def clear(self):
        self.mode = 0
        draw_canvas.clear()
    
    def toggle_draw_mode(self, mode = ''):
        self.iteration = 0
        if mode != '':
            self.mode = mode
        else:
            self.mode = (self.mode + 1) % 2
            if self.mode == 1:
                draw_canvas.clear()

class Drawcanvas(Widget):
    def __init__(self, **kwargs):
        super(Drawcanvas, self).__init__(**kwargs)
        self.size = (800, 600)
        self.tex = Texture.create(size = self.size)
        self.clear()
    
    def clear(self):
        self.texture_array = [0 for _ in range(self.size[0] * self.size[0] * 3)]
        
    def draw_canvas(self):
        self.canvas.clear()
        self.texture_arr = array('B', self.texture_array)
        if self.tex.min_filter != 'nearest' or self.tex.mag_filter != 'nearest':
            self.tex.min_filter = 'nearest'
            self.tex.mag_filter = 'nearest'
        self.padding_x = 0
        self.padding_y = Window.size[1] * 0.22
        self.pix_size_x = Window.size[0]
        self.pix_size_y = Window.size[1] * 0.78
        self.tex.blit_buffer(self.texture_arr, colorfmt='rgb', bufferfmt='ubyte')
        with self.canvas:
            Rectangle(texture = self.tex, pos = (self.padding_x, self.padding_y), size = (self.pix_size_x, self.pix_size_y))

class AFunc(App):
    def build(self):
        global main_screen
        main_screen = MainScreen()
        main_screen.toggle_draw_mode(0)
        main_screen.iteration = 0
        global draw_canvas
        draw_canvas = Drawcanvas()
        draw_canvas.touch = False
        main_screen.add_widget(draw_canvas)
        return main_screen

    def on_start(self, **kwargs):
        self.mainloop = Clock.schedule_interval(main_screen.main_loop_func, 1 / 180)
                   
if __name__ == '__main__':
    AFunc().run()