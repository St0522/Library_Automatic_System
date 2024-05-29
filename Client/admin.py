# admin.py
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QScrollArea
from bookList import BookListWindow
from addBook import AddBookWindow
from addUser import AddUserWindow

class AdminWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 창 제목 및 크기 설정
        self.setWindowTitle('관리자 화면')
        self.resize(1280, 720)

        # 대여 목록 테이블 생성
        self.table = QTableWidget()
        self.table.setColumnCount(6)  # 열 개수 설정 (회원 이름, 책 ID, 책 이름, 대여일, 반납일, 반납여부)
        self.table.setHorizontalHeaderLabels(['회원 이름', '책 ID', '책 이름', '대여일', '반납일', '반납여부'])

        # 샘플 데이터 추가 (실제로는 데이터베이스나 파일에서 로드)
        self.loadSampleData()

        # 스크롤 영역 설정
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.table)

        # 도서 추가 버튼
        add_book_button = QPushButton('도서 추가')
        add_book_button.clicked.connect(self.showAddBookWindow)

        # 회원 추가 버튼
        add_user_button = QPushButton('회원 추가')
        add_user_button.clicked.connect(self.showAddUserWindow)

        # 회원 목록 버튼
        user_list_button = QPushButton('회원 목록')
        user_list_button.clicked.connect(self.showUserListWindow)

        # 책 리스트 버튼
        book_list_button = QPushButton('책 리스트')
        book_list_button.clicked.connect(self.showBookListWindow)

        # 로그아웃 버튼 추가
        logout_button = QPushButton('로그아웃')
        logout_button.clicked.connect(self.logout)

        # 버튼 레이아웃 설정
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(add_book_button)
        button_layout.addWidget(add_user_button)
        button_layout.addWidget(user_list_button)
        button_layout.addWidget(book_list_button)
        button_layout.addWidget(logout_button)
        button_layout.addStretch()

        # 전체 레이아웃 설정
        layout = QVBoxLayout()
        layout.addWidget(scroll)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def loadSampleData(self):
        # 샘플 데이터 설정
        data = [
            ('사용자1', '1', '책 제목1', '2024-05-01', '2024-05-10', '반납 완료'),
            ('사용자2', '2', '책 제목2', '2024-05-02', '', '미반납'),
            ('사용자3', '3', '책 제목3', '2024-05-03', '2024-05-12', '반납 완료')
        ]

        self.table.setRowCount(len(data))
        for row, (user_name, book_id, book_name, rent_date, return_date, is_returned) in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(user_name))
            self.table.setItem(row, 1, QTableWidgetItem(book_id))
            self.table.setItem(row, 2, QTableWidgetItem(book_name))
            self.table.setItem(row, 3, QTableWidgetItem(rent_date))
            self.table.setItem(row, 4, QTableWidgetItem(return_date))
            self.table.setItem(row, 5, QTableWidgetItem(is_returned))

    def showAddBookWindow(self):
        self.add_book_window = AddBookWindow()
        self.add_book_window.show()

    def showAddUserWindow(self):
        self.add_user_window = AddUserWindow()
        self.add_user_window.show()

    def showUserListWindow(self):
        self.user_list_window = UserListWindow()
        self.user_list_window.show()

    def showBookListWindow(self):
        self.book_list_window = BookListWindow()
        self.book_list_window.show()

    def logout(self):
        self.close()
        self.parent().show()  # 로그인 창 다시 표시

class UserListWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('회원 목록')
        self.resize(600, 400)

        # 회원 목록 테이블 생성
        self.table = QTableWidget()
        self.table.setColumnCount(2)  # 열 개수 설정 (회원 이름, 학번)
        self.table.setHorizontalHeaderLabels(['회원 이름', '학번'])

        # 샘플 데이터 추가 (실제로는 데이터베이스나 파일에서 로드)
        self.loadSampleData()

        # 스크롤 영역 설정
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.table)

        # 전체 레이아웃 설정
        layout = QVBoxLayout()
        layout.addWidget(scroll)
        self.setLayout(layout)

    def loadSampleData(self):
        # 샘플 데이터 설정
        data = [
            ('사용자1', '20240001'),
            ('사용자2', '20240002'),
            ('사용자3', '20240003')
        ]

        self.table.setRowCount(len(data))
        for row, (user_name, user_id) in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(user_name))
            self.table.setItem(row, 1, QTableWidgetItem(user_id))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    admin_window = AdminWindow()
    admin_window.show()
    sys.exit(app.exec_())
