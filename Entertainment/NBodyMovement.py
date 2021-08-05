import numpy as np
import numpy.linalg as la
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d.axes3d import Axes3D


def get2Body():
    mass = np.array([5.965e24, 7.349e22], dtype=float)
    coordinate = np.array([
        [0, 0, 0],
        [0, 3.844e8, 0]
    ], dtype=float)
    speed = np.array([
        [0, 0, 0],
        [-1023, 0, 0]
    ], dtype=float)
    return mass, coordinate, speed


def get3Body():
    mass = np.array([7.5e23, 7.5e23, 7.5e23], dtype=float)
    coordinate = np.array([
        [0, 0, 0],
        [0, 2e8, 0],
        [1.732e8, 1e8, 0]
    ], dtype=float)
    speed = np.array([
        [433, -250, 0],
        [-433, -250, 0],
        [0, 500, 0]
    ], dtype=float)
    return mass, coordinate, speed


def get4Body():
    mass = np.array([7.5e23, 7.5e23, 7.5e23, 7.5e23], dtype=float)
    coordinate = np.array([
        [0, 0, 0],
        [0, 2e8, 0],
        [2e8, 2e8, 0],
        [2e8, 0, 0]
    ], dtype=float)
    v = 410
    speed = np.array([
        [1.01 * v, -v, 0],
        [-v, -v, 0],
        [-v, v, 0],
        [v, 0.99 * v, 0]
    ], dtype=float)
    return mass, coordinate, speed


def getNBody(N: int, mass_base: float = 2e24, coordinate_base: float = 2e8, speed_base: float = 0):
    mass = mass_base * (np.random.rand(N) - 0.5)
    coordinate = coordinate_base * (np.random.rand(N, 3) - 0.5)
    speed = speed_base * (np.random.rand(N, 3) - 0.5)
    return mass, coordinate, speed


def _update_(num, trace, lines, tail):
    if tail is not None and num > tail:
        for line, one_trace in zip(lines, trace):
            line.set_data(one_trace[0:2, num - tail: num])
            line.set_3d_properties(one_trace[2, num - tail: num])
    else:
        for line, one_trace in zip(lines, trace):
            line.set_data(one_trace[0:2, :num])
            line.set_3d_properties(one_trace[2, :num])
    return lines


class Uniuerse:
    _G_ = 6.67e-11
    _colors_ = ['deepskyblue', 'red', 'limegreen', 'c', 'aqua', 'm', 'y', 'deeppink', 'darkorange', 'grey']
    SECOND, MINUTE, HOUR, DAY, WEEK, MONTH, YEAR = 1, 60, 3600, 86400, 604800, 2592000, 31536000

    def __init__(self, mass: np.ndarray, coordinate: np.ndarray, speed: np.ndarray):
        self._N_ = mass.shape[0]
        self._lims_ = []
        self._mode_ = 'default'
        self._mass_ = mass
        self._coordinate_ = coordinate
        self._speed_ = speed
        self._dist_ = np.zeros((self._N_, self._N_))
        self._acceleration_ = np.zeros((3, self._N_, self._N_))
        self._trace_ = [[] for i in range(self._N_)]
        for i in range(self._N_):
            self._trace_[i].append(self._coordinate_[i].copy())

    def _cal_dist_(self):
        for i in range(self._N_):
            self._dist_[i] = la.norm(self._coordinate_ - self._coordinate_[i], axis=1)
        self._dist_ += np.eye(self._N_)

    def _cal_acceleration_(self):
        for i in range(self._N_):
            for j in range(self._N_):
                if i != j:
                    self._acceleration_[:, i, j] = self._coordinate_[j] - self._coordinate_[i]
        self._acceleration_ /= np.power(self._dist_, 3)
        self._acceleration_ *= Uniuerse._G_ * np.broadcast_to(self._mass_, (3, self._N_, self._N_))

    def _cal_range_(self, lims):
        xlim = [np.min(lims[0][0]), np.max(lims[1][0])]
        ylim = [np.min(lims[0][1]), np.max(lims[1][1])]
        zlim = [np.min(lims[0][2]), np.max(lims[1][2])]
        xrange = xlim[1] - xlim[0] + 1
        yrange = ylim[1] - ylim[0] + 1
        zrange = zlim[1] - zlim[0] + 1
        xlim = [xlim[0] - 0.3 * xrange, xlim[1] + 0.3 * xrange]
        ylim = [ylim[0] - 0.3 * yrange, ylim[1] + 0.3 * yrange]
        zlim = [zlim[0] - 0.3 * zrange, zlim[1] + 0.3 * zrange]
        return xlim, ylim, zlim

    def setlims(self, mode, xlim: list = None, ylim: list = None, zlim: list = None):
        if mode == 'default':
            self._mode_ = mode
        elif mode == 'auto':
            self._mode_ = mode
        elif mode == 'custom':
            self._mode_ = mode
            self._lims_ = [xlim, ylim, zlim]

    def move(self, t: float, dt: float = 1):
        acceleration = np.zeros((self._N_, 3), dtype=float)
        for times in range(int(t / dt)):
            self._cal_dist_()
            self._cal_acceleration_()
            for i in range(self._N_):
                acceleration[i] = np.sum(self._acceleration_[:, i, :], axis=1)
            self._speed_ += dt * acceleration
            self._coordinate_ += dt * self._speed_
            for i in range(self._N_):
                self._trace_[i].append(self._coordinate_[i].copy())

    def trace(self, interval: int = 1, tail: int = None, static: bool = False):
        fig = plt.figure()
        ax = Axes3D(fig)
        ax.set_xlabel('x axis')
        ax.set_ylabel('y axis')
        ax.set_zlabel('z axis')
        self._trace_ = [np.array(t).T for t in self._trace_]
        cut_trace, lims = [], [[[], [], []], [[], [], []]]
        interval_index = [i for i in range(0, self._trace_[0].shape[1], interval)]
        for one_trace in self._trace_:
            cut_trace.append(one_trace[:, interval_index])
            for i in range(3):
                lims[0][i].append(np.min(cut_trace[-1][i]))
                lims[1][i].append(np.max(cut_trace[-1][i]))
        if self._mode_ == 'custom':
            xlim, ylim, zlim = self._lims_
            ax.set_xlim3d(xlim)
            ax.set_ylim3d(ylim)
            ax.set_zlim3d(zlim)
        elif self._mode_ == 'auto':
            xlim, ylim, zlim = self._cal_range_(lims)
            ax.set_xlim3d(xlim)
            ax.set_ylim3d(ylim)
            ax.set_zlim3d(zlim)
        if static:
            for one_trace in cut_trace:
                ax.plot(one_trace[0], one_trace[1], one_trace[2])
        else:
            lines = [ax.plot(one_trace[0: 1, 0], one_trace[1: 2, 0], one_trace[2: 3, 0])[0] for one_trace in cut_trace]
            anim = animation.FuncAnimation(fig, _update_, self._trace_[0].shape[1], fargs=(cut_trace, lines, tail), interval=0, blit=True, repeat=True)
        plt.show()
        self._trace_ = [[] for i in range(self._N_)]


def main():
    mass, coordinate, speed = get3Body()
    xlim, ylim, zlim = [-1.5e8, 1.5e8], [-1.5e8, 1.5e8], [-1.5e8, 1.5e8]
    sys = Uniuerse(mass, coordinate, speed)
    sys.setlims('auto', xlim, ylim, zlim)
    circular_time = Uniuerse.HOUR
    run_times = 3 * Uniuerse.MONTH // circular_time
    for i in range(run_times):
        sys.move(t=circular_time, dt=Uniuerse.MINUTE)
        print('\r{:.2f} %'.format(100 * (i + 1) / run_times), end='')
    print()
    sys.trace(interval=120, tail=60, static=False)


if __name__ == '__main__':
    main()
