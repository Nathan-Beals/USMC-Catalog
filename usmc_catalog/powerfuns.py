import numpy as np


def pfun_ODSUASLarge(m=np.linspace(1604, 2167, 100), V=np.linspace(0.1, 5.5, 100)):
    """

    :param m: total mass (including empty weight + payload) in grams
    :param V: forward speed of vehicle
    :return: power required
    """
    mm, VV = np.meshgrid(m, V)
    q1 = mm - 1732.36430209377
    q2 = VV - 4.20052519787045
    P = -45.952887494116 + 0.12308218418175*mm + 0.09418974202318*VV + \
        0.00018646959266*q1**2 + 0.00503179158534*q1*q2 - 0.4994068002927*q2**2
    return P, mm, VV, m, V


def pfun_ODSUASSmall(m=np.linspace(1277, 1554, 100), V=np.linspace(0, 5.5, 100)):
    mm, VV = np.meshgrid(m, V)
    q1 = mm - 1415.60258877997
    q2 = VV - 4.09112359606267
    P = -95.593207832974 + 0.27069824534698*mm + 5.09719902899635*VV + \
        0.00098502759429*q1**2 + 0.00442224684513*q1*q2 + 0.59435253538876*q2**2
    return P, mm, VV, m, V

power_models = {'ODSUAS Large': pfun_ODSUASLarge, 'ODSUAS Small': pfun_ODSUASSmall, 'MITRE Nibbler': None}