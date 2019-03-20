class CFOrder(object):

    def __init__(self, code, val):
        self.code = code
        self.master_code = ''
        self.run = val['run']
        self.week = val['week']
        self.prod_planned = val[2]
        self.prod_att = val[3]
        self.waste = val[4]
        self.shrinkage = val[5]
        self.machine = val[6]
        self.start = val[7]
        self.end = val[8]
        self.interval = val[8] - val[7]
        self.hours = val[9]

    def update_mf(self, mf):
        self.master_code = mf

#dict('code':list(CFOrder))
#done because many weeks or multiple runs could break the dictionary
def fill_cf_orders(out_cf):
    orders ={}
    for row, val in out_cf.iterrows():
        if row in orders:
            orders[row].append(CFOrder(row, val))
        else: 
            orders[row] = [CFOrder(row, val)]
    return orders
