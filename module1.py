import sys, hashlib, sqlite3, re, PyQt5.QtGui
import qdarkstyle, datetime, webbrowser
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (QApplication, QSplitter, QGridLayout, QHBoxLayout, QPushButton, 
                            QTreeWidget, QFrame, QLabel, QHBoxLayout, QMainWindow,
                            QStackedLayout, QWidget, QVBoxLayout, QLineEdit, QRadioButton,
                            QTreeWidgetItem, QDesktopWidget, QTabWidget, QSpinBox, QComboBox,
                            QCalendarWidget, QDateTimeEdit, QMessageBox, QAbstractItemView,
                            QHeaderView, QTableWidget, QTableWidgetItem, QStyledItemDelegate,
                            QSizePolicy, QTextEdit, QScrollArea, QGroupBox)
from PyQt5.QtCore import Qt, QUrl, QDate
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon, QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
import numpy as np
import matplotlib.pyplot as plt

# blank interface for drawing
class MymplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=500, height=400):
        plt.style.use('fivethirtyeight')
        self.fig = Figure(figsize=(width, height))
        self.axes = self.fig.add_subplot(111) # Multi-interface drawing
        self.axes.yaxis.tick_right()
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, 
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )
        FigureCanvas.updateGeometry(self)

    # Drawing method of drawing class
    def plot_time(self, *args):
        # Modify font
        n_bins = 10
        x = np.arange(n_bins)
        y1, y2, y3, y4 = np.random.randint(1, 25, size=(4, n_bins))

        self.axes.clear()
        self.fig.suptitle("Tabulation: NCST MMA contest information statistics")
        width = 0.2
        self.axes.bar(x, y1, width = 0.2)
        self.axes.bar(x + width, y2, width = 0.2)
        self.axes.bar(x + width * 2, y3, width = 0.2)
        self.axes.bar(x + width * 3, y4, width = 0.2)
        self.axes.set_ylabel("Statistics of participants")
        self.axes.grid(True)
        self.draw()


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
        self.setWindowIcon(QIcon("d439.png"))

        # Set the window style
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

         # Set the overall layout to display left and right
        pagelayout = QGridLayout()

        # link sql and query
        try:
            self.db = sqlite3.connect('mathmodel.db')
            self.query = self.db.cursor()
        except:
            QMessageBox.critical(None, ("Could not open database"), ("SQlite support"), QMessageBox.Cancel)
            return False

        """
        The basic functions of the layout page are completed here
        The layout is divided into left and right sides, the left side is the button, the right side is the stack layout, and the page switching function of the mouse click is completed.
        The last two layouts are deployed in the splitter to complete the drag-and-drop interface variable size inside the page
        """

        """ Start layout on the left """
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
        self.input_btn = QPushButton("input information")
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
        space_btn = QPushButton("personal space")
        space_btn.setFixedSize(100, 30)
        button_layout.addWidget(space_btn)
        # exit button
        quit_btn = QPushButton(top_left_frame)
        quit_btn.setFixedSize(100, 30), quit_btn.setText("Quit")
        button_layout.addWidget(quit_btn)
        # Increase the spacing and beautify the interface
        button_layout.addStretch(1)

        """
        Start the layout on the right, click the button on the left, and correspond to different interfaces on the right
        The layout of each interface is introduced in detail
        """

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
        # Divided into super management and general management. Tourists do not have an account and cannot log in if the account password is wrong.
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
        
        """
        This is the page where ordinary administrators enter game information
        Modeling field input Modeling student blog information treeview control loading control options close or expand
        The built-in webengine library is not applicable, and the cache is not easy to get stuck. Choose to call the system browser to complete the loading.
        Competition entry Enter the competition information of three people (there is no primary key in the database): Student ID Name College Major Gender Teacher Competition Award Start time of the competition End time Award time
        """

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

        # Enter game information The player's information control is created using a dictionary
        # Because I want to enter the game information of three people, I chose a for loop instead of writing three times
        self.team = {}
        for i in range(1, 4):
            self.team['team_layout' + str(i)] = QHBoxLayout()
            self.team['team_id' + str(i)] = QLineEdit()
            self.team['team_id' + str(i)].setFixedWidth(230)
            self.team['team_id' + str(i)].setPlaceholderText("Please enter the student ID")
            self.team['team_name' + str(i)] = QLineEdit()
            self.team['team_name' + str(i)].setFixedWidth(220)
            self.team['team_name' + str(i)].setPlaceholderText("Please enter your name")
            self.team['team_price' + str(i)] = QComboBox()
            self.team['team_price' + str(i)].setFixedWidth(220)
            self.team['team_college' + str(i)] = QComboBox()
            self.team['team_major' + str(i)] = QComboBox()
            self.team['team_gender' + str(i)] = QComboBox()
            self.team['team_layout' + str(i)].addWidget(self.team['team_id' + str(i)])
            self.team['team_layout' + str(i)].addWidget(self.team['team_name' + str(i)])
            self.team['team_layout' + str(i)].addWidget(self.team['team_price' + str(i)])
            self.team['team_layout' + str(i)].addWidget(self.team['team_college' + str(i)])
            self.team['team_layout' + str(i)].addWidget(self.team['team_major' + str(i)])
            self.team['team_layout' + str(i)].addWidget(self.team['team_gender' + str(i)])
            input_contest_layout.addLayout(self.team['team_layout' + str(i)])

        # Prevent input errors from happening Add delete Modify button (easy to modify, the view here can be edited)
        # You can resubmit the database after modification, and the modification content is only the data entered this time, not the modification of historical data
        input_contest_button_layout = QHBoxLayout()
        input_contest_button_input = QPushButton("Confirm input of personnel information")
        input_contest_button_del = QPushButton("Confirm delete personnel information")
        input_contest_button_update = QPushButton("Confirm commit changes")
        input_contest_button_layout.addWidget(input_contest_button_input)
        input_contest_button_layout.addWidget(input_contest_button_del)
        input_contest_button_layout.addWidget(input_contest_button_update)
        input_contest_layout.addLayout(input_contest_button_layout)
        self.input_contest_info_table = QTableWidget()
        self.table['input_contest_info_table'] = self.input_contest_info_table
        input_contest_layout.addWidget(self.table['input_contest_info_table'])
        # Should be adding an interface to delete a person's historical data to be added

        """
        The interface for querying information can be queried only by the identity of the visitor, that is, only the administrator can enter the data, and other outsiders can only view it.
        Therefore, this part of the database should be loaded at the beginning
        """
        
        # search information
        output_tab = QTabWidget(right_frame)
        self.right_layout.addWidget(output_tab)
        output_year = QWidget()
        output_teacher = QWidget()
        output_sduent = QWidget()
        # Also divided into four tags
        output_tab.addTab(output_year, "Query by time")
        output_tab.addTab(output_teacher, "Query by teacher")
        output_tab.addTab(output_sduent, "Query by student")

        # Query by year The query content is
        # Comparison of the number of people in several competitions in one year Comparison of the total number of people in a competition over the years
        # Ordinary users can only see statistical pictures, administrators can save data when they click the button
        output_year_layout = QVBoxLayout()
        output_year.setLayout(output_year_layout)
        output_year_button_layout = QHBoxLayout()
        self.output_year_comobo = QComboBox()
        self.output_year_comobo.addItem("Select the game to query")
        self.output_year_comobo.setItemDelegate(self.delegate)
        output_year_oneyear = QPushButton("Number of participants in this year")
        output_year_allyear = QPushButton("Comparison of this competition over the years")
        output_year_button_layout.addWidget(self.output_year_comobo)
        output_year_button_layout.addWidget(output_year_oneyear)
        output_year_button_layout.addWidget(output_year_allyear)
        output_year_layout.addLayout(output_year_button_layout)
        # Add panels and toolbars for matplotlib plotting
        mpl_layout = QVBoxLayout()
        self.mpl = MymplCanvas(self)
        self.mpl_tool = NavigationToolbar(self.mpl, self)
        mpl_layout.addWidget(self.mpl)
        mpl_layout.addWidget(self.mpl_tool)
        mpl_scroll = QScrollArea()
        mpl_groupBox = QGroupBox()
        mpl_groupBox.setLayout(mpl_layout)
        mpl_scroll.setWidget(mpl_groupBox)
        mpl_scroll.setWidgetResizable(True)
        # Modify according to the actual situation

        self.mpl.setFixedWidth(5000)
        output_year_layout.addWidget(mpl_scroll)

        # Query by teacher
        output_teacher_layout = QVBoxLayout()
        output_teacher.setLayout(output_teacher_layout)
        self.output_teacher_comobo = QComboBox()
        self.output_teacher_result = QTextEdit()
        # The output query result is read-only and not writable
        self.output_teacher_result.setReadOnly(True)
        output_teacher_layout.addWidget(self.output_teacher_comobo)
        output_teacher_layout.addWidget(self.output_teacher_result)
        self.insert_teacher_comobo(self.output_teacher_comobo)
        
        # Query by student
        output_sduent_layout = QVBoxLayout()
        output_sduent.setLayout(output_sduent_layout)
        self.output_sduent_line = QLineEdit()
        self.output_sduent_line.setPlaceholderText("Enter student number and press Enter to query")
        self.output_sduent_result = QTextEdit()
        # Also read-only query
        self.output_sduent_result.setReadOnly(True)
        output_sduent_layout.addWidget(self.output_sduent_line)
        output_sduent_layout.addWidget(self.output_sduent_result)

        # Three interface, draggable
        self.splitter1 = QSplitter(Qt.Vertical)
        # top_left_frame.setFixedHeight(280)
        self.splitter1.addWidget(top_left_frame)
        self.splitter1.setMinimumWidth(150)
        self.splitter2 = QSplitter(Qt.Horizontal)
        self.splitter2.addWidget(self.splitter1)
        self.splitter2.setMinimumWidth(250)
        # Add the layout on the right
        self.splitter2.addWidget(right_frame)

        # widget add layout
        widget = QWidget()
        pagelayout.addWidget(self.splitter2)
        widget.setLayout(pagelayout)
        self.setCentralWidget(widget)

        """
        Here is the functional area, which completes the logic part of interacting with the user, and responds to the user's operation events.
        """

        """Show consistent pages"""
        # At the beginning, the interface of login information management information entry is not optional
        self.user_btn.setEnabled(False)
        self.register_btn.setEnabled(False)
        self.input_btn.setEnabled(False)
        # Authentication button Corresponding page: choose whether it is a visitor or an administrator
        verifyid_btn.clicked.connect(self.show_verifyid_page)
        # Log in to the corresponding page. If the login button can be shown to the visitor
        self.user_btn.clicked.connect(self.show_login_page)
        # This page can only be loaded once
        self.show_register_page_count = 0
        # Corresponding to the page of information management
        self.register_btn.clicked.connect(self.show_register_page)
        # Used to set the number of times to prevent multiple clicks. Load the data of the modeling field multiple times. Just load it once
        self.page_count = 1
        # Corresponding to the page of the modeling field
        friend_btn.clicked.connect(self.show_friend_page)
        # Corresponding to the page for entering information
        self.input_btn.clicked.connect(self.show_input)
        # Treeview's click event After clicking, the system browser is called to load the page
        self.friend_tree.clicked.connect(self.show_firend_web)
        # The page corresponding to the query information
        query_btn.clicked.connect(self.show_output)
        # Corresponding to the exit page
        quit_btn.clicked.connect(self.quit_act)

        """ Logic function corresponding to the button"""

        # The initial confirmation identity radio button can only select one judgment state
        self.radio_btn_user.toggled.connect(self.change_status)
        self.radio_btn_admin.toggled.connect(self.change_status)

        # Click the button, the super administrator will delete the ordinary administrator
        register_btn_del.clicked.connect(self.del_admin)

        # After clicking the login button, you need to link the database to confirm whether the password is correct
        login_btn_confirm.clicked.connect(self.confirm_password)

        # When applying for a general administrator, insert the information into the database
        self.register_confirm_btn.clicked.connect(self.insert_admin)

        # Teacher management tab under the information management page. After confirming the account of applying for the teacher, the data table is displayed. The default state is not displayed.
        teacher_input_btn_confirm.clicked.connect(self.input_teacher_info)
        # After clicking the button, delete the teacher account
        teacher_input_btn_del.clicked.connect(self.delete_teacher_info)
        # Make sure to delete college and professional information
        colleage_major_del_btn.clicked.connect(self.del_college_major)

        # Information management page Under the competition management tab, click to insert a competition. When deleting a competition, the data table that displays the competition information is not displayed by default.
        manage_contest_button_input.clicked.connect(self.process_contest)
        manage_contest_button_del.clicked.connect(self.process_contest)

        # Under the information management page, the colleges and majors are displayed in a double-column form. Click the college to query the corresponding major of the college.
        self.table['colleage_major_twoside'].clicked.connect(self.show_major)

        # The college major management tab under the information management page Set the number of tags to count the number of the last major. The next time it is displayed, it will be cleared and displayed, so it needs to be counted
        self.major_count = 0
        # College and major management tab under the information management page Insert, college and major information
        self.colleage_major_input_btn.clicked.connect(self.insert_college_major)
        # Insert the content of the college and major inserted before it is allowed to be inserted, otherwise it will be repeated
        self.colleage_major_info_college.textChanged.connect(self.enable_colleage_major_input_btn)
        self.colleage_major_info_major.textChanged.connect(self.enable_colleage_major_input_btn)

        # Under the information entry page, enter and delete the modeling student blog
        input_friend_button.clicked.connect(self.insert_stublog)
        del_friend_button.clicked.connect(self.del_friend_table)

        # Enter the information page Select the game specified by the super administrator from the comobox
        self.input_contest_class.setItemDelegate(self.delegate)
        
        # Entry information page Select teacher information from (comobox)
        self.insert_teacher_comobo(self.input_contest_teacher_name)

        # Information query page shows matplotlib drawing after clicking the button
        output_year_oneyear.clicked.connect(self.draw_one_year)
        output_year_allyear.clicked.connect(self.draw_all_year)

        # When the general administrator inserts the row number of the statistical table, when new data is input again, it is appended after the original data
        self.input_contest_row_count = 0
        # Insert information of ordinary administrators Insert three people at a time
        input_contest_button_input.clicked.connect(self.input_contest_one)
        # delete only one
        input_contest_button_del.clicked.connect(self.del_contest_one)
        # In order to facilitate the input of the administrator, the table is set to be editable. After editing, click Update to complete the update of the database side.
        input_contest_button_update.clicked.connect(self.update_contest_info)

        # Here is the entered data for the competition and gender selection box on the information entry page
        # This part of the data is not confidential, so it can be loaded directly when the software is running and leaked into memory
        # Academy of three players
        for i in range(1, 4):
            self.query.execute("select * from college")
            colleges = self.query.fetchall()
            self.team["team_college" + str(i)].setItemDelegate(self.delegate)
            self.team["team_major" + str(i)].setItemDelegate(self.delegate)
            self.team["team_college" + str(i)].addItem("")
            for college_name in colleges:
                college_ = str(college_name[0])
                self.team["team_college" + str(i)].addItem(college_)
        
        # The gender of the three players
        for i in range(1, 4):
            self.team["team_gender" + str(i)].setFixedWidth(50)
            self.team["team_gender" + str(i)].setItemDelegate(self.delegate)
            for gender in ['male', 'female']:
                self.team["team_gender" + str(i)].addItem(gender)

        # When the college changes, the major changes, that is, only a few majors corresponding to the college can be seen to reduce the search volume of majors
        self.team["team_college1"].currentIndexChanged.connect(self.change_major1)
        self.team["team_college2"].currentIndexChanged.connect(self.change_major2)
        self.team["team_college3"].currentIndexChanged.connect(self.change_major3)

        # When the competition changes, the awards follow the change
        self.input_contest_class.currentIndexChanged.connect(self.select_contest_class)

        # Double-click on the table to trigger an edit event to determine whether it is empty.
        # Empty: Indicates entering information in a blank cell This is not allowed
        # Non-empty: Indicates that there is content in the cell and can be edited at this time
        self.table['input_contest_info_table'].cellDoubleClicked.connect(self.confirm_update)

        # Query page Enter the student number of the student and press Enter to query
        self.output_sduent_line.returnPressed.connect(self.query_sdu)

        # Query by teacher Triggered when the teacher drop-down box is changed
        self.output_teacher_comobo.currentTextChanged.connect(self.query_teacher)

    # Information input interface
    def select_contest_class(self):
        """
        The name of the competition selected according to input_contest_class corresponds to the award of the competition
        """
        if self.input_contest_class.currentText() == 'National Undergraduate Mathematical Contest in Modeling':
            for i in range (1, 4):
                self.team['team_price' + str(i)].setItemDelegate(self.delegate)
                self.team['team_price' + str(i)].addItem('National First Prize')
                self.team['team_price' + str(i)].addItem('National Second Prize')
                self.team['team_price' + str(i)].addItem('Provincial First Prize')
                self.team['team_price' + str(i)].addItem('Provincial Second Prize')
                self.team['team_price' + str(i)].addItem('Successful entry award')
        if self.input_contest_class.currentText() == 'American Mathematical Contest in Modeling':
            for i in range (1, 4):
                self.team['team_price' + str(i)].setItemDelegate(self.delegate)
                self.team['team_price' + str(i)].addItem('Outstanding Winner')
                self.team['team_price' + str(i)].addItem('Finalist')
                self.team['team_price' + str(i)].addItem('Meritorious Winner')
                self.team['team_price' + str(i)].addItem('Honorable Mention')
                self.team['team_price' + str(i)].addItem('Successful Participant')
                self.team['team_price' + str(i)].addItem('Unsuccessful Participant')
                self.team['team_price' + str(i)].addItem('Disqualified')

    # Information management Information input interface
    def init_table(self, string = ''):
        """
        Because multiple interfaces involve the initialization of the table, it is encapsulated into a function
        Put all tables into a dictionary Call the object according to the ID of the dictionary Add a string parameter to judge the calling object
        It's just that the location where the initialization form is called is different. When the form can be displayed also requires strict logic.
        """
        
        # None of the vertical headers are displayed
        self.table[string].verticalHeader().setVisible(False)

        # Uneditable Modeling Corner Competition Management Teacher Management General Admin Management
        # The view is only for observation and cannot be modified. Tableview can be used, and tablewidget can also be used
        if string in ['input_friend_table', 'contest_info_table', 'teacher_table', 'registor_table']:
            self.table[string].setEditTriggers(QAbstractItemView.NoEditTriggers)

        # view the entire row selected
        if string in ['input_friend_table', 'input_contest_info_table', 'contest_info_table', 'teacher_table']:
            self.table[string].setSelectionBehavior(QAbstractItemView.SelectRows)

        # Adaptive scaling cannot use elif
        if string in ['input_friend_table', 'contest_info_table', 'colleage_major_twoside', 'teacher_table', 'registor_table']:
            self.table[string].horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        if string == 'input_friend_table':
            # Blog form
            self.table[string].setColumnCount(2)
            self.table[string].setRowCount(1000)
            self.table[string].setHorizontalHeaderLabels(['person','other information'])

        elif string == 'input_contest_info_table':
            # Enter the form for the game
            self.table[string].setColumnCount(11)
            self.table[string].setRowCount(1000)
            self.table[string].setHorizontalHeaderLabels(['student number','name','college','major','gender','start time','end time','award time'
                , 'Instructor', 'Competition', 'Award Level'])
            self.table[string].setColumnWidth(0, 150)
            self.table[string].setColumnWidth(1, 150)
            self.table[string].setColumnWidth(2, 200)
            self.table[string].setColumnWidth(3, 200)
            self.table[string].setColumnWidth(4, 80)
            self.table[string].setColumnWidth(5, 150)
            self.table[string].setColumnWidth(6, 150)
            self.table[string].setColumnWidth(7, 150)
            self.table[string].setColumnWidth(8, 150)
            self.table[string].setColumnWidth(9, 300)
            self.table[string].setColumnWidth(10, 100)

        elif string == 'contest_info_table':
            # Forms for competition management
            self.table[string].setFixedHeight(400)
            # self.contest_info_table.setFixedHeight
            self.table[string].setRowCount(100)
            self.table[string].setColumnCount(3)
            self.table[string].setHorizontalHeaderLabels(['Organizer','Competition level','Competition name'])

        elif string == 'colleage_major_twoside':
            # Information management page Forms for college majors
            self.table[string].setColumnCount(2)
            self.table[string].setRowCount(50)
            self.table[string].setHorizontalHeaderLabels(['College','Professional'])

        elif string == 'teacher_table':
            # Information management page Teacher's form
            self.table[string].setFixedHeight(400)
            self.table[string].setRowCount(100)
            self.table[string].setColumnCount(3)
            self.table[string].setHorizontalHeaderLabels(['teacher name','teacher college','teacher job number'])

        elif string == 'register_table':
            # If it is the information management page, watch the form of ordinary administrators
            # A total of 100 rows and 1 column
            self.table[string].setRowCount(100)
            self.table[string].setColumnCount(1)
            self.table[string].setHorizontalHeaderLabels(['account name'])

    # Query the teacher's guidance in the query interface
    def query_teacher(self):
        """
        Input: The teacher's ID number selected in the combobox
        Output: Query the situation of this teacher guiding the game
        """
        flag = 0
        info_ = self.output_teacher_comobo.currentText()
        self.query.execute("select * from sducontest where teacher = \"{}\"".format(info_))
        results = self.query.fetchall()
        if len(results) == 0:
            self.output_teacher_result.setText("No information yet")
        else:
            string = ""
            for result in results:
                # Student ID is not output
                for i in result:
                    string += i
                    string += " "
                string += "\n"
            self.output_teacher_result.setText(string)

   # Query the teacher's guidance in the query interface
    def query_teacher(self):
        """
        Input: The teacher's ID number selected in the combobox
        Output: Query the situation of this teacher guiding the game
        """
        flag = 0
        info_ = self.output_teacher_comobo.currentText()
        self.query.execute("select * from sducontest where teacher = \"{}\"".format(info_))
        results = self.query.fetchall()
        if len(results) == 0:
            self.output_teacher_result.setText("No information yet")
        else:
            string = ""
            for result in results:
                # Student ID is not output
                for i in result:
                    string += i
                    string += " "
                string += "\n"
            self.output_teacher_result.setText(string)

    # Query the student participation status label in the query interface
    def query_sdu(self):
        """
        Input: student number or name Input illegal reminder: invalid input
        Output: output the student's name, gender, student number (including grade), major, award status (including instructors), QQ number (whether to output, only the administrator can see)
        """
        # Check for valid input
        flag = 0
        info_ = self.output_sduent_line.text()
        if (str.isdigit(info_)):
            self.query.execute("select * from sducontest where id = \"{}\"".format(info_))
            results = self.query.fetchall()
        elif (str.isalpha(info_)):
            self.query.execute("select * from sducontest where name = \"{}\"".format(info_))
            results = self.query.fetchall()
        else:
            QMessageBox.information(None, ("Friendly reminder"), ("Invalid input"), QMessageBox.Cancel)
            flag = 1
        if flag == 0:
            string = ""
            # have query results
            if len(results) != 0:
                for result in results:
                    # Student ID is not output
                    for i in result:
                        string += i
                        string += " "
                    string += "\n"
                self.output_sduent_result.setText(string)
            else:
                self.output_sduent_result.setText("No such person found")

    def insert_contest_combo(self, a):
        """
        a is the calling object
        Because of the information management, the combox of entering the competition and querying the competition need to be added to the competition box to avoid code duplication. This part of the program is encapsulated as a function
        contest is the data table of the contest
        """
        a.clear()
        self.query.execute("select * from contest")
        rows = self.query.fetchall()
        for row in rows:
            item = str(row[2])
            a.addItem(item)

    # The entry competition label of the entry information interface
    def confirm_update(self):
        """
        Determine whether the currently edited table item is empty
        If it is empty, the prompt cannot be modified and the table is set as uneditable
        If not empty, double-click event is allowed to cancel the uneditable state of the table. Alledittriggers are not available.
        """
        item = self.table['input_contest_info_table'].currentItem()
        try:
            text = item.text()
            # Allow table editing Cancel uneditable events that may have been set last time
            self.table['input_contest_info_table'].setEditTriggers(QAbstractItemView.DoubleClicked)
        except :
            QMessageBox.information(None, ("Friendly reminder"), ("Empty content cannot be modified, only existing content can be modified"), QMessageBox.Cancel)
            self.table['input_contest_info_table'].setEditTriggers(QAbstractItemView.NoEditTriggers)

    # The entry competition label of the entry information interface
    def update_contest_info(self):
        """
        Get the modified part Submit the modified form to the database Complete the modification
        """
        # self.input_contest_info_table
        pass

    # The entry competition label of the entry information interface
    def del_contest_one(self):
        """
        Delete the selected match. There is no need to delete the information of three people because of one person's input error.
        """
        # self.input_contest_info_table
        pass

    # The entry competition label of the entry information interface
    def del_contest_one(self):
         """
         Delete the selected match. There is no need to delete the information of three people because of one person's input error.
         """
         # self.input_contest_info_table
         pass

     # The entry competition label of the entry information page
    def input_contest_one(self):
         """
         Create an empty list and add the information of the three players (1, 4) because the initial dictionary is set up for this index
         After adding, insert it into the database and display it in the table
         """
         # Student ID Name College Major Gender Start Time End Time Award Time Teacher Competition Name Award Level
    id_, name_, college_, major_, gender_, begin_time, end_time, in_time, teacher_, contest_, class_ \
            = [], [], [], [], [], [], [], [], [], [], [] 
    for i in range(1, 4):
            id_.append(self.team['team_id' + str(i)].text())
            name_.append(self.team['team_name' + str(i)].text())
            college_.append(self.team['team_college' + str(i)].currentText())
            major_.append(self.team['team_major' + str(i)].currentText())
            gender_.append(self.team['team_gender' + str(i)].currentText())
            begin_time.append(self.input_contest_time_begincomo.date().toString(Qt.ISODate))
            end_time.append(self.input_contest_time_endcomo.date().toString(Qt.ISODate))
            in_time.append(self.input_contest_time_incomo.date().toString(Qt.ISODate))
            teacher_.append(self.input_contest_teacher_name.currentText())
            contest_.append(self.input_contest_class.currentText())
            class_.append(self.team['team_price' + str(i)].currentText())
    for i in range (3):
            self.query.execute("insert into sducontest(id, name, college, major, gender, begin_time, end_time, in_time, teacher, \
                contest, price) values(\"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\")" \
                .format(id_[i], name_[i], college_[i], major_[i], gender_[i], begin_time[i], \
                end_time[i], in_time[i], teacher_[i], contest_[i], class_[i]))
            self.db.commit()
            # The number of lines is automatically incremented when displayed to ensure that each addition is added after the last addition
            self.table['input_contest_info_table'].setItem(self.input_contest_row_count, 0, QTableWidgetItem(id_[i]))
            self.table['input_contest_info_table'].setItem(self.input_contest_row_count, 1, QTableWidgetItem(name_[i]))
            self.table['input_contest_info_table'].setItem(self.input_contest_row_count, 2, QTableWidgetItem(college_[i]))
            self.table['input_contest_info_table'].setItem(self.input_contest_row_count, 3, QTableWidgetItem(major_[i]))
            self.table['input_contest_info_table'].setItem(self.input_contest_row_count, 4, QTableWidgetItem(gender_[i]))
            self.table['input_contest_info_table'].setItem(self.input_contest_row_count, 5, QTableWidgetItem(begin_time[i]))
            self.table['input_contest_info_table'].setItem(self.input_contest_row_count, 6, QTableWidgetItem(end_time[i]))
            self.table['input_contest_info_table'].setItem(self.input_contest_row_count, 7, QTableWidgetItem(in_time[i]))
            self.table['input_contest_info_table'].setItem(self.input_contest_row_count, 8, QTableWidgetItem(teacher_[i]))
            self.table['input_contest_info_table'].setItem(self.input_contest_row_count, 9, QTableWidgetItem(contest_[i]))
            self.table['input_contest_info_table'].setItem(self.input_contest_row_count, 10, QTableWidgetItem(class_[i]))
            self.input_contest_row_count += 1

    # Enter the competition label of the entry information tab
    def change_major(self):
        """
        A college must be selected before a major can be selected. After modifying the college, call this function to query the corresponding major and add it to the combox to make the major correspond to the college
        Return majors are all the majors corresponding to the college
        """
        sender = self. sender()
        college_ = sender.currentText()
        self.query.execute("select major_name from major where college_name = \"{}\"".format(college_))
        majors = self.query.fetchall()
        return majors

    def change_major3(self):
        """
        When the college of the third player changes, query the corresponding major
        clear is to clear the last query result, only the current query content can be captured
        """
        self.team["team_major3"].clear()
        majors = self.change_major()
        for major_name in majors:
            major_ = str(major_name[0])
            self.team["team_major3"].addItem(major_)

    # Same as above Query the profession of the second player
    def change_major2(self):
        self.team["team_major2"].clear()
        majors = self.change_major()
        for major_name in majors:
            major_ = str(major_name[0])
            self.team["team_major2"].addItem(major_)

    # Same as above Query the major of the first player
    def change_major1(self):
        majors = self.change_major()
        self.team["team_major1"].clear()
        for major_name in majors:
            major_ = str(major_name[0])
            self.team["team_major1"].addItem(major_)
        
    # Delete college professional information on the information management page
    def del_college_major(self):
        """
        todo: (should make editable and then update, not delete and enter again)
        Input: item gets the content of the current item pos judges whether the current item is a college or a major according to the location. Selecting an empty line prompt has no effect.
        Response: Show the Faculty after the Faculty is removed and the Major after it is removed.
        """
        item = self.table['colleage_major_twoside'].currentItem()
        pos = self.table['colleage_major_twoside'].currentColumn()
        try:
            info = item.text()
            if pos == 0:
                self.query.execute("delete from college where name = \"{}\"".format(info))
                self.db.commit()
                self.show_college(self.table['colleage_major_twoside'])
            if pos == 1:
                self.query.execute("delete from major where major_name = \"{}\"".format(info))
                self.db.commit()
                self.show_major()
        # clear
        except:
            QMessageBox.information(None, ("Friendly Reminder"), ("Please do not select a blank line"), QMessageBox.Cancel)

    # School of Management and Majors tab of the information management page
    def enable_colleage_major_input_btn(self):
        """
        Can only be entered if the college or major has changed, otherwise it cannot be entered
        """
        self.colleage_major_input_btn.setEnabled(True)

    # School of Management and Majors tab of the information management page
    def insert_college_major(self):
        """
        Input: College name and major name
        Response: If the college is not empty, insert the corresponding college name and major name. Otherwise, prompt: You cannot enter if you do not select a college
        """
        college_name = self.colleage_major_info_college.text()
        major_name = self.colleage_major_info_major.text()
        if major_name != "":
            self.query.execute("insert into major values(\"{}\", \"{}\")".format(major_name, college_name))
        elif major_name == "":
            QMessageBox.information(None, ("Friendly Reminder"), ("Please select a college before entering a major"), QMessageBox.Cancel)
        self.db.commit()
        self.show_college(self.table['colleage_major_twoside'])
        self.show_major()
        self.colleage_major_input_btn.setEnabled(False)

    # Display majors under the Major Management tab of the School of Information Management
    def show_major(self):
        """
        pos judges whether the current input is a college or a major according to the location
        If it is a college, clear the major column before displaying the major corresponding to the college, and then display it, otherwise it will not respond.
        """
        pos = self.table['colleage_major_twoside'].currentColumn()
        if pos == 0:
            for i in range(self.major_count + 1):
                item = QTableWidgetItem("")
                self.table['colleage_major_twoside'].setItem(i, 1, item)
        item = self.table['colleage_major_twoside'].currentItem()
        try:
            college_info = item.text()
            self.query.execute("select major_name from major where college_name = \"{}\"".format(college_info))
            rows = self.query.fetchall()
            for row in rows:
                inx = rows.index(row)
                # Record the current professional number for the next clearing
                self.major_count = inx
                major_name = QTableWidgetItem(row[0])
                self.table['colleage_major_twoside'].setItem(inx, 1, major_name)
        # Colleges corresponding to blank lines cannot display majors
        except:
            QMessageBox.information(None, ("Friendly Reminder"), ("Please do not select an empty line, it cannot display professional"), QMessageBox.Cancel)

    # College Professional Management tab under the information management page
    # The entry competition label in the entry information
    def show_college(self, a):
        """
        If it is an information management page, it is a Qtablewidget object, which is set to be displayed in the table at this time.
        If it is the input information interface, it is the Qcombobox object. At this time, it is set to add the college to the drop-down box.
        """
        self.query.execute("select * from college")
        rows = self.query.fetchall()
        self.pattern = re.compile("'(.*)'")
        # Input information interface call
        if isinstance(a, QComboBox):
            a.setItemDelegate(self.delegate)
            for row in rows:
                i = self.pattern.findall(str(row))
                a.addItem(i[0])
        # Information management interface call
        if isinstance(a, QTableWidget):
            for row in rows:
                inx = rows.index(row)
                college_name = QTableWidgetItem(row[0])
                self.table['colleage_major_twoside'].setItem(inx, 0, college_name)

    # Enter the teacher information in the competition
    def insert_teacher_comobo(self, a):
        """
        Select a teacher through the drop-down list (with a job number, the teacher is guaranteed to be unique)
        """
        self.query.execute("select * from teacher")
        rows = self.query.fetchall()
        a.setItemDelegate(self.delegate)
        for row in rows:
            item = str(row[0]) + "--" + str(row[2])
            a.addItem(item)

    # Query by game on the information query page
    def draw_one_year(self):
        """
        Input: The selection is a certain year, no competition is selected
        Output: The chart of the total number of participants this year under the selected year
        """
        # pass
        self.mpl.plot_time()

    # Query by game on the information query page
    def draw_all_year(self):
        """
        Enter: select a race, do not select a year
        Output: A graph of the historical number of participants for this competition
        """
        # pass
        self.mpl.plot_time()

    # Modeling field label under the information input interface
    def del_friend_table(self):
         """
         Select the content to be deleted and click delete to delete it in the database according to the url (primary key)
         There is no need to join to judge whether there is or not. If not, it will not be displayed. Because it can only be displayed after querying the database
         """
         row_num = -1
         for i in self.table['input_friend_table'].selectionModel().selection().indexes():
             row_num = i.row()
         if self.table['input_friend_table'].item(row_num, 0):
             del_id = self.table['input_friend_table'].item(row_num, 1).text()
             # delete only in view
             self.table['input_friend_table'].removeRow(row_num)
             # delete from the database
             self.query.execute("delete from sdublog where url = '%s'" % del_id)
             self.db.commit()
             QMessageBox.information(None, ("Friendly reminder"), ("Deletion completed"), QMessageBox.Ok)
         self.show_firend_table()

    # Modeling field label under the information input interface
    def show_firend_table(self):
        """
        In conjunction with the del_friend_table function and the insert_stublog function, it must be executed before the two functions are executed
        Only displayed first, can be selected and deleted
        """
        self.query.execute("select * from sdublog")
        rows = self.query.fetchall()
        for row in rows:
            inx = rows.index(row)
            name = QTableWidgetItem(row[0])
            self.table['input_friend_table'].setItem(inx, 0, name)
            info_ = QTableWidgetItem(row[1])
            self.table['input_friend_table'].setItem(inx, 1, info_)

    # Modeling field label under the information input interface
    def insert_stublog(self):
        """
        Input: Name URL (primary key cannot be repeated) Grade Major (free input) Personalized signature Highest award
        And the domain name is empty and cannot be inserted. After inserting into database and displaying in table.
        """
        name = self.input_friend_name.text()
        url = self.input_friend_url.text()
        # Can avoid the trouble of setting the button to be available or unavailable
        if url == "":
            QMessageBox.information(None, ("Friendly reminder"), ("URL cannot be empty"), QMessageBox.Ok)
        else:
            grade = str(self.input_friend_class.value())
            sign = self.input_friend_sign.text()
            price = self.input_friend_price.text()
            self.query.execute("INSERT INTO sdublog VALUES(\"{}\", \"{}\", \"{}\", \"{}\", \"{}\")".
                format(name, url, grade, sign, price))
            self.db.commit()
            # display visualization in table
            self.show_firend_table()
            # Because the setting is to display the table first, there can be existing data, whether it is duplicated with the existing URL
            self.input_friend_url.setPlaceholderText("The domain name cannot be empty when reinserting, and cannot be repeated with the existing one")

    # Competition management tab of the information management page
    def show_contest(self):
        """
        Show all competitions in a table under the current tab
        todo: all places involved in competition are added
        """
        self.query.execute("select * from contest")
        rows = self.query.fetchall()
        for row in rows:
            # print(row)
            inx = rows.index(row)
            column = 0
            for i in row:
                item = QTableWidgetItem(i)
                self.table['contest_info_table'].setItem(inx, column, item)
                column = column + 1

    # Competition management tab of the information management page
    def process_contest(self):
        """
        If the button clicked is to enter the contest then enter and display the result
        If the button clicked is to delete the match, delete it and show the result
        """
        sender = self. sender()
        text = sender.text()
        if text == 'Enter match':
            sponsor = self.contest_input_sponsor_line.text()
            class_ = self.contest_input_class_line.text()
            id_ = self.contest_input_id_line.text()
            self.query.execute("INSERT INTO contest VALUES(\"{}\", \"{}\", \"{}\")".format(sponsor, class_, id_))
            self.db.commit()
            self.show_contest()
        if text == 'delete match':
            row_num = -1
            for i in self.table['contest_info_table'].selectionModel().selection().indexes():
                row_num = i.row()
            if self.table['contest_info_table'].item(row_num, 0):
                del_id = self.table['contest_info_table'].item(row_num, 2).text()
                # delete from the database
                self.query.execute("delete from contest where id = '%s'" % del_id)
                self.db.commit()
                QMessageBox.information(None, ("Friendly reminder"), ("Deletion completed"), QMessageBox.Ok)
                self.show_contest()
        
    # Teacher information management on the information management page
    def delete_teacher_info(self):
        """
        The information of the selected teacher in the table is deleted according to the job number
        """
        row_num = -1
        for i in self.table['teacher_table'].selectionModel().selection().indexes():
            row_num = i.row()
        if self.table['teacher_table'].item(row_num, 0):
            del_id = self.table['teacher_table'].item(row_num, 2).text()
            # remove from view
            self.table['teacher_table'].removeRow(row_num)
            # delete from the database
            self.query.execute("delete from teacher where id = '%s'" % del_id)
            self.db.commit()
            QMessageBox.information(None, ("Friendly reminder"), ("Deletion completed"), QMessageBox.Ok)
        self.show_teacher()

    # Teacher information management on the information management page
    def show_teacher(self):
        """
        Display teacher information in a table on the current page
        todo: this function is loaded wherever teachers are involved
        """
        self.query.execute("select * from teacher")
        rows = self.query.fetchall()
        for row in rows:
            # print(row)
            inx = rows.index(row)
            column = 0
            for i in row:
                item = QTableWidgetItem(i)
                self.table['teacher_table'].setItem(inx, column, item)
                column = column + 1

    # Teacher information management on the information management page
    def input_teacher_info(self):
        """
        Insert teacher information After inserting, call the show_teacher function to complete the display
        In addition, it is also related to the query interface and the information entry interface
        """
        name = self.teacher_input_name_line.text()
        college = self.teacher_input_college_como.currentText()
        id = self.teacher_input_id_line.text()
        self.query.execute("INSERT INTO teacher VALUES(\"{}\", \"{}\", \"{}\")".format(name, college, id))
        self.db.commit()
        self.show_teacher()
        # Associate the teacher information in the query interface
        self.insert_contest_combo(self.output_year_comobo)
        # Associate the teacher information in the input interface
        self.insert_contest_combo(self.input_contest_class)

    # Account management tab under the information management interface
    def del_admin(self):
        """
        Account for deleting unused administrators
        Wuyuhang's super administrator account cannot be deleted
        """
        row_num = -1
        for i in self.table['registor_table'].selectionModel().selection().indexes():
            row_num = i.row()
        if self.table['register_table'].item(row_num, 0):
            del_id = self.table['register_table'].item(row_num, 0).text()
            if del_id != "wuyuhang@admin":
                # delete only in view
                self.table['register_table'].removeRow(row_num)
                # delete from the database
                self.query.execute("delete from admin where id = '%s'" % del_id)
                self.db.commit()
                QMessageBox.information(None, ("Friendly reminder"), ("Deletion completed"), QMessageBox.Ok)
            else:
                QMessageBox.information(None, ("Friendly reminder"), ("This account cannot be deleted"), QMessageBox.Ok)

    # Account management tab under the information management interface
    def insert_admin(self):
        """
        Register a general administrator account with the competition department or the information department
        Verify password: The password entered twice can only be registered, and the registration is inserted into the database
        And the password is stored in the database in the form of md5 encryption to prevent password leakage
        """
        in_id = self.register_id.text()
        psd = self.register_psd.text()
        confirm_psd = self.register_confirm.text()
        ls = []
        for row in self.query.execute("select id from admin where id = '%s'" % in_id):
            ls.append(row)
        if len(ls) != 0:
            QMessageBox.information(None, ("Friendly Reminder"), ("This account has already been registered, please register again"), QMessageBox.Cancel)
        elif psd != confirm_psd:
            QMessageBox.information(None, ("Friendly reminder"), ("The passwords entered twice are inconsistent"), QMessageBox.Cancel)
        else:
            # Add a logical judgment that the password is not empty
            if psd == confirm_psd and in_id != "" and psd != "":
                # Password encrypted and inserted into the database
                if self.query.execute("INSERT INTO admin VALUES(\"{}\", \"{}\")".format(in_id,
                        hashlib.md5(psd.encode('utf-8')).hexdigest())):
                    QMessageBox.information(None, ("Friendly Reminder"), ("Registration Successful"), QMessageBox.Ok)
                    self.db.commit()
                else:
                    QMessageBox.information(None, ("Friendly Reminder"), ("Registration Failed"), QMessageBox.Cancel)
        self.show_admin()

    # login interface
    def confirm_password(self):
        """
        Connect to the database to verify that the password is correct If the password is incorrect, you cannot log in
        When verifying the password, the password also needs to be encrypted by md5 to verify whether it is the same as the one stored in the database.
        If verified as a super administrator, open the information management interface and input information interface
        If the verification is an ordinary administrator, the information management interface will not be opened, only the input information interface will be opened.
        """
        self.register_btn.setEnabled(False)
        in_userid = self.user_line.text()
        in_psd = hashlib.md5(self.password_line.text().encode('utf-8')).hexdigest()
        # super administrator
        # self.query.execute("SELECT * FROM admin ")
        self.query.execute("SELECT * FROM admin WHERE id = '%s'" % in_userid)
        info = self.query.fetchall()
        if info:
            # super administrator
            if self.user_line.text() == 'wuyuhang@admin':
                if in_psd == info[0][1]:
                    self.register_btn.setEnabled(True)
                    self.input_btn.setEnabled(True)
                else:
                    QMessageBox.information(None, ("Friendly reminder"), ("Wrong password input"), QMessageBox.Cancel)
            # Ordinary administrator
            else:
                if in_psd == info[0][1]:
                    self.input_btn.setEnabled(True)
                else:
                    QMessageBox.information(None, ("Friendly reminder"), ("Wrong password input"), QMessageBox.Cancel)

    # Confirm identity interface
    def change_status(self):
        """
        Tourist identity: login information management All input information interfaces are closed
        Manage identity: only open the login interface
        """
        if self.radio_btn_user.isChecked():
            self.user_btn.setEnabled(False)
            self.register_btn.setEnabled(False)
            self.input_btn.setEnabled(False)
        else:
            self.user_btn.setEnabled(True)

    # Query the size settings of the information page
    def show_output(self):
        self.setFixedSize(1800, 1000)
        self.center()
        self.right_layout.setCurrentIndex(5)
        self.insert_contest_combo(self.output_year_comobo)

    # input info page
    def show_input(self):
        """
        Takes up a lot of space, so full screen and loading forms
        """
        screen = QDesktopWidget().screenGeometry()
        self.setFixedSize(screen.width(), screen.height())
        self.center()
        self.right_layout.setCurrentIndex(4)
        # Initialize the form for entering the blog
        self.init_table('input_friend_table')
        # Initialize the form for entering the game
        self.init_table('input_contest_info_table')
        self.show_firend_table()
        self.insert_contest_combo(self.input_contest_class)

    # Button click Called when switching pages
    def init(self):
        """
        Reinitialize the size of the current page
        Pay attention to the order, resize in the front will make the code invalid
        """
        # Have to set these two in advance
        self.splitter1.setMinimumWidth(150)
        self.splitter2.setMinimumWidth(250)
        self.setFixedSize(600, 400)

    # Modeling garden interface
    def show_firend_web(self):
        """
        TreeView's click event webengine is easy to crash, you need to adjust the system browser
        The browser opens the selected URL
        """
        item = self.friend_tree.currentItem()
        # Because the current item is a combination of name and URL, you need to separate the URL with spaces
        url = item.text(1).split(" ")[1]
        # Add logical judgment
        if url[:4] == "http":
            webbrowser.open(url)

    # Modeling garden interface
    def show_friend_page(self):
        """
        Connect to the database (connect only once), query the grade of the student, and construct the tree structure according to the grade, that is, put the 16th level together and the 17th level together
        When querying the database: query all grade distributions create a root node
        Query all students divided by grade to the corresponding root node and join
        """
        self.right_layout.setCurrentIndex(3)
        self.init()
        self.setFixedSize(960, 650)
        self.center()
        self.page_count += 1
        if self.page_count == 2:
            # Load the blog database
            self.query.execute("SELECT DISTINCT grade FROM sdublog")
            rows = self.query.fetchall()
            ls = []
            for j in rows:
                ls.append(str(j[0]))
                locals() ['child_' + str(j[0])] = QTreeWidgetItem(self.friend_tree)
                locals() ['child_' + str(j[0])].setText(0, str(j[0]) + 'level')
            self.query.execute("select * from sdublog")
            rows = self.query.fetchall()
            key = 0
            string = ""
            for row in rows:
                locals() ['child_' + str(row[2]) + '_' + str(key)] = QTreeWidgetItem(locals() ['child_' + str(row[2])])
                for j in row:
                    # Add spaces between different items to beautify the display
                    if str(j) not in ls:
                        string += (str(j) + ' ')
                locals() ['child_' + str(row[2]) + '_' + str(key)].setText(1, string)
                key += 1
                string = ""

    # Information management page
    def show_register_page(self):
        """
        Multiple clicks are loaded only once, otherwise there will be a segfault
        This page is loaded to display General Admin Management Academy Professional Management Teacher Information Management and Competition Management
        """
        self.init()
        self.setFixedSize(1000, 700)
        self.center()
        self.right_layout.setCurrentIndex(2)
        if self.show_register_page_count == 0:
            self.show_register_page_count += 1
            # Initialize the normal admin table
            self.init_table('register_table')
            # Initialize teacher management form and display
            self.init_table('teacher_table')
            self.show_teacher()
            # Initialize the college professional management table
            self.init_table('colleage_major_twoside')
            # Initialize the form for competition management
            self.init_table('contest_info_table')
            # College query on the information management page
            self.show_college(self.table['colleage_major_twoside'])
            # When inserting a teacher in the information management page, select the teacher college
            self.show_college(self.teacher_input_college_como)
            # Display information about the match
            self.show_contest()
            # Display administrator information
            self.show_admin()

    # show normal admin
    def show_admin(self):
        self.query.execute("SELECT id FROM admin")
        rows = self.query.fetchall()
        for row in rows:
            # print(row)
            inx = rows.index(row)
            str_re1 = self.pattern.findall(str(row))
            item = QTableWidgetItem(str_re1[0])
            self.table['register_table'].setItem(inx, 0, item)

    # Display the login page
    def show_login_page(self):
        """
        Under the login interface, the registration button, the input information button is not displayed
        The login password can only be displayed after the correct password
        """
        self.init()
        self.register_btn.setEnabled(False)
        self.input_btn.setEnabled(False)
        self.right_layout.setCurrentIndex(1)

    # Display the authentication page
    def show_verifyid_page(self):
        """
        radio button can only choose one identity, guest or administrator
        """
        self.init()
        self.right_layout.setCurrentIndex(0)

    # exit the interface
    def quit_act(self):
        """
        Prompt with a message box asking if you want to confirm the exit
        """
        # sender is the object that sends the signal
        # sender = self. sender()
        # print(sender.text() + 'Key pressed')
        message = QMessageBox.question(self, ' ', 'Are you sure to exit?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if message == QMessageBox.Yes:
            self.db.close()
            qApp = QApplication.instance()
            qApp.quit()

    # window centering function
    def center(self):
        """
        Get the length and width of the desktop Get the length and width of the window Calculate the position Move
        """
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())