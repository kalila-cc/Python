# -*- coding: utf-8 -*-

import copy
from fractions import Fraction


"""
目前仅支持矩阵的行变换，并且对其进行操作记录，支持撤销操作，支持增广炬阵，可用于求逆矩阵或方程的解
"""
class LinearAlgebraAssistant:
    
    def __init__(self):
        self.table = []
        self.table_history = []
        self.operation_history = []
    
    @staticmethod
    def trans(s):
        return [Fraction(t) for t in s.split()]
    
    def display(self):
        print('当前矩阵为：')
        for i in range(len(self.table)):
            print('  '.join(['{:8}'.format(str(Fraction(x))) for x in self.table[i]]))
        print('操作历史：\n', self.operation_history, sep='')
    
    def E_ij(self, i, j):
        self.table[i - 1], self.table[j - 1] = self.table[j - 1], self.table[i - 1]
        operation = 'r{}<->r{}'.format(i, j)
        return operation

    def E_ik(self, i, k):
        self.table[i - 1] = [k * t for t in self.table[i - 1]]
        operation = 'r{}×({})'.format(i, k)
        return operation

    def E_ijk(self, i, j, k):
        for t in range(len(self.table[0])):
            self.table[i - 1][t] += k * self.table[j - 1][t]
        operation = 'r{}+r{}×({})'.format(i, j, k)
        return operation

    def reset(self):
        self.table = []
        row, column = (eval(x) for x in input('请输入矩阵的行和列：\n').split())
        if row < 1 or column < 1:
            print('请给矩阵行和列赋正整数的值！\n')
            return self.reset()
        for t in range(row):
            self.table.append(self.trans(input('请输入第{:d}行的{:d}个元素：\n'.format(t + 1, column))))
            while len(self.table[-1]) != column:
                if len(self.table[-1]) > column:
                    print('输入元素个数过多，已默认截取前{:d}个元素!\n'.format(column))
                    self.table[-1] = self.table[-1][:column]
                else:
                    self.table[-1] += self.trans(input('输入元素个数过少，请追加元素!\n'))

    def modify(self):
        if len(self.table) == 0:
            print('未创建过矩阵，请选择重新建立!')
        else:
            choose = eval(input('请选择修改模式：\n1.增广矩阵   2.单个修改   3.批量修改\n'))
            if choose == 1:
                self.extend()
            elif choose == 2:
                while True:
                    try:
                        cr, cc, vl = tuple(input('请分别输入所需修改的行，列, 值, 只能修改已存在的元素，完成修改后请输入0 0 0：\n').split())
                        cr, cc, vl = eval(cr), eval(cc), Fraction(vl)
                        if cr <= 0 or cc <= 0:
                            break
                        self.table[cr - 1][cc - 1] = vl
                    except Exception as e:
                        print('参数输入错误，请重新输入!')
                        print(e)
            elif choose == 3:
                while True:
                    try:
                        x = input('请输入所需修改的行/列, 行用 R/r 开头, 列用 C/c 开头, 完成修改后输入 0 以退出本模块：\n')
                        if x == '0':
                            break
                        elif x[0] not in 'RrCc' or not x[1:].strip().isdigit():
                            print('请输入正确的操作符格式!\n')
                            continue
                        else:
                            if x[0] in 'rR' and (int(x[1:]) > len(self.table) or int(x[1:]) < 1):
                                print('请输入合适范围的行数!\n')
                                continue
                            elif x[0] in 'Cc' and (int(x[1:]) > len(self.table[0]) or int(x[1:]) < 1):
                                print('请输入合适范围的列数!\n')
                                continue
                            else:
                                if x[0] in 'rR':
                                    s = self.trans(input('请输入需要覆盖第{:d}行的{:d}个数据:\n'.format(int(x[1:]),len(self.table[0]))))
                                    if len(s) > len(self.table[0]):
                                        print('输入元素过多，已默认截取前{:d}个元素\n'.format(len(self.table[0])))
                                        self.table[int(x[1:])-1] = s[:len(self.table[0])]
                                    else:
                                        while len(s) < len(self.table[0]):
                                            s += self.trans(input('输入元素过少，请追加元素：\n'))
                                        if len(s) > len(self.table[0]):
                                            print('输入元素过多，已默认截取前{:d}个元素\n'.format(len(self.table[0])))
                                            self.table[int(x[1:])-1] = s[:len(self.table[0])]
                                        else:
                                            self.table[int(x[1:])-1] = s
                                else:
                                    s = self.trans(input('请输入需要覆盖第{:d}列的{:d}个数据:\n'.format(int(x[1:]), len(self.table))))
                                    if len(s) > len(self.table):
                                        print('输入元素过多，已默认截取前{:d}个元素\n'.format(len(self.table)))
                                        for m in range(len(self.table)):
                                            self.table[m][int(x[1:])-1] = s[m]
                                    else:
                                        while len(s) < len(self.table):
                                            s += self.trans(input('输入元素过少，请追加元素：\n'))
                                        if len(s) > len(self.table):
                                            print('输入元素过多，已默认截取前{:d}个元素\n'.format(len(self.table)))
                                        for m in range(len(self.table)):
                                            self.table[m][int(x[1:]) - 1] = s[m]
                    except Exception as e:
                        print('指令参数出错，请重新输入!\n')
                        print(e)
            else:
                print('指令出错，已默认不对矩阵进行修改!')

    def extend(self):
        choose = eval(input('请选择增广类型：\n1.E  2.b  3.B\n'))
        if choose == 1:
            for t in range(len(self.table)):
                s = [0] * (len(self.table) - 1)
                s.insert(t, 1)
                self.table[t] += s
            self.backup()
        elif choose == 2:
            bv = []
            while len(bv) < len(self.table):
                bv = self.trans(input('请输入增广所需列向量的{:d}个元素：\n'.format(len(self.table))))
                if len(bv) >= len(self.table):
                    if len(bv) > len(self.table):
                        print('输入元素过多，已默认截取前{:d}个元素\n'.format(len(self.table)))
                    for m in range(len(self.table)):
                        self.table[m] += [bv[m]]
                else:
                    while len(bv) < len(self.table):
                        bv += self.trans(input('输入元素过少，请追加元素：\n'))
                    if len(bv) > len(self.table):
                        print('输入元素过多，已默认截取前{:d}个元素\n'.format(len(self.table)))
                    for m in range(len(self.table)):
                        self.table[m] += [bv[m]]
            self.backup()
        elif choose == 3:
            B_column = eval(input('请输入列向量组的列的数量：\n'))
            for i in range(B_column):
                bv = []
                while len(bv) < len(self.table):
                    bv = self.trans(input('请输入增广所需的第{:d}个列向量的{:d}个元素：\n'.format(i+1,len(self.table))))
                    if len(bv) >= len(self.table):
                        if len(bv) > len(self.table):
                            print('输入元素过多，已默认截取前{:d}个元素\n'.format(len(self.table)))
                        for m in range(len(self.table)):
                            self.table[m] += [bv[m]]
                    else:
                        while len(bv) < len(self.table):
                            bv += self.trans(input('输入元素过少，请追加元素：\n'))
                        if len(bv) > len(self.table):
                            print('输入元素过多，已默认截取前{:d}个元素\n'.format(len(self.table)))
                        for m in range(len(self.table)):
                            self.table[m] += [bv[m]]
            self.backup()
        else:
            print('指令出错，默认不对矩阵进行修改')

    def backup(self):
        self.table_history.append(copy.deepcopy(self.table))

    def handler(self):
        keep_operate = True
        choose = eval(input('\n'+'-'*70+'\n请输入需要进行的操作：\n1.E(ij)   2.E(i(k))   3.E(ij(k))   4.撤回   5.修改   6.退出\n'))
        # 退出
        if choose == 6:
            keep_operate = False
        # 不退出
        else:
            # 撤回
            if choose == 4:
                if len(self.table_history) > 0:
                    self.table = self.table_history.pop()
                if len(self.operation_history) > 0:
                    self.operation_history.pop()
            # 否则, 行/列变换
            else:
                # 需要修改矩阵数据
                if choose == 5:
                    self.modify()
                # 直接进行变换
                else:
                    if choose in (1, 2, 3):
                        try:
                            self.backup()
                            if choose == 1:
                                i, j = (eval(x) for x in input('请输入对应的i，j：\n').split())
                                operation = self.E_ij(i, j)
                            elif choose == 2:
                                i, k = tuple(input('请输入对应的i，k：\n').split())
                                i, k = eval(i), Fraction(k)
                                operation = self.E_ik(i, k)
                            else:
                                i, j, k = tuple(input('请输入对应的i，j，k：\n').split())
                                i, j, k = eval(i), eval(j), Fraction(k)
                                operation = self.E_ijk(i, j, k)
                            self.operation_history.append(operation)
                        except Exception as e:
                            self.table_history.pop()
                            print('矩阵操作错误, 请重试')
                            print(e)
                    else:
                        print('请输入正确的指令!\n')
        return keep_operate

    def run(self):
        # 初始化
        try:
            self.reset()
            self.backup()
            self.display()
        except Exception as e:
            print('矩阵建立出错，请重试\n')
            print(e)
        # 若 table 不为空，则执行主操作
        if len(self.table) > 0:
            keep_operate = True
            # 询问是否需要扩增为增广矩阵
            try:
                choose = eval(input('是否需要扩为增广矩阵：\n1.是  2.否\n'))
                if choose == 1:
                    self.extend()
                    self.display()
                elif choose == 2:
                    pass
                else:
                    print('指令错误, 默认不对矩阵进行修改')
            except Exception as e:
                print('矩阵扩增出错,请重试')
                print(e)
            # 循环处理
            while keep_operate:
                try:
                    keep_operate = self.handler()
                    if not keep_operate:
                        break
                    self.display()
                except Exception as e:
                    print('矩阵操作出错，请重试!\n')
                    print(e)
            print('欢迎下次使用, 再见！')


def main():
    laa = LinearAlgebraAssistant()
    laa.run()


if __name__ == '__main__':
    main()
