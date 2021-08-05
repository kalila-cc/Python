# -*- coding: utf-8 -*-

import numpy as np
import numpy.linalg as la
import matplotlib.pyplot as plt


"""
该手动实现的网络仅支持输出值域在 [0, 1] 之间，也不支持偏置值，但支持多值输出
"""
class FullyConnectedNeuralNetwork:
    def __init__(self, layer: tuple):
        self.__num_layers = len(layer)
        self.__W = []
        for i in range(len(layer) - 1):
            self.__W.append(np.random.rand(layer[i + 1], layer[i]))
        self.__neuron = []
        for i in range(len(layer)):
            self.__neuron.append(np.zeros((layer[i], 1)))

    def fit(self, X: np.ndarray, Y: np.ndarray, max_epoch: int = 1000, eta: float = 0.05):
        num_samples = X.shape[0]
        loss_record = [self.__calc_loss(X, Y)]
        for epoch in range(max_epoch):
            for i in range(num_samples):
                x, y = X[[i]].T, Y[[i]].T
                neuron = [x]
                for layer in range(self.__num_layers - 1):
                    neuron.append(self.__sigmoid(self.__W[layer] @ neuron[layer]))
                pLpn = [neuron[self.__num_layers - 1] - y]
                for layer in range(self.__num_layers - 1, 1, -1):
                    pLpn.append(self.__W[layer - 1].T @ (pLpn[-1] * neuron[layer] * (1 - neuron[layer])))
                pLpn.reverse()
                pLpW = []
                for layer in range(self.__num_layers - 1):
                    pLpW.append((pLpn[layer] * neuron[layer + 1] * (1 - neuron[layer + 1])) @ neuron[layer].T)
                    self.__W[layer] -= eta * pLpW[layer]
            loss_record.append(self.__calc_loss(X, Y))
            print('\rtraining: {:5.2f} %'.format(100 * (epoch + 1) / max_epoch), end='')
        print()
        # 测试误差是否正在下降
        plt.plot(range(len(loss_record)), loss_record)
        plt.show()

    def pred(self, X: np.ndarray):
        pred_Y = []
        if len(X.shape) < 2:
            X = np.array([X])
        for x in X:
            neuron = [x]
            for layer in range(self.__num_layers - 1):
                neuron.append(self.__sigmoid(self.__W[layer] @ neuron[layer]))
            pred_Y.append(neuron[-1])
        return np.array(pred_Y)

    def __calc_loss(self, X: np.ndarray, Y: np.ndarray) -> float:
        loss = 0.0
        num_samples = X.shape[0]
        for i in range(num_samples):
            x, y = X[[i]], Y[[i]]
            loss += 0.5 * np.squeeze(la.norm(self.pred(x) - y))
        return loss

    @staticmethod
    def __sigmoid(x: np.ndarray) -> np.ndarray:
        return 1.0 / (1.0 + np.exp(-x))


def main():
    # 设置参数
    x_num = 1000
    train_ratio = 0.9
    # 生成数据集，为了保证 Y = WX 在 [0, 1] 之间，只要 W 本身以及 X_i 都在二维单位圆内即可
    radius = np.random.rand()
    theta = np.random.rand()
    W = np.array([[radius * np.sin(theta), radius * np.cos(theta)]]).T
    radius = np.random.rand(x_num)
    theta = np.random.rand(x_num)
    X = np.array([radius * np.sin(theta), radius * np.cos(theta)])
    Y = W.T @ X
    # 分割数据集
    sep = int(x_num * train_ratio)
    train_X, test_X = X[:, :sep].T, X[:, sep:].T
    train_Y, test_Y = Y[:, :sep].T, Y[:, sep:].T
    # 训练模型
    fcnn = FullyConnectedNeuralNetwork((2, 2, 1))
    fcnn.fit(train_X, train_Y, max_epoch=1000, eta=0.1)
    pred_Y = fcnn.pred(test_X)
    print(pred_Y.T[0])
    print(test_Y.T[0])
    pass


if __name__ == '__main__':
    main()

