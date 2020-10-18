% for plot in plots:

var chart${loop.index} = c3.generate(
{
    data: 
    {
        xs: 
        {
        % for i in range(plot.get_number_of_lines()):
            '${plot.get_label(i)}': 'x${i}',
        % endfor      
        },
        columns:
        [
        % for i in range(plot.get_number_of_lines()):
            ['x${i}',
            % for x in plot.get_x_in_c3_format(i):
             ${x},
            % endfor
            ],
            ['${plot.get_label(i)}',
            % for y in plot.get_y(i):
             ${y},
            % endfor
            ],
        % endfor
        ]
    },
    zoom: {
        enabled: true
    },
    color: {
        pattern: [  
                    '#de0000', '#ff9896', 
                    '#1f77b4', '#aec7e8', 
                    '#2ca02c', '#98df8a', 
                    '#ff7f0e', '#ffbb78', 
                    '#9467bd', '#c5b0d5', 
                    '#8c564b', '#c49c94', 
                    '#e377c2', '#f7b6d2', 
                    '#7f7f7f', '#c7c7c7', 
                    '#17becf', '#9edae5',
                    '#bcbd22', '#dbdb8d' 
                ]
    },
    axis: 
    {
        x: 
        { 
        % if plot.x_type=='timeseries':
            type: 'timeseries',
            tick: {format: '%Y-%m-%d', count: ${plot.x_count}}
        % else:
            tick: {count: ${plot.x_count}}
        % endif
        }
    },
    bindto: '#chart${loop.index}'
});

% endfor

setTimeout(function () {chart.load(); }, 1000);

