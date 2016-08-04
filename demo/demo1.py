import histone
import histone.figure
from time import strftime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib
import numpy as np

"""
demonstlation of histone library.
In this file, we demonstlate the histone code without DNA methylation model.
As are imported above, you have to have two libraries, numpy, matplotlib on
your local computer.

This code outputs a figure that has a list of histone in y-axis, and 
time series in x-axis.

NUM_OF_HISTONE ... global variable, a length of histones that you keep track.
WINDOW ... global variable, a length of locus in the list of histones.
TIME1 ... global variable, a time length of how long histones are held before
the environment changes.
TIME2 ... global variable, a time length of how long histones are held after
the environment changes.
"""

NUM_OF_HISTONE = 81
WINDOW = 10
TIME1 = 3 * 7 * 24  # 3 week in hours
TIME2 = 3 * 7 * 24  # 3 week in hours


def main():
    k_plus = 0.145
    k_minus = 0.145

    percent = 100

    R = 0
    A = 1
    secR = 1
    secA = 1

    k_nuc = 0.05
    k_ace = 0
    k_nuc2 = 1
    k_ace2 = 0

    # init_genome
    #
    # initializes a list of histone objects.
    # if you want to have a list of histones with
    # specific characterestics, you can custumize it with
    # keyword arguments.
    # input:
    # (list of keyword arguments)
    # - percentage .. probability of methylated histones.
    # - a_bool .. having activator On.
    # - hst_n .. number of histones in a list
    # - kp .. probability of k plus
    # - kp2 .. probability of k plus 2
    # - km .. probability of k minus
    # - ka .. probability of k ace
    #
    # output:
    # a list of histone objects
    histoneList1 = histone.init_genome(percentage=percent,
                                       a_bool=A,
                                       hst_n=NUM_OF_HISTONE,
                                       kp=k_plus,
                                       kp2=k_plus,
                                       km=k_minus,
                                       ka=k_ace
                                       )

    # track_epigenetic_process
    # 
    # returns a dictionary of the result of the records under
    # a specific environment. you can setup the environment
    # with keyword arguments.
    # input:
    # (list of keyword arguments)
    # - hst_list .. the initial condition of list of histones
    # - time .. the time length of tracking
    # - a_bool
    # - r_bool
    # - t_bool .. whether transcription happended last time or
    #             not. For the first tracking, we set up t_bool
    #             to be 0 as a default.
    T = 0
    P = True

    # - ace_prob .. K-ace probability.
    # - nuc_prob .. K-nuc probability.
    # output:
    # dictionary object that contains three data,
    # key: vectorize, value: a record of timeseries of list of histones.
    # key: hstL, value: a final status of list of histones
    # key: TList, value: a record of timeseries of whether transcription happens.
    dictH = histone.track_epigenetic_process(hst_list=histoneList1,
                                             time=TIME1,
                                             a_bool=A,
                                             r_bool=R,
                                             t_bool=T,
                                             p_bool=P,
                                             ace_prob=k_ace,
                                             nuc_prob=k_nuc
                                             )
    tracker = dictH["vectorize"]
    hstL = dictH["hstL"]
    TList = dictH["TList"]
    PList = dictH["PList"]

    dictH2 = histone.track_epigenetic_process(hst_list=hstL,
                                              time=TIME2,
                                              a_bool=secA,
                                              r_bool=secR,
                                              t_bool=TList[-1],
                                              p_bool=PList[-1],
                                              ace_prob=k_ace2,
                                              nuc_prob=k_nuc2
                                              )
    tracker2 = dictH2["vectorize"]
    TList2 = dictH2["TList"]
    PList2 = dictH2["PList"]

    finalTracker = np.concatenate((tracker, tracker2))
    finalTList = np.concatenate((TList, TList2))
    finalPList = np.concatenate((PList, PList2))


    # basic setup for matplotlib
    plt.style.use('ggplot')
    font = {'family': 'sans-serif'}
    matplotlib.rc('font', **font)

    fig = plt.figure()

    histone.figure.sequence(fig, finalTracker, 3, 1, 1, kace=k_ace, knuc=k_nuc, kace2=k_ace2, knuc2=k_nuc2)
    histone.figure.window(fig, finalTracker, 6, 1, 3)
    histone.figure.package(fig, finalPList, 6, 1, 4)
    histone.figure.transcription(fig, finalTList, 6, 1, 5)
    histone.figure.m_stat(fig, tracker, 6, 4, 22)
    histone.figure.m_stat(fig, tracker2, 6, 4, 24)
    plt.show()

    # to save a figure to pdf file
    title = "demo/result/test_{}____k+{}_k-{}_kace{}_knuc{}_percent{}.pdf".format(strftime("%Y_%m%d_%H%M"), k_plus,
                                                                                  k_minus, k_ace, k_nuc, percent)
    pp = PdfPages(title)
    pp.savefig(fig)
    pp.close()

if __name__ == "__main__":
    main()
