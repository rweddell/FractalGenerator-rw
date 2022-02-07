import sys
from gui.maker_window import MakerWindow
from gui.maker_controller import MakerController
from PyQt5.QtWidgets import QApplication

ERROR_MSG = "ERROR"

def evaluateExpression(expression):
    """Evaluate an expression."""
    try:
        result = str(eval(expression, {}, {}))
    except Exception:
        result = ERROR_MSG

    return result

def main():
    """Main function."""
    # Create an instance of `QApplication`
    pycalc = QApplication(sys.argv)
    # Show the calculator's GUI
    view = MakerWindow()
    view.show()
    # Create instances of the model and the controller
    model = evaluateExpression
    MakerController(model=model, view=view, error_msg=ERROR_MSG)
    # Execute calculator's main loop
    sys.exit(pycalc.exec_())


if __name__ == "__main__":
    main()