import ReactECharts from 'echarts-for-react';
import { Box } from "@mui/material";
import { tokens } from "../theme";
import { Typography, useTheme } from "@mui/material";

const Heatmp = ({backenddata}) => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    console.log(backenddata)
    console.log(backenddata.map((item) => item.compiledate));
    let compiledates = [...new Set(backenddata.map((item) => item.compiledate))];

    let positions = [...new Set(backenddata.map((item) => item.position))];


    let seriesData = backenddata.map((item) => {
      let compiledateIndex = compiledates.indexOf(item.compiledate);
      let positionIndex = positions.indexOf(item.position);
      let openinterest = item.openinterest;

      return [compiledateIndex, positionIndex, openinterest];
    });
    const option = {
        tooltip: {},
        grid: {
            height: '60%',
            top: '10%',
            left: '6%',
          },
        xAxis: {
            type: 'category',
            data: compiledates,
            splitArea: {
                show: true
            }
        },
        yAxis: {
          type: 'category',
          data: positions,
          splitArea: {
            show: true
          },
          name: 'Out the money',

        },
        visualMap: {
          min: -10000,
          max: 10000,
          calculable: true,
          realtime: false,
          bottom: '15%',
          left: 'center',
          orient: 'horizontal',
          inRange: {
            color: [
              colors.redAccent[100],
              colors.redAccent[200],
              colors.redAccent[300],
              colors.redAccent[400],
              colors.redAccent[500],
              colors.redAccent[600],
              colors.redAccent[700],
              colors.redAccent[800],
              colors.grey[900],
              colors.greenAccent[100],
              colors.greenAccent[200],
              colors.greenAccent[300],
              colors.greenAccent[400],
              colors.greenAccent[500],
              colors.greenAccent[600],
              colors.greenAccent[700],
              colors.greenAccent[800],

            ]
          }
        },
        series: [
          {
            name: 'Open Interest',
            type: 'heatmap',
            data: seriesData,
            emphasis: {
                itemStyle: {
                  shadowBlur: 10,
                  shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
              },
            animation: false
          }
        ]
      };

      return (
        <Box display="flex">
            <Box marginTop="22vh" marginRight="-5vh">
              <Typography color={colors.grey[200]}>
                At the money
                </Typography>
            </Box>
            <ReactECharts option={option}
              style = {{width:"125vh", height:"58vh"}}
              />

        </Box>
      )
}

export default Heatmp;
