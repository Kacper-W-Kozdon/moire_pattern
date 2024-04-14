import time
import math
import tkinter as tk
from tkinter import messagebox
from tkinter import *
from tkinter.ttk import *

class Window():

    window_shape = (1024, 1024)
    canvas_shape = (512, 512)
    num_rays_1 = 40
    num_rays_2 = 60
    speed_1 = 1.5
    speed_2 = 1
    ray_length = 300
    centre_1 = 200
    centre_2 = 312
    spin_resolution = math.pi * 4

    def __init__(self):
          self.spin = False
          self.move = False
          self.root = None
          self.canvas = None
          self.angle_1 = 0
          self.angle_2 = 0
          self.step = 10
          self.bunch_1 = None
          self.bunch_2 = None
          self.main_window()

    def make_it_move(self):
        if self.move == True:
            return None
        self.move = True
        if self.spin is not True:
            self.update_canvas()

    def make_it_spin(self):
        if self.spin == True:
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

        if not all([self.bunch_1, self.bunch_2]):
            return None

        if self.spin is True:

            self.angle_1 += 1/spin_resolution
            self.angle_1 = self.angle_1 if self.angle_1 < spin_resolution else 0

            for line_id, line in enumerate(self.bunch_1):
                self.update_line(line, centre_1, speed_1, self.angle_1, line_id, direction=1)

            self.angle_2 += 1/spin_resolution
            self.angle_2 = self.angle_2 if self.angle_2 < spin_resolution else 0

            for line_id, line in enumerate(self.bunch_2):
                self.update_line(line, centre_2, speed_2, self.angle_2, line_id, direction=-1)

        if any([self.spin, self.move]):
            self.root.after(20, self.update_canvas)

    def update_line(self, line, centre, speed, angle, line_id, direction=1):
        spin_resolution = Window.spin_resolution
        ray_length = Window.ray_length
        canvas_width, canvas_height = Window.canvas_shape

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
            midx = centre
            midy = canvas_height/2
            x1 = midx + direction * ray_length * math.sin((direction * speed * angle + line_id) * math.pi/spin_resolution)
            x2 = midx - direction * ray_length * math.sin((direction * speed * angle + line_id) * math.pi/spin_resolution)
            y1 = midy - direction * ray_length * math.cos((direction * speed * angle + line_id) * math.pi/spin_resolution)
            y2 = midy + direction * ray_length * math.cos((direction * speed * angle + line_id) * math.pi/spin_resolution)
            self.canvas.coords(line, x1, y1, x2, y2)

    def make_bunch(self, ray_length, centre, num_rays):
        canvas_height = Window.canvas_shape[0]
        bunch = list()
        self.angle = 0
        x1, y1, x2, y2 = centre, canvas_height - ray_length, centre, canvas_height + ray_length

        for _ in range(num_rays):
            self.angle += 1
            self.angle = self.angle if self.angle < 60 else 0

            x1 = centre + ray_length * math.sin(self.angle * math.pi/num_rays)
            x2 = centre - ray_length * math.sin(self.angle * math.pi/num_rays)
            y1 = canvas_height/2 - ray_length * math.cos(self.angle * math.pi/num_rays)
            y2 = canvas_height/2 + ray_length * math.cos(self.angle * math.pi/num_rays)
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

        self.canvas = Canvas(self.root, bg="black", width=canvas_width, height=canvas_height)

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

        move_it_button = Button(self.root, text="Move it", command=self.make_it_move)
        # move_it_button.pack()

        spin_it_button = Button(self.root, text="Spin it", command=self.make_it_spin)
        spin_it_button.pack()

        stop_it_button = Button(self.root, text="Stop it", command=self.make_it_stop)
        stop_it_button.pack()
        del_shape_button = Button(self.root, text="Restart", 
                                command= lambda: (self.__setattr__("move", False),
                                self.__setattr__("spin", False),
                                self.prep_moire()))
        del_shape_button.pack()

        self.prep_moire()

        self.root.mainloop()

test = Window()