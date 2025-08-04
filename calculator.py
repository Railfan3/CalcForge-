import sys
import math
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLineEdit, QCheckBox, QLabel, QTabWidget, QTextEdit, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class CalcForge(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CalcForge - Advanced GUI Calculator")
        self.setGeometry(200, 200, 480, 700)

        self.history = []
        self.current_expression = ""
        self.dark_mode = True

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Theme Toggle
        self.theme_toggle = QCheckBox("Toggle Dark/Light Theme")
        self.theme_toggle.setChecked(True)
        self.theme_toggle.stateChanged.connect(self.toggle_theme)
        main_layout.addWidget(self.theme_toggle)

        # Tabs: Calculator and History
        self.tabs = QTabWidget()
        self.calc_tab = QWidget()
        self.history_tab = QWidget()

        self.tabs.addTab(self.calc_tab, "Calculator")
        self.tabs.addTab(self.history_tab, "History")
        main_layout.addWidget(self.tabs)

        # Calculator Tab
        calc_layout = QVBoxLayout()
        self.calc_tab.setLayout(calc_layout)

        self.input_field = QLineEdit()
        self.input_field.setAlignment(Qt.AlignRight)
        self.input_field.setFont(QFont("Courier", 22))
        self.input_field.setPlaceholderText("Enter Expression...")
        calc_layout.addWidget(self.input_field)

        self.live_display = QLineEdit()
        self.live_display.setReadOnly(True)
        self.live_display.setAlignment(Qt.AlignRight)
        self.live_display.setFont(QFont("Courier", 16))
        calc_layout.addWidget(self.live_display)

        # Buttons Layout
        buttons = [
            ["AC", "C", "ANS", "View"],
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            ["0", ".", "=", "+"],
            ["(", ")", "mod", "sqrt"],
            ["sin", "cos", "tan", "log"],
            ["ln", "exp", "abs", "!"],
            ["π", "ℯ"]
        ]

        for row in buttons:
            row_layout = QHBoxLayout()
            for btn_text in row:
                button = QPushButton(btn_text)
                button.clicked.connect(self.on_button_click)
                button.setFixedHeight(50)
                button.setStyleSheet(self.get_button_style(btn_text))
                row_layout.addWidget(button)
            calc_layout.addLayout(row_layout)

        # History Tab
        self.history_display = QTextEdit()
        self.history_display.setReadOnly(True)
        self.history_tab.setLayout(QVBoxLayout())
        self.history_tab.layout().addWidget(self.history_display)

        self.setLayout(main_layout)
        self.toggle_theme()

    def get_button_style(self, text):
        if text in {"+", "-", "*", "/", "=", "sqrt", "^", "mod", "!"}:
            return "background-color: #ff9500; color: black; font-weight: bold; border-radius: 8px;"
        elif text in {"sin", "cos", "tan", "log", "ln", "exp", "abs"}:
            return "background-color: #ffb84d; color: black; border-radius: 8px;"
        elif text == "ANS":
            return "background-color: #888; color: white; border-radius: 8px;"
        elif text in {"C", "AC"}:
            return "background-color: #d32f2f; color: white; border-radius: 8px;"
        elif text == "View":
            return "background-color: #666; color: white; border-radius: 8px;"
        elif text in {"π", "ℯ"}:
            return "background-color: #333; color: white; font-weight: bold; border-radius: 8px;"
        else:
            return "background-color: #333; color: white; border-radius: 8px;"

    def on_button_click(self):
        sender = self.sender()
        btn_text = sender.text()
        current = self.input_field.text()

        if btn_text == "AC":
            self.input_field.clear()
            self.live_display.clear()
        elif btn_text == "C":
            self.input_field.setText(current[:-1])
        elif btn_text == "=":
            self.evaluate()
        elif btn_text == "ANS":
            if self.history:
                self.input_field.setText(str(self.history[-1][1]))
        elif btn_text == "View":
            self.tabs.setCurrentWidget(self.history_tab)
        elif btn_text == "sqrt":
            self.input_field.setText(current + "math.sqrt(")
        elif btn_text == "!":
            self.input_field.setText(current + "math.factorial(")
        elif btn_text in {"sin", "cos", "tan", "log", "ln", "exp", "abs"}:
            func_map = {
                "ln": "math.log(",
                "log": "math.log10(",
                "exp": "math.exp(",
                "abs": "abs(",
                "sin": "math.sin(",
                "cos": "math.cos(",
                "tan": "math.tan(",
            }
            self.input_field.setText(current + func_map[btn_text])
        elif btn_text == "mod":
            self.input_field.setText(current + "%")
        elif btn_text == "π":
            self.input_field.setText(current + "math.pi")
        elif btn_text == "ℯ":
            self.input_field.setText(current + "math.e")
        else:
            self.input_field.setText(current + btn_text)
        self.update_live_display()

    def evaluate(self):
        expr = self.input_field.text()
        try:
            result = eval(expr)
            self.history.append((expr, result))
            self.input_field.setText(str(result))
            self.live_display.clear()
            self.update_history()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Invalid Expression:\n{str(e)}")

    def update_history(self):
        self.history_display.clear()
        for expr, result in self.history[-50:]:
            self.history_display.append(f"{expr} = {result}")

    def update_live_display(self):
        expr = self.input_field.text()
        try:
            result = eval(expr)
            self.live_display.setText(str(result))
        except:
            self.live_display.setText("")

    def toggle_theme(self):
        if self.theme_toggle.isChecked():
            self.setStyleSheet("""
                QWidget { background-color: #121212; color: white; }
                QLineEdit, QTextEdit { background-color: #1e1e1e; color: white; border: 2px solid #888; border-radius: 8px; }
                QPushButton { background-color: #333; color: white; border-radius: 8px; }
                QPushButton:hover { background-color: #666; }
                QTabBar::tab { background: #ddd; color: black; padding: 8px; border-top-left-radius: 6px; border-top-right-radius: 6px; }
                QTabBar::tab:selected { background: white; color: black; }
            """)
        else:
            self.setStyleSheet("""
                QWidget { background-color: #f0f0f0; color: black; }
                QLineEdit, QTextEdit { background-color: #fff; color: black; border: 2px solid #333; border-radius: 8px; }
                QPushButton { background-color: #ddd; color: black; border-radius: 8px; }
                QPushButton:hover { background-color: #bbb; }
                QTabBar::tab { background: #eee; color: black; padding: 8px; border-top-left-radius: 6px; border-top-right-radius: 6px; }
                QTabBar::tab:selected { background: white; color: black; }
            """)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = CalcForge()
    calc.show()
    sys.exit(app.exec_())
