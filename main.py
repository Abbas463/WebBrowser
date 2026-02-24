from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import QIcon

class MyWebBrowser():
    def __init__(self):

        self.window = QWidget()
        self.window.setWindowIcon(QIcon("images/icon.ico"))
        self.window.setWindowTitle("AFG Browser")

        self.layout = QVBoxLayout()
        self.horizontal = QHBoxLayout()

        self.url_bar = QTextEdit()
        self.url_bar.setMaximumHeight(30)

        self.go_btn = QPushButton("Go")
        self.go_btn.setMinimumHeight(30)

        self.back_btn = QPushButton("<")
        self.back_btn.setMinimumHeight(30)
        
        self.forward_btn = QPushButton(">")
        self.forward_btn.setMinimumHeight(30)
        
        self.new_tab_btn = QPushButton("+")
        self.new_tab_btn.setMinimumHeight(30)
        self.new_tab_btn.clicked.connect(self.add_new_tab)
        
        self.horizontal.addWidget(self.url_bar)
        self.horizontal.addWidget(self.go_btn)
        self.horizontal.addWidget(self.back_btn)
        self.horizontal.addWidget(self.forward_btn)
        self.horizontal.addWidget(self.new_tab_btn)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        
        self.add_new_tab()

        self.go_btn.clicked.connect(lambda: self.navigate(self.url_bar.toPlainText()))
        self.back_btn.clicked.connect(self.go_back)
        self.forward_btn.clicked.connect(self.go_forward)

        self.layout.addLayout(self.horizontal)
        self.layout.addWidget(self.tabs)

        self.window.setLayout(self.layout)
        self.window.show()
    
    def add_new_tab(self):
        browser = QWebEngineView()
        browser.setUrl(QUrl("http://www.google.com"))
        
        self.browser = browser
        self.tabs.addTab(browser, "New Tab")
        self.tabs.setCurrentWidget(browser)
        
        browser.urlChanged.connect(lambda url, b=browser: self.update_url_bar(url, b))
        browser.titleChanged.connect(lambda title, b=browser: self.update_tab_title(title, b))
    
    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
        else:
            pass
    
    def update_url_bar(self, url, browser):
        if self.tabs.currentWidget() == browser:
            self.url_bar.setText(url.toString())
    
    def update_tab_title(self, title, browser):
        index = self.tabs.indexOf(browser)
        if index != -1:
            self.tabs.setTabText(index, title if title else "New Tab")
    
    def navigate(self, url):
        if not url.startswith("http"):
            url = "http://" + url
            self.url_bar.setText(url)
        current_browser = self.tabs.currentWidget()
        if current_browser:
            current_browser.setUrl(QUrl(url))
    
    def go_back(self):
        current_browser = self.tabs.currentWidget()
        if current_browser:
            current_browser.back()
    
    def go_forward(self):
        current_browser = self.tabs.currentWidget()
        if current_browser:
            current_browser.forward()


app = QApplication([])
window = MyWebBrowser()
app.exec_()
