import sys
import platform
import psutil
import os
from PyQt6 import QtWidgets, QtCore

class CompatibilityChecker(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Set the main window properties
        self.setWindowTitle("System Compatibility Check for Sundial")
        self.setFixedSize(600, 400)
        
        # Create main layout
        main_layout = QtWidgets.QHBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)  # Add margins to the main layout
        # main_layout.setSpacing(10)  # Add spacing between left and right frames
        
        # Left Frame for requirements
        left_frame = QtWidgets.QFrame(self)
        left_frame.setLayout(QtWidgets.QVBoxLayout())
        left_frame.setContentsMargins(10, 10, 10, 10)  # Adjust margins for left frame
        
        # Requirements Label
        requirements_label = QtWidgets.QLabel("", self)
        left_frame.layout().addWidget(requirements_label)

        # Requirements List
        requirements_text = (
            "System Requirements : \n\n"
            "OS : Windows 11 / 10\n"
            "RAM : 8GB or more\n"
            "Processor : Intel i5/i7/i9\n"
            "Available Disk Space : 1GB or more"
        )
        requirements_list = QtWidgets.QLabel(requirements_text, self)
        left_frame.layout().addWidget(requirements_list)
        
        # Check Compatibility Button
        check_button = QtWidgets.QPushButton("Check System Compatibility", self)
        check_button.clicked.connect(self.check_compatibility)
        left_frame.layout().addWidget(check_button)
        
        # Add left frame to main layout
        main_layout.addWidget(left_frame)

        # Right Frame for system details
        right_frame = QtWidgets.QFrame(self)
        right_frame.setFrameShape(QtWidgets.QFrame.Shape.Box)
        right_frame.setStyleSheet("background-color: black; color: green;")
        right_frame.setLayout(QtWidgets.QVBoxLayout())
        right_frame.setContentsMargins(10, 10, 10, 10)  # Adjust margins for right frame
        
        # System Details Label
        details_label = QtWidgets.QLabel("System Details  :", self)
        right_frame.layout().addWidget(details_label)

        # System Details List
        self.os_text = QtWidgets.QLabel("", self)
        self.ram_text = QtWidgets.QLabel("", self)
        self.processor_text = QtWidgets.QLabel("", self)
        self.disk_space_text = QtWidgets.QLabel("", self)
        self.compatibility_status_text = QtWidgets.QLabel("", self)
        
        # Remove default spacing between labels
        for label in [self.os_text, self.ram_text, self.processor_text, self.disk_space_text, self.compatibility_status_text]:
            label.setStyleSheet("margin: 0; padding: 0;")  # Remove any default padding/margin
            right_frame.layout().addWidget(label)
        
        # Add right frame to main layout
        main_layout.addWidget(right_frame)

        # Create a context menu
        self.context_menu = QtWidgets.QMenu(self)
        
        self.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def check_compatibility(self):
        os_compatible = self.check_os()
        ram_compatible = self.check_ram()
        processor_compatible = self.check_processor()
        disk_space_compatible = self.check_disk_space()

        compatibility_status = "Compatibility Status :\n"
        compatibility_status += f"OS : {'Compatible' if os_compatible else 'Incompatible'}\n"
        compatibility_status += f"RAM : {'Compatible' if ram_compatible else 'Incompatible'}\n"
        compatibility_status += f"Processor : {'Compatible' if processor_compatible else 'Incompatible'}\n"
        compatibility_status += f"Available Disk Space : {'Compatible' if disk_space_compatible else 'Incompatible'}\n"

        self.os_text.setText(f"OS : {platform.system()} {platform.release()}")
        self.ram_text.setText(f"RAM : {psutil.virtual_memory().total / (1024 ** 3):.2f} GB")
        self.processor_text.setText(f"Processor : {platform.processor()}")
        self.disk_space_text.setText(f"Available Disk Space : {psutil.disk_usage(os.path.expanduser('~')).free / (1024 ** 3):.2f} GB")
        self.compatibility_status_text.setText(compatibility_status)

        if os_compatible and ram_compatible and processor_compatible and disk_space_compatible:
            self.compatibility_status_text.setStyleSheet("color: green;")
            self.proceed_with_installation()
        else:
            self.compatibility_status_text.setStyleSheet("color: red;")
            self.exit_installation()

    def check_os(self):
        os_version = platform.system() + " " + platform.release()
        return os_version in ["Windows 10", "Windows 11"]

    def check_ram(self):
        ram_gb = psutil.virtual_memory().total / (1024 ** 3)
        return ram_gb >= 8

    def check_processor(self):
        processor = platform.processor()
        return any(cpu in processor for cpu in ["Intel", "i5", "i7", "i9"])

    def check_disk_space(self):
        disk_space_gb = psutil.disk_usage(os.path.expanduser("~")).free / (1024 ** 3)
        return disk_space_gb >= 1

    def proceed_with_installation(self):
        QtWidgets.QMessageBox.information(self, "System Check", "System is compatible. Proceeding with installation...")
        self.close()

    def exit_installation(self):
        QtWidgets.QMessageBox.critical(self, "System Check", "System is not compatible. Exiting installation...")
        self.close()

    def show_context_menu(self, pos):
        self.context_menu.exec(self.mapToGlobal(pos))

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = CompatibilityChecker()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
