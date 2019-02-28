import drawSvg as draw
import math
import random
import os
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg
import glob
from PyPDF2 import PdfFileMerger


class Renderer:

    def __init__(self):
        a4_size = [4961, 7016]
        scaling = 10
        a4_rescaled = [size / scaling for size in a4_size]
        self.stroke_width = 5
        self.drawing = draw.Drawing(a4_rescaled[0], a4_rescaled[1], origin='center')
        self.points = {"circle": {}, "grid": {}}

    def createLayout(self):

        # Draw circle
        circle_diameter = 200
        center = [0, 0]
        self.drawing.append(draw.Circle(center[0], center[1], circle_diameter, fill='none', stroke='black',
                                        stroke_width=self.stroke_width))
        self.points["circle"]["circle"] = {"x": 0, "y": 0}

        # Draw circle points
        point_number = 1
        for degree in range(0, 360, 30):
            x = circle_diameter * math.cos(degree * math.pi / 180)
            y = circle_diameter * math.sin(degree * math.pi / 180)
            self.drawing.append(draw.Circle(x, y, 10, fill='black'))
            self.points["circle"][point_number] = {"x": x, "y": y}
            point_number += 1

        # Draw grid
        indent = 35
        upper_left = [(circle_diameter - indent) * math.cos(135 * math.pi / 180),
                      (circle_diameter - indent) * math.sin(135 * math.pi / 180)]
        upper_right = [(circle_diameter - indent) * math.cos(45 * math.pi / 180),
                       (circle_diameter - indent) * math.sin(45 * math.pi / 180)]
        down_left = [(circle_diameter - indent) * math.cos(225 * math.pi / 180),
                     (circle_diameter - indent) * math.sin(225 * math.pi / 180)]
        down_right = [(circle_diameter - indent) * math.cos(315 * math.pi / 180),
                      (circle_diameter - indent) * math.sin(315 * math.pi / 180)]
        vertical_step = (upper_left[1] - down_left[1]) / 4
        horizontal_step = (upper_right[0] - upper_left[0]) / 4

        # Draw horizontal lines
        for i in range(0, 5):
            difference = i * vertical_step
            self.drawing.append(draw.Line(upper_left[0], upper_left[1] - difference,
                                          upper_right[0], upper_right[1] - difference,
                                          fill='black',
                                          stroke='black',
                                          stroke_width=self.stroke_width))

        # Draw vertical lines
        for i in range(0, 5):
            difference = i * horizontal_step
            self.drawing.append(draw.Line(upper_right[0] - difference, upper_right[1],
                                          down_right[0] - difference, down_right[1],
                                          fill='black',
                                          stroke='black',
                                          stroke_width=self.stroke_width))
        # Draw grid points
        point_number = 0
        for vertical_move in range(0, 5):
            y = down_left[1] + vertical_move * vertical_step
            for horizontal_move in range(0, 5):
                point_number += 1
                x = down_left[0] + horizontal_move * horizontal_step
                self.drawing.append(draw.Circle(x, y, 10, fill='black'))
                self.points["grid"][point_number] = {"x": x, "y": y}

    def highlight_point(self, x, y):
        highlight_diameter = 15
        highlight_color = "red"
        self.drawing.append(draw.Circle(x, y, highlight_diameter, fill=highlight_color))

    def highlight_selected_points(self, number_of_points, type):

        # check max number of points
        if (type == "circle") and (number_of_points > 12):
            raise Exception(
                "Nubmer of points to highlight (" + number_of_points + ") is higher than number of points in the cicrle (12).")

        if (type == "grid") and (number_of_points > 25):
            raise Exception(
                "Nubmer of points to highlight (" + number_of_points + ") is higher than number of points in the grid (25).")

        if type == "circle":
            point_list = list(range(1, 13))
        elif type == "grid":
            point_list = list(range(1, 26))
        else:
            raise Exception("Unknown type: ", type)

        # Select random points
        random_points = random.sample(point_list, number_of_points)

        for point in random_points:
            x = self.points[type][point]["x"]
            y = self.points[type][point]["y"]
            self.highlight_point(x=x, y=y)

    def rescale(self, scaling_factor):
        self.drawing.setPixelScale(scaling_factor)

    def save_svg(self, filename):
        self.drawing.saveSvg(filename)
        print('File ' + filename + " saved.")

    def svg_to_pdf(self, svg_file):
        pdf_file = svg_file.split('.')[0] + ".pdf"
        drawing = svg2rlg(svg_file)
        renderPDF.drawToFile(drawing, pdf_file)
        print('PDF File ' + pdf_file + " saved.")

    def pdf_merger(self, output_path, input_paths):

        pdf_mrg = PdfFileMerger()

        for path in input_paths:
            pdf_mrg.append(path)

        with open(output_path, 'wb') as fileobj:
            pdf_mrg.write(fileobj)


    def merge_pdf(self, directory, output_file):
        paths = glob.glob(directory + '*.pdf')
        paths.sort()
        self.pdf_merger(output_file, paths)
        for path in paths:
            try:
                os.remove(path)
            except Exception as e:
                print("Error while deleting file ", e)

    def __del__(self):
        print("Deleting instance")