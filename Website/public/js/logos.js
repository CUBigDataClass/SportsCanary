function getLogoForTeam(team) {
    console.log('testing');
    switch(team) {
    case 1:
       alert('Hey');
       break;
    default:
    	console.log("Error");
        console.log('testing');
        return "images/nba_logos/Error-img.jpeg";
	}
}
var chart = c3.generate({
    data: {
        x: 'x',
        columns: [
            ['x', '2014-07-24', '2014-07-25', '2014-07-26', '2014-07-27', '2014-07-28', '2014-07-29'],
            ['temperature', 5, 2, 4, -3, 6, 5],
            ['data2', 130, 340, 200, 500, 250, 350],
            ['data3', 500, 50, 250, 450, 60, 350]
        ],
        axes: {
            'temperature': 'y2'
        },
        type: 'bar',
        types: {
            temperature: 'line'
        }
    },
    subchart: {
        show: true
    },
    zoom: {
        enabled: true
    },
    axis: {
        x: {
            type: 'timeseries',
            tick: {
                format: '%Y-%m-%d'
            }
        },
        y: {
            label: {
                text: 'Some data',
                position: 'outer-middle'
            }
        },
        y2: {
            show: true,
            label: {
                text: 'avg. temperature',
                position: 'outer-middle'
            },
            max: 30,
            min: -10
        }
    }
});