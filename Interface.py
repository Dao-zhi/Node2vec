from PyQt5 import QtCore, QtGui, QtWidgets    # Qt基本模块
from PyQt5.QtWidgets import QFileDialog, QGraphicsPixmapItem, QGraphicsItem, QGraphicsView, QGraphicsTextItem   # 文件对话框
from PyQt5.QtCore import QFile, QSize     # 文件模块
from PyQt5.QtGui import QPixmap, QColor    # 图像处理模块
import sys
sys.path.append(r'../')
from node2vecApplication import execute_node2vec
import shutil
import networkx as nx
import pandas as pd    # 用于矩阵处理
from sklearn.cluster import KMeans    # 用于k-means聚类
from sklearn.manifold import TSNE    # 用于降维并可视化显示
import threading    # 用于实现多线程
import ctypes    # 用于隐藏控制台窗口

import os    # 打印当前目录用

class Ui_Widget(QtWidgets.QMainWindow):
    GLOBALEMBEDDINGS = {}
    loadFlag = False
    excuteFlag = False
    classificationFlag = False
    def __init__(self):
        super().__init__()
    
    def setupUi(self, Widget):
        Widget.setObjectName("Widget")
        Widget.resize(1320, 817)
        self.groupBox_4 = QtWidgets.QGroupBox(Widget)
        self.groupBox_4.setGeometry(QtCore.QRect(10, 140, 1281, 101))
        self.groupBox_4.setObjectName("groupBox_4")
        self.label_4 = QtWidgets.QLabel(self.groupBox_4)
        self.label_4.setGeometry(QtCore.QRect(20, 40, 45, 18))
        self.label_4.setObjectName("label_4")
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.groupBox_4)
        self.doubleSpinBox.setGeometry(QtCore.QRect(100, 40, 76, 24))
        self.doubleSpinBox.setProperty("value", 0.25)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.label_5 = QtWidgets.QLabel(self.groupBox_4)
        self.label_5.setGeometry(QtCore.QRect(450, 40, 45, 18))
        self.label_5.setObjectName("label_5")
        self.doubleSpinBox_2 = QtWidgets.QDoubleSpinBox(self.groupBox_4)
        self.doubleSpinBox_2.setGeometry(QtCore.QRect(530, 40, 76, 24))
        self.doubleSpinBox_2.setProperty("value", 4.0)
        self.doubleSpinBox_2.setObjectName("doubleSpinBox_2")
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.label_setproperty = QtWidgets.QLabel(self.groupBox_4)
        self.label_setproperty.setGeometry(QtCore.QRect(900, 40, 75, 30))
        self.label_setproperty.setObjectName("label_setproperty")
        self.spinBox = QtWidgets.QSpinBox(self.groupBox_4)
        self.spinBox.setGeometry(QtCore.QRect(980, 40, 112, 34))
        self.spinBox.setObjectName("spinBox")
        self.spinBox.setProperty("value", 3)
        self.groupBox = QtWidgets.QGroupBox(Widget)
        self.groupBox.setGeometry(QtCore.QRect(10, 270, 441, 531))
        self.groupBox.setObjectName("groupBox")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(14, 32, 72, 18))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(14, 66, 63, 18))
        self.label_2.setObjectName("label_2")
        self.graphicsView = QtWidgets.QGraphicsView(self.groupBox)
        self.graphicsView.setGeometry(QtCore.QRect(14, 129, 411, 391))
        self.graphicsView.setObjectName("graphicsView")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_2.setGeometry(QtCore.QRect(102, 32, 321, 24))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_3.setGeometry(QtCore.QRect(102, 66, 321, 24))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(189, 100, 72, 18))
        self.label_3.setObjectName("label_3")
        self.groupBox_2 = QtWidgets.QGroupBox(Widget)
        self.groupBox_2.setGeometry(QtCore.QRect(460, 270, 431, 531))
        self.groupBox_2.setObjectName("groupBox_2")
        # self.textEdit = QtWidgets.QTextEdit(self.groupBox_2)
        # self.textEdit.setGeometry(QtCore.QRect(14, 75, 411, 391))
        # self.textEdit.setObjectName("textEdit")
        self.graphicsView_3 = QtWidgets.QGraphicsView(self.groupBox_2)
        self.graphicsView_3.setGeometry(QtCore.QRect(14, 75, 411, 391))
        self.graphicsView_3.setObjectName("graphicsView3")
        self.pushButton_3 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_3.setGeometry(QtCore.QRect(140, 30, 173, 34))
        self.pushButton_3.setObjectName("pushButton_3")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_4.setGeometry(QtCore.QRect(10, 480, 171, 25))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.pushButton_4 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_4.setGeometry(QtCore.QRect(190, 480, 112, 34))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_5.setGeometry(QtCore.QRect(310, 480, 112, 34))
        self.pushButton_5.setObjectName("pushButton_5")
        self.groupBox_3 = QtWidgets.QGroupBox(Widget)
        self.groupBox_3.setGeometry(QtCore.QRect(900, 270, 411, 531))
        self.groupBox_3.setObjectName("groupBox_3")
        # self.label_7 = QtWidgets.QLabel(self.groupBox_3)
        # self.label_7.setGeometry(QtCore.QRect(140, 30, 108, 18))
        # self.label_7.setObjectName("label_7")
        self.pushButton_classification = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_classification.setGeometry(QtCore.QRect(140, 30, 173, 34))
        self.pushButton_classification.setObjectName("pushButton_classification")
        self.graphicsView_2 = QtWidgets.QGraphicsView(self.groupBox_3)
        self.graphicsView_2.setGeometry(QtCore.QRect(10, 80, 391, 381))
        self.graphicsView_2.setObjectName("graphicsView_2")
        self.graphicsView_2.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.pushButton_6 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_6.setGeometry(QtCore.QRect(170, 480, 112, 34))
        self.pushButton_6.setObjectName("pushButton_6")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEdit_5.setGeometry(QtCore.QRect(10, 480, 151, 25))
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.pushButton_7 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_7.setGeometry(QtCore.QRect(290, 480, 112, 34))
        self.pushButton_7.setObjectName("pushButton_7")
        self.lineEdit = QtWidgets.QLineEdit(Widget)
        self.lineEdit.setGeometry(QtCore.QRect(30, 40, 1111, 24))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(Widget)
        self.pushButton.setGeometry(QtCore.QRect(1170, 40, 112, 34))
        self.pushButton.setFlat(False)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Widget)
        self.pushButton_2.setGeometry(QtCore.QRect(1170, 90, 112, 34))
        self.pushButton_2.setObjectName("pushButton_2")
        self.retranslateUi(Widget)

        # 自定义按钮响应函数
        self.pushButton.clicked.connect(self.selectFile)
        self.pushButton_2.clicked.connect(self.loadFile)
        self.pushButton_3.clicked.connect(self.excute_button)
        self.pushButton_4.clicked.connect(self.selectEmbeddingsFile)
        self.pushButton_6.clicked.connect(self.selectClassificationFile)
        self.pushButton_5.clicked.connect(self.exportEmbeddings)
        self.pushButton_7.clicked.connect(self.exportClassification)
        self.pushButton_classification.clicked.connect(self.classification_button)
        QtCore.QMetaObject.connectSlotsByName(Widget)

    def retranslateUi(self, Widget):
        _translate = QtCore.QCoreApplication.translate
        Widget.setWindowTitle(_translate("Widget", "图神经网络Node2vec算法的研究和实现"))
        self.groupBox_4.setTitle(_translate("Widget", "参数设置"))
        self.label_4.setText(_translate("Widget", "P参数："))
        self.label_5.setText(_translate("Widget", "Q参数："))
        # self.spinbox.setText(_translate("Widget", "设置参数"))
        self.groupBox.setTitle(_translate("Widget", "网络信息"))
        self.label.setText(_translate("Widget", "结点数："))
        self.label_2.setText(_translate("Widget", "边 数："))
        self.label_3.setText(_translate("Widget", "网络展示"))
        self.label_setproperty.setText(_translate("Widget", "分类类别："))
        self.groupBox_2.setTitle(_translate("Widget", "向量化表示结果"))
        self.pushButton_3.setText(_translate("Widget", "生成向量化表示结果"))
        self.pushButton_4.setText(_translate("Widget", "选择路径"))
        self.pushButton_5.setText(_translate("Widget", "导出文件"))
        self.groupBox_3.setTitle(_translate("Widget", "结点分类"))
        # self.label_7.setText(_translate("Widget", "分类结果展示"))
        self.pushButton_6.setText(_translate("Widget", "选择路径"))
        self.pushButton_7.setText(_translate("Widget", "导出文件"))
        self.lineEdit.setText(_translate("Widget", "data\\Wiki_edgelist.txt"))
        self.pushButton.setText(_translate("Widget", "选择文件"))
        self.pushButton_2.setText(_translate("Widget", "加载文件"))
        self.pushButton_classification.setText(_translate("Widget", "显示分类结果"))
    
    def selectFile(self):
        fileName, filetype = QFileDialog.getOpenFileName(self,
                                    "选取文件",
                                    "./",
                                    "All Files (*);;Text Files (*.txt)")   #设置文件扩展名过滤,注意用双分号间隔
        if fileName == "":
            self.lineEdit.setText("data\\Wiki_edgelist.txt")
        else:
            self.lineEdit.setText(fileName)

    def selectEmbeddingsFile(self):
        # fileName, filetype = QFileDialog.getSaveFileName(self,
        #                             "选取文件",
        #                             "./",
        #                             "Text Files (*.txt)")   #设置文件扩展名过滤,注意用双分号间隔
        fileName =   QFileDialog.getExistingDirectory()
        self.lineEdit_4.setText(fileName)

    def selectClassificationFile(self):
        # fileName, filetype = QFileDialog.getSaveFileName(self,
        #                             "选取文件",
        #                             "./",
        #                             "Image Files (*.png;*.jpg)")   #设置文件扩展名过滤,注意用双分号间隔
        fileName =   QFileDialog.getExistingDirectory()
        self.lineEdit_5.setText(fileName)

    def loadFile(self):
        # try:
        fileName = self.lineEdit.text()
        if fileName:                                                                   #判断路径非空
            f = QFile(fileName)                                                       #创建文件对象，不创建文件对象也不报错 也可以读文件和写文件                                                                                       #open()会自动返回一个文件对象
            f = open(fileName, "r")                                                    #打开路径所对应的文件， "r"以只读的方式 也是默认的方式
            with f:
               data = f.read()
               self.scene = QtWidgets.QGraphicsScene() # 创建一个图形管理场景
               self.graphicsView.setScene(self.scene)    # 为graphicsView设置图形管理器
               item = QtWidgets.QGraphicsTextItem()    # 创建文本对象
               item.setPlainText(data)    # 为文本对象添加文本
               item.setPos(50, 50)
               self.scene.addItem(item) # 添加对象  
            f.close()
            count = len(open(fileName,'r').readlines())# 读取边的数目即文本的行数
            G=nx.read_edgelist(fileName,create_using = nx.DiGraph(), 
                      nodetype = None, data = [('weight', int)])    # 读取图
            # print(len(G.nodes))
            # print(len(G.edges))
            self.lineEdit_2.setText(str(len(G.nodes)))    # 显示结点数
            self.lineEdit_3.setText(str(len(G.edges)))    # 显示边数

        self.loadFlag = True
        # except:
        #     QtWidgets.QMessageBox.warning(self, "警告", "加载文件失败，请检查文件名！", QtWidgets.QMessageBox.Yes)

    def excute_button(self):
        if self.loadFlag:
            self.excute()
            self.excuteFlag = True
        else:
            QtWidgets.QMessageBox.warning(self, "警告", "请先加载网络文件！", QtWidgets.QMessageBox.Yes)
        # try:
        #     new_thread = threading.Thread(target=self.excute)#创建线程
        #     new_thread.setDaemon(True)#设置为后台线程，这里默认是False，设置为True之后则主线程不用等待子线程
        #     new_thread.start()    #开启线程
        # except:
        #     QMessageBox.warning(self, "警告对话框", "创建线程失败，请重试！", QMessageBox.Yes)
             
    def excute(self):
        p = self.doubleSpinBox.value()    # 读取超参数p
        q = self.doubleSpinBox_2.value()    # 读取超参数q
        fileName = self.lineEdit.text()    # 读取文件路径
        # print(os.getcwd())    # 打印当前路径
        try:
            embeddings = execute_node2vec(fileName, p, q)    # 执行node2vec算法
        except:
            QtWidgets.QMessageBox.warning(self, "警告", "算法运行出现错误，请检查文件是否正确加载！", QtWidgets.QMessageBox.Yes)
        self.GLOBALEMBEDDINGS = embeddings
        # 显示嵌入结果
        # for i in embeddings:
        #     self.textEdit.append(str(i))
        # 这儿的位置用来显示可视化结果了
        # for keys,values in embeddings.items():
        #     # print(keys)
        #     # print(values)
        #     self.textEdit.append(str(keys))
        #     self.textEdit.append(str(values))
        #     self.textEdit.append('---------------')
        # print(type(embeddings))
        # self.textEdit.append(str(embeddings))
        # 显示可视化结果
        self.graphicsView_3.setGeometry(QtCore.QRect(10, 80, 391, 381)) # 设置图形视图的矩形区域
        self.scene = QtWidgets.QGraphicsScene() # 创建一个图形管理场景
        self.graphicsView_3.setScene(self.scene)
        picSize = QSize(391, 381)    # 画布大小
        png = QtGui.QPixmap() # 创建一个绘图类
        png.load("./results/Visualization.png") # 从png中加载一个图片
        # png.load("logo.png")
        png = png.scaled(picSize)
        item = QtWidgets.QGraphicsPixmapItem(png) #创建一个QGraphicsPixmapItem
        self.scene.addItem(item) # 添加对象   

    def classification_button(self):
        try:
            # new_thread = threading.Thread(target=self.classification)#创建线程
            # new_thread.setDaemon(True)#设置为后台线程，这里默认是False，设置为True之后则主线程不用等待子线程
            # new_thread.start()    #开启线程
            self.classification()
            self.classificationFlag = True
        except Exception:
            QtWidgets.QMessageBox.warning(self, "警告", "线程执行出错，请检查是否生成向量化结果！", QtWidgets.QMessageBox.Yes)

    def classification(self):
        print("聚类类别：" + str(self.spinBox.value()))
        embeddings = self.GLOBALEMBEDDINGS
        # 聚类
        k = 3 #聚类的类别
        k = self.spinBox.value()
        iteration = 3 #聚类最大循环次数
        kmeans_data = pd.DataFrame.from_dict(embeddings, orient = 'index')    # 将字典转化为DataFrame
        kmeans_data.head()    # 加入表头
        kmeans_data_sz = 1.0*(kmeans_data - kmeans_data.mean())/kmeans_data.std() #数据标准化，std()表示求总体样本方差(除以n-1),numpy中std()是除以n
        print(kmeans_data)    # 显示DataFrame
        print(kmeans_data_sz)    # 显示DataFrame

        # table = QTableView()
        model = KMeans(n_clusters = k, max_iter = iteration)    # 初始化聚类模型，分为k类
        # table.setModel(model)
        model.fit(kmeans_data_sz)    # 开始聚类

        #简单打印结果
        r1 = pd.Series(model.labels_).value_counts() #统计各个类别的数目
        r2 = pd.DataFrame(model.cluster_centers_) #找出聚类中心
        r = pd.concat([r2, r1], axis = 1) #横向连接（0是纵向），得到聚类中心对应的类别下的数目
        print(r)
        r.columns = list(kmeans_data.columns) + [u'类别数目'] #重命名表头
        print(r)
        
        #详细输出原始数据及其类别
        outputfile = './results/data_type.xlsx'
        r = pd.concat([kmeans_data, pd.Series(model.labels_, index = kmeans_data.index)], axis = 1)  #详细输出每个样本对应的类别
        r.columns = list(kmeans_data.columns) + [u'聚类类别'] #重命名表头
        r.to_excel(outputfile) #保存结果
        
        #用TSNE进行数据降维并展示聚类结果
        tsne = TSNE()
        tsne.fit_transform(kmeans_data) #进行数据降维,并返回结果
        tsne = pd.DataFrame(tsne.embedding_, index = kmeans_data.index) #转换数据格式
        
        import matplotlib.pyplot as plt
        plt.rcParams['font.sans-serif'] = ['SimHei'] #用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False #用来正常显示负号
        
        #不同类别用不同颜色和样式绘图
        plt.cla()    # 清除画布中的内容
        for i in range(0, k):
            d = tsne[r[u'聚类类别'] == i]     #找出聚类类别为0的数据对应的降维结果
            plt.plot(d[0], d[1], linestyle='',marker = 'o')
        # d = tsne[r[u'聚类类别'] == 0]     #找出聚类类别为0的数据对应的降维结果
        # plt.plot(d[0], d[1], 'r.')
        # d = tsne[r[u'聚类类别'] == 1]
        # plt.plot(d[0], d[1], 'go')
        # d = tsne[r[u'聚类类别'] == 2]
        # plt.plot(d[0], d[1], 'b*')
        # plt.show()    # 显示分类结果
        plt.savefig("./results/Classification.png")    # 保存图片

        # 显示分类结果
        self.graphicsView_2.setGeometry(QtCore.QRect(10, 80, 391, 381)) # 设置图形视图的矩形区域
        self.scene = QtWidgets.QGraphicsScene() # 创建一个图形管理场景
        self.graphicsView_2.setScene(self.scene)
        picSize = QSize(391, 381)    # 画布大小
        png = QtGui.QPixmap() # 创建一个绘图类
        png.load("./results/Classification.png") # 从png中加载一个图片
        # png.load("logo.png")
        png = png.scaled(picSize)
        item = QtWidgets.QGraphicsPixmapItem(png) #创建一个QGraphicsPixmapItem
        self.scene.addItem(item) # 添加对象 

    def exportEmbeddings(self):
        if not self.excuteFlag:
            QtWidgets.QMessageBox.warning(self, "警告", "请先执行向量化算法！", QtWidgets.QMessageBox.Yes)
            return
        if self.lineEdit_4.text():
            fileName = self.lineEdit_4.text() + '/embedding.txt'
        else:
            fileName ='embedding.txt'
        f = open(fileName, 'w')
        with f:
            for keys,values in self.GLOBALEMBEDDINGS.items():
                # print(keys)
                # print(values)
                f.write(str(keys))
                f.write('\n')
                f.write(str(values))
                f.write('\n')
                f.write('------------------------------------------')
                f.write('\n')
        f.close()
        if self.lineEdit_4.text():
            fileName = self.lineEdit_4.text() + '/Visualization.png'
        else:
            fileName ='Visualization.png'
        shutil.copyfile('./results/Visualization.png', fileName)

    def exportClassification(self):
        if not self.classificationFlag:
            QtWidgets.QMessageBox.warning(self, "警告", "请先执行分类算法！", QtWidgets.QMessageBox.Yes)
            return
        if self.lineEdit_5.text():
            fileName = self.lineEdit_5.text() + '/Classification.png'
        else:
            fileName = 'Classification.png'
        shutil.copyfile('./results/Classification.png', fileName)
        if self.lineEdit_5.text():
            fileName = self.lineEdit_5.text() + '/data_type.xlsx'
        else:
            fileName = 'data_type.xlsx'
        shutil.copyfile('./results/data_type.xlsx', fileName)

def controller(ui):
    p = ui.doubleSpinBox.value()    # 读取超参数p
    q = ui.doubleSpinBox_2.value()    # 读取超参数q

    # 显示p，q
    ui.textEdit.append(str(p))
    ui.textEdit.append(str(q))

if __name__ == '__main__':  
    # 隐藏控制台窗口
    whnd = ctypes.windll.kernel32.GetConsoleWindow()    
    if whnd != 0:    
        ctypes.windll.user32.ShowWindow(whnd, 0)    
        ctypes.windll.kernel32.CloseHandle(whnd)
    app = QtWidgets.QApplication(sys.argv)    # 创建应用对象
    MainWindow = QtWidgets.QMainWindow()    # 创建主界面
    ui = Ui_Widget()    # 创建ui对象
    ui.setupUi(MainWindow)     # 为主界面设置ui
    
    MainWindow.show()    # 显示主界面
    QtWidgets.QApplication.processEvents()
    sys.exit(app.exec_())     # 安全退出