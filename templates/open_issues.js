
var chart = c3.generate(
{
    data: 
    {
        x: 'x',
        columns:
        [
            // ['x',
            // '2020-07-02','2020-08-12','2020-08-15','2020-08-16'],
            // ['open issues',
            // 2,2,5,4]   
            --gs_replace_me_chart--  
        ]
    },
    color: 
    {
        pattern: ['#de0000']         
    },
    axis: 
    {
        x: 
        {
            type: 'timeseries',
            tick: {format: '%Y-%m-%d', count: 10}
        }
    },
     bindto: '#chart'
});

var chart = c3.generate(
{
    data: 
    {
        x: 'x',
        columns:
        [
            // ['x',
            // '2020-07-02','2020-08-12','2020-08-15','2020-08-16'],
            // ['open issues',
            // 2,2,5,12]      
            --gs_replace_me_chart2--       
        ]
    },
    color: 
    {
        pattern: ['#de0000']         
    },
    axis: 
    {
        x: 
        {
            type: 'timeseries',
            tick: {format: '%Y-%m-%d', count: 10}
        }
    },
     bindto: '#chart2'
});

setTimeout(function () {chart.load(); }, 1000);

