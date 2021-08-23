# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os

"""
自定义表达式中的 a 和 r 的值：
    x^r + y^r = a^r
    x^(r/(r+1)) + y^(r/(r+1)) = a^(r/(r+1))
"""
a, r = 1, 1

"""
定义变量（允许修改）：
    frames: 画线密度
    duration: 画线持续时间，单位 ms
    delay: 延迟显示拟合曲线时间，单位 ms
"""
frames = 20
duration = 3 * 1000
delay = 1 * 1000

"""
绘图选项（允许修改）：
    axis_accuracy: 坐标轴精度
    colors: 可用线条颜色
"""
axis_accuracy = 0.2
colors = ['grey', 'green']

"""
导出配置（允许修改）：
    save_as_video: 是否导出视频
    save_path: 出视频路径，默认导出到桌面
    fps: 导出视频帧率
(备注：目前导出功能可能用不了，暂时无法解决，可以选择录屏方式进行报错)
"""
save_as_video = False
save_path = os.path.join(os.path.expanduser('~'), 'Desktop')
fps = 24

"""
计算变量（不需修改）：
    interval: 动画刷新间隔
    total_frames: 总帧数
"""
interval = duration // frames
total_frames = frames + np.ceil(delay / interval).astype(int)


# 初始化坐标轴
def init_ax(ax, a):
    # 设置网格
    ax.grid(True, linestyle='-.')
    # 设置坐标轴范围
    ax.set_xlim(0, a)
    ax.set_ylim(0, a)
    # 设置坐标轴精度
    ax.xaxis.set_major_locator(plt.MultipleLocator(axis_accuracy))
    ax.yaxis.set_major_locator(plt.MultipleLocator(axis_accuracy))
    # 设置坐标轴比例
    ax.set_aspect('equal', adjustable='box')


# 更新动画
def update(frame, ax, a, r):
    if frame > frames:
        if frame + 1 == total_frames:
            plot_eq(ax, a, r)
    else:
        x = a * (frame / frames)
        minus = np.abs(np.power(a, r) - np.power(x, r))
        y = 0 if minus == 0 else np.power(minus, 1 / r)
        ax.plot((x, 0), (0, y), color=colors[0], linewidth=1)


# 绘制拟合曲线
def plot_eq(ax, a, r):
    exponent = r / (r + 1)
    x = np.linspace(0, a, 100)
    y = np.power(np.power(a, exponent) - np.power(x, exponent), 1 / exponent)
    ax.plot(x, y, color=colors[1], linewidth=3)
    ax.text(a * 0.4, a * 0.6, f'$x^\\frac{{{r}}}{{{r + 1}}}+y^\\frac{{{r}}}{{{r + 1}}}=a^\\frac{{{r}}}{{{r + 1}}}$', fontSize=15)


# 主函数
def main():
    # 获取子图对象
    fig = plt.figure()
    ax = fig.add_subplot('111')
    fig_manager = plt.get_current_fig_manager()
    fig_manager.window.state('zoomed')
    # 初始化子图
    init_ax(ax, a)
    # 开启动画
    anim = animation.FuncAnimation(fig, update, frames=total_frames, interval=interval, fargs=(ax, a, r), repeat=False)
    if save_as_video:
        ffmpeg_path = os.popen('where ffmpeg').read().rstrip()
        if os.path.exists(ffmpeg_path):
            plt.rcParams['animation.ffmpeg_path'] = ffmpeg_path
            print('动画正在准备导出为视频，请稍等')
            try:
                writer = animation.FFMpegWriter(fps=fps)
                anim.save(save_path, writer=writer)
                print(f'动画已导出为视频，请前往 "{save_path}" 查看')
            except Exception as e:
                print('导出过程出现未知错误')
        else:
            print('导出为视频需要安装 ffmpeg 并配置环境变量，未检测到 ffmpeg 的存在')
    plt.show()


if __name__ == '__main__':
    main()
