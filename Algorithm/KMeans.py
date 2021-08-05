# -*- coding: utf-8 -*-

import numpy as np
import numpy.linalg as la


class Kmeans:
    def __init__(self, k: int):
        self.k = k
        self.max_epoch = 3 * k
        self.rand_times = 2 * k
        self.dim = None
        self.kernel = None
        self.label = None

    def fit(self, X: np.ndarray):
        num_samples = X.shape[0]
        self.dim = X.shape[1]
        self.kernel = np.zeros((self.k, self.dim))
        self.label = np.zeros((num_samples,))
        lim = np.zeros((2, self.dim))
        lim[0] = np.min(X, axis=0)
        lim[1] = np.max(X, axis=0)
        kernel_list = []
        for times in range(self.rand_times):
            for dim in range(self.dim):
                self.kernel[:, dim] = lim[0, dim] + (lim[1, dim] - lim[0, dim]) * np.random.rand(self.k)
            epoch = 0
            while True:
                for i in range(num_samples):
                    self.label[i] = np.argmin(la.norm(self.kernel - X[i], axis=1))
                old_loss_value = self.loss(X, self.kernel, self.label)
                for i in range(self.k):
                    co_label = self.label == i
                    self.kernel[i] = np.random.rand(self.dim) if not co_label.any() else np.mean(X[co_label], axis=0)
                new_loss_value = self.loss(X, self.kernel, self.label)
                delta_loss_value = abs(old_loss_value - new_loss_value)
                epoch += 1
                if delta_loss_value < 1e-2 or epoch >= self.max_epoch:
                    break
            loss = self.loss(X, self.kernel, self.label)
            kernel_list.append((times, loss, self.kernel.copy()))
        opt_kernel_info = min(kernel_list, key=lambda x: x[1])
        self.kernel = opt_kernel_info[2].copy()
        for i in range(num_samples):
            self.label[i] = np.argsort(la.norm(self.kernel - X[i], axis=1))[0]

    def test(self, X: np.ndarray, y: np.ndarray):
        num_err = 0
        num_samples = X.shape[0]
        for i in range(self.k):
            co_label = self.label == i
            if co_label.any():
                co_y = y[co_label]
                num_err += np.count_nonzero(co_y - np.argmax(np.bincount(co_y)))
        return 1.0 - num_err / num_samples

    @staticmethod
    def loss(X: np.ndarray, kernel: np.ndarray, label: np.ndarray):
        label = label.astype(np.int)
        loss_value = 0
        num_samples = X.shape[0]
        for i in range(num_samples):
            loss_value += la.norm(X[i] - kernel[label[i]])
        return loss_value
