import drawSvg as draw
import math

class Renderer:

    def __init__(self):
        a4_size = [4961, 7016]
        scaling = 10
        a4_rescaled = [size / scaling for size in a4_size]
        self.stroke_width = 5
        self.drawing = draw.Drawing(a4_rescaled[0], a4_rescaled[1], origin='center')

    def createLayout(self):

        # Draw circle
        circle_diameter = 200
        self.drawing.append(draw.Circle(0,0,circle_diameter, fill='none', stroke = 'black', stroke_width = self.stroke_width))

        # Draw circle points
        for degree in range(0,360,30):
            x = circle_diameter * math.cos(degree * math.pi / 180)
            y = circle_diameter * math.sin(degree * math.pi / 180)
            self.drawing.append(draw.Circle(x,y,10, fill='black'))

        # Draw grid

        indent = 30
        upper_left = [(circle_diameter - indent) * math.cos(135 * math.pi / 180),
                       circle_diameter * math.sin(135 * math.pi / 180)]
        upper_right = [(circle_diameter - indent) * math.cos(45 * math.pi / 180),
                       circle_diameter * math.sin(45 * math.pi / 180)]
        down_left = [(circle_diameter - indent) * math.cos(225 * math.pi / 180),
                      circle_diameter * math.sin(225 * math.pi / 180)]
        down_right = [(circle_diameter - indent) * math.cos(315 * math.pi / 180),
                      circle_diameter * math.sin(315 * math.pi / 180)]
        vertical_step = (upper_left[1] - down_left[1]) / 4
        horizontal_step = (upper_right[0] - upper_left[0]) / 4

        self.drawing.append(draw.Line(upper_left[0], upper_left[1],
                                      down_left[0], down_right[1],
                                      fill= 'black',
                                      stroke = 'black',
                                      stroke_width = self.stroke_width))
        # Draw horizontal lines
        for i in range(0,5):
             difference = i * vertical_step

             self.drawing.append(draw.Line(upper_left[0] , upper_left[1] - difference,
                                       upper_right[0] , upper_right[1] - difference,
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

    def rescale(self,scaling_factor):
        self.drawing.setPixelScale(scaling_factor)

    def save_svg(self, filename):
        self.drawing.saveSvg(filename)
        print('File ' + filename + " saved.")
