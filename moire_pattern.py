import time
import math
import tkinter as tk
from tkinter import messagebox
from tkinter import *
from tkinter.ttk import *

class Window():

    window_shape = (1080, 720)
    canvas_shape = (1024, 512)
    num_rays_1 = 100
    num_rays_2 = 200
    speed_1 = 1
    speed_2 = 2
    ray_length = 500
    centre_1 = (0.5 * canvas_shape[0], 0.35 * canvas_shape[1])
    centre_2 = (0.5 * canvas_shape[0], 0.6 * canvas_shape[1])
    spin_resolution = math.pi * 8
    refresh_rate = 240

    def __init__(self):
        self.spin = False
        self.move = False
        self.root = None
        self.canvas = None
        self.angle = 0
        self.angle_1 = 0
        self.angle_2 = 0
        self.step = 10
        self.bunch_1 = None
        self.bunch_2 = None
        self.main_window()

    def make_it_move(self):
        if self.move is True:
            return None
        self.move = True
        if self.spin is not True:
            self.update_canvas()

    def make_it_spin(self):
        if self.spin is True:
            return None
        self.spin = True
        if self.move is not True:
            self.update_canvas()

    def make_it_stop(self):
        self.move = False
        self.spin = False

    def update_canvas(self):
        centre_1, centre_2 = Window.centre_1, Window.centre_2
        spin_resolution = Window.spin_resolution
        speed_1, speed_2 = Window.speed_1, Window.speed_2
        num_rays_1, num_rays_2 = Window.num_rays_1, Window.num_rays_2

        if not all([self.bunch_1, self.bunch_2]):
            return None

        if self.spin is True:

            self.angle_1 += 1/spin_resolution
            self.angle_1 = self.angle_1 if \
                self.angle_1 < spin_resolution else 0

            for line_id, line in enumerate(self.bunch_1):
                self.update_line(line, centre_1, speed_1, self.angle_1,
                                 line_id, num_rays_1, direction=1)

            self.angle_2 += 1/spin_resolution
            self.angle_2 = self.angle_2 if \
                (self.angle_2 < spin_resolution) else 0

            for line_id, line in enumerate(self.bunch_2):
                self.update_line(line, centre_2, speed_2, self.angle_2,
                                 line_id, num_rays_2, direction=-1)

        if any([self.spin, self.move]):
            self.root.after(int(1/Window.refresh_rate * 1000), self.update_canvas)

    def update_line(self, line, centre, speed, angle, line_id, num_rays, direction=1):
        ray_length = Window.ray_length
        canvas_width = Window.canvas_shape[0]
        centre_x, centre_y = centre

        if self.move is True:
            x1, y1, x2, y2 = self.canvas.coords(line)
            midx = centre
            self.step = self.step if (midx < canvas_width and self.step >= 0) else -self.step
            self.step = -self.step if (midx > 0 and self.step < 0) else self.step
            x1 += self.step
            x2 += self.step
            self.canvas.coords(line, x1, y1, x2, y2)

        if self.spin is True:

            x1, y1, x2, y2 = self.canvas.coords(line)

            x1 = centre_x - direction * ray_length * math.sin((direction * speed * angle + line_id) * 2 * math.pi/num_rays)
            x2 = centre_x + direction * ray_length * math.sin((direction * speed * angle + line_id) * 2 * math.pi/num_rays)
            y1 = centre_y + direction * ray_length * math.cos((direction * speed * angle + line_id) * 2 * math.pi/num_rays)
            y2 = centre_y - direction * ray_length * math.cos((direction * speed * angle + line_id) * 2 * math.pi/num_rays)
            self.canvas.coords(line, x1, y1, x2, y2)

    def make_bunch(self, ray_length, centre, num_rays):
        bunch = list()
        self.angle = 0

        for _ in range(num_rays):
            self.angle += 1
            self.angle = self.angle if self.angle < num_rays else 0

            centre_x, centre_y = centre

            x1 = centre_x + ray_length * math.sin(self.angle * 2 * math.pi/num_rays)
            x2 = centre_x - ray_length * math.sin(self.angle * 2 * math.pi/num_rays)
            y1 = centre_y - ray_length * math.cos(self.angle * 2 * math.pi/num_rays)
            y2 = centre_y + ray_length * math.cos(self.angle * 2 * math.pi/num_rays)
            line = self.canvas.create_line((x1, y1, x2, y2), fill='white')
            self.canvas.coords(line, x1, y1, x2, y2)

            self.canvas.pack()
            bunch.append(line)

        return bunch

    def prep_moire(self):

        canvas_width, canvas_height = Window.canvas_shape
        num_rays_1, num_rays_2 = Window.num_rays_1, Window.num_rays_2
        centre_1, centre_2 = Window.centre_1, Window.centre_2
        ray_length = Window.ray_length

        if self.canvas is not None:
            self.canvas.destroy()

        self.canvas = Canvas(self.root, bg="black", width=canvas_width,
                             height=canvas_height)

        self.bunch_1 = self.make_bunch(ray_length, centre_1, num_rays_1)
        self.bunch_2 = self.make_bunch(ray_length, centre_2, num_rays_2)

    def Close(self):
        self.root.destroy()

    def main_window(self):

        window_width, window_height = Window.window_shape

        self.root = Tk()
        self.root.geometry(f"{window_width}x{window_height}")

        # Button for closing 
        exit_button = Button(self.root, text="Exit", command=self.Close)
        exit_button.pack(pady=20)

        move_it_button = Button(self.root, text="Move it",
                                command=self.make_it_move)
        # move_it_button.pack()

        spin_it_button = Button(self.root, text="Spin it",
                                command=self.make_it_spin)
        spin_it_button.pack()

        stop_it_button = Button(self.root, text="Stop it",
                                command=self.make_it_stop)
        stop_it_button.pack()
        del_shape_button = Button(self.root, text="Restart",
                                  command=lambda:
                                  (self.__setattr__("move", False),
                                   self.__setattr__("spin", False),
                                   self.prep_moire()))
        del_shape_button.pack()

        self.prep_moire()

        self.root.mainloop()


test = Window()
