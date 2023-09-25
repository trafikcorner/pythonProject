import urllib
import json

import pandas as pd
from collections import defaultdict
from itertools import groupby
from operator import itemgetter


class odbeRendeles:
    def __init__(self, tabla):
        self.tabla = tabla

    # ----- A táblából RETURN érték gyártók ------
    def szallitok(self):
        toReplace = [" Kft", " Zrt", " KFT"]
        query = self.tabla.objects.raw("SELECT * FROM trafik_app_odberkkv GROUP BY gyarto")
        gyartok = []
        for sor in query:
            ujGyarto = sor.gyarto
            for keres in toReplace:
                if keres in ujGyarto:
                    ujGyarto = ujGyarto.replace(keres, "").replace(".","")
            gyartok.append(ujGyarto)
        return gyartok





