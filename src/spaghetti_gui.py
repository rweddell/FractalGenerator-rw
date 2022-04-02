import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import numpy as np
from datetime import datetime
import cv2
import os


def mandelbrot_set(x_dim, y_dim):

    max_iter = 80
    re_start = -2
    re_end = 2
    im_start = -1
    im_end = 1

    image = np.zeros((x_dim, y_dim))

    def mandelbrot_fractal(comp=90, max_iter=80):
        z = 0
        n = 0
        while abs(z) <= 2 and n < max_iter:
            z = z*z + comp
            n += 1
        return n
    
    for x in range(x_dim):
        for y in range(y_dim):
            c = complex(re_start+(x/x_dim)*(re_end - re_start),
                im_start+(y/y_dim)*(im_end-im_start))
            m = mandelbrot_fractal(c, max_iter)
            image[x][y] = 255 - int(m*255/max_iter)

    return image


def julia_set(x_dim, y_dim):
    scale = int(x_dim*0.6)
    x_space = np.linspace(-x_dim/scale, y_dim/scale, num=x_dim).reshape((1,x_dim))
    y_space = np.linspace(-y_dim/scale, y_dim/scale, num=y_dim).reshape((y_dim,1))
    z_space = np.tile(x_space,(y_dim,1)) + 1j * np.tile(y_space, (1,x_dim))
    curve = np.full((y_dim, x_dim), -0.4 + 0.6j)
    X = np.full((y_dim, x_dim), True, dtype=bool)
    image = np.zeros((y_dim, x_dim))
    for pixel_val in range(256):
        z_space[X] = z_space[X] * z_space[X] + curve[X]
        X[np.abs(z_space) > 2] = False
        image[X] = pixel_val
    return image

def barnesly_fern(x_dim, y_dim):
    pass

def binary_tree(x_dim, y_dim, theta=0.05):
    # start point
    # angle is 90
    # draw line for length 
    # recurse?
    trunk_len = y_dim//2
    delta_x = trunk_len * np.cos()
    delta_y = trunk_len * np.cos()
    pass

def koch_snowflake(x_dim, y_dim):
    pass

class MainWindow(qtw.QWidget):

    def __init__(self):
        super().__init__()

        DEFAULT_FONT_SIZE = 12
        self.height=200
        self.width=200
        self.fractal_image = None
        self.display = qtg.QPixmap()
        self.default_fractal_pattern = 'binary_tree'
        self.default_image_path = f'{self.default_fractal_pattern}_{datetime.now().strftime("%d%m%Y")}.png'

        self.setWindowTitle('Fractal Maker')

        fractal_form = qtw.QFormLayout()
        self.setLayout(fractal_form)

        
        # self.setLayout(qtw.QVBoxLayout())
        self.fractal_picker = qtw.QComboBox(self)
        self.fractal_picker.setObjectName('Fractals')
        self.fractal_picker.setToolTip("Choose a fractal pattern")
        self.fractal_picker.setFont(qtg.QFont('Helvetica', DEFAULT_FONT_SIZE))
        
        fractal_ref = {
            'Binary Tree': 'binary_tree',
            'Barnesly Fern': 'barnesly',
            "Koch Snowflake": 'koch',
            'Julia Set': 'julia',
            'Mandelbrot Set': 'mandelbrot'
        }
        for fractal in fractal_ref:
            self.fractal_picker.addItem(fractal, fractal_ref[fractal])

        self.fractal_picker.currentTextChanged.connect(self.update_fractal_pattern)

        self.main_label = qtw.QLabel('Select fractal parameters')
        self.main_label.setFont(qtg.QFont('Helvetica', 18))

        self.entry_box = qtw.QLineEdit()
        self.entry_box.setObjectName("Information")
        self.entry_box.setFont(qtg.QFont('Helvetica', 12))
        self.entry_box.setText(self.default_image_path)

        self.width_picker = qtw.QSpinBox(
            value=1920,
            minimum=16,
            maximum=1920,
            singleStep=1)
        self.width_picker.setSpecialValueText('Image width (0 - 1920)')
        self.width_picker.setToolTip('Select an image width from 16 - 1920')
        self.width_picker.setObjectName('image_width')
        self.width_picker.setFont(qtg.QFont('Helvetica', DEFAULT_FONT_SIZE))
        self.height_picker = qtw.QSpinBox(
            value=1080,
            minimum=16,
            maximum=1080,
            singleStep=1)
        self.height_picker.setObjectName('image_height')
        self.height_picker.setToolTip('Select an image height from 16 to 1080')
        self.height_picker.setSpecialValueText('Image height (0 - 1080)')
        self.height_picker.setFont(qtg.QFont('Helvetica', DEFAULT_FONT_SIZE))

        self.start_button = qtw.QPushButton('START', clicked=self.create_fractal_image)

        self.save_button = qtw.QPushButton('SAVE', clicked=self.save_fractal_image)

        # Doesn't seem to work unless rows and widgets are both added
        self.layout().addWidget(self.main_label)
        self.layout().addWidget(self.entry_box)
        self.layout().addWidget(self.fractal_picker)
        self.layout().addWidget(self.width_picker)
        self.layout().addWidget(self.height_picker)

        fractal_form.addRow('Filepath:', self.entry_box)
        fractal_form.addRow('Fractal Patterns:', self.fractal_picker)
        fractal_form.addRow('Image Width:', self.width_picker)
        fractal_form.addRow('Image Height:', self.height_picker)
        self.layout().addWidget(self.start_button)
        self.layout().addWidget(self.save_button)

        self.show()

    def update_fractal_pattern(self, new_pattern):
        self.default_fractal_pattern = self.fractal_picker.currentData()
        self.default_image_path = os.path.join('images', f'{self.fractal_picker.currentData()}_{datetime.now().strftime("%d%m%Y")}.png')
        self.entry_box.setText(self.default_image_path)
        self.main_label.setText(f'Filepath: {self.entry_box.text()}\nPattern: {new_pattern}')

    def create_fractal_image(self):
        width = self.width_picker.value()
        height = self.height_picker.value()
        # TODO: if these are moved into modules, keep in mind to import them directly or change this line
        pattern_matcher = {
            'binary_tree': binary_tree,
            'mandelbrot': mandelbrot_set,
            'barnesly': barnesly_fern,
            'julia': julia_set,
            'koch': koch_snowflake
        }
        self.fractal_image = pattern_matcher[self.default_fractal_pattern](width, height)
        label = qtw.QLabel(self)
        pixmap = qtg.QPixmap(qtg.QImage(self.fractal_image, self.fractal_image.shape[0], self.fractal_image.shape[0]))
        label.setPixmap(pixmap)
        
    def save_fractal_image(self, path=None):
        self.main_label.setText(f'Filepath: {self.entry_box.text()}\nPattern: {self.fractal_picker.currentText()}')
        if not path:
            path = self.default_image_path
        try:
            cv2.imwrite(path, self.fractal_image)
            self.main_label.setText(f'Saving image at: {path}')
        except Exception as problem:
            error_string = f'There was a problem saving the image: \n{problem}'
            self.main_label.setText(error_string)


def main():
    app = qtw.QApplication([])
    mw = MainWindow()
    app.exec()


if __name__ == '__main__':
    main()