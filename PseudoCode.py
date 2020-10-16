def selectFile():
    fileName = QFileDialog.getOpenFileName()   #获得文件名
    if fileName == "":    # 判断文件名是否为空
        lineEdit.setText("默认文件路径")
    else:
        lineEdit.setText(fileName)

def loadFile()
    fileName = lineEdit.text()    # 获得文件路径
    if fileName:                #判断路径非空
        f = QFile(fileName)       #创建文件对象                                                                                     #open()会自动返回一个文件对象
        f = open(fileName, "r")     #打开路径所对应的文件， "r"以只读的方式 也是默认的方式
        with f:
           data = f.read()
        f.close()
        count = len(open(fileName,'r').readlines())    # 读取边的数目即文本的行数
        lines = (line.decode(encoding) for line in count)
        G=nx.read_edgelist(fileName,create_using = nx.DiGraph(), 
                  nodetype = None, data = [('weight', int)])    # 读取图
        lineEdit_1.setText(str(len(G.nodes)))    # 显示结点数
        lineEdit_2.setText(str(len(G.edges)))    # 显示边数
        textEdit.setText(data)    # 显示网络详细信息

def exportEmbeddings():
    fileName =  QFileDialog.getExistingDirectory()
    lineEdit.setText(fileName)
    fileName = lineEdit.text() + '/embedding.txt'
    f = open(fileName, 'w')
    with f:
        for keys,values in GLOBALEMBEDDINGS.items():
            f.write(data)
    f.close()

    filaName = lineEdit.text() + '/Visualization.png'
    shutil.copyfile('./results/Visualization.png', filaName)

def classification(self):
    embeddings = self.GLOBALEMBEDDINGS
    # 聚类
    k = spinbox.value() #聚类的类别
    iteration = 3 #聚类最大循环次数
    kmeans_data = pd.DataFrame.from_dict(embeddings, orient = 'index')    # 将字典转化为DataFrame
    kmeans_data.head()    # 加入表头
    kmeans_data_sz = 1.0*(kmeans_data - kmeans_data.mean())/kmeans_data.std() #数据标准化
    model = KMeans(n_clusters = k, max_iter = iteration)    # 初始化聚类模型，分为k类
    model.fit(kmeans_data_sz)    # 开始聚类
    
    #用TSNE进行数据降维并展示聚类结果
    tsne = TSNE()
    tsne.fit_transform(kmeans_data) #进行数据降维,并返回结果
    tsne = pd.DataFrame(tsne.embedding_, index = kmeans_data.index) #转换数据格式

    png = QtGui.QPixmap() # 创建一个绘图类
    png = draw(tsne)    # 绘图

    item = QtWidgets.QGraphicsPixmapItem(png) #创建一个QGraphicsPixmapItem
    self.scene.addItem(item) # 添加对象

def exportClassification():
    if fileName:
        filaName = lineEdit.text() + '/Classification.png'
        shutil.copyfile('./results/Classification.png', filaName)
        filaName = lineEdit.text() + '/data_type.xlsx'
        shutil.copyfile('./results/data_type.xlsx', filaName)

self.pushButton.clicked.connect(self.selectFile)
self.pushButton_2.clicked.connect(self.loadFile)
self.pushButton_3.clicked.connect(self.excute)
self.pushButton_4.clicked.connect(self.selectEmbeddingsFile)
self.pushButton_6.clicked.connect(self.selectClassificationFile)
self.pushButton_5.clicked.connect(self.exportEmbeddings)
self.pushButton_7.clicked.connect(self.exportClassification)
self.pushButton_classification.clicked.connect(self.classification)