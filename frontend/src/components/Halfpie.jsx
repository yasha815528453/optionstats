import ReactECharts from 'echarts-for-react';
import { Box } from "@mui/material";
import React from 'react';
import * as echarts from 'echarts/core';
import { tokens } from "../theme";
import { Typography, useTheme } from "@mui/material";

const Halfpie = ({backenddata}) => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    const dataCopy = backenddata.slice();
    dataCopy.sort((a, b) => b.dollarestimate - a.dollarestimate);

    const top10 = dataCopy.slice(0, 10);
    const totalSum = top10.reduce((sum, item) => sum + item.dollarestimate, 0);
    const piechartData = top10.map(item => ({
        name: item.INDUSTRY,
        value: item.dollarestimate
      }));
    piechartData.push({
        value: totalSum,
        itemStyle: {
            color: 'none',
            decal: {
              symbol: 'none'
            }
          },
          label: {
            show: false
          }
    })
    const options = {
        title: {
          text: "",
          left: 'right',
          top:'0'
        },
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b} : {c}$ ({d}%)',
        },

        series: [
          {
            name: '$ traded ON:',
            type: 'pie',
            radius: ['40%', '100%'],
            center: ['100%', '55%'],
            data: piechartData,
            startAngle: 270,
            label: {
                color: colors.primary[100],
                show: true,
                formatter(param) {
                  // correct the percentage
                  return param.name + ' (' + param.percent * 2 + '%)';
                }
            },
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              },
            }
          }
        ]
      };

    return (
        <Box height="75vh">
            <ReactECharts option={options} style= {{width:'55vh', height:'65vh'}}/>
        </Box>
    )

};

export default Halfpie;
