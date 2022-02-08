import sys
from PyQt5 import QtWidgets
import datetime, webbrowser
from PyQt5.QtWidgets import (QApplication, QSplitter, QGridLayout, QHBoxLayout, QPushButton, 
                            QTreeWidget, QFrame, QLabel, QHBoxLayout, QMainWindow,
                            QStackedLayout, QWidget, QVBoxLayout, QLineEdit, QRadioButton,
                            QTreeWidgetItem, QDesktopWidget, QTabWidget, QSpinBox, QComboBox,
                            QCalendarWidget, QDateTimeEdit, QMessageBox, QAbstractItemView,
                            QHeaderView, QTableWidget, QTableWidgetItem, QStyledItemDelegate,
                            QSizePolicy, QTextEdit, QScrollArea, QGroupBox)
from PyQt5.QtCore import Qt, QUrl, QDate
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon, QFont

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        # set window name
        self.setWindowTitle("Centre for Microsystems")

        # set status bar
        self.status = self.statusBar()
        self.status.showMessage("Centre for Microsystems")

        # set the initial window size
        self.setFixedSize(600, 400)

        # set the initialized window position
        self.center()

        # Set Qcomobox to display normally, otherwise an item will be too large
        self.delegate = QStyledItemDelegate()

        # Set window transparency
        # self.setWindowOpacity(0.9) 

        # settings icon
        self.setWindowIcon(QIcon("icon.png"))

        # Set the overall layout to display left and right
        pagelayout = QGridLayout()

    # Start layout on the left 

        # Create the left main window
        top_left_frame = QFrame(self)
        # draw rectangle panel
        top_left_frame.setFrameShape(QFrame.StyledPanel)
        # The left button is vertical layout
        button_layout = QVBoxLayout(top_left_frame)
        # login button for authentication
        verifyid_btn = QPushButton("Verify ID")
        verifyid_btn.setFixedSize(100, 30)
        button_layout.addWidget(verifyid_btn)

        # Enter username Password button
        # Because you need to choose whether to be an administrator in the radiobutton
        # Therefore, it is necessary to determine whether certain buttons are available, so, set to self to facilitate the calling of sub-functions
        self.user_btn = QPushButton("Login")
        self.user_btn.setFixedSize(100, 30)
        button_layout.addWidget(self.user_btn)
        # Information management button (available for super administrators)
        self.register_btn = QPushButton("Information Management")
        self.register_btn.setFixedSize(100, 30)
        button_layout.addWidget(self.register_btn)
        # Enter information button (available to ordinary administrators)
        self.input_btn = QPushButton("Input information")
        self.input_btn.setFixedSize(100, 30)
        button_layout.addWidget(self.input_btn)
        # Information query button (viewable by all)
        query_btn = QPushButton("Query information")
        query_btn.setFixedSize(100, 30)
        button_layout.addWidget(query_btn)
        # Modeling Home button (Modeling student's blog does not support blogs without technical thresholds)
        friend_btn = QPushButton("Modeling Field")
        friend_btn.setFixedSize(100, 30)
        button_layout.addWidget(friend_btn)
        # Personal control button (reserved interface to complete the dynamic modeling, teaming and other functions)
        space_btn = QPushButton("Personal Space")
        space_btn.setFixedSize(100, 30)
        button_layout.addWidget(space_btn)
        # exit button
        quit_btn = QPushButton(top_left_frame)
        quit_btn.setFixedSize(100, 30), quit_btn.setText("Quit")
        button_layout.addWidget(quit_btn)
        # Increase the spacing and beautify the interface
        button_layout.addStretch(1)

    #Start the layout on the right, click the button on the left, and correspond to different interfaces on the right

        #The layout of each interface is introduced in detail
        right_frame = QFrame(self)
        right_frame.setFrameShape(QFrame.StyledPanel)
        # The right side is displayed as a stack layout, that is, click the button, and different pages will be loaded on the right side
        self.right_layout = QStackedLayout(right_frame)
        # The right_frame parameter has been passed in to the layout on the right, so subsequent controls do not need to add this parameter layout addwidget

        # Confirm identity interface
        # admin identity
        self.radio_btn_admin = QRadioButton()
        self.radio_btn_admin.setText("I am the administrator, to enter data")
        # Tourist status, you can only choose one of the two
        self.radio_btn_user = QRadioButton()
        self.radio_btn_user.setText("I am a tourist, just come and see")
        # Manage with a vertical layout manager and set it as the first interface
        radio_btn_layout = QVBoxLayout()
        radio_btn_widget = QWidget()
        radio_btn_layout.addWidget(self.radio_btn_admin)
        radio_btn_layout.addWidget(self.radio_btn_user)
        radio_btn_widget.setLayout(radio_btn_layout)
        self.right_layout.addWidget(radio_btn_widget)

        # Admin login interface
        # Divided into super management and general management. 
        self.user_line = QLineEdit()
        self.user_line.setPlaceholderText("Please enter the account number:")
        self.user_line.setFixedWidth(400)
        self.password_line = QLineEdit()
        self.password_line.setPlaceholderText("Please enter password:")
        self.password_line.setEchoMode(QLineEdit.Password)
        self.password_line.setFixedWidth(400)
        # Layout of account and password
        login_layout = QVBoxLayout()
        login_btn_layout = QHBoxLayout()
        login_btn_cancel = QPushButton("Cancel")
        login_btn_cancel.setFixedWidth(80)
        login_btn_confirm = QPushButton("Confirm")
        login_btn_confirm.setFixedWidth(80)
        # button layout
        login_btn_layout.addWidget(login_btn_cancel)
        login_btn_layout.addWidget(login_btn_confirm)
        login_widget = QWidget()
        login_widget.setLayout(login_layout)
        # Add the layout of all elements
        login_layout.addWidget(self.user_line)
        login_layout.addWidget(self.password_line)
        login_layout.addLayout(login_btn_layout)
        # Add to the layout layout on the right is also the second interface
        self.right_layout.addWidget(login_widget)

        # Information management page
        # Only super administrators can see
        # This interface is the interface for Qtabwidget multi-window switching. Click different tabs to complete the switching between different interfaces in the interface.
        info_mana = QTabWidget()
        self.right_layout.addWidget(info_mana)
        # Divided into four tab pages: registration general management, teacher management, college professional management, and competition management
        admin_info = QWidget()
        teach_info = QWidget()
        colleage_major_info = QWidget()
        contest_info = QWidget()
        # Add the above four tags
        info_mana.addTab(admin_info, "Account Management")
        info_mana.addTab(teach_info, "Teacher Management")
        info_mana.addTab(colleage_major_info, "College Major Management")
        info_mana.addTab(contest_info, "Contest Management")
        register_label = QLabel("Apply for an account here")

        # The page for registering an account, enter the confirm password, you can delete the form display
        self.register_id = QLineEdit()
        self.register_id.setPlaceholderText("Please enter a new account number:")
        self.register_id.setFixedWidth(400)
        self.register_psd = QLineEdit()
        # registered password
        self.register_psd.setPlaceholderText("Please enter password:")
        self.register_psd.setFixedWidth(400)
        # Set to password display, that is, not to display the original text
        self.register_psd.setEchoMode(QLineEdit.Password)
        # Enter the password again The two passwords are inconsistent and cannot be registered
        self.register_confirm = QLineEdit()
        self.register_confirm.setPlaceholderText("Please confirm the password:")
        self.register_confirm.setFixedWidth(400)
        self.register_confirm.setEchoMode(QLineEdit.Password)
        self.register_confirm_btn = QPushButton("Confirm Submit")
        self.register_confirm_btn.setFixedSize(100, 30)
        # After refreshing, you can see the general administrator account of all registration applications
        register_btn_del = QPushButton("Confirm delete")
        register_btn_del.setFixedSize(100, 30)
        # Set up a form for displaying ordinary administrator accounts, easy to display
        self.register_table = QTableWidget()
        # The view is only for observation and cannot be modified. The tableview parent class is available, and the tablewidget subclass can also be used, so the subclass is selected
        # Put all the tables into a dictionary to facilitate the same initialization later, and the code is easy to maintain
        # Use a dictionary to determine which object called the method during initialization because the specific operation of each object is somewhat different
        # Later, I found that it is possible to add a parameter to solve this problem.
        self.table = {}
        # Only displayed on the super administrator page, the normal state is only created but not loaded
        self.table['register_table'] = self.register_table
        # Set the layout of the registered account and add controls
        register_btn_layout = QHBoxLayout()
        register_layout = QVBoxLayout()
        register_widget = QWidget()
        register_widget.setLayout(register_layout)
        register_layout.addWidget(register_label)
        register_layout.addWidget(self.register_id)
        register_layout.addWidget(self.register_psd)
        register_layout.addWidget(self.register_confirm)
        register_btn_layout.addWidget(self.register_confirm_btn)
        register_btn_layout.addWidget(register_btn_del)
        register_layout.addLayout(register_btn_layout)
        register_layout.addWidget(self.table['register_table'])
        # Finally, deploy the layout of the added control to the first tab bar
        admin_info.setLayout(register_layout)

        # Start to set up the tab bar of teacher information management, enter registration, there is a delete button, the form is displayed
        teacher_layout = QVBoxLayout()
        teacher_table_layout = QHBoxLayout()
        teacher_input_layout = QVBoxLayout()
        teacher_layout.addLayout(teacher_input_layout)
        teacher_layout.addLayout(teacher_table_layout)
        # A table showing teacher information
        self.teacher_table = QTableWidget()
        # Only displayed on the super administrator page, the normal state is only created but not loaded
        self.table['teacher_table'] = QTableWidget()
        teacher_table_layout.addWidget(self.table['teacher_table'])
        self.teacher_input_name_line = QLineEdit()
        self.teacher_input_name_line.setPlaceholderText("Please enter the teacher's name")
        teacher_input_como_layout = QHBoxLayout()
        teacher_input_college_label = QLabel("Please enter teacher college")
        teacher_input_college_label.setFixedWidth(200)
        # The college is connected to the database load option in the comobox and cannot be arbitrarily entered and can only be loaded in the super administrator state
        self.teacher_input_college_como = QComboBox()
        teacher_input_como_layout.addWidget(teacher_input_college_label)
        teacher_input_como_layout.addWidget(self.teacher_input_college_como)
        self.teacher_input_id_line = QLineEdit()
        self.teacher_input_id_line.setPlaceholderText("Please enter the teacher ID")
        teacher_input_btn_layout = QHBoxLayout()
        teacher_input_btn_confirm = QPushButton("Confirm Application")
        teacher_input_btn_layout.addWidget(teacher_input_btn_confirm)
        teacher_input_btn_del = QPushButton("Confirm delete")
        teacher_input_btn_layout.addWidget(teacher_input_btn_del)
        # Add the above controls
        teacher_input_layout.addWidget(self.teacher_input_name_line)
        teacher_input_layout.addLayout(teacher_input_como_layout)
        teacher_input_layout.addWidget(self.teacher_input_id_line)
        teacher_input_layout.addLayout(teacher_input_btn_layout)
        # Set the layout of the teacher page
        teach_info.setLayout(teacher_layout)
        
        # College professional management label interface input with delete button table display
        colleage_major_info_layout = QVBoxLayout()
        colleage_major_info_button_layout = QHBoxLayout()
        colleage_major_info_layout.addLayout(colleage_major_info_button_layout)
        self.colleage_major_info_college = QLineEdit()
        self.colleage_major_info_college.setPlaceholderText("Please enter the inserted college")
        self.colleage_major_info_major = QLineEdit()
        self.colleage_major_info_major.setPlaceholderText("Please enter the inserted major")
        self.colleage_major_input_btn = QPushButton("OK to insert")
        colleage_major_del_btn = QPushButton("Delete OK")
        colleage_major_info_button_layout.addWidget(self.colleage_major_info_college)
        colleage_major_info_button_layout.addWidget(self.colleage_major_info_major)
        colleage_major_info_button_layout.addWidget(self.colleage_major_input_btn)
        colleage_major_info_button_layout.addWidget(colleage_major_del_btn)
        self.colleage_major_twoside = QTableWidget()
        self.table['colleage_major_twoside'] = self.colleage_major_twoside
        colleage_major_info_layout.addWidget(self.table['colleage_major_twoside'])
        colleage_major_info.setLayout(colleage_major_info_layout)

        # Label page of competition management Enter competition Delete button to complete deletion Table display
        contest_layout = QVBoxLayout()
        contest_info.setLayout(contest_layout)
        self.contest_info_table = QTableWidget()
        self.table['contest_info_table'] = self.contest_info_table
        contest_input_layout = QVBoxLayout()
        self.contest_input_sponsor_line = QLineEdit()
        self.contest_input_sponsor_line.setPlaceholderText("input sponsor")
        self.contest_input_class_line = QLineEdit()
        self.contest_input_class_line.setPlaceholderText("Contest level")
        self.contest_input_id_line = QLineEdit()
        self.contest_input_id_line.setPlaceholderText("Contest name")
        contest_input_layout.addWidget(self.contest_input_sponsor_line)
        contest_input_layout.addWidget(self.contest_input_class_line)
        contest_input_layout.addWidget(self.contest_input_id_line)
        contest_layout.addLayout(contest_input_layout)
        contest_layout.addWidget(self.table['contest_info_table'])
        manage_contest_layout = QHBoxLayout()
        manage_contest_button_input = QPushButton()
        manage_contest_button_input.setText("Enter Contest")
        manage_contest_button_del = QPushButton()
        manage_contest_button_del.setText("Delete Contest")
        manage_contest_layout.addWidget(manage_contest_button_input)
        manage_contest_layout.addWidget(manage_contest_button_del)
        contest_layout.addLayout(manage_contest_layout)

        # Modeling field Use TreeView horizontal layout, you can set options to show or close selection
        # Read the database (name, major, grade, domain name) and load the blog of the modeling student (and even if it is not an administrator)
        self.friend_tree = QTreeWidget()
        self.friend_tree.setColumnCount(2) # Three columns
        # set title
        self.friend_tree.setHeaderLabels(['Grade', 'Personnel, URL, individual signature, has won the highest award, click to open the webpage (please use Chrome or Firefox to open)'])
        self.friend_tree.setColumnWidth(1, 400) # Set the width of the first column
        friend_widget = QWidget()
        friend_layout = QVBoxLayout()
        friend_widget.setLayout(friend_layout)
        friend_label = QLabel("If you want to join your own blog, please contact the official staff of the Modeling Association.")
        friend_label1 = QLabel("Note: blogs without technical thresholds written on CSDN, Blog Park, Zhihu, etc. with the help of third-party platforms are not supported. Encourage and recommend hexo or jekyll.")
        friend_layout.addWidget(friend_label)
        friend_layout.addWidget(friend_label1)
        friend_layout.addWidget(self.friend_tree)
        self.right_layout.addWidget(friend_widget)
        input_tab = QTabWidget()
        self.right_layout.addWidget(input_tab)
        # Enter the modeling field in the information
        input_friend_widget = QWidget()
        input_friend_layout = QVBoxLayout()
        self.input_friend_name = QLineEdit()
        self.input_friend_name.setPlaceholderText("Please enter your name")
        self.input_friend_url = QLineEdit()
        self.input_friend_url.setPlaceholderText("Please enter the URL (can not be empty, can not be repeated with the existing URL)")
        input_friend_label = QLabel("Please select a grade")
        input_friend_label.setMaximumHeight(20)
        # Input with up and down arrow keys to prevent random input
        self.input_friend_class = QSpinBox()
        self.input_friend_class.setMinimum(2013)
        self.input_friend_class.setMaximum(3000)
        # set to current year
        current_year = datetime.datetime.now().year
        self.input_friend_class.setValue(current_year)
        self.input_friend_sign = QLineEdit()
        self.input_friend_sign.setPlaceholderText("Please enter a personalized signature")
        self.input_friend_price = QLineEdit()
        self.input_friend_price.setPlaceholderText("Please enter the highest award, no write no")
        input_friend_button = QPushButton("Confirm input")
        del_friend_button = QPushButton("Confirm delete")
        # Create a view of the blog for easy maintenance
        self.input_friend_table = QTableWidget(right_frame)
        self.table['input_friend_table'] = self.input_friend_table
        # add controls
        input_friend_layout.addWidget(self.input_friend_name)
        input_friend_layout.addWidget(self.input_friend_url)
        input_friend_layout.addWidget(input_friend_label)
        input_friend_layout.addWidget(self.input_friend_class)
        input_friend_layout.addWidget(self.input_friend_sign)
        input_friend_layout.addWidget(self.input_friend_price)
        input_friend_layout.addWidget(input_friend_button)
        input_friend_layout.addWidget(self.table['input_friend_table'])
        input_friend_layout.addWidget(del_friend_button)
        input_friend_widget.setLayout(input_friend_layout)
        input_tab.addTab(input_friend_widget, "Modeling Corner")

        # The entry competition label in the entry information
        input_contest_widget = QWidget(right_frame)
        # First horizontal layout, select race
        input_contest_layout = QVBoxLayout()
        input_contest_widget.setLayout(input_contest_layout)
        input_contest_name_layout = QHBoxLayout()
        input_contest_label = QLabel("Please select a contest")
        input_contest_label.setFixedWidth(100)
        # should load data after confirming identity instead of loading data but not showing it to normal users may leak to memory
        self.input_contest_class = QComboBox()
        input_contest_teacher_label = QLabel("Teacher")
        self.input_contest_teacher_name = QComboBox()
        input_contest_teacher_label.setFixedWidth(100)
        input_contest_name_layout.addWidget(input_contest_label)
        input_contest_name_layout.addWidget(self.input_contest_class)
        input_contest_name_layout.addWidget(input_contest_teacher_label)
        input_contest_name_layout.addWidget(self.input_contest_teacher_name)
        input_contest_layout.addLayout(input_contest_name_layout)
        # The second horizontal layout, choose the start and end time of the game
        input_contest_time_layout = QHBoxLayout()
        input_contest_time_begin = QLabel("Start Time")
        input_contest_time_begin.setFixedWidth(100)
        self.input_contest_time_begincomo = QDateTimeEdit()
        # Three years ago, that is, the maximum age for entering the competition is three years. If you do not enter within three years, you will not be able to enter.
        self.input_contest_time_begincomo.setMinimumDate(QDate.currentDate().addDays(-1095))
        self.input_contest_time_begincomo.setCalendarPopup(True)
        input_contest_time_end = QLabel("End Time")
        input_contest_time_end.setFixedWidth(100)
        self.input_contest_time_endcomo = QDateTimeEdit()
        self.input_contest_time_endcomo.setMinimumDate(QDate.currentDate().addDays(-1095))
        self.input_contest_time_endcomo.setCalendarPopup(True)
        input_contest_time_in = QLabel("Award time")
        input_contest_time_in.setFixedWidth(100)
        self.input_contest_time_incomo = QDateTimeEdit()
        self.input_contest_time_incomo.setMinimumDate(QDate.currentDate().addDays(-1095))
        self.input_contest_time_incomo.setCalendarPopup(True)
        input_contest_time_layout.addWidget(input_contest_time_begin)
        input_contest_time_layout.addWidget(self.input_contest_time_begincomo)
        input_contest_time_layout.addWidget(input_contest_time_end)
        input_contest_time_layout.addWidget(self.input_contest_time_endcomo)
        input_contest_time_layout.addWidget(input_contest_time_in)
        input_contest_time_layout.addWidget(self.input_contest_time_incomo)
        input_contest_layout.addLayout(input_contest_time_layout)
        # add this tab bar
        input_tab.addTab(input_contest_widget, "Enter Contest")
            

    def center(self):
        """
        Get the length and width of the desktop Get the length and width of the window Calculate the position Move
        """
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()

    def closeEvent(self, event):
        result = QMessageBox.question(self, 'Leaving...','Do you want to exit?', QMessageBox.Yes | QMessageBox.No)
        if result == QMessageBox.Yes:

            event.accept()  
        else:
            event.ignore()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())