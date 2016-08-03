from numpy.random import sample
import numpy as np


class Histone(object):
    def __init__(self, position=0,
                 kp=0.12,
                 kp2=0.12,
                 km=0.117,
                 a_bool=False,
                 ka=0.12,
                 nextnode=None,
                 prenode=None,
                 inherited=False,
                 inherited_hst=None):
        """

        :param position: a position of histone, to differentiate
                  from other histone instances.
        :param kp:
        :param kp2:
        :param km:
        :param a_bool: a boolean value, activator of transcription factors
                       if A is true, then the K_ACE is the given paramater.
                       else, K_ACE is 0, which means no histones can be \
                       turned to be acetilated.
        :param ka:
        :param nextnode: a neighbor of the instances, judged by position + 1
        :param prenode: a neighbor of the instances, judged by position - 1
        :param inherited:
        :param inherited_hst:
        """

        self.status = ""
        self.k_list = {0: self.k_plus, 1: self.k_minus, 2: self.k_ace}

        # inherited the info of histone object
        if inherited:
            assert inherited_hst is not None
            self.position = inherited_hst.position

            self.prenode = inherited_hst.prenode  # doubly-linked
            if inherited_hst.prenode is not None:
                inherited_hst.prenode.nextnode = self

            self.nextnode = inherited_hst.nextnode  # doubly-linked
            if inherited_hst.nextnode is not None:
                inherited_hst.nextnode.prenode = self

            Histone.K_ACE = inherited_hst.K_ACE
            Histone.K_PLUS = inherited_hst.K_PLUS
            Histone.K_PLUS2 = inherited_hst.K_PLUS2
            Histone.K_MINUS = inherited_hst.K_MINUS

        # create new histone object based on the arguments
        else:
            self.position = position
            self.prenode = prenode
            self.nextnode = nextnode
            # if A_bool is false, K_ACE is set to be 0.
            if a_bool:
                Histone.K_ACE = ka
            else:
                Histone.K_ACE = 0
            Histone.K_PLUS = kp
            Histone.K_PLUS2 = kp2
            Histone.K_MINUS = km

    def set_adjhistone(self, nextnode):
        """
        Set the input to self.nextNode, one of its instance variables.
        :param nextnode:
        :return:
        """
        self.nextnode = nextnode
        nextnode.prenode = self

    # BUG k_ace should be subject to k_minus
    def set_ka(self, a_bool,k_ace):
        """
        set the default of Histone.K_ACE.
        :param a_bool: boolean value, if a_bool is true, then Histone.KCE is set to the
        :return:
        """
        if a_bool:
            Histone.K_ACE = k_ace
        else:
            Histone.K_ACE = 0

    def dna_methylation(self):
        """
        used only when we care about CpG methylation system
        :return:
        """
        return self

    @staticmethod
    def k(hst):
        f_list = [0, 1, 2]
        np.random.shuffle(f_list)
        for f in f_list:
            hst = hst.k_list[f]()
        return hst

    def k_plus(self):
        """
        the unmethylated histone will get methylated by K_PLUS probability
        return methylated object if the histone will get methylated
        :return:
        """
        return self

    def k_minus(self):
        """
        the methylated histone will be get unmethylated by K_MINUS probability
        or
        the acetilated histone will be get unacetylated by K_MINUS probability
        :return: unmethylated histone object if the histone will get unmethylated
        """

        if sample() < self.K_MINUS:
            return UHistone(inherited=True, inherited_hst=self)
        else:
            return self

    def k_ace(self):
        """
        the unmethylated hitone will be get acetilated by K_ACE probability
        :return: acetilated histone if the histone will get acetilated
        """
        return self

    def __lt__(self, other):
        """
        :return: true when the position of self is smaller than that of other
        """
        return self.position < other.position

    def __str__(self):
        """
        :return: all info about the instance of this object.
        """
        if self.status == 'm':
            st = "methylated"
        elif self.status == 'a':
            st = "acetylated"
        else:
            st = "unmethylated"
        sentence = "pos: {}  status: {}\t".format(self.position, st)
        return sentence



class MHistone(Histone):
    def __init__(self, **kwarg):
        super().__init__(**kwarg)
        self.status = "m"


class UHistone(Histone):
    def __init__(self, **kwarg):
        super().__init__(**kwarg)
        self.status = "u"

    def k_plus(self):
        if (self.prenode is not None and self.prenode.status == "m"
            and sample() < self.K_PLUS):
            # preNode is methylated and sample() gets smaller than K_PLUS
            return MHistone(inherited=True, inherited_hst=self)
        if (self.nextnode is not None and self.nextnode.status == "m"
            and sample() < self.K_PLUS):
            # nextNode is methylated and sample() gets smaller than K_PLUS
            return MHistone(inherited=True, inherited_hst=self)
        return self

    def k_minus(self):
        return self

    def k_ace(self):
        if sample() < self.K_ACE:
            return AHistone(inherited=True, inherited_hst=self)
        else:
            return self


class AHistone(Histone):
    def __init__(self, **kwarg):
        super().__init__(**kwarg)
        self.status = "a"

    def k_plus(self):
        if (self.prenode is not None and self.prenode.status == "m"
            and sample() < self.K_PLUS2):
            # preNode is methylated and sample() gets smaller than KPLUS2
            return UHistone(inherited=True, inherited_hst=self)
        if (self.nextnode is not None and self.nextnode.status == "m"
            and sample() < self.K_PLUS2):
            # nextNode is methylated and sample() gets smaller than KPLUS2
            return UHistone(inherited=True, inherited_hst=self)
        return self


class HistoneOct4(Histone):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.k_list = {0: self.k_plus, 1: self.k_minus, 2: self.k_ace, 3: self.dna_methylation}

        # copy histone info from copy_histone
        if kwargs.pop('inherited', None):
            self.CpGislandlist = kwargs.pop('inherited_hst', None).CpGislandlist

        # create new histone object based on the argument
        else:
            position = kwargs.pop('position', 0)
            if position == -2:
                self.CpGislandlist = [0, 0, 0, 0]
            elif position == -1:
                self.CpGislandlist = [0, 0, 0, 0]
            elif position == 0:
                self.CpGislandlist = [0, 0]
            else:
                self.CpGislandlist = []

    def k_minus(self):
        if sample() < self.K_MINUS:
            return UHistoneOct4(inherited=True, inherited_hst=self)
        else:
            return self

    def dna_methylation(self):
        if sample() < sum(self.CpGislandlist) * self.K_PLUS:
            # the chance gets higher, depends on the num of CpG island sites
            return MHistoneOct4(inherited=True, inherited_hst=self)
        else:
            return self

    @staticmethod
    def k(hst):
        f_list = [0, 1, 2, 3]
        np.random.shuffle(f_list)
        for f in f_list:
            print(hst, f, hst.k_list[f])
            hst = hst.k_list[f]()

        return hst


class MHistoneOct4(HistoneOct4):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.status = "m"


class UHistoneOct4(HistoneOct4):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.status = "u"

    def k_plus(self):
        if (self.prenode is not None and self.prenode.status == "m"
            and sample() < self.K_PLUS):
            # preNode is methylated and sample() gets smaller than K_PLUS
            return MHistoneOct4(inherited=True, inherited_hst=self)
        if (self.nextnode is not None and self.nextnode.status == "m"
            and sample() < self.K_PLUS):
            # nextNode is methylated and sample() gets smaller than KPLUS
            return MHistoneOct4(inherited=True, inherited_hst=self)
        return self

    def k_minus(self):
        return self

    def k_ace(self):
        # if histone has CpG island on it
        if 1 in self.CpGislandlist:
            # histone cannnot get acetylated
            return self

        else:
            if sample() < self.K_ACE:
                return AHistoneOct4(inherited=True, inherited_hst=self)
            else:
                return self


class AHistoneOct4(HistoneOct4):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.status = "a"

    def k_plus(self):
        if (self.prenode is not None and self.prenode.status == "m"
            and sample() < self.K_PLUS2):
            # preNode is methylated and sample() gets smaller than PLUS2
            return UHistoneOct4(inherited=True, inherited_hst=self)

        if (self.nextnode is not None and self.nextnode.status == "m"
            and sample() < self.K_PLUS2):
            # nextNode is methylated and sample() gets smaller  than PLUS2
            return UHistoneOct4(inherited=True, inherited_hst=self)

        return self


def init_genome(percentage=50,
                a_bool=1,
                hst_n=81,
                kp=0.176,
                kp2=0.17,
                km=0.117,
                ka=0.12):
    """
    percentage ... the probability of having methylated hitone.
    this method returns a list of histone randomly generated with respect to
    the inputs.
    """
    before_promoter = hst_n // 2
    hst_list = []  # hst_list stores histones
    ratio = percentage / 100  # ratio should be float number between 0 and 1

    for i in range(hst_n):

        if sample() < ratio:
            hst_list.append(MHistone(position=i - before_promoter,
                                     kp=kp,
                                     kp2=kp2,
                                     km=km,
                                     ka=ka,
                                     a_bool=a_bool
                                     )
                            )
        else:
            hst_list.append(UHistone(position=i - before_promoter,
                                     kp=kp,
                                     kp2=kp2,
                                     km=km,
                                     ka=ka,
                                     a_bool=a_bool
                                     )
                            )

        hst_list[i - 1].set_adjhistone(hst_list[i])

    hst_list[0].prenode = None  # disjoint the edge histone to itself.
    return hst_list


def init_genome_oct4(percentage=50,
                     a_bool=1,
                     hst_n=81,
                     kp=0.176,
                     kp2=0.17,
                     km=0.117,
                     ka=0.12):
    """
    this method is a modified version of createRandomHistoneList
    used for Oct4 histones.
    """
    before_promoter = hst_n // 2
    hst_list = []  # hst_list stores histones
    ratio = percentage / 100  # ratio should be float number between 0 and 1

    for i in range(hst_n):

        if sample() < ratio:
            hst_list.append(MHistoneOct4(position=i - before_promoter,
                                         kp=kp,
                                         kp2=kp2,
                                         km=km,
                                         ka=ka,
                                         a_bool=a_bool
                                         )
                            )
        else:
            hst_list.append(AHistoneOct4(position=i - before_promoter,
                                         kp=kp,
                                         kp2=kp2,
                                         km=km,
                                         ka=ka,
                                         a_bool=a_bool
                                         )
                            )

        hst_list[i - 1].set_adjhistone(hst_list[i])

    hst_list[0].prenode = None  # disjoint the edge histone to itself.
    return hst_list


def next_genome(hst_list, a_bool, r_bool, window, k_nuc):
    """
    this method takes histone list and returns the next generation out of them.
    """
    ahst_n = 0
    mhst_n = 0

    for i, hst in enumerate(hst_list):

        if -window // 2 <= hst.position <= window // 2:
            if hst.status == "a":
                ahst_n += 1
            elif hst.status == "m":
                mhst_n += 1

        hst = Histone.k(hst)

        hst_list[i] = hst

    # transcription happens if there are more than 5 acetylated histones at
    # the locus, and also less than 3 methylated histones at the locus.
    t_bool = (ahst_n > 5) and (mhst_n < 3)
    """
    WINDOW is size 10(11 histones note that there is E0 between E(-1) and E(1)), 
    so acetylated histones will be dominant if non-acetylated histones are less than 5.
    """
    eext_bool = False

    # if transcription does not happen, then with k_nuc
    # probability, we recover E0 histone to be methylated.
    if t_bool is False and sample() < k_nuc:
        eext_bool = True


    # if in the locus, we have more than two methylated histones,
    # then with 100% prob, we recover E0 histone to be
    # methylated.

    # this is a histone memory part.
    if mhst_n > 2:
        eext_bool = True

    if eext_bool is True:
        center = len(hst_list) // 2
        hst_list[center] = MHistone(inherited=True, inherited_hst=hst_list[center])

    return hst_list, t_bool


# TODO change the eert bool rule later
def next_genome_oct4(hst_list, a_bool, r_bool, window, p_off):
    """
    this method takes histone list and returns the next generation of them.
    """
    ahst_n = 0
    mhst_n = 0

    for i, hst in enumerate(hst_list):
        if -window // 2 <= hst.position <= window // 2:
            if hst.status == "a":
                ahst_n += 1
            elif hst.status == "m":
                mhst_n += 1

            for index in range(len(hst.CpGislandlist)):
                # p_on probability
                if hst.status == 'm' and sample() < 0.001133:
                    hst.CpGislandlist[index] = 1

                # p_off probability   
                if sample() < p_off:
                    hst.CpGislandlist[index] = 0

        hst = HistoneOct4.k(hst)

        hst_list[i] = hst
    t_bool = a_bool and (ahst_n > window // 2)
    """
    WINDOW is size 10(11 histones note that there is E0 between E(-1) and E(1)), 
    so acetylated histones will be dominant if non-acetylated histones are less than 5.
    """
    if r_bool == 1:
        eext_bool =  1 if t_bool is False and sample() < Histone.K_PLUS else 0
    else:
        eext_bool =  1 if mhst_n > 2 and sample() < Histone.K_PLUS else 0

    if eext_bool:
        center = len(hst_list) // 2
        hst_list[center] = MHistoneOct4(inherited=True, inherited_hst=hst_list[center])

    return hst_list, t_bool


def vectorize(hst_list):
    """
    this method takes a list of histone objects, and returns three dimention numpy array
    in which three bit vectors are stored. 
    """
    hst_n = len(hst_list)
    v_mlist = np.zeros(hst_n, dtype=bool)
    v_ulist = np.zeros(hst_n, dtype=bool)
    v_alist = np.zeros(hst_n, dtype=bool)
    for i, h in enumerate(hst_list):
        if h.status == "m":
            v_mlist[i] = 1
        elif h.status == "u":
            v_ulist[i] = 1
        else:
            v_alist[i] = 1

    return np.array([v_mlist,
                     v_ulist,
                     v_alist],
                    dtype=bool)


# TODO change the compound statements to the enumeratative for loop
def vectorize_oct4(hst_list):
    hst_n = len(hst_list)
    v_mlist = np.zeros(hst_n, dtype=bool)
    v_ulist = np.zeros(hst_n, dtype=bool)
    v_alist = np.zeros(hst_n, dtype=bool)
    v_cpg = np.array([sum(h.CpGislandlist) for h in hst_list], dtype=np.int8)

    return np.array([v_mlist,
                     v_ulist,
                     v_alist,
                     v_cpg])


def track_epigenetic_process(hst_list,  # initial histone list
                             time,  # time for tracking (in hour)
                             a_bool,  # activator bool
                             r_bool,  # repressor bool
                             t_bool,  # transcription bool
                             ace_prob,
                             nuc_prob,
                             window=10,  # default is 10
                             ):
    hst_n = len(hst_list)
    for i, hst in enumerate(hst_list):
        hst_list[i].set_ka(a_bool,ace_prob)

    vectorizedgene_list = np.zeros((time, 3, hst_n))  # array of compressed data of vectors
    t_list = np.zeros(time, dtype=bool)  # one dimension array

    for t in range(time):
        vectorizedgene_list[t] = vectorize(hst_list)
        t_list[t] = t_bool
        hst_list, t_bool = next_genome(hst_list, a_bool, r_bool, window, nuc_prob)

    return {"vectorize": vectorizedgene_list, "hstL": hst_list, "TList": t_list}


def track_epigenetic_process_oct4(hst_list,  # initial histone list
                                  time,  # time for tracking (in hour)
                                  a_bool,  # activator bool
                                  r_bool,  # repressor bool
                                  t_bool,  # transcription bool
                                  p_off,  # prob of CpG island site gets OFF
                                  window=10  # default is 10
                                  ):
    hst_n = len(hst_list)
    for i, hst in enumerate(hst_list):
        hst_list[i].set_ka(a_bool)

    vectorizedgene_list = np.zeros((time, 4, hst_n))  # array of compressed data of vectors
    t_list = np.zeros(time, dtype=bool)  # one dimension array
    for t in range(time):
        vectorizedgene_list[t] = vectorize_oct4(hst_list)
        t_list[t] = t_bool
        hst_list, t_bool = next_genome_oct4(hst_list, a_bool, r_bool, window, p_off)

    return {"vectorize": vectorizedgene_list, "hstL": hst_list, "TList": t_list}


# TODO inefficient implementation
def gettime_mhst_dieout(vectorizedgene_list):
    for time in range(len(vectorizedgene_list)):
        if vectorizedgene_list[time][0][40] == 0:
            for else_in_window in range(35, 45):
                if vectorizedgene_list[time][0][else_in_window] == 1:
                    break
                return time
    return -1


