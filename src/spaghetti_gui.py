import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import numpy as np
from datetime import datetime
import cv2



def mandelbrot_set(x_dim, y_dim):
    pass

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

def binary_tree(x_dim, y_dim):
    pass

def koch_snowflake(x_dim, y_dim):
    pass

class MainWindow(qtw.QWidget):

    def __init__(self):
        super().__init__()

        DEFAULT_FONT_SIZE = 12
        self.height=200
        self.width=200
        self.default_fractal_pattern = 'binary_tree'
        self.default_image_path = f'{self.default_fractal_pattern}_{datetime.now().strftime("%d%m%Y")}.png'

        self.setWindowTitle('Fractal Maker')

        fractal_form = qtw.QFormLayout()
        self.setLayout(fractal_form)
        
        # self.setLayout(qtw.QVBoxLayout())
        self.fractal_picker = qtw.QComboBox(self)
        self.fractal_picker.setObjectName('Fractals')
        self.fractal_picker.setToolTip("curvehoose a fractal pattern")
        self.fractal_picker.setFont(qtg.QFont('Helvetica', DEFAULT_FONT_SIZE))
        self.fractal_picker.addItem('Binary Tree', 'binary_tree')
        self.fractal_picker.addItem('Barnesly Fern', 'barnesly')
        self.fractal_picker.addItem("Koch Snowflake", 'koch')
        self.fractal_picker.addItem('Julia Set', 'julia')
        self.fractal_picker.addItem('Mandelbrot Set', 'mandelbrot') 


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

        self.start_button = qtw.QPushButton('START',clicked = self.create_fractal_image)

        self.save_button = qtw.QPushButton('SAVE',clicked = self.save_fractal_image)

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
        self.default_image_path = f'{""}{self.fractal_picker.currentData()}_{datetime.now().strftime("%d%m%Y")}.png'
        self.entry_box.setText(self.default_image_path)
        self.main_label.setText(f'Filepath: {self.entry_box.text()}\nPattern: {new_pattern}')

    def create_fractal_image(self):
        width = self.width_picker.value()
        height = self.height_picker.value()
        pattern_matcher = {
            'binary_tree': binary_tree,
            'mandelbrot': mandelbrot_set,
            'barnesly': barnesly_fern,
            'julia': julia_set,
            'koch': koch_snowflake
        }
        return pattern_matcher[self.default_fractal_pattern](width, height)
        
    def save_fractal_image(self, fractal_image, path=None):
        self.main_label.setText(f'Filepath: {self.entry_box.text()}\nPattern: {self.fractal_picker.currentText()}')
        if not path:
            path = self.default_image_path
        try:
            cv2.imwrite(path, fractal_image)
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