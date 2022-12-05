from iOpt.trial import Point


class SolverParameters:
    def __init__(self,
                 eps: float = 0.01,
                 r: float = 2.0,
                 itersLimit: int = 20000,
                 evolventDensity: int = 10,
                 epsR: float = 0.001,
                 refineSolution: bool = False,
                 startPoint: Point = Point([], [])
                 ):
        """
        :param eps:method tolerance. Less value -- better search precision, less probability of early stop.
        :param r: reliability parameter. Higher value of r -- slower convergence,
               higher chance to cache the global minima.
        :param itersLimit: max number of iterations.
        :param evolventDensity:density of evolvent. By default density is 2^-12 on hybercube [0,1]^N,
               which means that maximum search accuracy is 2^-12.
               If search hypercube is large the density can be increased accordingly to achieve better accuracy.
        :param epsR: parameter which prevents method from paying too much attention to constraints. Greater values of
               this parameter speed up convergence, but global minima can be lost.
        :param refineSolution: if true, the final solution will be refined with the HookJeves method.
        """
        self.eps = eps
        self.r = r
        self.itersLimit = itersLimit
        self.evolventDensity = evolventDensity
        self.epsR = epsR
        self.refineSolution = refineSolution
        self.startPoint = startPoint
