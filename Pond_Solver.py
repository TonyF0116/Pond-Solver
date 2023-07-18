import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QComboBox, QLabel, QInputDialog
from PyQt5.QtGui import QPixmap
from solver import solver


class Pond_Solver(QMainWindow):
    def __init__(self, manuel_input=[]):
        super().__init__()

        self.blocks = []
        self.blocks.append(['Empty'])
        self.label_list = []
        self.label_list.append(['Empty'])

        self.setWindowTitle("Pond_Solver")
        self.setGeometry(100, 100, 850, 1000)

        canvas = QPixmap("res/canvas.png")
        self.red = QPixmap("res/red.png")
        self.yellow_horizontal = QPixmap("res/yellow_horizontal.png")
        self.yellow_vertical = QPixmap("res/yellow_vertical.png")
        self.blue_horizontal = QPixmap("res/blue_horizontal.png")
        self.blue_vertical = QPixmap("res/blue_vertical.png")

        canvas_label = QLabel(self)
        canvas_label.setPixmap(canvas)
        canvas_label.setGeometry(5, 2, 750, 700)

        self.row_label = QLabel('Row index:', self)
        self.row_label.setGeometry(50, 700, 100, 50)
        self.row_idx = QLineEdit(self)
        self.row_idx.setGeometry(50, 750, 100, 50)

        self.col_label = QLabel('Column index:', self)
        self.col_label.setGeometry(250, 700, 120, 50)
        self.col_idx = QLineEdit(self)
        self.col_idx.setGeometry(250, 750, 100, 50)

        self.orientation_label = QLabel('Orientation index:', self)
        self.orientation_label.setGeometry(450, 700, 120, 50)
        self.orientation = QComboBox(self)
        self.orientation.addItem('Horizontal')
        self.orientation.addItem('Vertical')
        self.orientation.setGeometry(450, 750, 100, 50)

        self.color_label = QLabel('Color index:', self)
        self.color_label.setGeometry(650, 700, 120, 50)
        self.color = QComboBox(self)
        self.color.addItem('Red')
        self.color.addItem('Yellow')
        self.color.addItem('Blue')
        self.color.setGeometry(650, 750, 100, 50)

        self.add_block_button = QPushButton('Add block', self)
        self.add_block_button.setGeometry(50, 850, 100, 50)
        self.add_block_button.clicked.connect(self.add_block)

        self.remove_last_button = QPushButton('Remove last', self)
        self.remove_last_button.setGeometry(200, 850, 150, 50)
        self.remove_last_button.clicked.connect(self.remove_last)

        self.solve_button = QPushButton('Solve', self)
        self.solve_button.setGeometry(400, 850, 100, 50)
        self.solve_button.clicked.connect(self.solve)

        instruction = "Instructions:\n1. Make sure that the red block is added as the first block, otherwise there might be some undefined behavior.\n2. When adding block, enter the (smaller) coordinates of the left/up-most grid of the block.\n3. Press 'Solve' button to get the solution when finished adding blocks."
        self.instruction = QLabel(instruction, self)
        self.instruction.setGeometry(25, 900, 850, 100)

        if manuel_input != []:
            for i in range(1, len(manuel)):
                self.manuel_add_block(manuel_input[i])

    def manuel_add_block(self, block):
        self.blocks.append(block)
        # print(self.blocks)

        if block[1] == 'Red':
            label = QLabel(self)
            label.setPixmap(self.red)
            label.setGeometry(
                100 * (block[4] + 1), 100 * (block[3] + 1), 200, 100)
            label.show()
        elif block[1] == 'Yellow':
            if block[2] == 'Horizontal':
                label = QLabel(self)
                label.setPixmap(self.yellow_horizontal)
                label.setGeometry(
                    100 * (block[4] + 1), 100 * (block[3] + 1), 200, 100)
                label.show()
            elif block[2] == 'Vertical':
                label = QLabel(self)
                label.setPixmap(self.yellow_vertical)
                label.setGeometry(
                    100 * (block[4] + 1), 100 * (block[3] + 1), 100, 200)
                label.show()
        elif block[1] == 'Blue':
            if block[2] == 'Horizontal':
                label = QLabel(self)
                label.setPixmap(self.blue_horizontal)
                label.setGeometry(
                    100 * (block[4] + 1), 100 * (block[3] + 1), 300, 100)
                label.show()
            elif block[2] == 'Vertical':
                label = QLabel(self)
                label.setPixmap(self.blue_vertical)
                label.setGeometry(
                    100 * (block[4] + 1), 100 * (block[3] + 1), 100, 300)
                label.show()
        self.label_list.append(label)

    def add_block(self):
        color = self.color.currentText()
        orientation = self.orientation.currentText()
        x1 = int(self.row_idx.text())
        y1 = int(self.col_idx.text())
        x2 = x1
        y2 = y1
        if color == 'Red':
            y2 += 1
        elif color == 'Yellow':
            if orientation == 'Horizontal':
                y2 += 1
            else:
                x2 += 1
        elif color == 'Blue':
            if orientation == 'Horizontal':
                y2 += 2
            else:
                x2 += 2
        block = [len(self.blocks), color, orientation, x1, y1, x2, y2]
        self.manuel_add_block(block)

    def remove_last(self):
        # print(self.blocks)
        if len(self.blocks) == 1:
            return
        self.blocks.pop(len(self.blocks)-1)
        self.label_list[len(self.label_list)-1].deleteLater()
        self.label_list.pop(len(self.label_list)-1)

    def solve(self):
        text, ok = QInputDialog.getText(
            self, '', 'Sure you want to start the solving process?')
        if not ok:
            return
        # print(self.blocks)
        self.solution = solver(self.blocks)

        # print(self.solution)
        if len(self.solution) == 0:
            print('Unsolvable')
            print(self.blocks)
            exit()

        self.current_index = 0

        self.row_label.setVisible(False)
        self.row_idx.setVisible(False)
        self.col_label.setVisible(False)
        self.col_idx.setVisible(False)
        self.orientation_label.setVisible(False)
        self.orientation.setVisible(False)
        self.color_label.setVisible(False)
        self.color.setVisible(False)
        self.add_block_button.setVisible(False)
        self.remove_last_button.setVisible(False)
        self.solve_button.setVisible(False)

        if hasattr(self, 'title'):
            self.title.setText("Current step: {}, Total step: {}".format(
                self.current_index+1, len(self.solution)))
            self.title.setVisible(True)
            self.button_prev.setVisible(True)
            self.button_next.setVisible(True)
            self.button_back.setVisible(True)
        else:
            self.title = QLabel("Current step: {}, Total step: {}".format(
                self.current_index+1, len(self.solution)), self)
            self.title.setGeometry(300, 700, 300, 50)
            self.title.show()

            self.button_prev = QPushButton("Previous", self)
            self.button_prev.clicked.connect(self.show_previos_dict)
            self.button_prev.move(300, 750)
            self.button_prev.show()
            self.button_next = QPushButton("Next", self)
            self.button_next.clicked.connect(self.show_next_dict)
            self.button_next.move(400, 750)
            self.button_next.show()

            self.button_back = QPushButton("Back", self)
            self.button_back.clicked.connect(self.go_back)
            self.button_back.move(25, 25)
            self.button_back.show()

    def go_back(self):
        self.row_label.setVisible(True)
        self.row_idx.setVisible(True)
        self.col_label.setVisible(True)
        self.col_idx.setVisible(True)
        self.orientation_label.setVisible(True)
        self.orientation.setVisible(True)
        self.color_label.setVisible(True)
        self.color.setVisible(True)
        self.add_block_button.setVisible(True)
        self.remove_last_button.setVisible(True)
        self.solve_button.setVisible(True)
        self.title.setVisible(False)
        self.button_prev.setVisible(False)
        self.button_next.setVisible(False)
        self.button_back.setVisible(False)

    def show_previos_dict(self):
        # self.label.setVisible(False)
        self.current_index = (self.current_index - 1) % len(self.solution)
        self.title.setText("Current step: {}, Total step: {}".format(
            self.current_index+1, len(self.solution)))

        current_step = self.solution[self.current_index]
        # print(current_step)

        for i in range(1, len(current_step)):
            block = current_step[i]
            self.label_list[block[0]].move(
                100 * (block[4] + 1), 100 * (block[3] + 1))

    def show_next_dict(self):
        self.current_index = (self.current_index + 1) % len(self.solution)
        self.title.setText("Current step: {}, Total step: {}".format(
            self.current_index+1, len(self.solution)))

        current_step = self.solution[self.current_index]
        # print(current_step)

        for i in range(1, len(current_step)):
            block = current_step[i]
            # print(block)
            self.label_list[block[0]].move(
                100 * (block[4] + 1), 100 * (block[3] + 1))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    manuel = [['Empty'], [1, 'Red', 'Horizontal', 2, 0, 2, 1], [2, 'Yellow', 'Horizontal', 0, 0, 0, 1], [3, 'Yellow', 'Horizontal', 4, 2, 4, 3], [4, 'Yellow', 'Horizontal', 5, 2, 5, 3], [5, 'Yellow', 'Horizontal', 5, 4, 5, 5], [6, 'Yellow', 'Horizontal',
                                                                                                                                                                                                                                    3, 4, 3, 5], [7, 'Yellow', 'Vertical', 0, 3, 1, 3], [8, 'Yellow', 'Vertical', 0, 5, 1, 5], [9, 'Yellow', 'Vertical', 2, 3, 3, 3], [10, 'Yellow', 'Vertical', 4, 1, 5, 1], [11, 'Blue', 'Vertical', 3, 0, 5, 0], [12, 'Blue', 'Vertical', 0, 4, 2, 4]]
    window = Pond_Solver()
    # window.setStyleSheet("background-color: white;")
    window.show()
    sys.exit(app.exec())
