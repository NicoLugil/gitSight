from . import data_classes

class gs_page:
    """
    A class bunding data like gs_plot for multiple plots on 1 page
    """

    def __init__(self, title='<Page Title>'):
        self.title=title
        self.plots=[]   # will be array of gs_plot

    def add_plot(self, plot):
        self.plots.append(plot)

    def get_number_of_plots(self):
        return len(self.plots)

class gs_plot:
    """ 
    A class that bundles all data related to (multiple) to be plotted lines (single plot)
    """

    def __init__(self, x_type='timeseries', x_count=10, title='<Plot Title>', default_type='line'):
        """ gs_line constructor

        Args:
            x_type: type of the line (see c3 doc for options). For now only None or 'timeseries' is supported
            x_count: number of ticks
            default_type: the default style used for all 'lines' (see c3.js data.type for possibilities)
        """
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
            type_override: use this type for this 'line', overriding the default_type of the gs_plot ctor

        """

        m_line=data_classes.xy(label,x,y)
        self.lines.append(m_line)
        self.type.append(type_override)
        #print(f'line added, type length = {len(self.type)}')

    def add_xy_line(self, xy, type_override=None):
        """ add a line by passing an xy object

        Args:
            xy: data_classes.xy object to be added
            type_override: use this type for this 'line', overriding the default_type of the gs_plot ctor
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

