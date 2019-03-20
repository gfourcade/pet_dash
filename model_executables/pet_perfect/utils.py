
from bokeh.plotting import figure
from bokeh.events import Tap, DoubleTap
from bokeh.models import ColumnDataSource, Legend, CDSView, BooleanFilter, GroupFilter, IndexFilter
from bokeh.models import HoverTool, TapTool, Button
from bokeh.layouts import widgetbox, layout
from bokeh.models.widgets import Select, Div, TextInput, RadioButtonGroup
from . import html_texts as ht
import pandas as pd


def get_identifier(skus):
    return [s.get_code() for s in skus]


def circles_of_packlines(p, ss, identifier, pline, data_generator, x, y, color):
    aux = {identifier:get_identifier(ss)}
    for meth, arg, name in data_generator:
        aux[name] = [meth(s, arg) for s in ss]

    source = ColumnDataSource(data=aux)

    booleans = [True if y_val > 0 else False for y_val in source.data[x]]
    view = CDSView(source=source, filters=[BooleanFilter(booleans)])
    smth = p.circle(x, y, color=color, size=12, fill_alpha=0.6,
                    line_color=None, source=source, view=view)

    return (pline, [smth])#this will help us in the legend setup

def gaston_nombrala_plot_circles(partition_method, class_partition, data_generator,
                                 axis_names, universe, universe_name, hover_names=None):
# data_generator is a dict list of tuples
# for each class in the partition we have how to generate the data in columns
    if not hover_names:
        hover_names = []
    hover = HoverTool(
        tooltips=[
            (universe_name, '@'+universe_name)
        ]
    )
    p = figure(plot_width=700, plot_height=400, tools=[hover])
    p.xaxis.axis_label = axis_names[0]
    p.yaxis.axis_label = axis_names[1]

    legend_items = []
    for clas in class_partition:
        ss = partition_method(universe, clas)
        leg_item = circles_of_packlines(p, ss, universe_name, clas,
                                        data_generator[clas],
                                        axis_names[0],
                                        axis_names[1],
                                        class_partition[clas])
        legend_items.append(leg_item)

    legend = Legend(items=legend_items)
    legend.location = (10, 0)
    legend.click_policy = 'hide'
    p.add_layout(legend, 'right')

    return p


def create_div_mf(div2, dic_mf_similarities, option, mf_code):
    # The index of the selected glyph is : new['1d']['indices'][0]
    string_divs = ["<ul>"]
    if mf_code in dic_mf_similarities[option]:
        string_divs = string_divs + ["".join(["<li>", mf, "</li>"])
                                     for mf in dic_mf_similarities[option][mf_code]]
        string_divs.append("</ul>")
        string_div = "".join(string_divs)
        if not dic_mf_similarities[option][mf_code]:
            string_div = "".join(["No similar master formulas where found on ",
                                  option, " for the master formula ", mf_code, "."])

    else:
        string_div = "No master formula under the name: "+mf_code+"."
    div2.text = string_div



def add_mf_similarities_widgetobox(dic_similarities):
    div = Div(text=ht.mf_similarities_exp)

    select = Select(title="Master formula similarity function:",
                    value=list(dic_similarities.keys())[0],
                    options=list(dic_similarities.keys())
                   )

    div2 = Div(width=400)
    text_input = TextInput(value="default", title="Master Formula to search:")

    text_input.on_change('value', lambda attr, old,
                                         new: create_div_mf(div2, dic_similarities,
                                                            select.value, text_input.value))
    select.on_change('value', lambda attr, old,
                                     new: create_div_mf(div2, dic_similarities,
                                                        select.value, text_input.value))
    # search

    return widgetbox([div, text_input, select, div2], width=300)


def dict_obj_to_df(dct):
    key = list(dct.keys())[0]
    dic_aux ={}
    if isinstance(dct[key], list):
        for identifier in dct[key][0].__dict__:
            aux_list = []
            for dic in dct:
                for obj in dct[dic]:
                    aux_list.append(obj.__dict__[identifier])
            dic_aux[identifier] = aux_list
    else:
        for identifier in dct[key].__dict__:
            aux_list = []
            for dic in dct:
                aux_list.append(dct[dic].__dict__[identifier])
            dic_aux[identifier] = aux_list
    return pd.DataFrame(data = dic_aux)

###############
#  ocupation  # 
###############


    
def machine_occupation(machine, orders, total_days=7):
    total_hours_left = total_days*24
    for order in orders:
        if orders[order].machine == machine:
            total_hours_left -= orders[order].hours
    return total_days*24-total_hours_left


def barplot_occupation(machines, orders, title="Total hours of production"):
    time = [machine_occupation(m, orders) for m in machines]
    ax = pd.DataFrame(time, index=machines).plot.bar()
    ax.title(title)
    return ax

def occupation(df, tools, title,view, df_waste=None):
    cds_machine = ColumnDataSource(df.dropna())
    
    
    p = figure(x_axis_type='datetime', plot_height=200, plot_width=500, tools=tools, title=title)
    # formatting
    p.yaxis.minor_tick_line_color = None
    p.ygrid[0].ticker.desired_num_ticks = 1
    p.x_range.bounds = 'auto'
    p.y_range.bounds = 'auto'
    m_view = CDSView(source=cds_machine, filters=[GroupFilter(column_name='run', group=view)])
    m_glyph = p.quad(left='start',right='end',bottom='low', top='high', source=cds_machine, view=m_view)#,selection_color="firebrick")
    

    for tool in p.tools:
        if tool.renderers is "auto":
            tool.renderers = [m_glyph]
        else:
            tool.renderers.append(m_glyph)
    if df_waste is not None:
        cds_waste = ColumnDataSource(df_waste)
        w_view = CDSView(source=cds_waste, filters=[GroupFilter(column_name='run', group=view)])
        w_glyph = p.quad(left='start',right='end',bottom='low', top='high',name="waste", source=cds_waste, view=w_view, color ="red")
        tools[1].renderers.append(w_glyph)

    return p

def get_rows_with_mf(mfs, data_source):
    dt = data_source.data
    idxs = []
    for mf in mfs:
        for idx in range(len(dt['master_code'])):
            if(dt['master_code'][idx] == mf):
                idxs.append(idx)
    return idxs

def cb_inter_glyphs_mf_union(attr, old, new, data_source, renders):
    mfs = set([data_source.data['master_code'][idx] for idx in new])
    for glyph in renders:
        if glyph.name is "waste":
            idx_to_show = get_rows_with_mf(mfs, glyph.data_source)
            if len(new) is 0:
                idx_to_show = list(range(len(glyph.data_source.data['master_code'])))
            w_view = CDSView(source=glyph.data_source, filters=[IndexFilter(indices=idx_to_show)])
            glyph.view = w_view
        else:
            glyph.data_source.selected.indices = get_rows_with_mf(mfs, glyph.data_source)

def all_occupation(df_extr, df_bins, df_plines, df_bin_waste=None):

    runs = df_bins.run.unique().tolist()
    view = runs[0]
    tap = TapTool()
    hover_ext = HoverTool(
            tooltips=[
                ('code', '@code'),
                ('master formula', '@master_code'),
                ('start', '@start{%D %T}'),
                ('end', '@end{%D %T}'),
                ('run', '@run'),

                ('hours', '@interval{%H:%M}'),
                ('planned', '@prod_planned T'),
                ('attained', '@prod_att T'),

            ],
        formatters = { 'start': 'datetime',
                        'end': 'datetime',
                        'interval': 'datetime'
                        }
        )
    p1 = occupation(df_extr, [hover_ext, tap], "Extruder occupation", view=view, df_waste=None)

    hover_bin= HoverTool(
            tooltips=[
                ('code', '@code'),
                ('master formula', '@master_code'),
                ('start', '@start{%D %T}'),
                ('end', '@end{%D %T}'),
                ('run', '@run'),

                ('hours', '@interval{%H:%M}'),
                ('flowed', '@prod T'),
                ('waste', '@waste T'),

            ],
        formatters = { 'start': 'datetime',
                        'end': 'datetime',
                        'interval': 'datetime'
                        }
        )
    p2 = occupation(df_bins, [hover_bin, tap], "Bins occupation",view=view, df_waste=df_bin_waste)


    hover_pline = HoverTool(
            tooltips=[
                ('code', '@code'),
                ('master formula', '@master_code'),
                ('start', '@start{%D %T}'),
                ('end', '@end{%D %T}'),
                ('run', '@run'),

                ('hours', '@interval{%H:%M}'),
                ('demand', '@dem_tons T'),
                ('attained', '@att_tons T'),

            ],
        formatters = { 'start': 'datetime',
                        'end': 'datetime',
                        'interval': 'datetime'
                        }
        )

    
    p3 = occupation(df_plines, [hover_pline, tap], "Packline occupation", view=view, df_waste=None)
    
    radio_button_red = RadioButtonGroup(
        labels=runs, active=0)
    
    def change_run_view(attr):
        for glyph in tap.renderers:
            view = CDSView(source=glyph.data_source, filters=[GroupFilter(column_name='run', group=runs[attr])])
            glyph.view = view
    radio_button_red.on_click(change_run_view)
    #tap.callback    


    l = layout([p1, p2, p3, radio_button_red], sizing_mode='fixed')

    tap.renderers[0].data_source.selected.on_change('indices', lambda attr, old, new : cb_inter_glyphs_mf_union(attr, old, new, tap.renderers[0].data_source, tap.renderers))
    tap.renderers[1].data_source.selected.on_change('indices', lambda attr, old, new : cb_inter_glyphs_mf_union(attr, old, new, tap.renderers[1].data_source, tap.renderers))
    tap.renderers[2].data_source.selected.on_change('indices', lambda attr, old, new : cb_inter_glyphs_mf_union(attr, old, new, tap.renderers[2].data_source, tap.renderers))
    tap.renderers[3].data_source.selected.on_change('indices', lambda attr, old, new : cb_inter_glyphs_mf_union(attr, old, new, tap.renderers[3].data_source, tap.renderers))
    # No anda el glyph.data_source del lambda termina con siempre el mismo valor.
    # for glyph in tap.renderers:
    #     print(glyph.data_source)
    #     glyph.data_source.selected.on_change('indices', lambda attr, old, new : cb_inter_glyphs_mf_union(attr, old, new, glyph.data_source, tap.renderers))
    
    return l


def start_occupation_graphics(cf_orders, bins, fg_orders, df_bin_waste=None):
    df_extr = dict_obj_to_df(cf_orders)
    df_extr.fillna({"run":"default"}, inplace=True)
    df_bins = dict_obj_to_df(bins)
    df_bins.fillna({"run":"default"}, inplace=True)
    df_plines = dict_obj_to_df(fg_orders)
    df_plines.fillna({"run":"default"}, inplace=True)

    df_extr['low'] = df_extr['machine'] - 0.25
    df_extr['high'] = df_extr['machine'] + 0.25
    df_bins['low'] = df_bins['machine'] - 0.25
    df_bins['high'] = df_bins['machine'] + 0.25
    df_bins['interval'] = df_bins['end'] - df_bins['start']
    df_plines['low'] = df_plines['machine'] - 0.25
    df_plines['high'] = df_plines['machine'] + 0.25
    
    if df_bin_waste is None:
        df_bin_waste = pd.DataFrame(columns=['run','machine', 'start', 'end', 'interval'])
    
    df_bin_waste['end'] = df_bin_waste['ending']
    df_bin_waste['start'] = df_bin_waste['starting']
    df_bin_waste['interval'] = df_bin_waste['end'] - df_bin_waste['start']
    df_bin_waste['low']  = df_bin_waste['machine'] - 0.25
    df_bin_waste['high'] = df_bin_waste['machine'] - 0.10
    
    df_bin_waste.fillna({"run":"default"}, inplace=True)
    return all_occupation(df_extr, df_bins, df_plines, df_bin_waste)