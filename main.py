import sys
import asyncio
import qasync
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
                               QTextEdit, QLineEdit, QPushButton, QWidget, QLabel,
                               QScrollArea, QFormLayout, QDoubleSpinBox, QSpinBox,
                               QPlainTextEdit, QSizePolicy)
from PySide6.QtCore import Qt
from PySide6.QtGui import QTextCursor, QPixmap
from vertex_ai import BisonChatApp

app = QApplication(sys.argv)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.vertex_chat_app = None

        self.setWindowTitle("Vertex Chat App")
        self.setGeometry(100, 100, 800, 600)

        self.init_config_form()
        self.init_chat_layout()

        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

    def init_chat_layout(self):
        self.chat_layout = QVBoxLayout()
        self.chat_widget = QWidget()
        self.chat_widget.setLayout(self.chat_layout)

    def init_config_form(self):
        self.layout = QVBoxLayout()
        self.form_layout = QFormLayout()

        # Context input field
        self.context_input = QPlainTextEdit()
        self.context_input.setPlaceholderText("Enter context (optional)")
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(4)
        size_policy.setVerticalStretch(1)
        self.context_input.setSizePolicy(size_policy)
        self.form_layout.addRow("Context:", self.context_input)

        # Examples input fields
        self.examples_layout = QVBoxLayout()

        self.add_example_button = QPushButton("Add Example")
        self.add_example_button.clicked.connect(self.add_example_input)
        self.examples_layout.addWidget(self.add_example_button)

        self.form_layout.addRow("Examples:", self.examples_layout)

        self.temperature_input = QDoubleSpinBox()
        self.temperature_input.setRange(0, 1)
        self.temperature_input.setSingleStep(0.1)
        self.temperature_input.setValue(0.2)
        self.form_layout.addRow(QLabel("Temperature:"), self.temperature_input)

        self.max_output_tokens_input = QSpinBox()
        self.max_output_tokens_input.setRange(1, 1000)
        self.max_output_tokens_input.setValue(100)
        self.form_layout.addRow(
            QLabel("Max Output Tokens:"), self.max_output_tokens_input)

        self.top_p_input = QDoubleSpinBox()
        self.top_p_input.setRange(0, 1)
        self.top_p_input.setSingleStep(0.05)
        self.top_p_input.setValue(0.95)
        self.form_layout.addRow(QLabel("Top P:"), self.top_p_input)

        self.top_k_input = QSpinBox()
        self.top_k_input.setRange(1, 100)
        self.top_k_input.setValue(40)
        self.form_layout.addRow(QLabel("Top K:"), self.top_k_input)

        self.layout.addLayout(self.form_layout)

        self.start_chat_button = QPushButton("Start Chat")
        self.start_chat_button.clicked.connect(self.start_chat)

        self.layout.addWidget(self.start_chat_button)

    def init_chat_ui(self):
        # Create a QTextEdit for the chat display
        self.chat_display_text_edit = QTextEdit()
        self.chat_display_text_edit.setReadOnly(True)

        # Wrap the QTextEdit inside a QScrollArea
        self.chat_display = QScrollArea()
        self.chat_display.setWidget(self.chat_display_text_edit)
        self.chat_display.setWidgetResizable(True)
        self.chat_layout.addWidget(self.chat_display)

        message_input_layout = QHBoxLayout()

        self.message_input = QLineEdit()
        message_input_layout.addWidget(self.message_input)

        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(
            lambda: asyncio.create_task(self.send_message()))
        message_input_layout.addWidget(self.send_button)
        self.message_input.returnPressed.connect(self.send_button.click)

        self.chat_layout.addLayout(message_input_layout)

        self.clear_chat_button = QPushButton("Clear Chat")
        self.clear_chat_button.clicked.connect(self.clear_chat)
        self.chat_layout.addWidget(self.clear_chat_button)

        self.end_chat_button = QPushButton("End Chat")
        self.end_chat_button.clicked.connect(self.end_chat)
        self.chat_layout.addWidget(self.end_chat_button)

        # Initialize loading_image and loading_label
        self.loading_image = QPixmap('loading.png')
        self.loading_label = QLabel()
        self.loading_label.setPixmap(self.loading_image.scaled(
            self.loading_label.width(), self.loading_label.height(), Qt.KeepAspectRatio))
        self.loading_label.hide()
        self.chat_layout.addWidget(
            self.loading_label, alignment=Qt.AlignCenter)

    def start_chat(self):
        context = self.context_input.toPlainText()
        examples = self.get_examples()

        temperature = self.temperature_input.value()
        max_output_tokens = self.max_output_tokens_input.value()
        top_p = self.top_p_input.value()
        top_k = self.top_k_input.value()

        self.vertex_chat_app = BisonChatApp(
            context=context,
            examples=examples,
            temperature=temperature,
            max_output_tokens=max_output_tokens,
            top_p=top_p,
            top_k=top_k
        )

        # Remove config form and start button
        for i in reversed(range(self.form_layout.count())):
            item = self.form_layout.itemAt(i)
            if item.widget() is not None:
                item.widget().setParent(None)
        self.start_chat_button.setParent(None)
        self.add_example_button.setParent(None)

        # Initialize chat UI
        self.init_chat_layout()
        self.init_chat_ui()
        self.setCentralWidget(self.chat_widget)

        # set focus on the input field
        self.message_input.setFocus()

    def show_error(self, message):
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.append(f"Error: {message}")
        self.layout.addWidget(self.chat_display)

    async def send_message(self):
        message = self.message_input.text()
        self.chat_display_text_edit.moveCursor(QTextCursor.End)
        # self.chat_display_text_edit.insertPlainText(f"User: {message}\n")
        self.chat_display_text_edit.insertHtml(
            f'<p style="color:yellow;"><b>User</b>: &nbsp;{message}</p><br>')
        self.message_input.clear()

        # Show loading image
        self.loading_label.show()

        # Disable input elements during message sending
        self.message_input.setEnabled(False)
        self.send_button.setEnabled(False)
        self.update()

        # Introduce a small delay for changes to update
        await asyncio.sleep(0.1)

        response = await self.vertex_chat_app.chat(message)

        # Hide loading image
        self.loading_label.hide()

        # Re-enable input elements
        self.message_input.setEnabled(True)
        self.send_button.setEnabled(True)

        self.chat_display_text_edit.moveCursor(QTextCursor.End)
        # self.chat_display_text_edit.insertPlainText(f"{response['author']}: {response['content']}\n\n")
        if response["author"] == 'System':
            self.chat_display_text_edit.insertHtml(
                f'<p style="color:red;"><b>{response["author"]}</b>: &nbsp;{response["content"]}<br><br>')
        else:
            self.chat_display_text_edit.insertHtml(
                f'<p style="color:green;"><b>{response["author"]}</b>: &nbsp;{response["content"]}<br><br>')
        self.chat_display_text_edit.moveCursor(QTextCursor.End)

        self.message_input.setFocus()

    def clear_chat(self):
        self.chat_display_text_edit.clear()
        self.vertex_chat_app.clear_messages()

    def end_chat(self):
        # Remove chat UI elements
        self.chat_display.setParent(None)
        self.message_input.setParent(None)
        self.send_button.setParent(None)
        self.clear_chat_button.setParent(None)
        self.end_chat_button.setParent(None)

        self.vertex_chat_app.end_chat()

        self.init_config_form()

        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

    def add_example_input(self):
        example_input = QTextEdit()
        example_input.setPlaceholderText("Input")
        example_output = QTextEdit()
        example_output.setPlaceholderText("Output")

        example_row = QHBoxLayout()
        example_row.addWidget(example_input)
        example_row.addWidget(example_output)

        self.examples_layout.insertLayout(
            self.examples_layout.count() - 1, example_row)

    def get_examples(self):
        examples = []

        for i in range(self.examples_layout.count() - 1):
            example_row = self.examples_layout.itemAt(i)
            example_input = example_row.itemAt(0).widget()
            example_output = example_row.itemAt(1).widget()

            input_text = example_input.toPlainText().strip()
            output_text = example_output.toPlainText().strip()

            if input_text and output_text:
                examples.append({"input": {"content": input_text},
                                "output": {"content": output_text}})

        return examples


def main():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    else:
        sys.argv.extend(app.arguments())

    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = MainWindow()
    window.show()

    with loop:
        sys.exit(loop.run_forever())


if __name__ == "__main__":
    main()
