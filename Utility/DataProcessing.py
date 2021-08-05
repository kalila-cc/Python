# -*- coding: utf-8 -*-

import os, re
from math import *
import matplotlib.pyplot as plt

ConfProb = {1:1, 3:1.32, 4:1.20, 5:1.14, 6:1.11, 7:1.09, 8:1.08, 9:1.07, 10:1.06, 15:1.04, 20:1.03}
path = "Cache.txt"

if not os.path.exists("Cache.txt"):
    open(path, "w", encoding="utf-8").write(str({}))
var = eval(open("Cache.txt", "r").read())


def getData(name):
    if var.get(name, None) != None:
        if input(name + "已存在，真的要覆盖它吗？(输入1或0以确认或取消)") == "1":
            var.pop(name)
        else:
            return 0
    print("\n请开始输入数据(按'q'退出输入)：\n")
    var[name] = {}
    v = var[name]
    v["namec"] = re.findall("[a-zA-Z\d]+", name)[0]
    v["data"] = []
    flag = "1"
    i = 0
    while flag != "q":
        i += 1
        flag = input(f"第{i}个数据：")
        v["data"].append(flag)
    v["inserr"] = eval(input("\n请输入仪器误差(无则输入0)："))
    v["zeroerr"] = eval(input("\n请输入零点偏差(无则输入0)："))
    if input("\n数据输入完成，请确认数据都已经准确输入了吗？(输入1或0以确认或修改)\n") != "1":
        confirmData(name)
    v["data"] = list(map(eval, v["data"][:-1]))
    v["length"] = len(v["data"])
    v["average"] = sum(v["data"]) / v["length"]
    v["stdev"] = sqrt(sum(list(map(lambda x: (x - v["average"]) ** 2, v["data"]))) / (v["length"] - 1)) if v["length"]>1 else 0
    v["stdunA"] = v["stdev"] / sqrt(v["length"])
    v["stdunB"] = v["inserr"] / sqrt(3)
    v["cmbun"] = sqrt((ConfProb[v["length"]]*v["stdunA"])**2+(v["stdunB"])**2)
    v["rlvun"] = v["cmbun"]/(v["average"]-v["zeroerr"])


def confirmData(name):
    if var.get(name, None) == None:
        print("\n这个数据表不存在！")
    else:
        v = var[name]
        main_choose = input("\n请选择需要更改的数据类型(可多选)：1.表格数据  2.其他数据\n")
        if "1" in main_choose:
            choose = input("\n已选[表格数据]，请选择处理方式(可多选)：1.更改数据  2.删除数据  3.增加数据\n")
            if "1" in choose:
                while True:
                    iv = input("\n请输入需要更改的数据序号及新数据(输入'q'完成操作)：")
                    if iv == "q":
                        break
                    index, value = tuple(iv.split())
                    v["data"][int(index) - 1] = value
            if "2" in choose:
                while True:
                    iv = input("\n请输入需要删除的数据序号(输入'q'完成操作)：")
                    if iv == "q":
                        break
                    v["data"].pop(int(iv))
            if "3" in choose:
                while True:
                    iv = input("\n请输入需要插入的数据序号及新数据(输入'q'完成操作)：")
                    if iv == "q":
                        break
                    index, value = iv.split()
                    v["data"].insert(int(index) - 1, value)
        if "2" in main_choose:
            while True:
                iv = input("\n已选[其他数据]，请输入所属更改的数据名称及新数据(输入'q'完成更改)：")
                if iv == "q":
                    break
                index, value = iv.split()
                v[index] = eval(value)


def displayData(name=None):
    displayList = var.keys() if name == None else [name]
    for key in displayList:
        v = var[key]
        print("\n\n{:s}的数据处理如下所示：\n(提示：数据仅供参考，请手动把握精度)\n".format(key))
        print("仪器误差：{:f}".format(v["inserr"]))
        print("零点偏差：{:f}".format(v["zeroerr"]))
        print("平均数：{:f}".format(v["average"]))
        print("标准差：{:f}".format(v["stdev"]))
        print("A类不确定度：{:f}".format(v["stdunA"]))
        print("B类不确定度：{:f}".format(v["stdunB"]))
        print("合成不确定度：{:f}".format(v["cmbun"]))
        print("相对不确定度：{:f}".format(v["rlvun"]))


def saveData():
    open(path, "w").write(str(var))
    print("\n数据已成功保存！")


def clearData(name=None):
    global var
    if var.get(name, None) == None:
        open("Cache.txt", "w", encoding="utf-8").write("")
        var = {}
        print("\n成功清空数据表！")
    else:
        var.pop(name)
        print("\n成功清除数据表{:s}！".format(name))


def checkHistory(name=None):
    checkList = var.keys() if name == None else [name]
    for key in checkList:
        v = var[key]
        print("\n\n{:s}的原始数据如下所示：\n(提示：数据仅供参考，请手动把握精度)\n".format(key))
        print("仪器误差：{:f}".format(v["inserr"]))
        print("零点偏差：{:f}".format(v["zeroerr"]))
        print("平均数：{:f}".format(v["average"]))
        print("标准差：{:f}".format(v["stdev"]))
        print("A类不确定度：{:f}".format(v["stdunA"]))
        print("B类不确定度：{:f}".format(v["stdunB"]))
        print("合成不确定度：{:f}".format(v["cmbun"]))
        print("相对不确定度：{:f}".format(v["rlvun"]))


def calu(exp):
    try:
        exp = exp.replace("pi", str(pi)).replace("^", "**")
        keys = sorted(var.keys(), key=lambda x: len(var[x]["namec"]), reverse=True)
        for key in keys:
            v = var[key]
            exp = exp.replace(v["namec"], str(v["cmbun"]))
        print("\n经计算，该间接不确定度为：", eval(exp), sep="")
    except:
        print("\n表达式输入错误！")


def cala(exp):
    try:
        exp = exp.replace("pi", str(pi)).replace("^", "**")
        keys = sorted(var.keys(), key=lambda x: len(var[x]["namec"]))
        keys.reverse()
        arg, d = 0, {}
        for key in keys:
            nc = var[key]["namec"]
            mv = re.findall(nc, exp)
            for mvi in range(len(mv)):
                exp = exp.replace(nc, "@" + str(arg))
                d["@" + str(arg)] = nc
                arg += 1
        for k, v in d.items():
            exp = exp.replace(k, f"(var[getName('{v:s}')]['data'][i]-var[getName('{v:s}')]['zeroerr'])")
        lens, sum = var[getName(d["@0"])]["length"], 0
        for i in range(lens):
            sum += eval(exp)
        print("\n经计算，该间接测量量的平均值为：{:f}".format(sum / lens))
    except:
        print("\n表达式输入错误！")


def getName(namec):
    for key in var.keys():
        if namec == var[key]["namec"]:
            return key
    return "404"


def draw(name):
    v = var[name]
    plt.xlabel("次数")
    plt.ylabel(name)
    plt.plot(list(range(1, v["length"] + 1)), v["data"], "ro")
    plt.show()


if __name__ == "__main__":
    while True:
        displayData()
        if input("\n---------------------------------------------\n需要添加新的数据表格吗？(输入1或0以确认或取消)\n") == "1":
            getData(input("\n请输入新的数据表的名字："))
        if input("\n需要额外功能吗？(包括：更改数据，画图，清除/清空/保存数据表，查看原始数据，计算间接平均值/不确定度，更改不确定度结果等)\n") == "1":
            choose = input(
                "\n"
                "请选择需要的功能：\n"
                "1.更改数据\n"
                "2.画散点图\n"
                "3.清除数据表\n"
                "4.清空数据表\n"
                "5.保存数据表\n"
                "6.计算间接不确定度  \n"
                "7.计算间接平均值\n"
            )
            if choose == "1":
                confirmData(getName(input("\n请输入需要修改数据的名字：")))
            elif choose == "2":
                draw(getName(input("\n请输入需要画图的数据表的名字：")))
            elif choose == "3":
                clearData(getName(input("\n请输入需要清除的数据表的名字：")))
            elif choose == "4":
                clearData()
            elif choose == "5":
                saveData()
            elif choose == "6":
                checkHistory()
            elif choose == "7":
                calu(input("\n请输入计算表达式："))
            elif choose == "8":
                cala(input("\n请输入计算表达式："))
        if input("\n需要退出程序吗？(输入1或0以确认或取消)\n") == "1":
            break
