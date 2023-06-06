import sys
from PyQt5 import QtWidgets, QtCore
import mysql.connector


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Logushev Database')
        self.setGeometry(200, 200, 335, 350)

        self.label = QtWidgets.QLabel('Tables List:', self)
        self.label.move(15, 10)
        self.user_table_button = QtWidgets.QPushButton('User Table', self)
        self.user_table_button.clicked.connect(self.open_user_table)
        self.user_table_button.move(15, 40)
        self.backup_table_button = QtWidgets.QPushButton('Backup Table', self)
        self.backup_table_button.clicked.connect(self.open_backup_table)
        self.backup_table_button.move(15, 75)
        self.dispatch_table_button = QtWidgets.QPushButton('Dispatch Table', self)
        self.dispatch_table_button.clicked.connect(self.open_dispatch_table)
        self.dispatch_table_button.move(15, 110)
        self.product_table_button = QtWidgets.QPushButton('Product Table', self)
        self.product_table_button.clicked.connect(self.open_product_table)
        self.product_table_button.move(15, 145)
        self.invoice_table_button = QtWidgets.QPushButton('Invoice Table', self)
        self.invoice_table_button.clicked.connect(self.open_invoice_table)
        self.invoice_table_button.move(15, 180)

    def open_user_table(self):
        self.hide()
        self.user_table = UserTable()
        self.user_table.show()

    def open_backup_table(self):
        self.hide()
        self.backup_table = BackupTable()
        self.backup_table.show()

    def open_dispatch_table(self):
        self.hide()
        self.dispatch_table = DispatchTable()
        self.dispatch_table.show()

    def open_product_table(self):
        self.hide()
        self.product_table = ProductTable()
        self.product_table.show()

    def open_invoice_table(self):
        self.hide()
        self.invoice_table = InvoiceTable()
        self.invoice_table.show()


class UserTable(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, 665, 350)
        self.setWindowTitle('User Table')

        self.table = QtWidgets.QTableWidget(self)
        self.table.setGeometry(10, 10, 646, 280)
        self.table.setColumnCount(5)  # изменено на 5
        self.table.setHorizontalHeaderLabels(
            ['User ID', 'Username', 'Surname', 'User Login', 'User Password'])  # добавлен новый заголовок столбца
        self.add_button = QtWidgets.QPushButton('Add user', self)
        self.add_button.clicked.connect(self.add_user)
        self.add_button.move(10, 300)
        self.edit_button = QtWidgets.QPushButton('Edit user', self)
        self.edit_button.clicked.connect(self.edit_user)
        self.edit_button.move(100, 300)
        self.delete_button = QtWidgets.QPushButton('Delete user', self)
        self.delete_button.clicked.connect(self.delete_user)
        self.delete_button.move(190, 300)
        self.back_button = QtWidgets.QPushButton('Back to list', self)
        self.back_button.clicked.connect(self.back_to_list)
        self.back_button.move(280, 300)


        self.load_data()

    def back_to_list(self):
        self.hide()
        self.all_tables=MainWindow()
        self.all_tables.show()

    def load_data(self):
        try:
            conn = mysql.connector.connect(user='root', password='',
                                           host='localhost',
                                           database='lab4')
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM user")
            result = cursor.fetchall()

            for row_num, row_data in enumerate(result):
                self.table.insertRow(row_num)
                self.table.setItem(row_num, 0,
                                   QtWidgets.QTableWidgetItem(str(row_data[0])))
                for col_num, col_data in enumerate(row_data[1:], start=1):
                    self.table.setItem(row_num, col_num, QtWidgets.QTableWidgetItem(str(col_data)))

            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            print("Error: {}".format(err))

    def add_user(self):
        username, surname, userlogin, userpassword = self.get_user_data()

        try:
            conn = mysql.connector.connect(user='root', password='',
                                           host='localhost',
                                           database='lab4')
            cursor = conn.cursor()

            cursor.execute("SELECT MAX(user_id) FROM user")
            max_id = cursor.fetchone()[0]
            if max_id is None:
                user_id = 1
            else:
                user_id = max_id + 1

            query = "INSERT INTO user (user_id, username, surname, userlogin, userpassword) VALUES (%s, %s, %s, %s, %s)"
            data = (user_id, username, surname, userlogin, userpassword)
            cursor.execute(query, data)
            conn.commit()

            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            print("Error: {}".format(err))
            return

        row_num = self.table.rowCount()
        self.table.insertRow(row_num)
        self.table.setItem(row_num, 0, QtWidgets.QTableWidgetItem(str(user_id)))
        self.table.setItem(row_num, 1, QtWidgets.QTableWidgetItem(username))
        self.table.setItem(row_num, 2, QtWidgets.QTableWidgetItem(surname))
        self.table.setItem(row_num, 3, QtWidgets.QTableWidgetItem(userlogin))
        self.table.setItem(row_num, 4, QtWidgets.QTableWidgetItem("*" * len(userpassword)))

    def get_user_data(self):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle('Add user')

        form_layout = QtWidgets.QFormLayout(dialog)

        username_edit = QtWidgets.QLineEdit()
        surname_edit = QtWidgets.QLineEdit()
        userlogin_edit = QtWidgets.QLineEdit()
        userpassword_edit = QtWidgets.QLineEdit()
        userpassword_edit.setEchoMode(QtWidgets.QLineEdit.Password)

        form_layout.addRow('Username:', username_edit)
        form_layout.addRow('Surname:', surname_edit)
        form_layout.addRow('Login:', userlogin_edit)
        form_layout.addRow('Password:', userpassword_edit)

        ok_button = QtWidgets.QPushButton('OK', dialog)
        ok_button.clicked.connect(dialog.accept)
        cancel_button = QtWidgets.QPushButton('Cancel', dialog)
        cancel_button.clicked.connect(dialog.reject)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)

        form_layout.addRow(button_layout)

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            return (
                username_edit.text(),
                surname_edit.text(),
                userlogin_edit.text(),
                userpassword_edit.text(),
            )
        else:
            return (None, None, None, None)

    def edit_user(self):
        row = self.table.currentRow()
        if row == -1:
            return
        user_id = int(self.table.item(row, 0).text())
        username, surname, userlogin, userpassword = self.get_user_data()

        try:
            conn = mysql.connector.connect(user='root', password='',
                                           host='localhost',
                                           database='lab4')
            cursor = conn.cursor()

            query = "UPDATE user SET username=%s, surname=%s, userlogin=%s, userpassword=%s WHERE user_id=%s"
            data = (username, surname, userlogin, userpassword, user_id)
            cursor.execute(query, data)
            conn.commit()

            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            print("Error: {}".format(err))
            return

        self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(username))
        self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(surname))
        self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(userlogin))
        self.table.setItem(row, 4, QtWidgets.QTableWidgetItem(userpassword))

    def delete_user(self):
        selected_user_id = self.table.item(self.table.currentRow(), 0).text()
        try:
            conn = mysql.connector.connect(user='root', password='',
                                           host='localhost',
                                           database='lab4')
            cursor = conn.cursor()

            delete_query = """DELETE FROM user WHERE user_id = %s"""
            cursor.execute(delete_query, (selected_user_id,))
            conn.commit()

            self.table.removeRow(self.table.currentRow())

            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            print("Error: {}".format(err))


class BackupTable(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, 550, 350)
        self.setWindowTitle('Backup Table')

        self.table = QtWidgets.QTableWidget(self)
        self.table.setGeometry(10, 10, 510, 280)
        self.table.setColumnCount(4)  # изменено на 4
        self.table.setHorizontalHeaderLabels(
            ['Size of backup', 'Date of backup', 'Info about backup', 'User name'])
        self.add_button = QtWidgets.QPushButton('Add backup', self)
        self.add_button.clicked.connect(self.add_backup)
        self.add_button.move(10, 300)
        self.edit_button = QtWidgets.QPushButton('Edit backup', self)
        self.edit_button.clicked.connect(self.edit_backup)
        self.edit_button.move(100, 300)
        self.delete_button = QtWidgets.QPushButton('Delete backup', self)
        self.delete_button.clicked.connect(self.delete_backup)
        self.delete_button.move(190, 300)
        self.back_button = QtWidgets.QPushButton('Back to list', self)
        self.back_button.clicked.connect(self.back_to_list)
        self.back_button.move(280, 300)

        self.load_data()

    def back_to_list(self):
        self.hide()
        self.all_tables=MainWindow()
        self.all_tables.show()

    def load_data(self):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="lab4"
        )
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM backup")
        result = cursor.fetchall()

        self.table.setRowCount(len(result))
        for i, row in enumerate(result):
            for j, col in enumerate(row):
                self.table.setItem(i, j, QtWidgets.QTableWidgetItem(str(col)))

        cursor.close()
        conn.close()

    def add_backup(self):
        Sizeofbackup, dateofbackup, Infoaboutbackup, User_username = self.get_backup_data()

        try:
            conn = mysql.connector.connect(user='root', password='',
                                           host='localhost',
                                           database='lab4')
            cursor = conn.cursor()

            sql = "INSERT INTO backup (Sizeofbackup, dateofbackup, Infoaboutbackup, User_username) VALUES (%s, %s, %s, %s)"
            val = (Sizeofbackup, dateofbackup, Infoaboutbackup, User_username)
            cursor.execute(sql, val)

            conn.commit()

            self.table.setRowCount(self.table.rowCount() + 1)
            self.table.setItem(self.table.rowCount() - 1, 0, QtWidgets.QTableWidgetItem(str(Sizeofbackup)))
            self.table.setItem(self.table.rowCount() - 1, 1, QtWidgets.QTableWidgetItem(str(dateofbackup)))
            self.table.setItem(self.table.rowCount() - 1, 2, QtWidgets.QTableWidgetItem(str(Infoaboutbackup)))
            self.table.setItem(self.table.rowCount() - 1, 3, QtWidgets.QTableWidgetItem(str(User_username)))

            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            if err.errno == 1452:
                QtWidgets.QMessageBox.critical(self, 'Error', 'User not found')
            else:
                print("Error: {}".format(err))

    def get_backup_data(self):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle('Add backup')

        form_layout = QtWidgets.QFormLayout(dialog)

        Sizeofbackup_edit = QtWidgets.QLineEdit()
        dateofbackup_edit = QtWidgets.QLineEdit()
        Infoaboutbackup_edit = QtWidgets.QLineEdit()
        User_username_edit = QtWidgets.QLineEdit()

        form_layout.addRow('Size of backup:', Sizeofbackup_edit)
        form_layout.addRow('Date of backup:', dateofbackup_edit)
        form_layout.addRow('Info about backup:', Infoaboutbackup_edit)
        form_layout.addRow('User name:', User_username_edit)

        ok_button = QtWidgets.QPushButton('OK', dialog)
        ok_button.clicked.connect(dialog.accept)
        cancel_button = QtWidgets.QPushButton('Cancel', dialog)
        cancel_button.clicked.connect(dialog.reject)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)

        form_layout.addRow(button_layout)

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            return (
                Sizeofbackup_edit.text(),
                dateofbackup_edit.text(),
                Infoaboutbackup_edit.text(),
                User_username_edit.text(),
            )
        else:
            return (None, None, None, None)

    def edit_backup(self):
        selected_row = self.table.currentRow()

        if selected_row == -1:
            return

        _, dateofbackup, Infoaboutbackup, User_username = self.get_backup_data()

        size_of_backup_item = self.table.item(selected_row, 0)
        Sizeofbackup = size_of_backup_item.text()

        try:
            conn = mysql.connector.connect(user='root', password='',
                                           host='localhost',
                                           database='lab4')
            cursor = conn.cursor()

            sql = "UPDATE backup SET dateofbackup = %s, Infoaboutbackup = %s, User_username = %s WHERE Sizeofbackup = %s"
            val = (dateofbackup, Infoaboutbackup, User_username, Sizeofbackup)
            cursor.execute(sql, val)

            conn.commit()

            size_of_backup_item.setFlags(size_of_backup_item.flags() & ~QtCore.Qt.ItemIsEditable)
            self.table.setItem(selected_row, 1, QtWidgets.QTableWidgetItem(str(dateofbackup)))
            self.table.setItem(selected_row, 2, QtWidgets.QTableWidgetItem(str(Infoaboutbackup)))
            self.table.setItem(selected_row, 3, QtWidgets.QTableWidgetItem(str(User_username)))

            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            if err.errno == 1452:
                QtWidgets.QMessageBox.critical(self, 'Error', 'User not found')
            else:
                print("Error: {}".format(err))

    def delete_backup(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            return

        Sizeofbackup = int(self.table.item(selected_row, 0).text())

        try:
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='lab4')
            cursor = conn.cursor()
            sql = "DELETE FROM backup WHERE Sizeofbackup = %s"
            val = (Sizeofbackup,)
            cursor.execute(sql, val)
            conn.commit()

            self.table.removeRow(selected_row)

            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            print("Error: {}".format(err))


class DispatchTable(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, 370, 450)
        self.setWindowTitle('Dispatch Table')

        self.table = QtWidgets.QTableWidget(self)
        self.table.setGeometry(10, 10, 350, 280)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(
            ['Region name', 'Country near or far abroad'])
        self.add_button = QtWidgets.QPushButton('Add dispatch', self)
        self.add_button.clicked.connect(self.add_dispatch)
        self.edit_button = QtWidgets.QPushButton('Edit dispatch', self)
        self.edit_button.clicked.connect(self.edit_dispatch)
        self.delete_button = QtWidgets.QPushButton('Delete dispatch', self)
        self.delete_button.clicked.connect(self.delete_dispatch)
        self.back_button = QtWidgets.QPushButton('Back to list', self)
        self.back_button.clicked.connect(self.back_to_list)
        self.add_button.move(100, 300)
        self.add_button.setFixedSize(100, 40)
        self.edit_button.move(210, 300)
        self.edit_button.setFixedSize(100, 40)
        self.delete_button.move(100, 350)
        self.delete_button.setFixedSize(100, 40)
        self.back_button.move(210, 350)
        self.back_button.setFixedSize(100, 40)


        self.load_data()

    def back_to_list(self):
        self.hide()
        self.all_tables = MainWindow()
        self.all_tables.show()

    def load_data(self):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="lab4"
        )
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM dispatch")
        result = cursor.fetchall()

        self.table.setRowCount(len(result))
        for i, row in enumerate(result):
            for j, col in enumerate(row):
                self.table.setItem(i, j, QtWidgets.QTableWidgetItem(str(col)))

        cursor.close()
        conn.close()

    def add_dispatch(self):
        Region_name, country_near_or_far_abroad = self.get_dispatch_data()

        try:
            conn = mysql.connector.connect(user='root', password='',
                                           host='localhost',
                                           database='lab4')
            cursor = conn.cursor()

            sql = "INSERT INTO dispatch (Region_name, country_near_or_far_abroad) VALUES (%s, %s)"
            val = (Region_name, country_near_or_far_abroad)
            cursor.execute(sql, val)

            conn.commit()

            self.table.setRowCount(self.table.rowCount() + 1)
            self.table.setItem(self.table.rowCount() - 1, 0, QtWidgets.QTableWidgetItem(str(Region_name)))
            self.table.setItem(self.table.rowCount() - 1, 1,
                               QtWidgets.QTableWidgetItem(str(country_near_or_far_abroad)))

            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            print("Error: {}".format(err))

    def get_dispatch_data(self):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle('Add dispatch')

        form_layout = QtWidgets.QFormLayout(dialog)

        Region_name_edit = QtWidgets.QLineEdit()
        country_near_or_far_abroad_edit = QtWidgets.QLineEdit()

        form_layout.addRow('Region name:', Region_name_edit)
        form_layout.addRow('Country near or far abroad:', country_near_or_far_abroad_edit)

        ok_button = QtWidgets.QPushButton('OK', dialog)
        ok_button.clicked.connect(dialog.accept)
        cancel_button = QtWidgets.QPushButton('Cancel', dialog)
        cancel_button.clicked.connect(dialog.reject)
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)

        form_layout.addRow(button_layout)

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            return (
                Region_name_edit.text(),
                country_near_or_far_abroad_edit.text()
            )
        else:
            return (None, None, None, None)



    def edit_dispatch(self):
        selected_row = self.table.currentRow()

        if selected_row == -1:
            return

        _, country_near_or_far_abroad = self.get_dispatch_data()

        region_name_item = self.table.item(selected_row, 0)
        Region_name = region_name_item.text()

        try:
            conn = mysql.connector.connect(user='root', password='',
                                           host='localhost',
                                           database='lab4')
            cursor = conn.cursor()

            sql = "UPDATE dispatch SET country_near_or_far_abroad = %s WHERE Region_name = %s"
            val = (country_near_or_far_abroad, Region_name)
            cursor.execute(sql, val)

            conn.commit()

            region_name_item.setFlags(region_name_item.flags() & ~QtCore.Qt.ItemIsEditable)
            self.table.setItem(selected_row, 1, QtWidgets.QTableWidgetItem(str(country_near_or_far_abroad)))

            cursor.close()
            conn.close()


        except mysql.connector.Error as err:
            print("Error: {}".format(err))

    def delete_dispatch(self):
        selected_row = self.table.currentRow()

        if selected_row == -1:
            return

        region_name_item = self.table.item(selected_row, 0)
        Region_name = region_name_item.text()

        try:
            conn = mysql.connector.connect(user='root', password='',
                                           host='localhost',
                                           database='lab4')
            cursor = conn.cursor()

            sql = "DELETE FROM dispatch WHERE Region_name = %s"
            val = (Region_name,)
            cursor.execute(sql, val)

            conn.commit()

            self.table.removeRow(selected_row)

            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            print("Error: {}".format(err))


class ProductTable(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, 420, 350)
        self.setWindowTitle('Product Table')

        self.table = QtWidgets.QTableWidget(self)
        self.table.setGeometry(10, 10, 400, 280)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(
            ['Code of product', 'Name of product', 'Category'])
        self.add_button = QtWidgets.QPushButton('Add product', self)
        self.add_button.clicked.connect(self.add_product)
        self.add_button.move(10, 300)
        self.edit_button = QtWidgets.QPushButton('Edit product', self)
        self.edit_button.clicked.connect(self.edit_product)
        self.edit_button.move(100, 300)
        self.delete_button = QtWidgets.QPushButton('Delete product', self)
        self.delete_button.clicked.connect(self.delete_product)
        self.delete_button.move(190, 300)
        self.back_button = QtWidgets.QPushButton('Back to list', self)
        self.back_button.clicked.connect(self.back_to_list)
        self.back_button.move(280, 300)

        self.load_data()

    def back_to_list(self):
        self.hide()
        self.all_tables=MainWindow()
        self.all_tables.show()

    def load_data(self):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="lab4"
        )
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM product")
        result = cursor.fetchall()

        self.table.setRowCount(len(result))
        for i, row in enumerate(result):
            for j, col in enumerate(row):
                self.table.setItem(i, j, QtWidgets.QTableWidgetItem(str(col)))

        cursor.close()
        conn.close()

    def add_product(self):
        code_of_product, name_of_product, category = self.get_product_data()
        try:
            conn = mysql.connector.connect(user='root', password='',
                                           host='localhost',
                                           database='lab4')
            cursor = conn.cursor()

            sql = "INSERT INTO product (code_of_product, name_of_product, category) VALUES (%s, %s, %s)"
            val = (code_of_product, name_of_product, category)
            cursor.execute(sql, val)

            conn.commit()

            self.table.setRowCount(self.table.rowCount() + 1)
            self.table.setItem(self.table.rowCount() - 1, 0, QtWidgets.QTableWidgetItem(str(code_of_product)))
            self.table.setItem(self.table.rowCount() - 1, 1, QtWidgets.QTableWidgetItem(str(name_of_product)))
            self.table.setItem(self.table.rowCount() - 1, 2, QtWidgets.QTableWidgetItem(str(category)))

            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
                print("Error: {}".format(err))

    def get_product_data(self):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle('Add Product')

        form_layout = QtWidgets.QFormLayout(dialog)

        code_of_product_edit = QtWidgets.QLineEdit()
        name_of_product_edit = QtWidgets.QLineEdit()
        category_edit = QtWidgets.QLineEdit()

        form_layout.addRow('Code of product:', code_of_product_edit)
        form_layout.addRow('Name of product:', name_of_product_edit)
        form_layout.addRow('Category:', category_edit)

        ok_button = QtWidgets.QPushButton('OK', dialog)
        ok_button.clicked.connect(dialog.accept)
        cancel_button = QtWidgets.QPushButton('Cancel', dialog)
        cancel_button.clicked.connect(dialog.reject)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)

        form_layout.addRow(button_layout)

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            return (
                code_of_product_edit.text(),
                name_of_product_edit.text(),
                category_edit.text()
            )
        else:
            return (None, None, None)

    def edit_product(self):
        code_of_product, name_of_product, category = self.get_product_data()

        try:
            conn = mysql.connector.connect(user='root', password='',
                                           host='localhost',
                                           database='lab4')
            cursor = conn.cursor()

            sql = "UPDATE product SET name_of_product = %s, category = %s WHERE code_of_product = %s"
            val = (name_of_product, category, code_of_product)
            cursor.execute(sql, val)

            conn.commit()

            for i in range(self.table.rowCount()):
                if self.table.item(i, 0).text() == code_of_product:
                    self.table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(name_of_product)))
                    self.table.setItem(i, 2, QtWidgets.QTableWidgetItem(str(category)))
                    break

            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            print("Error: {}".format(err))

    def delete_product(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            return

        code_of_product = int(self.table.item(selected_row, 0).text())

        try:
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='lab4')
            cursor = conn.cursor()
            sql = "DELETE FROM product WHERE code_of_product = %s"
            val = (code_of_product,)
            cursor.execute(sql, val)
            conn.commit()

            self.table.removeRow(selected_row)

            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            print("Error: {}".format(err))


class InvoiceTable(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, 1600, 350)
        self.setWindowTitle('Invoice Table')

        self.table = QtWidgets.QTableWidget(self)
        self.table.setGeometry(10, 10, 1550, 280)
        self.table.setColumnCount(12)
        self.table.setHorizontalHeaderLabels(
            ['Current date', 'Company name', 'Receiver name', 'Number', 'Serial of document', 'Bank number',
             'Bank name', 'Selling price', 'Quantity of product', 'Individual', 'Legal entity', 'Region name'])
        self.add_button = QtWidgets.QPushButton('Add invoice', self)
        self.add_button.clicked.connect(self.add_invoice)
        self.add_button.move(10, 300)
        self.edit_button = QtWidgets.QPushButton('Edit invoice', self)
        self.edit_button.clicked.connect(self.edit_invoice)
        self.edit_button.move(100, 300)
        self.delete_button = QtWidgets.QPushButton('Delete invoice', self)
        self.delete_button.clicked.connect(self.delete_invoice)
        self.delete_button.move(190, 300)
        self.back_button = QtWidgets.QPushButton('Back to list', self)
        self.back_button.clicked.connect(self.back_to_list)
        self.back_button.move(280, 300)

        self.load_data()

    def back_to_list(self):
        self.hide()
        self.all_tables=MainWindow()
        self.all_tables.show()

    def load_data(self):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="lab4"
        )
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM invoice")
        result = cursor.fetchall()

        self.table.setRowCount(len(result))
        for i, row in enumerate(result):
            for j, col in enumerate(row):
                self.table.setItem(i, j, QtWidgets.QTableWidgetItem(str(col)))

        cursor.close()
        conn.close()

    def add_invoice(self):
        invoice_current_date, company_name, receiver_name, number, \
            serial_of_document, bank_number, bank_name, selling_price,\
            quantity_of_product, individual, legal_entity,\
            Address_Region_name = self.get_invoice_data()
        try:
            conn = mysql.connector.connect(user='root', password='',
                                           host='localhost',
                                           database='lab4')
            cursor = conn.cursor()

            sql = "INSERT INTO invoice (invoice_current_date, company_name, receiver_name, number, serial_of_document, " \
                  "bank_number, bank_name, selling_price, quantity_of_product," \
                  " individual, legal_entity, Address_Region_name)" \
                  " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (invoice_current_date, company_name, receiver_name, number, serial_of_document, bank_number,
                   bank_name, selling_price, quantity_of_product, individual, legal_entity, Address_Region_name)
            cursor.execute(sql, val)

            conn.commit()

            self.table.setRowCount(self.table.rowCount() + 1)
            self.table.setItem(self.table.rowCount() - 1, 0, QtWidgets.QTableWidgetItem(str(invoice_current_date)))
            self.table.setItem(self.table.rowCount() - 1, 1, QtWidgets.QTableWidgetItem(str(company_name)))
            self.table.setItem(self.table.rowCount() - 1, 2, QtWidgets.QTableWidgetItem(str(receiver_name)))
            self.table.setItem(self.table.rowCount() - 1, 3, QtWidgets.QTableWidgetItem(str(number)))
            self.table.setItem(self.table.rowCount() - 1, 4, QtWidgets.QTableWidgetItem(str(serial_of_document)))
            self.table.setItem(self.table.rowCount() - 1, 5, QtWidgets.QTableWidgetItem(str(bank_number)))
            self.table.setItem(self.table.rowCount() - 1, 6, QtWidgets.QTableWidgetItem(str(bank_name)))
            self.table.setItem(self.table.rowCount() - 1, 7, QtWidgets.QTableWidgetItem(str(selling_price)))
            self.table.setItem(self.table.rowCount() - 1, 8, QtWidgets.QTableWidgetItem(str(quantity_of_product)))
            self.table.setItem(self.table.rowCount() - 1, 9, QtWidgets.QTableWidgetItem(str(individual)))
            self.table.setItem(self.table.rowCount() - 1, 10, QtWidgets.QTableWidgetItem(str(legal_entity)))
            self.table.setItem(self.table.rowCount() - 1, 11, QtWidgets.QTableWidgetItem(str(Address_Region_name)))

            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
                print("Error: {}".format(err))

    def get_invoice_data(self):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle('Add Invoice')

        form_layout = QtWidgets.QFormLayout(dialog)

        invoice_current_date_edit = QtWidgets.QLineEdit()
        company_name_edit = QtWidgets.QLineEdit()
        receiver_name_edit = QtWidgets.QLineEdit()
        number_edit = QtWidgets.QLineEdit()
        serial_of_document_edit = QtWidgets.QLineEdit()
        bank_number_edit = QtWidgets.QLineEdit()
        bank_name_edit = QtWidgets.QLineEdit()
        selling_price_edit = QtWidgets.QLineEdit()
        quantity_of_product_edit = QtWidgets.QLineEdit()
        individual_edit = QtWidgets.QLineEdit()
        legal_entity_edit = QtWidgets.QLineEdit()
        Address_Region_name_edit = QtWidgets.QLineEdit()

        form_layout.addRow('Current date:', invoice_current_date_edit)
        form_layout.addRow('Company name:', company_name_edit)
        form_layout.addRow('Receiver name:', receiver_name_edit)
        form_layout.addRow('Number:', number_edit)
        form_layout.addRow('Serial of document:', serial_of_document_edit)
        form_layout.addRow('Bank number:', bank_number_edit)
        form_layout.addRow('Bank name:', bank_name_edit)
        form_layout.addRow('Selling price:', selling_price_edit)
        form_layout.addRow('Quantity of product:', quantity_of_product_edit)
        form_layout.addRow('Individual:', individual_edit)
        form_layout.addRow('Legal entity:', legal_entity_edit)
        form_layout.addRow('Region name:', Address_Region_name_edit)

        ok_button = QtWidgets.QPushButton('OK', dialog)
        ok_button.clicked.connect(dialog.accept)
        cancel_button = QtWidgets.QPushButton('Cancel', dialog)
        cancel_button.clicked.connect(dialog.reject)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)

        form_layout.addRow(button_layout)

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            return (
                invoice_current_date_edit.text(),
                company_name_edit.text(),
                receiver_name_edit.text(),
                number_edit.text(),
                serial_of_document_edit.text(),
                bank_number_edit.text(),
                bank_name_edit.text(),
                selling_price_edit.text(),
                quantity_of_product_edit.text(),
                individual_edit.text(),
                legal_entity_edit.text(),
                Address_Region_name_edit.text()
            )
        else:
            return (None, None, None, None, None, None, None, None, None, None, None, None)

    def edit_invoice(self):
        invoice_current_date, company_name, receiver_name, number, \
            serial_of_document, bank_number, bank_name, selling_price, \
            quantity_of_product, individual, legal_entity, \
            Address_Region_name = self.get_invoice_data()

        try:
            conn = mysql.connector.connect(user='root', password='',
                                           host='localhost',
                                           database='lab4')
            cursor = conn.cursor()

            sql = "UPDATE invoice SET company_name = %s, receiver_name = %s, number = %s, " \
                  "serial_of_document = %s, bank_number = %s, bank_name = %s, " \
                  "selling_price = %s, quantity_of_product = %s, individual = %s, " \
                  "legal_entity = %s, Address_Region_name = %s WHERE invoice_current_date = %s"
            val = (company_name, receiver_name, number,
                   serial_of_document, bank_number, bank_name,
                   selling_price, quantity_of_product, individual,
                   legal_entity, Address_Region_name, invoice_current_date)
            cursor.execute(sql, val)

            conn.commit()

            for i in range(self.table.rowCount()):
                if self.table.item(i, 0).text() == invoice_current_date:
                    self.table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(company_name)))
                    self.table.setItem(i, 2, QtWidgets.QTableWidgetItem(str(receiver_name)))
                    self.table.setItem(i, 3, QtWidgets.QTableWidgetItem(str(number)))
                    self.table.setItem(i, 4, QtWidgets.QTableWidgetItem(str(serial_of_document)))
                    self.table.setItem(i, 5, QtWidgets.QTableWidgetItem(str(bank_number)))
                    self.table.setItem(i, 6, QtWidgets.QTableWidgetItem(str(bank_name)))
                    self.table.setItem(i, 7, QtWidgets.QTableWidgetItem(str(selling_price)))
                    self.table.setItem(i, 8, QtWidgets.QTableWidgetItem(str(quantity_of_product)))
                    self.table.setItem(i, 9, QtWidgets.QTableWidgetItem(str(individual)))
                    self.table.setItem(i, 10, QtWidgets.QTableWidgetItem(str(legal_entity)))
                    self.table.setItem(i, 11, QtWidgets.QTableWidgetItem(str(Address_Region_name)))
                    break

            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            print("Error: {}".format(err))

    def delete_invoice(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            return

        invoice_current_date = int(self.table.item(selected_row, 0).text())

        try:
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='lab4')
            cursor = conn.cursor()
            sql = "DELETE FROM invoice WHERE invoice_current_date = %s"
            val = (invoice_current_date,)
            cursor.execute(sql, val)
            conn.commit()

            self.table.removeRow(selected_row)

            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            print("Error: {}".format(err))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())