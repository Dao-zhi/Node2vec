
import numpy as np
import sys
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
import networkx as nx
from sklearn.manifold import TSNE

sys.path.append(r'../')
from algorithm.classify import read_node_label, Classifier
from algorithm.node2vec import Node2Vec



def evaluate_embeddings(embeddings):
    X, Y = read_node_label(r'./data/wiki_labels.txt')
    tr_frac = 0.8
    print("Training classifier using {:.2f}% nodes...".format(
        tr_frac * 100))
    clf = Classifier(embeddings=embeddings, clf=LogisticRegression())
    clf.split_train_evaluate(X, Y, tr_frac)


def plot_embeddings(embeddings,):
    X, Y = read_node_label(r'./data/wiki_labels.txt')

    emb_list = []
    for k in X:
        emb_list.append(embeddings[k])
    emb_list = np.array(emb_list)

    model = TSNE(n_components=2)
    node_pos = model.fit_transform(emb_list)

    color_idx = {}
    for i in range(len(X)):
        color_idx.setdefault(Y[i][0], [])
        color_idx[Y[i][0]].append(i)

    for c, idx in color_idx.items():
        plt.scatter(node_pos[idx, 0], node_pos[idx, 1], label=c)
    plt.legend()    # 添加图例
    plt.savefig("./results/Visualization.png")    # 保存图片
    # plt.show()    # 显示可视化结果，仅供调试使用

def execute_node2vec(filename, p=0.25, q=4):
    # print("p: " + str(p) + ", q: " + str(q))    # 输出两个超参数
    G=nx.read_edgelist(filename,create_using = nx.DiGraph(), 
                       nodetype = None, data = [('weight', int)])    # 读取图

    model=Node2Vec(G, walk_length = 10, num_walks = 80, p=q, q=q, workers = 1)    # 初始化模型
    model.train(window_size = 5, iter = 3)    # 训练模型
    embeddings=model.get_embeddings()    # 获得嵌入向量

    evaluate_embeddings(embeddings)    # 评估嵌入向量
    plot_embeddings(embeddings)    # 绘制嵌入结果
    return embeddings

if __name__ == "__main__":
    G=nx.read_edgelist('data/Wiki_edgelist.txt',
                         create_using = nx.DiGraph(), nodetype = None, data = [('weight', int)])    # 读取图
    
    model=Node2Vec(G, walk_length = 10, num_walks = 80,
                   p = 0.25, q = 4, workers = 1)    # 初始化模型
    model.train(window_size = 5, iter = 3)    # 训练模型
    embeddings=model.get_embeddings()    # 获得嵌入向量

    evaluate_embeddings(embeddings)    # 评估嵌入向量
    plot_embeddings(embeddings)    # 绘制嵌入结果
