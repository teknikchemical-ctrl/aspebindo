# -*- coding: utf-8 -*-
import sys, copy
from kd import *
import kd, sh, kt
NS=10
def finish(name,strict=True):
    iss=check(verbose=True)
    d.pdf(name+'.pdf')
    if iss:
        check(verbose=False,overlay=True); d.pdf(name+'_chk.pdf')
    print(name,'ISU =',len(iss))
    return len(iss)
