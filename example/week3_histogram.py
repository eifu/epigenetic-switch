import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

example_n = 1000
dir1 = "example/data/withNUC/data{}/".format(example_n)
hst_n = 81
kp = 0.145
km = 0.145
kn2_list = np.arange(0, 0.5, 0.025)  # length 20


def main():
    ka_list = [0, 0.025, 0.05, 0.075, 0.1]  # length 5
    for ka in ka_list:
        submain(ka)


def submain(ka):
    plt.style.use('ggplot')
    font = {'family': 'sans-serif'}
    matplotlib.rc('font', **font)
    fig1 = plt.figure()

    for i_kn2, kn2 in enumerate(kn2_list):

        kn1 = 0
        ax = fig1.add_subplot(20, 2, 2 * i_kn2 + 1)
        if i_kn2 == 0:
            ax.set_title("kn1: 0")
        ax.set_yticks([])
        if i_kn2 % 4 == 0:
            ax.set_ylabel(round(kn2, 4))
        ax.set_xticks([])
        filename = dir1 + "kn{}ka{}_kn{}ka{}/".format(round(kn1, 4),
                                                      round(ka, 4),
                                                      round(kn2, 4),
                                                      round(ka, 4)) + "final_hst_list_k+{}k-{}_{}examples.csv".format(
            kp,
            km, example_n)

        data = np.genfromtxt(filename, delimiter=',', dtype=np.int8)

        container = np.zeros(12)  # from 0 to 11. total 12 paterns
        for _, row in enumerate(data):
            container[sum((row + row * row) / 2)] += 1
        ax.set_ylim(0, max(container))
        ax.bar([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], container)

        kn1 = 1
        ax = fig1.add_subplot(20, 2, 2 * i_kn2 + 2)
        if i_kn2 == 0:
            ax.set_title("kn1: 1")
        ax.set_yticks([])
        if i_kn2 % 4 == 0:
            ax.set_ylabel(round(kn2, 4))
        ax.set_xticks([])
        filename = dir1 + "kn{}ka{}_kn{}ka{}/".format(round(kn1, 4),
                                                      round(ka, 4),
                                                      round(kn2, 4),
                                                      round(ka, 4)) + "final_hst_list_k+{}k-{}_{}examples.csv".format(
            kp,
            km,
            example_n)

        data = np.genfromtxt(filename, delimiter=',', dtype=np.int8)

        container = np.zeros(12)  # from 0 to 11. total 12 paterns
        for _, row in enumerate(data):
            container[sum((row + row * row) / 2)] += 1
        ax.set_ylim(0, max(container))
        ax.bar([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], container)

        print(i_kn2 / 20)

    title = "week3_histogram__ka{}__k+{}k-{}_N{}.pdf".format(round(ka, 4),
                                                             round(kp, 4),
                                                             round(km, 4),
                                                             example_n)
    pp = PdfPages(title)
    pp.savefig(fig1)
    pp.close()


if __name__ == "__main__":
    main()
