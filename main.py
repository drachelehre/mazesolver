import random
from tkinter import Tk, BOTH, Canvas
import time


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
    def __init__(self, x1, y1, x2, y2, win=None, has_left_wall=True, has_right_wall=True, has_top_wall=True,
                 has_bottom_wall=True, visited=False):
        self.has_left_wall = has_left_wall
        self.has_right_wall = has_right_wall
        self.has_top_wall = has_top_wall
        self.has_bottom_wall = has_bottom_wall
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2
        self.__win = win
        self.visited = visited

    def draw(self):
        if self.__win is None:
            return

        top_left = Point(self.__x1, self.__y1)
        bottom_right = Point(self.__x2, self.__y2)
        bottom_left = Point(self.__x1, self.__y2)
        top_right = Point(self.__x2, self.__y1)
        if self.has_top_wall:
            top_line = Line(top_left, top_right)
            top_line.draw(self.__win.main, "black")
        else:
            top_line = Line(top_left, top_right)
            top_line.draw(self.__win.main, "white")
        if self.has_right_wall:
            right_line = Line(top_right, bottom_right)
            right_line.draw(self.__win.main, "black")
        else:
            right_line = Line(top_right, bottom_right)
            right_line.draw(self.__win.main, "white")
        if self.has_left_wall:
            left_line = Line(top_left, bottom_left)
            left_line.draw(self.__win.main, "black")
        else:
            left_line = Line(top_left, bottom_left)
            left_line.draw(self.__win.main, "white")
        if self.has_bottom_wall:
            bottom_line = Line(bottom_left, bottom_right)
            bottom_line.draw(self.__win.main, "black")
        else:
            bottom_line = Line(bottom_left, bottom_right)
            bottom_line.draw(self.__win.main, "white")

    def draw_move(self, to_cell, undo=False):
        from_point = Point((self.__x1+self.__x2)/2, (self.__y1+self.__y2)/2)
        to_point = Point((to_cell.__x1+to_cell.__x2)/2, (to_cell.__y1+to_cell.__y2)/2)
        path_line = Line(from_point, to_point)
        path_line.draw(self.__win.main, "red")
        if undo:
            path_line.draw(self.__win.main, "gray")


class Maze:
    def __init__(
            self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self._create_cells()
        self.seed = random.seed(seed) if seed is not None else None

    def _create_cells(self):
        self._cells = []
        # Creating cells and drawing them
        for i in range(self.num_cols):
            row_cells = []
            for j in range(self.num_rows):
                top_left_x = self.x1 + i * self.cell_size_x
                top_left_y = self.y1 + j * self.cell_size_y
                cell = Cell(top_left_x, top_left_y, top_left_x + self.cell_size_x, top_left_y + self.cell_size_y,
                            win=self.win)
                row_cells.append(cell)
            self._cells.append(row_cells)

        # Draw all cells
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._draw_cell(i, j)

        # Break entrance and exit walls
        self._break_entrance_and_exit()

        # Start breaking walls from the top-left corner
        self._break_walls_r(0, 0)

        self._reset_cells_visited()

    def _break_entrance_and_exit(self):
        entrance_cell = self._cells[0][0]
        exit_cell = self._cells[-1][-1]
        entrance_cell.has_top_wall = False
        self._draw_cell(0, 0)
        exit_cell.has_bottom_wall = False
        x = len(self._cells) - 1
        y = len(self._cells[0]) - 1
        self._draw_cell(x, y)

    def break_walls(self, current_cell, next_cell, direction):
        if direction == "up":
            current_cell.has_top_wall = False
            next_cell.has_bottom_wall = False
        elif direction == "down":
            current_cell.has_bottom_wall = False
            next_cell.has_top_wall = False
        elif direction == "right":
            current_cell.has_right_wall = False
            next_cell.has_left_wall = False
        elif direction == "left":
            current_cell.has_left_wall = False
            next_cell.has_right_wall = False

    def _break_walls_r(self, i, j):
        current_cell = self._cells[i][j]
        current_cell.visited = True
        while True:
            to_visit = []
            if j > 0:  # up
                cell_up = self._cells[i][j - 1]
                if not cell_up.visited:
                    to_visit.append((i, j - 1))
            if j < len(self._cells[0]) - 1:  # down
                cell_down = self._cells[i][j + 1]
                if not cell_down.visited:
                    to_visit.append((i, j + 1))
            if i < len(self._cells) - 1:  # right
                cell_right = self._cells[i + 1][j]
                if not cell_right.visited:
                    to_visit.append((i + 1, j))
            if i > 0:  # left
                cell_left = self._cells[i - 1][j]
                if not cell_left.visited:
                    to_visit.append((i - 1, j))

            if not to_visit:
                current_cell.draw()
                return

            dir_index = random.randint(0, len(to_visit) - 1)
            next_i, next_j = to_visit[dir_index]

            direction = ""
            if next_i > i:
                direction = "right"
            elif next_i < i:
                direction = "left"
            elif next_j > j:
                direction = "down"
            elif next_j < j:
                direction = "up"

            next_cell = self._cells[next_i][next_j]
            self.break_walls(current_cell, next_cell, direction)

            # Redraw current and next cell after breaking walls
            current_cell.draw()
            next_cell.draw()

            self._break_walls_r(next_i, next_j)

    def _reset_cells_visited(self):
        for i in range(len(self._cells)):
            for j in range(len(self._cells[0])):
                self._cells[i][j].visited = False

    def solve(self):
        self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._animate()
        current_cell = self._cells[i][j]
        current_cell.visited = True

        # Check if the current cell is the end cell
        if i == (len(self._cells) - 1) and j == (len(self._cells[0]) - 1):
            return True

        # Prepare list of next directions to visit
        to_visit = []
        if j > 0:  # up
            cell_up = self._cells[i][j - 1]
            if not cell_up.visited:
                to_visit.append((i, j - 1))
        if j < len(self._cells[0]) - 1:  # down
            cell_down = self._cells[i][j + 1]
            if not cell_down.visited:
                to_visit.append((i, j + 1))
        if i < len(self._cells) - 1:  # right
            cell_right = self._cells[i + 1][j]
            if not cell_right.visited:
                to_visit.append((i + 1, j))
        if i > 0:  # left
            cell_left = self._cells[i - 1][j]
            if not cell_left.visited:
                to_visit.append((i - 1, j))

        # Traverse through potential moves
        for direction in to_visit:
            next_i, next_j = direction
            next_cell = self._cells[next_i][next_j]

            # Check for walls blocking the path
            if ((i < next_i and current_cell.has_right_wall) or
                    (i > next_i and current_cell.has_left_wall) or
                    (j < next_j and current_cell.has_bottom_wall) or
                    (j > next_j and current_cell.has_top_wall)):
                continue

            # Draw the move between current_cell and next_cell
            current_cell.draw_move(next_cell)

            # Perform the recursive call
            if self._solve_r(next_i, next_j):
                return True

            # Undo the move if the path didn't work out
            current_cell.draw_move(next_cell, undo=True)

        return False


    def _draw_cell(self, i, j):
        cell = self._cells[i][j]  # Ensure accessing the valid range
        cell.draw()
        self._animate()

    def _animate(self):
        if self.win is None:
            return
        self.win.redraw()
        time.sleep(0.05)


def main():
    win = Window(800, 600)
    maze = Maze(num_cols=10, num_rows=10, cell_size_x=20, cell_size_y=20, x1=10, y1=10, win=win, seed=0)
    maze.solve()
    win.wait_for_close()


if __name__ == '__main__':
    main()
