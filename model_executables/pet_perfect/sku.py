

class Sku(object):

    def  __init__(self, code, group_breakout, code_demand,
                  rates_umbra, rates_parsons, rates_ptech, rates_thiele):

        self.code = code
        self.master_code = group_breakout['Master Formula Number'].values[0]
        self.weight = group_breakout['weight'].values[0]
        self.demands = code_demand
        self.fg_family = []
        self.rates_packlines = {}
        self.cfs = {}
        self.shrinkage = {}
        self.fg_orders = []

        aux_cf = group_breakout['Component Formula Number'].values
        aux_shrk = group_breakout['Shrinkage'].values
        aux_percentage = group_breakout['Blend Percentage'].values
        self.cfs = dict(zip(aux_cf, aux_percentage))
        self.shrinkage = dict(zip(aux_cf, aux_shrk))

        aux_packname = []
        aux_packrate = []
        if self.code in rates_umbra.index:
            aux_packname.append('umbra')
            aux_packrate.append(rates_umbra.loc[self.code, 'kg/s'])
        if self.code in rates_parsons.index:
            aux_packname.append('parsons')
            aux_packrate.append(rates_parsons.loc[self.code, 'kg/s'])
        if self.code in rates_ptech.index:
            aux_packname.append('ptech')
            aux_packrate.append(rates_ptech.loc[self.code, 'kg/s'])
        if self.code in rates_thiele.index:
            aux_packname.append('thiele')
            aux_packrate.append(rates_thiele.loc[self.code, 'kg/s'])
        self.rates_packlines = dict(zip(aux_packname, aux_packrate))


    def __str__(self):
        string = self.code+':\n'
        string += '\tweight: '+str(self.weight)+'\n'
        string += '\tdemand: '
        for dem in self.demands:
            string += str(dem)+' '
        string += '\n\tfg family: '
        for dem in self.fg_family:
            string += str(dem)+' '
        string += '\n\tcomponent formula (ratio, shrinkage): '
        for cf in self.cfs:
            string += str(cf)+' ('+str(self.cfs[cf])+','+str(self.shrinkage[cf])+') '
        string += '\n\trates packilnes: '
        for pl in self.rates_packlines:
            string += pl +': '+str(self.rates_packlines[pl])+ ' '
        return string

    def is_broken(self, display=False):
        #print errors
        errors = False
        if not self.rates_packlines:
            errors = True
            if display:
                print(self.code, "Has no packlines assigned.")

        if not self.cfs:
            errors = True
            if display:
                print(self.code, 'Has no cfs assigned.')
        sum_percentage = sum([self.cfs[cf] for cf in self.cfs])
        if sum_percentage < 0.99 or sum_percentage > 1.01:
            errors = True
            if display:
                print(self.code, 'Has wrong percentage', '{:.2f}'.format(sum_percentage))

        if self.weight == 0:
            errors = True
            if display:
                print(self.code, 'Has no weight.')

        if(errors and sum(self.demands) > 0):
            RED = '\033[91m'
            BOLD = '\033[1m'
            UNDERLINE = '\033[4m'
            END = '\033[0m'
            #print('\33[31m' + str(self.code) +'\33[0m', ' has demand and is broken')
            print(RED+BOLD+UNDERLINE+str(self.code) +END+': has demand and is broken', sum(self.demands))
            if(not display):
                print('=================')

        if(errors and display):
            print('=================')
        return errors

    def simple_equality(self, sku_check):
        equals = self.weight == sku_check.weight
        for pack in self.rates_packlines:
            equals = equals and (pack in sku_check.rates_packlines and
                                 self.rates_packlines[pack] == sku_check.rates_packlines[pack])

        blend_self = list(self.cfs.values())
        blend_self.sort()
        blend_check = [sku_check.cfs[cf] for cf in sku_check.cfs]
        blend_check.sort()
        equals = equals and blend_check == blend_self
        return equals

    def get_demand(self, ranges):
        first = ranges[0]
        last = ranges[1]
        return sum(self.demands[first:last])

    def get_weight(self, __):
        return self.weight

    def get_rate(self, pline):
        return self.rates_packlines[pline[0]]

    def exclusive_of_line(self, line):
        return (line in self.rates_packlines
                and self.rates_packlines[line] > 0
                and len(self.rates_packlines) == 1)

    def get_cfs(self):
        return list(self.cfs.keys())

    def get_code(self):
        return self.code


def fill_skus(fg_orders, breakout, demand, rates_umbra, rates_parsons, rates_ptech, rates_thiele, show_info=False):
    skus = {}
    groups_breakout = breakout.groupby(breakout.index)
    for code in breakout.index:
        group_breakout = groups_breakout.get_group(code)
        code_demand = [0 for i in range(24)]
        if code in demand.index:
            code_demand = demand.loc[code, demand.columns[3:27].values].values / 2000
        sk = Sku(code, group_breakout, code_demand,
                 rates_umbra, rates_parsons, rates_ptech, rates_thiele)
        if not sk.is_broken(show_info):
            skus[code] = sk
            fg_aux = []
            i = 0
            for order in fg_orders:
                if order == code:
                    fg_aux = fg_orders[order]
                    i+=1
            skus[code].fg_orders = fg_aux
            if(i>1):
                print('\033[91m'+'\033[1m'+'\033[4m'+"There was a problem filling skus"+'\033[0m')

    for s1 in skus:
        fam = []
        for s2 in skus:
            if s1 != s2 and skus[s1].cfs == skus[s2].cfs:
                fam.append(s2)
        skus[s1].fg_family = fam
    return skus

def formulas_demanded(skus):
    formulas = []
    for scode in skus:
        s = skus[scode]
        for cf in s.get_cfs():
            formulas.append(cf)
    return formulas

def skus_exclusive_of_line(skus, line):
    exclusives = []
    for scode in skus:
        s = skus[scode]
        if s.exclusive_of_line(line):
            exclusives.append(s)
    return exclusives

def time_to_pack_demand_of_line(skus, line, week):
    total_time = 0
    for sku in skus_exclusive_of_line(skus, line):
        d = sku.demands[week-1]
        r = sku.rates_packlines[line]
        total_time += ((d*1000)/r)/(3600*24)
    return total_time

def is_someone_on_family_of_formulas_exclusive_of_line(skus, line):
    exclusives = []
    for cf in formulas_demanded(skus):
        one_exc = 0
        for s in sku_family_of_formula(skus, cf):
            if s.exclusive_of_line(line) and s.get_demand([0, 24]) > 0:
                one_exc += 1
        if one_exc > 0:
            exclusives.append(cf)
    return exclusives

def skus_of_line(skus, line):
    items = []
    for scode in skus:
        s = skus[scode]
        if line in s.rates_packlines and s.rates_packlines[line] > 0:
            items.append(s)
    return items

def skus_of_n_neighbours(skus, n):
    codes = []
    for scode in skus:
        s = skus[scode]
        if len(s.cfs) == n:
            codes.append(s)
    return codes

def string_to_int(n):
    return {
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5
    }[n]


def skus_of_neighbours(skus, str_n):
    n = string_to_int(str_n)
    return skus_of_n_neighbours(skus, n)

def give_overall_info(skus, weeks):
    # Take into consideration that what we didnt produced may differ
    # because we sometimes overDo some skus
    demand = 0
    prod = 0
    for scode in skus:
        demand += sum(skus[scode].demands)
        prod += sum([fg.att_tons for fg in skus[scode].fg_orders if fg.week in weeks])
    return (demand, prod)

def give_skus_not_finished(skus, weeks=None, min_weight=0, max_weight=100,
                           min_cf_members=1, max_cf_members=5):
    if weeks is None:
        weeks = [1]
    not_finished = {}
    for scode in filter(lambda x: sum(skus[x].demands) > 0 and
                        (min_weight <= skus[x].weight) and
                        (skus[x].weight <= max_weight) and
                        (min_cf_members <= len(skus[x].cfs)) and
                        (len(skus[x].cfs) <= max_cf_members),
                        skus):

        total_demand = sum(skus[scode].demands)
        att_in_weeks = [fg.att_tons for fg in skus[scode].fg_orders if fg.week in weeks]
        att = sum(att_in_weeks)
        if att < total_demand:
            not_finished[scode] = att
    return not_finished

def give_not_produced_info(skus, weeks, threshold, going_print=False):
    skus_info = {}
    not_f = give_skus_not_finished(skus, weeks)
    not_prod = 0
    for scode in not_f:
        dem_aux = sum(skus[scode].demands)
        if dem_aux - not_f[scode] > threshold:
            sku = skus[scode]
            dic_aux = {'cf_comp':len(sku.get_cfs()),
                       'weight':sku.weight,
                       'demand':dem_aux,
                       'att':not_f[scode],
                       'not_att':dem_aux - not_f[scode]
                      }
            skus_info[scode] = dic_aux
            not_prod += dem_aux - not_f[scode]
            if going_print:
                print(scode)
                print('\t# component: ', dic_aux['cf_comp'])
                print('\tweight: ', dic_aux['weight'])
                print('\tdemand: ', '{:.2f}'.format(dic_aux['demand']),
                      ' attained: ', '{:.2f}'.format(dic_aux['att']),
                      'not produced: ', '{:.2f}'.format(dic_aux['not_att']))
                print("=====================")
    if going_print:
        print("amount not produced:", '{:.2f}'.format(not_prod))
