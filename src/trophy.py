import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

class Trophy:

    def __init__(self, bg_color, ft_color):
        self.bg_color = bg_color
        self.ft_color = ft_color

    def add_circle(self, ax, center, radius, color):
        circle = patches.Circle(center, radius, color=color, fill=True)
        ax.add_patch(circle)

    def add_triangle(self, ax, vertices, color):
        triangle = patches.Polygon(vertices, closed=True, color=color)
        ax.add_patch(triangle)

    def calculate_triangle_vertices(self, side_length, dist):
        height = np.sqrt(3) / 2 * side_length
        vertices = np.array([
            [0, np.sqrt(3) / 2 * dist],
            [-side_length / 2 + dist, height],
            [side_length / 2 - dist, height]
        ])
        return vertices

    def create_img(self):

        # 그림의 크기 설정
        fig, ax = plt.subplots(figsize=(10, 10))

        # 배경 색상 설정
        ax.set_facecolor('white')

        self.add_circle(ax, (2, 2.5), 2, 'black')
        self.add_circle(ax, (-2, 2.5), 2, 'black')

        vertices = np.array([
                [-2, 1.5],
                [2, 1.5],
                [2, 5],
                [-2, 5]
            ])
        self.add_triangle(ax, vertices, 'black')
        vertices = np.array([
                [1, -2],
                [1, 2],
                [-1, 2],
                [-1, -2]
            ])
        self.add_triangle(ax, vertices, 'black')
        self.add_circle(ax, (-1, -2), 1.5, 'black')
        self.add_circle(ax, (1, -2), 1.5, 'black')
        self.add_circle(ax, (0.5, 1.5), 2, 'black')
        self.add_circle(ax, (-0.5, 1.5), 2, 'black')
        vertices = np.array([
                [3, -1.5],
                [3, -3.5],
                [-3, -3.5],
                [-3, -1.5]
            ])
        self.add_triangle(ax, vertices, 'black')

        vertices = np.array([
                [0.5, -2],
                [0.5, 2],
                [-0.5, 2],
                [-0.5, -2]
            ])
        self.add_triangle(ax, vertices, 'gold')

        vertices = np.array([
                [1, -2],
                [1, -1],
                [-1, -1],
                [-1, -2]
            ])
        self.add_triangle(ax, vertices, 'gold')

        self.add_circle(ax, (-1, -2), 1, 'gold')
        self.add_circle(ax, (1, -2), 1, 'gold')

        self.add_circle(ax, (0.5, 1.5), 1.5, 'gold')
        self.add_circle(ax, (-0.5, 1.5), 1.5, 'gold')

        self.add_circle(ax, (2, 2.5), 1.5, 'gold')
        self.add_circle(ax, (-2, 2.5), 1.5, 'gold')
        self.add_circle(ax, (2, 2.5), 1, 'black')
        self.add_circle(ax, (-2, 2.5), 1, 'black')
        vertices = np.array([
                [-2, 1.5],
                [2, 1.5],
                [2, 4],
                [-2, 4]
            ])
        self.add_triangle(ax, vertices, 'gold')


        vertices = np.array([
                [2.5, -2],
                [2.5, -3],
                [-2.5, -3],
                [-2.5, -2]
            ])
        self.add_triangle(ax, vertices, 'brown')
        wedge = patches.Wedge(center=(-0.5, 1.5), r=1.5, theta1=180, theta2=270, color=self.bg_color)
        ax.add_patch(wedge)
        vertices = np.array([
                [-0.5, 0],
                [2.05, 1.5],
                [2.05, 3.5],
                [-2, 1.5]
            ])
        self.add_triangle(ax, vertices, self.bg_color)

        # 좌표 및 축 설정
        ax.set_xlim(-4.5, 4.5)
        ax.set_ylim(-4.5, 4.5)
        ax.set_aspect('equal')
        ax.axis('off')

        # 그림 저장 (배경 투명하게 설정)
        plt.savefig(f'../asset/img/trophy{self.bg_color[1:]}{self.ft_color[1:]}.png', bbox_inches='tight', transparent=True)


trophy = Trophy("#0000FF", "#FFFFFF")
trophy.create_img()