class MasterFormula(object):

    def __init__(self, code, skus, group_breakout):
        self.code = code
        self.skus = [sku for sku in group_breakout.index.values if sku in skus]

    def give_equals(self, skus, master_formulas, equality_function):
        equals = []
        for formula in master_formulas:
            if (self.code != formula and
                    equality_function(self, master_formulas[formula].skus, skus)):
                equals.append(formula)
        return equals

def fill_mf(big_skus, breakout):
    mfs = {}
    groups_breakout = breakout.groupby('Master Formula Number')
    for code in breakout['Master Formula Number']:
        group_breakout = groups_breakout.get_group(code)
        mf = MasterFormula(code, big_skus, group_breakout)
        if mf.skus:
            mfs[str(code)] = mf
    return mfs

def get_equals(skus, mfs, equality_function):
    equals = {}
    for mf in mfs:
        aux = mfs[mf].give_equals(skus, mfs, equality_function)
        equals[str(mf)] = aux
    return equals

def simple_equality(mf, skus_to_check, skus):
    equality = True
    for scode in filter(lambda x: x in skus, mf.skus):
        sku = skus[scode]
        sku_equal = False
        for scode_check in filter(lambda x: x in skus, skus_to_check):
            sku_check = skus[scode_check]
            if sku.simple_equality(sku_check):
                sku_equal = True
        equality = equality and sku_equal
    return equality

def simple_demand_equality(mf, skus_to_check, skus):
    equality = True
    qt_skus_with_demand = 0
    for scode in filter(lambda x: (x in skus) and sum(skus[x].demands) > 0, mf.skus):
        qt_skus_with_demand += 1
        sku = skus[scode]
        sku_equal = False
        for scode_check in filter(lambda x: x in skus, skus_to_check):
            sku_check = skus[scode_check]
            if sku.simple_equality(sku_check):
                sku_equal = True
        equality = equality and sku_equal
    return equality and qt_skus_with_demand > 0
