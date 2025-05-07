import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QListWidget,
    QLineEdit, QRadioButton, QCheckBox, QTextEdit, QComboBox, QMessageBox,
    QDialog, QButtonGroup, QHBoxLayout
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# Данные, хранящие вопросы и ответы
questions = []

class Question:
    def __init__(self, text, q_type, answers=None):
        self.text = text
        self.type = q_type  # 'single', 'multiple', 'text'
        self.answers = answers if answers else []

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Опросник")
        self.resize(600, 400)
        self.layout = QVBoxLayout()

        self.questions_list = QListWidget()
        self.layout.addWidget(self.questions_list)

        self.btn_add = QPushButton("Добавить вопрос")
        self.btn_edit = QPushButton("Редактировать выбранный вопрос")
        self.btn_start = QPushButton("Начать опрос")
        self.layout.addWidget(self.btn_add)
        self.layout.addWidget(self.btn_edit)
        self.layout.addWidget(self.btn_start)

        self.setLayout(self.layout)

        self.btn_add.clicked.connect(self.add_question)
        self.btn_edit.clicked.connect(self.edit_question)
        self.btn_start.clicked.connect(self.start_survey)

        self.update_questions_list()

    def update_questions_list(self):
        self.questions_list.clear()
        for idx, q in enumerate(questions):
            self.questions_list.addItem(f"{idx+1}. {q.text} ({q.type})")

    def add_question(self):
        dialog = QuestionDialog()
        if dialog.exec_():
            question = dialog.get_question()
            questions.append(question)
            self.update_questions_list()

    def edit_question(self):
        selected = self.questions_list.currentRow()
        if selected >= 0:
            q = questions[selected]
            dialog = QuestionDialog(q)
            if dialog.exec_():
                questions[selected] = dialog.get_question()
                self.update_questions_list()
        else:
            QMessageBox.warning(self, "Ошибка", "Выберите вопрос для редактирования.")

    def start_survey(self):
        if not questions:
            QMessageBox.warning(self, "Ошибка", "Нет вопросов для опроса.")
            return
        self.survey_window = SurveyWindow(questions)
        self.survey_window.show()


class QuestionDialog(QDialog):
    def __init__(self, question=None):
        super().__init__()
        self.setWindowTitle("Вопрос")
        self.layout = QVBoxLayout()

        self.txt_question = QLineEdit()
        self.layout.addWidget(QLabel("Текст вопроса:"))
        self.layout.addWidget(self.txt_question)

        self.cmb_type = QComboBox()
        self.cmb_type.addItems(["Один выбор", "Множественный выбор", "Ответ текстом"])
        self.layout.addWidget(QLabel("Тип вопроса:"))
        self.layout.addWidget(self.cmb_type)

        self.answers_edit = QTextEdit()
        self.answers_edit.setPlaceholderText("Ответы через строку, одна на строку")
        self.layout.addWidget(QLabel("Ответы (для выбора):"))
        self.layout.addWidget(self.answers_edit)

        self.btn_ok = QPushButton("ОК")
        self.layout.addWidget(self.btn_ok)

        self.setLayout(self.layout)

        self.cmb_type.currentIndexChanged.connect(self.toggle_answers)
        self.btn_ok.clicked.connect(self.accept)

        if question:
            self.txt_question.setText(question.text)
            if question.type != 'text':
                self.answers_edit.setPlainText("\n".join(question.answers))
            self.cmb_type.setCurrentIndex(self.type_to_index(question.type))
            self.toggle_answers()

    def toggle_answers(self):
        index = self.cmb_type.currentIndex()
        if index == 2:  # Ответ текстом
            self.answers_edit.setEnabled(False)
        else:
            self.answers_edit.setEnabled(True)

    def type_to_index(self, q_type):
        if q_type == 'single':
            return 0
        elif q_type == 'multiple':
            return 1
        else:
            return 2

    def get_question(self):
        text = self.txt_question.text()
        q_type = ['single', 'multiple', 'text'][self.cmb_type.currentIndex()]
        answers = []
        if q_type != 'text':
            answers = self.answers_edit.toPlainText().splitlines()
        return Question(text, q_type, answers)


class SurveyWindow(QWidget):
    def __init__(self, questions):
        super().__init__()
        self.setWindowTitle("Опрос")
        self.resize(600, 400)
        self.questions = questions
        self.answers = {}  # вопрос -> выбранные ответы

        self.layout = QVBoxLayout()

        self.question_widgets = []

        for q in questions:
            self.layout.addWidget(QLabel(q.text))
            if q.type == 'single':
                btn_group = QButtonGroup(self)
                options_layout = QVBoxLayout()
                btns = []
                for ans in q.answers:
                    rb = QRadioButton(ans)
                    btn_group.addButton(rb)
                    options_layout.addWidget(rb)
                self.question_widgets.append(('single', btn_group, options_layout))
                self.layout.addLayout(options_layout)
            elif q.type == 'multiple':
                checkboxes = []
                for ans in q.answers:
                    cb = QCheckBox(ans)
                    checkboxes.append(cb)
                    self.layout.addWidget(cb)
                self.question_widgets.append(('multiple', checkboxes))
            else:
                edt = QTextEdit()
                self.question_widgets.append(('text', edt))
                self.layout.addWidget(edt)

        self.btn_submit = QPushButton("Показать результаты")
        self.layout.addWidget(self.btn_submit)
        self.setLayout(self.layout)

        self.btn_submit.clicked.connect(self.show_results)

    def show_results(self):
        results = []

        for idx, q in enumerate(self.questions):
            w_type = self.question_widgets[idx][0]
            if w_type == 'single':
                group = self.question_widgets[idx][1]
                selected = group.checkedButton()
                if selected:
                    self.answers[q.text] = selected.text()
                else:
                    self.answers[q.text] = None
            elif w_type == 'multiple':
                checkboxes = self.question_widgets[idx][1]
                selected = [cb.text() for cb in checkboxes if cb.isChecked()]
                self.answers[q.text] = selected
            else:
                ans_text = self.question_widgets[idx][1].toPlainText()
                self.answers[q.text] = ans_text

        self.plot_results()

    def plot_results(self):
        self.result_window = ResultWindow(self.questions, self.answers)
        self.result_window.show()
        self.close()


class ResultWindow(QWidget):
    def __init__(self, questions, answers):
        super().__init__()
        self.setWindowTitle("Результаты опроса")
        self.resize(800, 600)
        self.layout = QVBoxLayout()
        self.questions = questions
        self.answers = answers

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)

        self.plot()

    def plot(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        # Собираем ответы по всем вопросам типа 'single'
        for q in self.questions:
            if q.type != 'single':
                continue
            q_text = q.text
            count_yes = 0
            count_no = 0
            for ans in self.answers.values():
                # Ответ может быть строкой или списком, в зависимости от вопроса
                if isinstance(ans, list):
                    for a in ans:
                        if a.strip().lower() == "да":
                            count_yes += 1
                        elif a.strip().lower() == "нет":
                            count_no += 1
                elif isinstance(ans, str):
                    if ans.strip().lower() == "да":
                        count_yes += 1
                    elif ans.strip().lower() == "нет":
                        count_no += 1
            # Построение диаграммы только если есть ответы "Да" или "Нет"
            total = count_yes + count_no
            if total > 0:
                labels = ['Да', 'Нет']
                counts = [count_yes, count_no]
                ax.pie(counts, labels=labels, autopct='%1.1f%%', startangle=90)
                ax.set_title('Результаты опросника (Соотношение ответов "Да" и "Нет")')
                self.canvas.draw()
                break  # Можно раскомментировать, чтобы показывать только одну диаграмму за раз
        else:
            # Если вопросов для отображения нет
            self.figure.clf()
            ax = self.figure.add_subplot(111)
            ax.text(0.5, 0.5, 'Нет данных для отображения', ha='center', va='center', fontsize=14)
            self.canvas.draw()


def add_cat_questions():
    cat_questions = [
        ("Любите ли вы котиков?", "single", ["Да", "Нет"]),
        ("У вас есть домашний кот?", "single", ["Да", "Нет"]),
        ("Котики приносят вам радость?", "single", ["Да", "Нет"]),
        ("Нравится ли вам смотреть видео с котиками?", "single", ["Да", "Нет"]),
        ("Вы бы хотели завести кота?", "single", ["Да", "Нет"]),
        ("Боитесь ли вы котов?", "single", ["Да", "Нет"]),
        ("Понимаете ли вы повадки котиков?", "single", ["Да", "Нет"]),
        ("Вы считаете котиков милыми?", "single", ["Да", "Нет"]),
        ("Делаете ли вы что-то для котиков, например, кормите бездомных?", "single", ["Да", "Нет"]),
        ("Верите ли вы, что котики могут предсказывать будущее?", "single", ["Да", "Нет"])
    ]
    for text, q_type, answers in cat_questions:
        questions.append(Question(text, q_type, answers))

if __name__ == "__main__":
    add_cat_questions()  # или add_cat_questions()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())