import PyQt5, sys, ctypes, math
import api
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
        self.ticker_name = "Loading"
        self.currency = "USD"
        self.stock_price_history = []
        self.time_history = []
        self.x_axis_labels = []
        self.y_axis_labels = []
        
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
        self.graph_title.setText("Fetching data...")
        
        # News Title
        self.news_title = QtWidgets.QLabel(self, objectName = "title")
        self.news_title.resize(300, 100)
        self.news_title.move(900, 0)
        self.news_title.setAlignment(QtCore.Qt.AlignCenter)
        self.news_title.setWordWrap(True)
        self.news_title.setText("Loading Headlines...")
        
        # Detailed stock price text
        self.price_label = QtWidgets.QLabel(self)
        self.price_label.resize(400, 20)
        self.price_label.move(100, 580)
        self.price_label.setAlignment(QtCore.Qt.AlignCenter)
        self.price_label.setText("Fetching price...")
        
        # Detailed stock price change text
        self.change_label = QtWidgets.QLabel(self)
        self.change_label.resize(400, 20)
        self.change_label.move(500, 580)
        self.change_label.setAlignment(QtCore.Qt.AlignCenter)
        self.change_label.setText("Waiting for more data...")
        
        # Create X-Axis labels
        for i in range(5):
            self.xlabel = QtWidgets.QLabel(self, objectName = "blah")
            self.xlabel.resize(100, 50)
            self.xlabel.move((i * 175) + 100, 500) # Spacing labels
            self.xlabel.setAlignment(QtCore.Qt.AlignCenter)
            self.x_axis_labels.insert(0, self.xlabel)
            
        # Create Y-Axis labels
        for i in range(10):
            self.ylabel = QtWidgets.QLabel(self, objectName="a")
            self.ylabel.resize(100, 22)
            self.ylabel.move(0, 42 * i + 100)
            self.ylabel.setAlignment(QtCore.Qt.AlignCenter)
            self.y_axis_labels.append(self.ylabel)
        
        # Timer - update data every 10 seconds
        self.update()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(10000)
    
    # Get API data and update labels
    def update(self):
        try:
            current_date = datetime.now().strftime("%H:%M:%S %d/%m/%Y")
            
            # Get API information
            self.ticker_name = api.get_ticker_name(self.ticker)
            self.ticker_price = float(api.get_stock_price(self.ticker))
            
            # Gathering information to create the graph (X, Y labels respectively)
            # Update price history
            if len(self.stock_price_history) == 5:
                self.stock_price_history.pop()
            self.stock_price_history.insert(0, self.ticker_price)
            
            # Update time history
            if len(self.time_history) == 5:
                self.time_history.pop()
            self.time_history.insert(0, current_date)
            
            # Change title date
            self.graph_title.setText(f"{self.ticker} Stock Price")
            
            # More detailed graph information
            self.price_label.setText(f"{self.ticker}: {self.ticker_price} {self.currency}")
            
            if len(self.stock_price_history) > 1:
                self.stock_change_percentage = (self.stock_price_history[0] - self.stock_price_history[1]) / self.stock_price_history[1]
                self.change_label.setText(f"Stock Price Change: {self.stock_change_percentage}%")
            
            # News
            self.news_title.setText(f"{self.ticker_name} Headlines")
            
            # Draw the graph
            self.draw_graph()
        except Exception as e:
            print(e)
            # If API data could not be fetched then do not update at all
            pass

    # Creating X and Y labels and plotting points
    def draw_graph(self):
        # Check if there is sufficient data (at least 1 data point)
        if len(self.time_history) >= 1:
            # Update X-Axis Labels (Time)
            for i in range(len(self.time_history)):
                self.x_axis_labels[i].setText(self.time_history[i].replace(" ", "\n")) # Split the time and date into new lines
            
            # Calculate price increments
            lower_bound = math.floor(min(self.stock_price_history) / 10) * 10
            upper_bound = math.ceil(max(self.stock_price_history) / 10) * 10
            bound = int(upper_bound - lower_bound)
            price_increment = bound / 10
            
            # Update 10 Y-Axis Labels (Stock Price)
            for i in range(10):
                self.y_axis_labels[i].setText(f"${upper_bound - (price_increment * i)}")

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