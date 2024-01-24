import PyQt5, sys, ctypes
import ticker_api
from datetime import datetime
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtGui import QCursor

class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        # Window properties
        self.setFixedSize(1200, 600)
        self.setWindowTitle("Stonk Viewer")
        self.setWindowIcon(QtGui.QIcon("assets/images/icon.jpg"))
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("why")
        
        # Fonts
        QtGui.QFontDatabase.addApplicationFont("assets//fonts//MonaSans.ttf")
        
        # Stylesheet
        with open("style.css", "r") as css:
            self.setStyleSheet(css.read())
        
        # Variables
        self.ticker = "MSFT"
        self.ticker_name = None
        self.currency = "USD"
        self.stock_prices = []
        
        # Draw widgets
        self.draw_widgets()
        
    def draw_widgets(self):
        self.graph_frame = QtWidgets.QFrame(self, objectName = "graph")
        self.graph_frame.resize(800, 400)
        self.graph_frame.move(100, 100)
        
        # Graph title
        self.graph_title = QtWidgets.QLabel(self, objectName = "title")
        self.graph_title.resize(800, 100)
        self.graph_title.move(100, 0)
        self.graph_title.setAlignment(QtCore.Qt.AlignCenter)
        self.graph_title.setWordWrap(True)
        self.graph_title.setText(f"{self.ticker_name} stock price as at TIME LOADING")
        
        # News Title
        self.news_title = QtWidgets.QLabel(self, objectName = "title")
        self.news_title.resize(300, 100)
        self.news_title.move(900, 0)
        self.news_title.setAlignment(QtCore.Qt.AlignCenter)
        self.news_title.setWordWrap(True)
        self.news_title.setText(f"{self.ticker_name} Headlines")
        
        # Detailed stock price text
        self.price_label = QtWidgets.QLabel(self)
        self.price_label.resize(400, 20)
        self.price_label.move(100, 500)
        self.price_label.setAlignment(QtCore.Qt.AlignCenter)
        
        # Detailed stock price change text
        self.change_label = QtWidgets.QLabel(self)
        self.change_label.resize(400, 20)
        self.change_label.move(500, 500)
        self.change_label.setAlignment(QtCore.Qt.AlignCenter)
        
        # Timer
        self.update()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(10000)
        
    def update(self):
        try:
            # Get API information
            self.ticker_name = ticker_api.get_ticker_name(self.ticker)
            self.ticker_price = float(ticker_api.get_stock_price(self.ticker))
            
            # Update price history
            if len(self.stock_prices) == 5:
                self.stock_prices.pop()
                self.stock_prices.insert(0, self.ticker_price)
            else:
                self.stock_prices.insert(0, self.ticker_price)
            
            # Change title date
            dt_string = datetime.now().strftime("%H:%M:%S %d/%m/%Y")
            self.graph_title.setText(f"{self.ticker_name} stock price as at {dt_string}")
            
            # More detailed graph information
            self.price_label.setText(f"{self.ticker}: {self.ticker_price} {self.currency}")
            
            if len(self.stock_prices) > 1:
                self.stock_change_percentage = (self.stock_prices[0] - self.stock_prices[1]) / self.stock_prices[1]
                
                if self.stock_change_percentage != 0:
                    if self.stock_change_percentage:
                        self.change_label.setText(f"{self.ticker_name}: +{self.stock_change_percentage}%")
                    else:
                        self.change_label.setText(f"{self.ticker_name}: -{self.stock_change_percentage}%")
                else:
                    self.change_label.setText(f"Stock Price Change: {self.stock_change_percentage}%")
            
            # News
            self.news_title.setText(f"{self.ticker_name} Headlines")
        except:
            self.graph_title.setText("Error fetching API data")
            self.price_label.setText("Error fetching API data")
            self.change_label.setText("Error fetching API data")
            self.news_title.setText("Error fetching API data")

def window():
    # Create window
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = App()
    # Show widgets
    window.show()
    # Close window when close button pressed
    sys.exit(app.exec_())

if __name__ == "__main__":
    window()