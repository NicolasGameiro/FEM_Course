import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

class MyApp(QDialog):
    def __init__(self):
        super(MyApp,self).__init__()
        uic.loadUi('app.ui',self)
        self.masse = self.findChild(QLineEdit,'massEdit')
        
        
        self.pushButton.clicked.connect(self.val)
        self.show()
        
    def val(self) : 
        print(self.masse.text())

if __name__ == "__main__" :
    print("hello")
    app = QApplication(sys.argv)
    myapp = MyApp()
    sys.exit(myapp.exec_())