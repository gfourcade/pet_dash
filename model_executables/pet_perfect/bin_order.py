class BinRow(object):

    def __init__(self, val):
        self.master_code = ''
        self.run = val[0]
        self.machine = val[1]
        self.code = val[2]
        self.prod = val[3]
        self.waste = val[4]
        self.start = val[7]
        self.end = val[8]
        self.hours = val[9]
        self.wasting = []

    def update_mf(self, mf):
        self.master_code = mf

def fill_bins(out_bins, out_bin_wasting):
    bin_rows = {}
    for row, val in out_bins.iterrows():
        bin_rows[row] = BinRow(val)
    return bin_rows
