from . import data_classes
from enum import Enum, auto

class gs_page:
    """
    A class bunding data for multiple plots on 1 page
    """

    def __init__(self, title='<Page Title>', n_columns=1):
        self.title=title
        self.gs_plots=gs_plots()
        self.col=[]     # for each plot, in which column it needs to go
        self.js=[]     # array of .js files to add
        allowed_n_columns=[1,2,3,4,6,12]
        if n_columns not in allowed_n_columns:
            raise f'number of columns must be from {allowed_n_columns}'
        self.n_col=n_columns   # columns

    def add_plot(self, plot, col=0):
        self.gs_plots.add_plot(plot)
        self.col.append(col)

    def get_number_of_plots(self):
        return self.gs_plots.get_number_of_plots()

    def add_js(self, js):
        self.js.append(js)

class gs_plots:
    """
    A class to store and manipulate an array of plots
    """

    def __init__(self):
        self.plots=[]

    def add_plot(self, plot):
        self.plots.append(plot)

    def get_number_of_plots(self):
        return len(self.plots)

    def get_plots_of_type(self, wanted_type):
        """
        Returns a new gs_plots object with only the plots of the given type (gs_plot_type)
        """

        new_plots = gs_plots()
        for p in self.plots:
            if p.plot_type==wanted_type:
                new_plots.add_plot(p)
        return new_plots

class gs_plot_type(Enum):
    LINE = auto()
    PIE = auto()

# TODO: base class for plots

class gs_line_plot:
    """ 
    A class that bundles all data related to (multiple) to be plotted lines (single plot)
    """

    def __init__(self, name, x_type='timeseries', x_count=10, title='<Plot Title>', default_type='line'):
        """ gs_line constructor

        Args:
            x_type: type of the line (see c3 doc for options). For now only None or 'timeseries' is supported
            x_count: number of ticks
            default_type: the default style used for all 'lines' (see c3.js data.type for possibilities)
        """
        self.name=name
        self.plot_type=gs_plot_type.LINE
        self.x_type=x_type
        if x_type=='timeseries':
            self.x_format='%Y-%m-%d'
        else:
            self.x_format=None
        self.x_count=x_count
        self.lines=[]                    # array of data_classes.xy objects
        self.title=title
        self.default_type=default_type
        self.type=[]                     # type per line, if None -> default_type (i.e. no override)

    def add_line(self, label='no-label', x=None, y=None, type_override=None):
        """ add a line by giving its individual components

        Args:
            label: string
            x: array of data for x-axis
            y: array of data for y-axis
            type_override: use this type for this 'line', overriding the default_type of the gs_line_plot ctor

        """

        m_line=data_classes.xy(label,x,y)
        self.lines.append(m_line)
        self.type.append(type_override)
        #print(f'line added, type length = {len(self.type)}')

    def add_xy_line(self, xy, type_override=None):
        """ add a line by passing an xy object

        Args:
            xy: data_classes.xy object to be added
            type_override: use this type for this 'line', overriding the default_type of the gs_line_plot ctor
        """

        self.lines.append(xy)
        self.type.append(type_override)

    def get_x_in_c3_format(self, index):
        """ will return x as array in format as desired by c3

        Args:
            index: index in lines[] to be returned

        Uses x_type to determine how to return:

        - timeseries -> return dates as string
        - other: return as given
        """

        m_line=self.lines[index]

        if self.x_type=='timeseries':
            x_c3=[]
            for x in m_line.x:
                x_c3.append(x.date().strftime('\'%Y-%m-%d\''))
            return x_c3
        else:
            return m_line.x

    def get_label(self, index):
        m_line=self.lines[index]
        return m_line.label

    def get_y(self, index):
        m_line=self.lines[index]
        return m_line.y

    def get_type(self, index):
        #print(f'get type index {index}')
        return self.type[index]

    def get_number_of_lines(self):
        return len(self.lines)

class gs_pie_plot:
    """ 
    A class that bundles all data related to a single pie plot
    """

    def __init__(self, name, title='<Plot Title>'):
        """ gs_pie_plot constructor

        Args:
            title: title of the plot
        """
        self.name=name
        self.plot_type=gs_plot_type.PIE
        self.title=title
        self.parts=[]

    def add_part(self, label, value):
        """ add a part of a pie chart, given a label and value (='size of the part')

        Args:
            label: string
            value: decimal number

        """

        m_part=data_classes.label_value_pair(label,value)
        self.parts.append(m_part)

    def get_label(self, index):
        m_part=self.parts[index]
        return m_part.label

    def get_value(self, index):
        m_part=self.parts[index]
        return m_part.value

    def get_number_of_parts(self):
        return len(self.parts)