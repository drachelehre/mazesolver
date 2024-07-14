from tkinter import Tk, BOTH, Canvas


class Window:
    def __init__(self, width, height):
        self.root = Tk()
        self.root.title("Maze Solver")
        self.main = Canvas(self.root, width=width, height=height)
        self.main.pack(fill=BOTH, expand=1)
        self.running = False
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def draw_line(self, line, fill_color):
        line.draw(self.main, fill_color)

    def redraw(self):
        self.root.update_idletasks()
        self.root.update()

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()

    def close(self):
        self.running = False


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def draw(self, canvas, fill_color):
        canvas.create_line(self.point1.x, self.point1.y, self.point2.x, self.point2.y, fill=fill_color, width=2)


class Cell:
    def __init__(self, x1, y1, x2, y2, win, has_left_wall= True, has_right_wall= True, has_top_wall= True, has_bottom_wall= True,
                 ):
        self.has_left_wall = has_left_wall
        self.has_right_wall = has_right_wall
        self.has_top_wall = has_top_wall
        self.has_bottom_wall = has_bottom_wall
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        self._win = win

    def draw(self, x1, y1, x2, y2):
        top_left = Point(x1, y1)
        bottom_right = Point(x2, y2)
        bottom_left = Point(x1, y2)
        top_right = Point(x2, y1)
        if self.has_top_wall:
            top_line = Line(top_left, top_right)
            self._win.draw_line(top_line, "black")
        if self.has_right_wall:
            right_line = Line(top_right, bottom_right)
            self._win.draw_line(right_line, "black")
        if self.has_left_wall:
            left_line = Line(top_left, top_right)
            self._win.draw_line(top_line, "black")





def main():
    win = Window(800, 600)
    point1 = Point(150, 250)
    point2 = Point(340, 500)
    line = Line(point1, point2)
    win.draw_line(line, "blue")
    point3 = Point(50, 400)
    point4 = Point(560, 10)
    line2 = Line(point3, point4)
    win.draw_line(line2, "red")
    win.wait_for_close()


if __name__ == '__main__':
    main()
