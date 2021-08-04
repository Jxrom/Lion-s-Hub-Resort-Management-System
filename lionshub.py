""" 
LIONS HUB RESORT MANAGEMENT SYSTEM 

============================
CREATION DATE: JULY 23, 2021
LAST UPDATED: AUGUST 5, 2021

============================
PROGRAMMER: Jxrom (つ▀¯▀)つ

============================
Note: If you find some bugs 🐞 email me pls! thankyou! ⊂(´・ω・｀⊂)
Email: jeromemarbebe@gmail.com
"""

from fpdf import FPDF
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.uic import loadUi
import sqlite3
import rsc
import os

# <====================================== MAIN WINDOW ======================================>

class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()
		loadUi("hotelresource.ui", self)

		self.connection = sqlite3.connect("hotelresource.db")
		self.cursor = self.connection.cursor()
		self.cursor.execute("CREATE TABLE IF NOT EXISTS guests(ID_NUMBER INTEGER PRIMARY KEY AUTOINCREMENT, GUEST_NAME TEXT, EMAIL TEXT, ROOM_NO TEXT, ROOM_TYPE TEXT, STATUS TEXT, CHECKED_IN TEXT, CHECKED_OUT TEXT, PAYCHECK TEXT)")
		self.cursor.close()

		self.Register_PushButton.clicked.connect(self.RegisterGuest)
		self.SetDate_PushButton.clicked.connect(self.ShowCalendar)
		self.Pay_PushButton.clicked.connect(self.ShowPay)
		self.Update_PushButton.clicked.connect(self.Refresh)
		self.Delete_PushButton.clicked.connect(self.Delete)
		self.Show_PushButton.clicked.connect(self.ShowReceipt)
		self.Print_PushButton.clicked.connect(self.Print)

		self.Refresh()
		self.setFixedSize(940, 648)

		self.show()

	def RegisterGuest(self):
		guest_name = ""
		email = ""
		room_no = ""
		room_type = ""
		status = ""

		guest_name = self.GuestName_LineEdit.text()
		email = self.Email_LineEdit.text()
		room_no = self.Room_LineEdit.text()
		room_type = self.RoomType_LineEdit.text()
		status = self.Status_LineEdit.text()

		try:
			self.connection = sqlite3.connect("hotelresource.db")
			self.cursor = self.connection.cursor()
			self.cursor.execute("INSERT INTO guests (GUEST_NAME, EMAIL, ROOM_NO, ROOM_TYPE, STATUS) VALUES (?, ?, ?, ?, ?)", (guest_name, email, room_no, room_type, status))
			self.connection.commit()
			self.cursor.close()
			self.connection.close()
			self.Refresh()
			self.Clear()
		except:
			self.ErrorDialog()

	def Delete(self):
		id_number = ""
		id_number = self.ID_Number_LineEdit.text()


		message = QMessageBox.question(self, "Delete", 
									   "Do you want to delete user?",
									   QMessageBox.Yes | 
									   QMessageBox.No)
		if message == QMessageBox.Yes:
			try:
				self.connection = sqlite3.connect("hotelresource.db")
				self.cursor = self.connection.cursor()
				self.cursor.execute("DELETE from guests WHERE ID_NUMBER="+str(id_number))
				self.connection.commit()
				self.cursor.close()
				self.connection.close()
				#self.QuestionDialog()
			except Exception:
				self.ErrorDialog()
		else:
			print("nothing happened")

# <====================================== PRINT DATA TO THE MAIN SCREEN ======================================>

	def ShowReceipt(self):
		id_number = ""
		id_number = self.ID_Number_LineEdit.text()

		try:
			self.connection = sqlite3.connect("hotelresource.db")
			self.cursor = self.connection.cursor()
			result = self.cursor.execute("SELECT * FROM guests WHERE ID_NUMBER ="+str(id_number))
			row = result.fetchone()
			self.searchresult = "ID Number: " + str(row[0]) + '\n' + "Guest Name: " + str(row[1]) + '\n' + "Email: " + str(row[2]) + '\n' \
				"Room No.: " + str(row[3]) + '\n' + "Room Type: " + str(row[4]) + '\n'+ "Status: " + str(row[5]) + '\n' \
				"Checked In: " + str(row[6]) + '\n' + "Checked Out: " + str(row[7]) + '\n' + "Amount: " + str(row[8])

			self.printText_window.setText(self.searchresult)
		except:
			self.ErrorDialog()

	def ErrorDialog(self):
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Critical)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("icons/oceanlogo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		msg.setWindowIcon(icon)
		msg.setText("Missing Input!")
		msg.setWindowTitle("Error")
		msg.exec_()

	def Refresh(self):
		self.connection = sqlite3.connect("hotelresource.db")
		query = "SELECT * FROM guests"
		result = self.connection.execute(query)
		self.table_widget.setRowCount(0)
		for row_number, row_data in enumerate(result):
			self.table_widget.insertRow(row_number)
			for column_number, data in enumerate(row_data):
				self.table_widget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
		self.connection.close()

	def Clear(self):
		self.GuestName_LineEdit.setText("")
		self.Email_LineEdit.setText("")
		self.Room_LineEdit.setText("")
		self.RoomType_LineEdit.setText("")
		self.Status_LineEdit.setText("")

# <====================================== EXPORT TO PDF FILE / CUSTOM MADE ======================================>

	def Print(self):

		id_number = ""
		id_number = self.ID_Number_LineEdit.text()

		message = QMessageBox.question(self, "Print", 
									   "Do you want to print receipt?",
									   QMessageBox.Yes | 
									   QMessageBox.No)

		if message == QMessageBox.Yes:
			try:
				class PDF(FPDF):
					def header(self):
						self.image('icons/lion.png', 20, 8, 25)
						self.image('icons/logo.png', 170, 8, 25)
						self.add_font('Montserrat', 'B', r'C:\Users\GodisGood\Documents\Hotel Resource Management\Fonts\Montserrat-Bold.ttf', uni=True)
						self.set_font('Montserrat', 'B', 20)
						self.cell(200, 10, 'Lions Hub Hotel and Resort', ln=1, align='C')

						self.add_font('Lora', 'B', r'C:\Users\GodisGood\Documents\Hotel Resource Management\Fonts\Lora-Bold.ttf', uni=True)
						self.set_font('Lora', 'B', 15)
						self.cell(200, 20, 'For Kings and Queens!', ln=1, align='C')
						self.ln(20)

				connection = sqlite3.connect("hotelresource.db")
				cursor = connection.cursor()
				result = cursor.execute("SELECT * FROM guests WHERE ID_NUMBER ="+str(id_number))
				row = result.fetchone()
				row0 = "ID Number:" + str(row[0])
				row1 = "Guest Name: " + str(row[1])
				row2 = "Email: " + str(row[2])
				row3 = "Room No: " + str(row[3])
				row4 = "Room Type: " + str(row[4])
				row5 = "Status: " + str(row[5])
				row6 = "Date Checked In: " + str(row[6])
				row7 = "Date Checked Out: " + str(row[7])
				row8 = "Amount: " + str(row[8])

				pdf = PDF('P', 'mm', 'Letter')

				pdf.add_page()
				pdf.set_left_margin(20)

				pdf.add_font('Lora', '', r'C:\Users\GodisGood\Documents\Hotel Resource Management\Fonts\Lora-Regular.ttf', uni=True)
				pdf.set_font('Lora', '', 16)

				pdf.cell(0, 10, row1, ln=1)
				pdf.cell(0, 10, row2, ln=1)
				pdf.cell(0, 10, row3, ln=1)
				pdf.cell(0, 10, row4, ln=1)
				pdf.cell(0, 10, row5, ln=1)
				pdf.cell(0, 10, row6, ln=1)
				pdf.cell(0, 10, row7, ln=1)
				pdf.cell(0, 10, row8, ln=1)
				pdf.cell(0, 10, '', ln=1)

				pdf.cell(0, 10, 'Accommodation:', ln=1)
				pdf.cell(0, 10, 'Meals on Full Board', ln=1)
				pdf.cell(0, 10, 'Spa', ln=1)
				pdf.cell(0, 10, 'Sauna', ln=1)
				pdf.cell(0, 10, 'Wifi Facilities and More', ln=1)

				pdf.cell(0, 10, '', ln=1)
				pdf.cell(0, 10, 'For Reservations: ', ln=1)
				pdf.cell(0, 10, 'Contact Us: +63951338193', ln=1)
				pdf.cell(0, 10, 'Email Us: jeromemarbebe@gmail.com', ln=1)
				pdf.cell(0, 10, 'Website: www.lionshub.com.ph', ln=1)

				pdf.output('guest_file.pdf')
				print('Print Complete')
				path = 'guest_file.pdf'
				os.system(path)
			except:
				print("No input")

	def ShowCalendar(self):
		self.window = Calendar()
		self.window.show()

	def ShowPay(self):
		self.window = Pay()
		self.window.show()

# <====================================== SHOW CALENDAR ======================================>

class Calendar(QWidget):
	def __init__(self):
		super(Calendar, self).__init__()
		loadUi("calendar.ui", self)

		self.setFixedSize(331, 319)

		self.SetCheckIn_PushButton.clicked.connect(self.SetCheckedIn)
		self.SetCheckOut_PushButton.clicked.connect(self.SetCheckedOut)

		self.show()

	def SetCheckedIn(self):
		value = self.calendarWidget.selectedDate()
		date = value.toString()

		update_IDNumber = ""

		update_IDNumber = self.ID_Number_LineEdit.text()

		try:
			query = "UPDATE guests SET CHECKED_IN = ? WHERE ID_NUMBER = ?"
			parameters = (date, update_IDNumber)
			self.connection = sqlite3.connect("hotelresource.db")
			self.cursor = self.connection.cursor() 
			self.cursor.execute(query, parameters)
			self.connection.commit()
			self.cursor.close()
			self.connection.close()
		except Exception:
			self.ErrorDialog()

	def SetCheckedOut(self):
		value = self.calendarWidget.selectedDate()
		date = value.toString()

		update_IDNumber = ""

		update_IDNumber = self.ID_Number_LineEdit.text()

		try:
			query = "UPDATE guests SET CHECKED_OUT = ? WHERE ID_NUMBER = ?"
			parameters = (date, update_IDNumber)
			self.connection = sqlite3.connect("hotelresource.db")
			self.cursor = self.connection.cursor() 
			self.cursor.execute(query, parameters)
			self.connection.commit()
			self.cursor.close()
			self.connection.close()
		except Exception:
			self.ErrorDialog()

	def Refresh(self):
			self.connection = sqlite3.connect("hotelresource.db")
			query = "SELECT * FROM guests"
			result = self.connection.execute(query)
			self.table_widget.setRowCount(0)
			for row_number, row_data in enumerate(result):
				self.table_widget.insertRow(row_number)
				for column_number, data in enumerate(row_data):
					self.table_widget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
			self.connection.close()

	def ErrorDialog(self):
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Critical)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("icons/lionshub.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		msg.setWindowIcon(icon)
		msg.setText("Could Not Find")
		msg.setWindowTitle("Error")
		msg.exec_()

# <====================================== SHOW PAY SCREEN ======================================>

class Pay(QWidget):
	def __init__(self):
		super(Pay, self).__init__()
		loadUi("pay.ui", self)
		self.setFixedSize(220, 190)
		self.RegAmount_PushButton.clicked.connect(self.RegAmount)
		self.show()

	def RegAmount(self):
		update_IDNumber = ""
		amount = ""

		update_IDNumber = self.ID_Number_LineEdit.text()
		amount = self.Amount_LineEdit.text()

		try:
			query = "UPDATE guests SET PAYCHECK = ? WHERE ID_NUMBER = ?"
			parameters = (amount, update_IDNumber)
			self.connection = sqlite3.connect("hotelresource.db")
			self.cursor = self.connection.cursor() 
			self.cursor.execute(query, parameters)
			self.connection.commit()
			self.cursor.close()
			self.connection.close()
			self.updated_msgbox()
		except:
			self.ErrorDialog()

	def updated_msgbox(self):
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Information)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("icons/lion.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		msg.setWindowIcon(icon)
		msg.setText("Pay Updated Sucessfully")
		msg.setWindowTitle("Pay Update")
		msg.exec_()

	def ErrorDialog(self):
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Critical)
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap("icons/lionshub.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		msg.setWindowIcon(icon)
		msg.setText("Could Not Find")
		msg.setWindowTitle("Error")
		msg.exec_()

# EXECUTE MAIN APPLICATION
if __name__ == "__main__":
	import sys
	app = QApplication(sys.argv)
	window = MainWindow()
	sys.exit(app.exec_())