import heapq
import tkinter as tk
from tkinter import messagebox

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cost = 0  # cost from start node to current node
        self.heuristic = 0  # heuristic cost from current node to destination node
        self.totalCost = 0  # total cost (cost + heuristic)
        self.parent = None

    def __lt__(self, other): # compares two nodes based on their total costs to determine the queue retrieve priority
        return self.totalCost < other.totalCost


def calculate_heuristic(node, dest):
    # Manhattan distance heuristic
    return abs(node.x - dest.x) + abs(node.y - dest.y)


def get_neighbours(node, grid):
    neighbours = []
    deltas = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # right, left, down, up

    for dx, dy in deltas:
        new_x = node.x + dx
        new_y = node.y + dy

        if 0 <= new_x < len(grid) and 0 <= new_y < len(grid[0]) and not grid[new_x][new_y]:
            neighbours.append(Node(new_x, new_y))

    return neighbours


def reconstruct_path(node):
    path = []
    current = node

    while current is not None:
        path.append((current.x, current.y))
        current = current.parent

    return path[::-1]


def astar_search(grid, start, dest):
    open_list = []
    closed_set = set()

    start_node = Node(*start)
    dest_node = Node(*dest)

    heapq.heappush(open_list, start_node)

    while open_list:
        current_node = heapq.heappop(open_list)

        if (current_node.x, current_node.y) == (dest_node.x, dest_node.y):
            return reconstruct_path(current_node)

        closed_set.add((current_node.x, current_node.y))

        neighbours = get_neighbours(current_node, grid)
        for neighbour in neighbours:
            if (neighbour.x, neighbour.y) in closed_set:
                continue

            neighbour.cost = current_node.cost + 1
            neighbour.heuristic = calculate_heuristic(neighbour, dest_node)
            neighbour.totalCost = neighbour.cost + neighbour.heuristic
            neighbour.parent = current_node

            heapq.heappush(open_list, neighbour)

    return None


class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[0] * height for _ in range(width)]
        self.start = None
        self.dest = None

        self.root = tk.Tk()
        self.root.title("Labirinto A*")
        self.canvas = tk.Canvas(self.root, width=self.width * 30, height=self.height * 30, bg="white")
        self.canvas.bind("<Button-1>", self.on_click)
        self.find_button = tk.Button(self.root, text="Encontrar caminho", command=self.calculate_path)
        self.clear_button = tk.Button(self.root, text="Limpar caminho", command=self.clear_path)

        self.canvas.pack()
        self.find_button.pack(side="left")
        self.clear_button.pack(side="right")
        
        for x in range(self.width):
            for y in range(self.height):
                self.draw_node(x, y, "white")
        
        self.show_message("Selecione o nó inicial")

        self.root.mainloop()

    def on_click(self, event):
        x = event.x // 30
        y = event.y // 30

        if not self.start:
            self.start = (x, y)
            self.draw_node(x, y, "green")
            self.show_message("Selecione o nó de destino")
        elif not self.dest:        
            self.dest = (x, y)
            self.draw_node(x, y, "red")
            self.show_message("Selecione os obstáculos")
        else:
            self.grid[x][y] = 1
            self.draw_node(x, y, "black")

    def clear_path(self):
        self.canvas.delete("all")
        self.grid = [[0] * self.height for _ in range(self.width)]
        self.start = None
        self.dest = None

        for x in range(self.width):
            for y in range(self.height):
                self.draw_node(x, y, "white")

        self.show_message("Selecione o nó inicial")

    @staticmethod
    def show_message(message):
        messagebox.showinfo("Message", message)

    def draw_node(self, x, y, color):
        outline = "black"
        self.canvas.create_rectangle(x * 30, y * 30, (x + 1) * 30, (y + 1) * 30, fill=color, outline=outline)

    def calculate_path(self):
        if self.start and self.dest: 

            path = astar_search(self.grid, self.start, self.dest)

            if path:
                for x, y in path[1:-1]:
                    self.draw_node(x, y, "blue")
            else:
                self.show_message("Sem caminhos possíveis")

# Starts the Maze
app = Maze(10, 10) # height and width in quantity of squares
