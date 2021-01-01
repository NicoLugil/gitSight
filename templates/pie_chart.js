% for plot in plots:

var chart${loop.index} = c3.generate(
{
    data: 
    {
        columns:
        [
        % for i in range(plot.get_number_of_parts()):
            ['${plot.get_label(i)}','${plot.get_value(i)}'],
        % endfor
        ],
        type: 'pie',
        order: null,
        onclick: function (d, i) { console.log("onclick", d, i); },
        onmouseover: function (d, i) { console.log("onmouseover", d, i); },
        onmouseout: function (d, i) { console.log("onmouseout", d, i); }
    },
    pie:
    {
        label:
        {
            format: function (value, ratio, id)
            {
                return value;
            }
        }
    },
    tooltip: 
    {
      format: 
      {
        value: function (value, ratio, id, index) { return value; }
      }
    },
    zoom: {
        enabled: true
    },
    // color: {
    //     pattern: [  
    //                 '#de0000', '#ff9896', 
    //                 '#1f77b4', '#aec7e8', 
    //                 '#2ca02c', '#98df8a', 
    //                 '#ff7f0e', '#ffbb78', 
    //                 '#9467bd', '#c5b0d5', 
    //                 '#8c564b', '#c49c94', 
    //                 '#e377c2', '#f7b6d2', 
    //                 '#7f7f7f', '#c7c7c7', 
    //                 '#17becf', '#9edae5',
    //                 '#bcbd22', '#dbdb8d' 
    //             ]
    // },
    bindto: '#chart${loop.index}'
});

% endfor

setTimeout(function () {chart.load(); }, 1000);

