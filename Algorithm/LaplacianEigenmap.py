# -*- coding: utf-8 -*-

import numpy as np
import numpy.linalg as la
import matplotlib.pyplot as plt
import sklearn.datasets as datasets
from mpl_toolkits.mplot3d import Axes3D


# 拉普拉斯特征映射 (Laplacian Eigenmaps) k 是近邻数，t 是 热核参数
def LaplacianEigenmap(original_data: np.ndarray, k: int = -1, t: float = -1):
    shape = original_data.shape
    # 初始化邻接矩阵
    W = np.zeros((shape[0], shape[0]))
    # 计算邻接矩阵
    if k > 0:
        for i in range(shape[0]):
            dist = la.norm(original_data - original_data[i], axis=1)
            knn_index = np.argsort(dist)[1: k + 1]
            knn_dist = np.exp(dist[knn_index] * dist[knn_index] / -t) if t > 0 else np.ones(k)
            W[i, knn_index] = knn_dist
            W[knn_index, i] = knn_dist
    else:
        for i in range(shape[0]):
            dist = la.norm(original_data - original_data[i], axis=1)
            knn_dist = np.exp(dist * dist / -t) if t > 0 else np.ones(shape[0])
            W[i, :] = knn_dist
            W[:, i] = knn_dist
    # 邻接矩阵构建完毕，计算 D 和 L
    D = np.diag(np.sum(W, axis=0))
    L = D - W
    # 计算广义特征值问题
    eigVal, eigVec = la.eig(np.diag(1 / np.sum(W, axis=0)) @ L)
    eigIdx = np.argsort(eigVal)
    # 找到非零特征值对应的特征向量
    non_zero_index = 0
    while eigVal[eigIdx[non_zero_index]] < 1e-12:
        non_zero_index += 1
    eigVec = eigVec[:, eigIdx[non_zero_index:]]
    # 返回非零特征值对应的特征向量
    return eigVec.real


# 论文涉及的算法示例
def main():
    # 生成瑞士卷数据集
    swiss_roll, color = datasets.samples_generator.make_swiss_roll(n_samples=2000)
    swiss_roll[:, 1] *= 5
    # 原始图像
    ax = Axes3D(plt.figure())
    ax.scatter(swiss_roll[:, 0], swiss_roll[:, 1], swiss_roll[:, 2], c=color, marker='+', cmap=plt.cm.get_cmap('nipy_spectral'))
    plt.show()
    # 试试降维后仍然 3D 输出
    mapped_swiss_roll = LaplacianEigenmap(swiss_roll, k=5, t=5)[:, 0:3]
    ax = Axes3D(plt.figure())
    ax.scatter(mapped_swiss_roll[:, 0], mapped_swiss_roll[:, 1], mapped_swiss_roll[:, 2], c=color, marker='+', cmap=plt.cm.get_cmap('nipy_spectral'))
    plt.show()
    # 多图预警（都降维至2D）
    row, col = 3, 3
    k_start, t_start, k_step, t_step = 5, -15, 5, 20
    for r, k in enumerate(range(k_start, k_start + k_step * row, k_step)):
        for c, t in enumerate(range(t_start, t_start + t_step * col, t_step)):
            print('k = {}, t = {}'.format(k, (t if t > 0 else 'oo')))
            axis = plt.subplot(row, col, r * col + c + 1)
            axis.set_title('k = {}, t = {}'.format(k, (t if t > 0 else 'oo')), fontsize=8)
            mapped_swiss_roll = LaplacianEigenmap(swiss_roll, k=k, t=t)[:, 0:2]
            plt.scatter(mapped_swiss_roll[:, 0], mapped_swiss_roll[:, 1], c=color, marker='+', cmap=plt.cm.get_cmap('nipy_spectral'))
    plt.tight_layout()
    plt.show()
    pass


# 如果想看看 3D 转 2D 再转 3D 的效果，请在最底下调用该函数
def just_for_fun():
    # 生成瑞士卷数据集
    swiss_roll, color = datasets.samples_generator.make_swiss_roll(n_samples=2000)
    swiss_roll[:, 1] *= 5
    # 3D 输出
    ax = Axes3D(plt.figure())
    ax.scatter(swiss_roll[:, 0], swiss_roll[:, 1], swiss_roll[:, 2], c=color, marker='+', cmap=plt.cm.get_cmap('nipy_spectral'))
    plt.show()
    # 3D -> 2D 输出
    mapped_swiss_roll = LaplacianEigenmap(swiss_roll, k=5, t=5)[:, 0:2]
    plt.scatter(mapped_swiss_roll[:, 0], mapped_swiss_roll[:, 1], c=color, marker='+', cmap=plt.cm.get_cmap('nipy_spectral'))
    plt.show()
    # 3D -> 2D -> 3D 输出
    mapped_swiss_roll = LaplacianEigenmap(mapped_swiss_roll, k=5, t=5)[:, 0:3]
    ax = Axes3D(plt.figure())
    ax.scatter(mapped_swiss_roll[:, 0], mapped_swiss_roll[:, 1], mapped_swiss_roll[:, 2], c=color, marker='+', cmap=plt.cm.get_cmap('nipy_spectral'))
    plt.show()
    pass


if __name__ == '__main__':
    # just_for_fun()
    main()
    pass
