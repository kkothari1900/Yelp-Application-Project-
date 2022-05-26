import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout, QPushButton
from PyQt5 import uic, QtCore, QtWidgets
from PyQt5.QtGui import QIcon, QPixmap, QBrush, QColor
import psycopg2
#To use textblob make sure you install the library
#pip install -U textblob
#python -m textblob.download_corpora
from textblob import TextBlob
qtCreatorFile = "Milestone2_4.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class milestone2_v2(QMainWindow):

    def __init__(self):
        super(milestone2_v2, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.loadStateList()
        self.ui.state_comboBox.currentTextChanged.connect(self.stateChanged)
        self.ui.City_listWidget.itemSelectionChanged.connect(self.cityChanged)
        self.ui.Zip_listWidget.itemSelectionChanged.connect(self.zipChanged)

        # self.pushButton = QtWidgets.QPushButton('selectButton',self)
        # self.pushButton.setObjectName('selectButton')
        # self.pushButton.setGeometry(190,10,93,28)
        # self.pushButton.move(220,324)
        # self.pushButton.clicked.connect(self.clickedButton)
        self.ui.selectButton.clicked.connect(self.clickedButton)
        #continue
        self.ui.SC_listWidget.itemSelectionChanged.connect(self.businessTable)
        self.ui.businessTable.itemSelectionChanged.connect(self.businessTableChanged)

        #User Page
        self.ui.login1_line_edit.textChanged.connect(self.login_user)
        self.ui.login2_list_widget.itemSelectionChanged.connect(self.user_id)

        #User page
        self.ui.login2_list_widget.itemSelectionChanged.connect(self.latest_tip_of_friends)
        self.ui.login2_list_widget.itemSelectionChanged.connect(self.myfriendsChanged)

        #Analysis
        self.ui.selectButton_2.clicked.connect(self.order_star)
        self.ui.selectButton_3.clicked.connect(self.order_price)
        self.ui.selectButton_4.clicked.connect(self.order_popularity)

    def executeQuery(self, sql_str):
        try:  # change dbname and password
            conn = psycopg2.connect("dbname='Check_project' user='postgres' host='localhost' password='Cuby190'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()
        cur.execute(sql_str)
        conn.commit()
        result = cur.fetchall()  # fetch all tuple result
        conn.close()
        return result

    def login_user(self):
        user_name = self.ui.login1_line_edit.displayText()
        sql_str = "SELECT user_id FROM yelp_user WHERE name LIKE '{}%' ORDER BY user_id;".format(user_name)
        try:
            result = self.executeQuery(sql_str)
            for row in result:
                self.ui.login2_list_widget.addItem(row[0]) # Changed from login1_line_edit

        except Exception as e:
            print("Login failed",e)


    def user_id(self):
        self.ui.myinfor_lineEdit_name.clear()  # clear the previous selection of user
        self.ui.myinfor_lineEdit_stars.clear()
        self.ui.myinfor_lineEdit_stars_2.clear()
        self.ui.myinfor_lineEdit_funny.clear()
        self.ui.myinfor_lineEdit_cool.clear()
        self.ui.myinfor_lineEdit_useful.clear()
        self.ui.MF_tableWidget.clear()
        selection = self.ui.login2_list_widget.selectedItems()
        if len(selection) > 0:
            #This is the user id,
            user_id_num = selection[0].text()

            sql_str = "SELECT distinct (name) FROM yelp_user WHERE user_id ~'{0}';".format(user_id_num)
            sql_str2= "SELECT distinct( average_stars ) FROM yelp_user WHERE user_id  ~'{0}';".format(user_id_num)
            sql_str3= "SELECT distinct( yelping_since)  FROM yelp_user WHERE user_id ~'{0}';".format(user_id_num)
            sql_str4="SELECT distinct( funny)  FROM yelp_user WHERE user_id ~'{0}';".format(user_id_num)
            #Cool
            sql_str5="SELECT distinct(cool)  FROM yelp_user WHERE user_id ~'{0}';".format(user_id_num)
            #useful
            sql_str6="SELECT distinct( useful)  FROM yelp_user WHERE user_id ~'{0}';".format(user_id_num)
            #should be referencing user_id_num
            sql_str8 = "SELECT DISTINCT(name), fans, average_stars, tipcount, yelping_since FROM yelp_user, friends WHERE yelp_user.user_id IN (SELECT (user_id_2) FROM friends WHERE user_id_1  ~'{0}');".format(user_id_num)
            try:
                result = self.executeQuery(sql_str)
                for row in result:
                    self.ui.myinfor_lineEdit_name.addItem(row[0])  #I just changed it to a list widget

                result2= self.executeQuery(sql_str2)
                for row in result2:
                    self.ui.myinfor_lineEdit_stars.addItem(str(row[0]))
                result3= self.executeQuery(sql_str3)
                for row in result3:
                    self.ui.myinfor_lineEdit_stars_2.addItem(str(row[0]))
                result4= self.executeQuery(sql_str4)
                for row in result4:
                    self.ui.myinfor_lineEdit_funny.addItem(str(row[0]))
                result5= self.executeQuery(sql_str5)
                for row in result5:
                    self.ui.myinfor_lineEdit_cool.addItem(str(row[0]))
                result6= self.executeQuery(sql_str6)
                for row in result6:
                    self.ui.myinfor_lineEdit_useful.addItem(str(row[0]))
                results8 = self.executeQuery(sql_str8)
                print(results8)
                self.ui.MF_tableWidget.setColumnCount(len(results8[0]))
                self.ui.MF_tableWidget.setRowCount(len(results8))
                self.ui.MF_tableWidget.setHorizontalHeaderLabels(['Friend Name', "Avg Stars", "Fans", "Tip Count", "Yelping Since"])
                self.ui.MF_tableWidget.resizeColumnsToContents()
                self.ui.MF_tableWidget.setColumnWidth(0, 150)
                self.ui.MF_tableWidget.setColumnWidth(1, 100)
                self.ui.MF_tableWidget.setColumnWidth(2, 50)
                self.ui.MF_tableWidget.setColumnWidth(3, 50)
                self.ui.MF_tableWidget.setColumnWidth(4, 100)
                currentRowCount1 = 0
                for row in results8:
                    for colCount in range(0, len(results8[0])):
                        self.ui.MF_tableWidget.setItem(currentRowCount1, colCount, QTableWidgetItem(str(row[colCount])))
                    currentRowCount1 += 1


            except Exception as e:
                print('Friends table',e)


    def loadStateList(self):
        self.ui.state_comboBox.clear()
        sql_str = "SELECT distinct(state) FROM yelp_business ORDER BY state;"
        try:
            result = self.executeQuery(sql_str)
            for row in result:
                self.ui.state_comboBox.addItem(row[0])
        except Exception as e:
            print("loadStateList failed")
        self.ui.state_comboBox.setCurrentIndex(-1)
        self.ui.state_comboBox.clearEditText()

    def stateChanged(self):
        self.ui.City_listWidget.clear()
        state = self.ui.state_comboBox.currentText()
        if (self.ui.state_comboBox.currentIndex() >= 0):
            sql_str = "SELECT distinct(city) FROM yelp_business WHERE state ='" + state + "' ORDER BY city;"

            try:
                result = self.executeQuery(sql_str)
                for row in result:
                    self.ui.City_listWidget.addItem(row[0])

            except Exception as e:
                print("stateChanged failed",e)


    def cityChanged(self):

        self.ui.Zip_listWidget.clear()
        if (self.ui.state_comboBox.currentIndex() >=0 )and (len(self.ui.City_listWidget.selectedItems())>0):
            state = self.ui.state_comboBox.currentText()
            city = self.ui.City_listWidget.selectedItems()[-1].text()
            sql_str = "SELECT DISTINCT postal_code FROM yelp_business WHERE city ='{0}' ORDER BY postal_code;".format(city)
            results = self.executeQuery(sql_str)

            try:

                for row in results:
                    self.ui.Zip_listWidget.addItem(row[0])

            except Exception as e:
                print("Postal code failed",e)

    def zipChanged(self):
        self.ui.BZIP_listWidget.clear()
        self.ui.TopCat_tableWidget.clear()

        if (len(self.ui.City_listWidget.selectedItems())>0)and  (len(self.ui.Zip_listWidget.selectedItems())>0):
            postal_code = self.ui.Zip_listWidget.selectedItems()[0].text()
            sql_str = "SELECT count(business_id) FROM yelp_business WHERE postal_code = '{0}' ;".format(postal_code)
            sql_str2 = "SELECT COUNT(DISTINCT business_id) AS no_of_Business , category_name FROM yelp_business NATURAL JOIN categories WHERE postal_code = '" + postal_code + "' GROUP BY category_name ORDER BY no_of_Business desc;"  # .format(postal_code)

            try:
                results = self.executeQuery(sql_str)
                str(results[0][0])
                results2 = self.executeQuery(sql_str2)
                self.ui.TopCat_tableWidget.setColumnCount(len(results2[0]))
                self.ui.TopCat_tableWidget.setRowCount(len(results2))
                self.ui.TopCat_tableWidget.setHorizontalHeaderLabels(['# of Business','Category Name'])
                self.ui.TopCat_tableWidget.resizeColumnsToContents()
                self.ui.TopCat_tableWidget.setColumnWidth(0,150)
                self.ui.TopCat_tableWidget.setColumnWidth(1,200)

                for row in results:
                    self.ui.BZIP_listWidget.addItem(str(row[0]))

                currentRowCount = 0
                for row in results2:
                    for colCount in range(0, len(results2[0])):
                        self.ui.TopCat_tableWidget.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1

            except Exception as e:
                print("Postal code failed",e)

    def clickedButton(self):
        self.ui.SC_listWidget.clear()
        self.ui.businessTable.clear()
        self.ui.AOPB_tableWidget.clear()

        self.ui.NOB_listWidget.clear()
        self.ui.NOPB_listWidget.clear()
        if  (len(self.ui.Zip_listWidget.selectedItems())>0):
            postal_code = self.ui.Zip_listWidget.selectedItems()[0].text()
            sql_str = "select DISTINCT(category_name) from categories NATURAL JOIN yelp_business WHERE postal_code ='"+ postal_code + "' ORDER BY category_name ;"
            sql_str2 = "SELECT name, address, city, stars, numtips, business_id FROM yelp_business  WHERE postal_code ='"+ postal_code + "' ORDER BY name ;"
            sql_str3 = "SELECT COUNT(attr_name) AS attr_counts, attr_name  FROM attributes, yelp_business WHERE attributes.business_id =  yelp_business.business_id AND postal_code = '"+ postal_code + "' GROUP BY attr_name ORDER BY attr_counts desc;"
            try:
                results = self.executeQuery(sql_str)
                for row in results:
                    self.ui.SC_listWidget.addItem(row[0])

                results2 = self.executeQuery(sql_str2)

                currentRowCount = 0
                self.ui.businessTable.setColumnCount(len(results2[0]))
                self.ui.businessTable.setRowCount(len(results2))
                self.ui.businessTable.setHorizontalHeaderLabels(['Business name','Address','City', 'Stars','Number of Tips', 'Business ID'])
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0,150)
                self.ui.businessTable.setColumnWidth(1,200)
                self.ui.businessTable.setColumnWidth(2,100)
                self.ui.businessTable.setColumnWidth(3,50)
                self.ui.businessTable.setColumnWidth(4,100)
                self.ui.businessTable.setColumnWidth(5,75)
                for row in results2:
                    for colCount in range(0, len(results2[0])):
                        self.ui.businessTable.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1

                results3= self.executeQuery(sql_str3)
                str(results3[0][0])

                self.ui.AOPB_tableWidget.setColumnCount(len(results3[0]))
                self.ui.AOPB_tableWidget.setRowCount(len(results3))
                self.ui.AOPB_tableWidget.setHorizontalHeaderLabels(['Count','Attribute'])
                self.ui.AOPB_tableWidget.resizeColumnsToContents()
                self.ui.AOPB_tableWidget.setColumnWidth(0,40)
                self.ui.AOPB_tableWidget.setColumnWidth(1,150)

                currentRowCount1 = 0
                for row in results3:
                    for colCount in range(0, len(results3[0])):
                        self.ui.AOPB_tableWidget.setItem(currentRowCount1, colCount, QTableWidgetItem(str(row[colCount])))
                    currentRowCount1 += 1



            except Exception as e:
                print(" failed", e)

    def businessTable(self):
        self.ui.businessTable.clear()
        self.ui.NOB_listWidget.clear()
        self.ui.NOPB_listWidget.clear()

        if  (len(self.ui.SC_listWidget.selectedItems())>0):
            postal_code = self.ui.Zip_listWidget.selectedItems()[0].text()
            category = self.ui.SC_listWidget.selectedItems()[0].text()
            sql_str ="SELECT name, address, city, stars, numtips,business_id FROM yelp_business NATURAL JOIN categories WHERE postal_code ='"+ postal_code + "' AND category_name ='"+ category+ "' ORDER BY name";
            sql_str2 = "SELECT COUNT(yelp_business.business_id) AS NOB FROM yelp_business, categories WHERE postal_code ='"+ postal_code  + "' AND category_name ='"+ category+"' AND  yelp_business.business_id = categories.business_id";
            sql_str3 = "SELECT COUNT(yelp_business.business_id) AS NOPB FROM yelp_business, categories WHERE postal_code ='"+ postal_code  + "' AND category_name ='"+ category+"' AND  yelp_business.business_id = categories.business_id AND yelp_business.stars >=4.5";

            try:
                results2 = self.executeQuery(sql_str)
                results3 = self.executeQuery(sql_str2)
                results4 = self.executeQuery(sql_str3)

                for row in results4:
                    self.ui.NOPB_listWidget.addItem(str(row[0]))

                for row in results3:
                    self.ui.NOB_listWidget.addItem(str(row[0]))

                currentRowCount = 0
                self.ui.businessTable.setColumnCount(len(results2[0]))
                self.ui.businessTable.setRowCount(len(results2))
                self.ui.businessTable.setHorizontalHeaderLabels(['Business name','Address','City', 'Stars','Number of Tips','Business ID'])#setting header labels
                self.ui.businessTable.resizeColumnsToContents()
                self.ui.businessTable.setColumnWidth(0,150)
                self.ui.businessTable.setColumnWidth(1,210)
                self.ui.businessTable.setColumnWidth(2,100)
                self.ui.businessTable.setColumnWidth(3,50)
                self.ui.businessTable.setColumnWidth(4,100)
                self.ui.businessTable.setColumnWidth(5,75)
                # SELECT count
                for row in results2:
                    for colCount in range(0, len(results2[0])):
                        self.ui.businessTable.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1
                    #Can I use currentrow count to count number of business?
                    #Connect business id but hide it, include business id in query (maybe just minimize it)


            except Exception as e:
                print("Select Category failed", e)



    def businessTableChanged(self):
        self.ui.COSB_listWidget.clear()
        self.ui.AOSB_listWidget_2.clear()
        if (len(self.ui.businessTable.selectedItems())>0):
            businessID = self.ui.businessTable.selectedItems()[0].text()
            sql_str = "SELECT category_name FROM categories WHERE business_id='{}';".format(businessID)
            sql_str1 = "SELECT attr_name FROM attributes WHERE business_id='{}';".format(businessID)

            results = self.executeQuery(sql_str)
            results1 = self.executeQuery(sql_str1)
            for row in results:
                self.ui.COSB_listWidget.addItem(str(row[0]))
            for row in results1:
                self.ui.AOSB_listWidget_2.addItem(str(row[0]))

    def latest_tip_of_friends(self):
        self.ui.LTOMF_tableWidget.clear()
        #uid = "pm2Xtpl0zwp94Yaj5cT26g"  #uid can be get from the previous part. Change this when combining code.
        selection = self.ui.login2_list_widget.selectedItems()
        uid = selection[0].text()
        sql_str = "select yelp_user.name, yelp_business.name, yelp_business.city, yelp_tips.date, yelp_tips.text from yelp_tips, yelp_user , yelp_business where (yelp_tips.user_id, yelp_tips.date) in (select user_id_2, max(date) from friends, yelp_tips where user_id_1 = '"+uid+"' and user_id_2 = yelp_tips.user_id group by user_id_2) and yelp_tips.user_id = yelp_user.user_id and yelp_tips.business_id = yelp_business.business_id;"
        if len(selection) > 0:
            try:
                results = self.executeQuery(sql_str)
                print(results)
                self.ui.LTOMF_tableWidget.setColumnCount(len(results[0]))
                self.ui.LTOMF_tableWidget.setRowCount(len(results))
                self.ui.LTOMF_tableWidget.setHorizontalHeaderLabels(['Friend Name','Business','City', 'Date','Review'])
                self.ui.LTOMF_tableWidget.resizeColumnsToContents()
                self.ui.LTOMF_tableWidget.setColumnWidth(0,120)
                self.ui.LTOMF_tableWidget.setColumnWidth(1,160)
                self.ui.LTOMF_tableWidget.setColumnWidth(2,100)
                self.ui.LTOMF_tableWidget.setColumnWidth(3,100)
                self.ui.LTOMF_tableWidget.setColumnWidth(4,500)
                currentRowCount = 0
                for row in results:
                    for colCount in range(0, len(results[0])):
                        self.ui.LTOMF_tableWidget.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1

            except Exception as e:
                print("Select latest tip failed", e)

    def myfriendsChanged(self):
        self.ui.FOMF_tableWidget.clear()
        #uid = "pm2Xtpl0zwp94Yaj5cT26g"  #uid can be get from the previous part. Change this when combining code.
        selection = self.ui.login2_list_widget.selectedItems()
        uid = selection[0].text()
        sql_str = "select name, average_stars, fans,tipcount,yelping_since from friends, yelp_user where user_id_1 in (select yelp_user.user_id from friends, yelp_user where user_id_1 = '"+uid+"' and user_id_2 = yelp_user.user_id) and user_id_2 = yelp_user.user_id group by name, average_stars, fans,tipcount,yelping_since"
        sql_str2 = "select name, average_stars, fans,tipcount,yelping_since from friends, yelp_user where user_id_1 in (select yelp_user.user_id from friends, yelp_user where user_id_1 in (select yelp_user.user_id from friends, yelp_user where user_id_1 = '"+uid+"' and user_id_2 = yelp_user.user_id) and user_id_2 = yelp_user.user_id) and user_id_2 = yelp_user.user_id group by name, average_stars, fans,tipcount,yelping_since"
        if len(selection) > 0:
            try:
                results1 = self.executeQuery(sql_str)
                results1_new = []
                #print(results1)
                for row in results1:
                    row_new = (1,) + row
                    results1_new.append(row_new)

                results2 = self.executeQuery(sql_str2)
                results2_new = []
                #print(results1)
                for row in results2:
                    row_new = (2,) + row
                    results2_new.append(row_new)
                results = results1_new + results2_new
                self.ui.FOMF_tableWidget.setColumnCount(len(results[0]))
                self.ui.FOMF_tableWidget.setRowCount(len(results))
                self.ui.FOMF_tableWidget.setHorizontalHeaderLabels(['degree','Friend Name','Avg Stars','Fans', 'Tip Count','Yelping Since'])
                self.ui.FOMF_tableWidget.resizeColumnsToContents()
                self.ui.FOMF_tableWidget.setColumnWidth(0,65)
                self.ui.FOMF_tableWidget.setColumnWidth(1,120)
                self.ui.FOMF_tableWidget.setColumnWidth(2,90)
                self.ui.FOMF_tableWidget.setColumnWidth(3,60)
                self.ui.FOMF_tableWidget.setColumnWidth(4,90)
                self.ui.FOMF_tableWidget.setColumnWidth(5,180)
                currentRowCount = 0
                for row in results:
                    for colCount in range(0, len(results[0])):
                        self.ui.FOMF_tableWidget.setItem(currentRowCount, colCount, QTableWidgetItem(str(row[colCount])))
                    currentRowCount += 1

            except Exception as e:
                print("friends changed failed", e)


        #when business table changes, change #should also show number of business, number of popular business and categories of selected business and attributes of selected business
    def analysis(self, order):
        self.ui.AnalysisTable.clear()
        #uid = "pm2Xtpl0zwp94Yaj5cT26g"  #uid can be get from the previous part. Change this when combining code.
        selection = self.ui.login2_list_widget.selectedItems()
        uid = selection[0].text()
        sql_str = "select yelp_business.business_id, yelp_business.name, yelp_business.stars, count(distinct user_id),case when value = '1' then '$' when value = '2' then '$$' when value = '3' then '$$$' when value = '4' then '$$$$' end Price_range, case when numcheckins < 51 then '*' when numcheckins > 50 and numcheckins < 101 then '**' when numcheckins > 100 and numcheckins < 501 then '***' when numcheckins > 500 and numcheckins < 801 then '****' when numcheckins > 800 then '*****' end Popularity from friends, yelp_tips, yelp_business, attributes where user_id_1 = '"+uid+"' and user_id_2 = yelp_tips.user_id and yelp_business.business_id = yelp_tips.business_id and yelp_business.business_id = attributes.business_id and attr_name = 'RestaurantsPriceRange2' group by yelp_business.business_id, yelp_business.name, stars, value, numcheckins, yelp_business.stars order by "+order+" desc"
        sql_str2 = "select business_id, text from yelp_tips where business_id in(select yelp_business.business_id from friends, yelp_tips, yelp_business, attributes where user_id_1 = '"+uid+"' and user_id_2 = yelp_tips.user_id and yelp_business.business_id = yelp_tips.business_id and yelp_business.business_id = attributes.business_id and attr_name = 'RestaurantsPriceRange2' group by yelp_business.business_id)"
        tips = {}
        tips_polarity = {}
        try:
            results = self.executeQuery(sql_str2)
            for row in results:
                #print(row)
                bid = row[0]
                text = row[1]
                if bid in tips:
                    tips[bid].append(text)
                else:
                    tips[bid] = [text]

            for key, value in tips.items():
                polarity_values = []
                #print(value)
                for text in value:
                    #print(text)
                    polarity = TextBlob(text).sentiment.polarity
                    #print(polarity)
                    polarity_values.append(polarity)
                polarity = sum(polarity_values)/len(polarity_values)
                tips_polarity[key] = polarity
            #print(tips_polarity)
            for key, value in tips_polarity.items():
                if value >= 0.5:
                    tips_polarity[key] = "+++++"
                elif value >= 0.4:
                    tips_polarity[key] = "++++"
                elif value >= 0.3:
                    tips_polarity[key] = "+++"
                elif value >= 0.2:
                    tips_polarity[key] = "++"
                elif value >= 0.1:
                    tips_polarity[key] = "+"
                elif value <= -0.05:
                    tips_polarity[key] = "-----"
                elif value <= -0.04:
                    tips_polarity[key] = "----"
                elif value <= -0.03:
                    tips_polarity[key] = "---"
                elif value <= -0.02:
                    tips_polarity[key] = "--"
                elif value <= -0.01:
                    tips_polarity[key] = "-"
                else:
                    tips_polarity[key] = "#"
            #print(tips_polarity)
        except Exception as e:
            print("Analysis failed", e)
        #print(tips)
        try:
            results = self.executeQuery(sql_str)
            results_new = []
            for row in results:
                row_new = row[1:] + (tips_polarity[row[0]],)
                results_new.append(row_new)
            results = results_new
            self.ui.AnalysisTable.setColumnCount(len(results[0]))
            self.ui.AnalysisTable.setRowCount(len(results))
            self.ui.AnalysisTable.setHorizontalHeaderLabels(['Name','Star','My friends reviewed','Price', 'Popularity', 'Review polarity'])
            self.ui.AnalysisTable.resizeColumnsToContents()
            self.ui.AnalysisTable.setColumnWidth(0,150)
            self.ui.AnalysisTable.setColumnWidth(1,50)
            self.ui.AnalysisTable.setColumnWidth(2,180)
            self.ui.AnalysisTable.setColumnWidth(3,60)
            self.ui.AnalysisTable.setColumnWidth(4,100)
            self.ui.AnalysisTable.setColumnWidth(5,140)
            currentRowCount = 0

            for row in results:
                for colCount in range(0, len(results[0])):
                    item = QTableWidgetItem(str(row[colCount]))
                    if colCount == 3:
                        if len(str(row[colCount])) == 4:
                            item.setForeground(QBrush(QColor("red")))
                        if len(str(row[colCount])) == 3:
                            item.setForeground(QBrush(QColor("magenta")))
                        if len(str(row[colCount])) == 2:
                            item.setForeground(QBrush(QColor("blue")))
                        if len(str(row[colCount])) == 1:
                            item.setForeground(QBrush(QColor("darkGreen")))
                    self.ui.AnalysisTable.setItem(currentRowCount, colCount, item)
                currentRowCount += 1

        except Exception as e:
            print("analysis 2 failed", e)

    def order_star(self):
        order = "yelp_business.stars"
        self.analysis(order)

    def order_price(self):
        order = "price_range"
        self.analysis(order)

    def order_popularity(self):
        order = "popularity"
        self.analysis(order)





if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = milestone2_v2()
    window.show()
    sys.exit(app.exec_())