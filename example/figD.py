"""
figure D

"""

import histone
import histone.figure as figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import matplotlib

NUM_OF_HISTONE = 81
WINDOW = 10
TIME1 = 1008
TIME2 = 1008
DELTA = 5

NUMEXAMPLE = 20


def main():
    count = 0
    list_tracker = []
    for _ in range(NUMEXAMPLE):
        list_tracker = submain(count, list_tracker)
        count += 1

    fig = plt.figure()

    figure.dynamic_change(fig, list_tracker)

    plt.show()

    title = "figD/fig_test4__{}examples.pdf".format(NUMEXAMPLE)
    pp = PdfPages(title)
    pp.savefig(fig)
    pp.close()


def submain(count, list_tracker):
    R = 0
    A = 1
    secR = 1
    secA = 1

    T = 0
    plt.style.use('ggplot')
    font = {'family': 'sans-serif'}
    matplotlib.rc('font', **font)

    histoneList1 = histone.init_genome(percentage=50,
                                       a_bool=A,
                                       hst_n=NUM_OF_HISTONE
                                       )

    dictH = histone.track_epigenetic_process(hst_list=histoneList1,
                                             time=TIME1,
                                             a_bool=A,
                                             r_bool=R,
                                             t_bool=T
                                             )
    tracker = dictH["vectorize"]
    hstL = dictH["hstL"]
    TList = dictH["TList"]

    dictH2 = histone.track_epigenetic_process(hst_list=hstL,
                                              time=TIME2,
                                              a_bool=secA,
                                              r_bool=secR,
                                              t_bool=TList[-1]
                                              )
    tracker2 = dictH2["vectorize"]

    finalTracker = np.concatenate((tracker, tracker2))

    list_tracker.append(finalTracker)

    print(count)
    return list_tracker


if __name__ == "__main__":
    main()
