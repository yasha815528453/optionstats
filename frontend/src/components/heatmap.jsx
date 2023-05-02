import ReactECharts from 'echarts-for-react';
import { Box } from "@mui/material";
import { tokens } from "../theme";
import { Typography, useTheme } from "@mui/material";

const Heatmp = ({backenddata}) => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    
    const option = {
        tooltip: {},
        grid: {
            height: '50%',
            top: '10%'
          },
        xAxis: {
            type: 'category',
            data: get from backenddata, 
            splitArea: {
                show: true
            }
        },
        yAxis: {
          type: 'category',
          data: getfrom backenddata,
          splitArea: {
            show: true
          }
        },
        visualMap: {
          min: 0,
          max: 1,
          calculable: true,
          realtime: false,
          inRange: {
            color: [
              colors.greenAccent[200],
              colors.greenAccent[400],
              colors.greenAccent[600],
              colors.greenAccent[800],
              colors.grey[800],
              colors.redAccent[800],
              colors.redAccent[600],
              colors.redAccent[400],
              colors.redAccent[200],
            ]
          }
        },
        series: [
          {
            name: 'Open Interest',
            type: 'heatmap',
            data: data,
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
}