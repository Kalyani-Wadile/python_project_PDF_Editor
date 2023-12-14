import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTextEdit, QPushButton, QVBoxLayout, QWidget, QFileDialog, QHBoxLayout, QSizePolicy  # Use QTextEdit instead of QLineEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfReader, PdfWriter

class MultilineTextEdit(QTextEdit):
    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.insertPlainText('\n')  # Insert a newline character
        else:
            super().keyPressEvent(event)

class PDFEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('PDF Editor')
        self.setGeometry(100, 100, 400, 200)

        # Create widgets
        self.label = QLabel('Enter text:')
        self.text_edit = MultilineTextEdit()  # Use the custom MultilineTextEdit
        self.save_button = QPushButton('Save PDF')
        self.edit_button = QPushButton('Edit PDF')

        # Apply styles to the widgets
        self.label.setStyleSheet('font: 14pt;')
        self.text_edit.setStyleSheet('font: 12pt;')
        self.save_button.setStyleSheet('font: bold 12pt; background-color: #4CAF50; color: white;')
        self.edit_button.setStyleSheet('font: bold 12pt; background-color: #008CBA; color: white;')

        # Connect button click events to functions
        self.save_button.clicked.connect(self.save_pdf)
        self.edit_button.clicked.connect(self.edit_pdf)

        # Create layout and add widgets
        layout = QVBoxLayout()

        # Add the label and text edit
        layout.addWidget(self.label, alignment=Qt.AlignTop | Qt.AlignHCenter)
        layout.addWidget(self.text_edit)

        # Create a spacer item to push the text field to the top
        spacer_item = QWidget()
        spacer_item.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(spacer_item)

        # Create a sub-layout for the buttons
        buttons_layout = QHBoxLayout()

        # Add the buttons to the sub-layout
        buttons_layout.addWidget(self.edit_button)
        buttons_layout.addWidget(self.save_button)

        # Add the buttons sub-layout to the main layout
        layout.addLayout(buttons_layout)

        # Set spacing for the main layout
        layout.setSpacing(10)

        # Create main container widget
        container = QWidget()
        container.setLayout(layout)

        # Set the central widget of the main window
        self.setCentralWidget(container)

    def save_pdf(self):
        text_to_add = self.text_edit.toPlainText()

        # Open a file dialog to get the filename
        filename, _ = QFileDialog.getSaveFileName(self, 'Save PDF', filter='PDF Files (*.pdf)')

        if filename:
            # Check if the file already exists
            if not filename.endswith('.pdf'):
                filename += '.pdf'

            # Create a PDF document
            c = canvas.Canvas(filename, pagesize=letter)

            # Split the text into lines
            lines = text_to_add.split('\n')

            # Set the initial y-coordinate for drawing text
            y_coordinate = 750

            # Draw each line of text
            for line in lines:
                c.drawString(100, y_coordinate, line)
                y_coordinate -= 12  # Adjust the vertical position for the next line

            c.save()

            print(f'PDF saved as {filename}')

    def edit_pdf(self):
        # Open a file dialog to get the filename
        filename, _ = QFileDialog.getOpenFileName(self, 'Edit PDF', filter='PDF Files (*.pdf)')

        if filename:
            # Read existing text from the PDF
            existing_text = self.read_pdf(filename)

            # Set the existing text to the text edit field
            self.text_edit.setPlainText(existing_text)

            print(f'PDF opened for editing: {filename}')

    def read_pdf(self, filename):
        # Read existing text from the PDF
        existing_text = ""
        try:
            pdf_reader = PdfReader(filename)
            for page_num in range(len(pdf_reader.pages)):
                existing_text += pdf_reader.pages[page_num].extract_text()
        except Exception as e:
            print(f'Error reading PDF: {e}')

        return existing_text

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PDFEditor()
    window.show()
    sys.exit(app.exec_())
