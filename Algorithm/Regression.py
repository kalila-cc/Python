# -*- coding: utf-8 -*-

import numpy as np
import numpy.linalg as la


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


def LinearRegression(X: np.ndarray, Y: np.ndarray):
    return la.inv(X.T @ X) @ X.T @ Y


def LogisticsRegression(X: np.ndarray, Y: np.ndarray, eta: float = 1e-2):
    W = np.random.rand(X.shape[1], Y.shape[1])
    for i in range(250):
        grad = X.T @ (sigmoid(X @ W) - Y)
        W -= eta * grad
    return W


def RidgeRegression(X: np.ndarray, Y: np.ndarray, alpha: float = 0):
    return la.inv((X.T @ X + np.diag([alpha] * X.shape[1]))) @ X.T @ Y
