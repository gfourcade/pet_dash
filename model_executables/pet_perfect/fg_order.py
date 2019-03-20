class FGOrder(object):

    def __init__(self, code, val, master_code):
        self.code = code
        self.master_code = master_code
        self.run = val['run']
        self.week = val['week']
        self.dem_bags = val[2]
        self.att_bags = val[3]
        self.dem_tons = val[4]
        self.att_tons = val[5]
        self.machine = val[6]
        self.start = val[7]
        self.end = val[8]
        self.interval = val[8] - val[7]
        self.hours = val[9]

    def not_finished(self, total_demand):
        return total_demand/2000 > self.att_tons

#dic('code':List(FGOrders))
#done because spliting fg orders could break dicitonary alone
def fill_fg_orders(out_fg, breakout):
    groups_breakout = breakout.groupby(breakout.index)
    orders = {}
    for row, val in  out_fg.iterrows():
        mf = groups_breakout.get_group(row)['Master Formula Number'].values[0]
        if row in orders:
            orders[row].append(FGOrder(row, val, mf))
        else:
            orders[row] =  [FGOrder(row, val, mf)]
    return orders
