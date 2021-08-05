# -*- coding: utf-8 -*-

import numpy as np
import numpy.linalg as la
from typing import Tuple


# 通过 Gram-Schmidt 算法进行 QR 分解
def GramSchmidt(A: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    m, n = A.shape
    Q = np.zeros((m, n))
    Q[:, [0]] = A[:, [0]] / la.norm(A[:, [0]])
    for i in range(1, n):
        Q_slice = Q[:, :i]
        Q[:, [i]] = (np.eye(n) - Q_slice @ Q_slice.T) @ A[:, [i]]
        Q[:, [i]] /= la.norm(Q[:, [i]])
    R = Q.T @ A
    return Q, R


# 通过 Householder 算法进行 QR 分解
def Householder(A: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    m, n = A.shape
    R = A.copy()
    Q = np.eye(n)
    for i in range(n - 1):
        B = R[i:, i:]
        e = np.zeros((n - i, 1))
        e[0, 0] = 1
        b = B[:, [0]]
        u = b - la.norm(b) * e
        u /= la.norm(u)
        if la.norm(u) < 1e-10:
            print(la.norm(u))
        H = np.eye(n)
        H[i:, i:] = np.eye(n - i) - 2 * u @ u.T
        R = H @ R
        Q = Q @ H
    return Q, R


# 计算上三角矩阵的逆
def invUTM(A: np.ndarray) -> np.ndarray:
    m, n = A.shape
    P = np.eye(n)
    for i in range(n):
        P[i, i] = 1 / A[i, i]
    for i in reversed(range(n - 1)):
        Pi = np.eye(n)
        Pi[i, i + 1:] = -1 * A[i, i + 1:] / A[i, i]
        P = Pi @ P
    return P
