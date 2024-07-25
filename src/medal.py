import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from PIL import Image


class Medal:

    def __init__(self, rank, bg_color, ft_color):
        self.rank = rank
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
            [0, np.sqrt(3) / 2 * dist - 1],
            [-side_length / 2 + dist, height - 1],
            [side_length / 2 - dist, height - 1]
        ])
        return vertices

    def create_img(self):

        # 그림의 크기 설정
        fig, ax = plt.subplots(figsize=(10, 10))

        # 배경 색상 설정
        ax.set_facecolor('white')
        r = 0.7

        # 정삼각형의 한 변의 길이 계산
        side_length = 2 * 3 * 20  # 메달의 지름(6)의 1.5배

        self.add_circle(ax, (0, -1), 4 * r, 'black')
        # 삼각형을 추가하는 함수 호출
        distances = [-1.5, 0, 1.5, 2.5, 4]
        colors = ['black', self.bg_color, self.ft_color, self.bg_color, 'black']

        for dist, color in zip(distances, colors):
            vertices = self.calculate_triangle_vertices(side_length, dist)
            self.add_triangle(ax, vertices, color)

        if self.rank == 1:
            self.add_circle(ax, (0, -1), 3 * r, '#E7AB0B')  # 밝은 금색
            self.add_circle(ax, (0, -1), 2 * r, '#C1840B')  # 어두운 금색
            # 숫자 1 추가 (밝은 금색)
            ax.text(0, -1.2, '1', fontsize=160, color='#E7AB0B', ha='center', va='center', fontweight='bold')
        elif self.rank == 2:
            self.add_circle(ax, (0, -1), 3 * r, '#BABABA')  # 밝은 은색
            self.add_circle(ax, (0, -1), 2 * r, '#707070')  # 어두운 은색
            # 숫자 2 추가 (밝은 은색)
            ax.text(0, -1.2, '2', fontsize=160, color='#BABABA', ha='center', va='center', fontweight='bold')
        else:
            self.add_circle(ax, (0, -1), 3 * r, '#E0814B')  # 밝은 동색
            self.add_circle(ax, (0, -1), 2 * r, '#B95019')  # 어두운 동색
            # 숫자 3 추가 (밝은 동색)
            ax.text(0, -1.2, '3', fontsize=160, color='#E0814B', ha='center', va='center', fontweight='bold')

        # 좌표 및 축 설정
        ax.set_xlim(-4.5, 4.5)
        ax.set_ylim(-4.5, 4.5)
        ax.set_aspect('equal')
        ax.axis('off')

        # 그림 저장 (배경 투명하게 설정)
        plt.savefig(f'../asset/img/medal{self.rank}{self.bg_color[1:]}{self.ft_color[1:]}.png', bbox_inches='tight', transparent=True)

