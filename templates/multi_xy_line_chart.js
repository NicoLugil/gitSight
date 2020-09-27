
var --gs_replace_me_bindto-- = c3.generate(
{
    data: 
    {
        xs: 
        {
            --gs_replace_me_xs--
        },
        columns:
        [
            --gs_replace_me_columns--  
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
        x: { --gs_replace_me_x_axis-- }
    },
    bindto: '#--gs_replace_me_bindto--'
});

setTimeout(function () {chart.load(); }, 1000);

