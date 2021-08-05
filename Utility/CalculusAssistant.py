# -*- coding: utf-8 -*-

from sympy import *


def desc():
    print(
        "欢迎使用简易微积分计算器！目前仅支持单变量计算，注意乘法表达式不能省略*符号。\n"
        "以下是可供使用的变量、常数和函数：\n"
        "E：自然对数的底数  pi：圆周率  I：虚数单位  oo：无穷大\n"
        "根号：sqrt(x)\n"
        "n次方根：root(x,n)\n"
        "指数：x**n | exp(x)\n"
        "对数：log(x,base=E)\n"
        "三角函数：sin/cos/tan/csc/sec/cot(x)\n"
        "反三角函数：asin/acos/atan/acsc/asec/acot(x)\n"
        "开始使用吧！\n"
    )


def main():
    # 输出提示
    desc()
    # 准备变量
    x, f = Symbol('x'), Function('f')
    # 循环
    while True:
        print("-----------------------------------------------------------")
        # 选择所需功能
        try:
            choice = int(input(
                "请输入需要的功能：\n"
                "1. 求不定积分\n"
                "2. 求定积分\n"
                "3. 求导\n"
                "4. 求零点\n"
                "5. 求极限\n"
                "6. 求解微分方程\n"
                "7. 退出程序\n"
            ))
            # 执行功能
            try:
                # 求不定积分
                if choice == 1:
                    eq = input("请输入需要计算不定积分函数表达式：\n")
                    print("{} 的原函数为 {}\n".format(eq, integrate(eval(eq), x)))
                # 求定积分
                elif choice == 2:
                    eq = input("请输入需要计算定积分的函数和上下限，三个量用空格分隔；\n")
                    func, a, b = tuple(map(eval, eq.split()))
                    print("{} 在 {} 到 {} 的积分值为 {}\n".format(func, a, b, integrate(func, (x, a, b))))
                # 求导
                elif choice == 3:
                    eq = input("请输入需要求导的函数表达式：\n")
                    print("{} 的导函数为 {}\n".format(eq, diff(eval(eq), x)))
                # 求零点
                elif choice == 4:
                    eq = input("请输入需要求零点的函数表达式：\n")
                    print('{} 的零点为 {}'.format(eq, solve(eval(eq), x)))
                # 求极限
                elif choice == 5:
                    eq = input("请输入需要求极限的函数表达式和取极限的点，用空格分隔：\n")
                    e, x0 = tuple(map(eval, eq.split()))
                    try:
                        left_lim = limit(e, x, x0, dir='-')
                    except Exception as e:
                        left_lim = nan
                        print(e)
                    try:
                        right_lim = limit(e, x, x0, dir='+')
                    except Exception as e:
                        right_lim = nan
                        print(e)
                    print("{} 在 x = {} 处的左极限为 {}  右极限为 {}\n".format(eq, x0, left_lim, right_lim))
                # 求解微分方程
                elif choice == 6:
                    eq = input("请输入需要求解的微分方程：\n")
                    eq = eq.replace("y", "f(x)").replace("''", ".diff(x, x)").replace("'", ".diff(x)")
                    lhs, rhs = (tuple(hs.strip() for hs in eq.split("=")))
                    lhs, rhs = eval(lhs), eval(rhs)
                    eq = Eq(lhs, rhs)
                    print("方程 {} 的解为 {}".format(eq, dsolve(eq)))
                # 退出程序
                elif choice == 7:
                    print('欢迎下次使用，再见！')
                    exit(0)
                # 输入错误
                else:
                    print("输入错误！")
            except Exception as e:
                print("计算过程出错！")
                print(e)
        except Exception as e:
            print("输入错误！")
            print(e)


if __name__ == '__main__':
    main()
