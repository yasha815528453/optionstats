import ReactECharts from 'echarts-for-react';
import { Box } from "@mui/material";
import React from 'react';
import * as echarts from 'echarts/core';
import { tokens } from "../theme";
import { Typography, useTheme } from "@mui/material";

const DPiechart = ({backenddata}) => {

    const piechartData = backenddata.map(item => ({
        name: item.INDUSTRY,
        value: item.dollarestimate,
      }));

    const options = {
        title: {
          text: "Today's $ traded on options",
          left: 'center',
          top:'0'
        },
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b} : {c} ({d}%)',
        },
        series: [
          {
            name: 'Dollar traded ON:',
            type: 'pie',
            radius: ['40%', '70%'],
            center: ['40%', '50%'],
            data: piechartData,
            startAngle: 270,
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      };

    return (
        <Box>
            <ReactECharts option={options} />
        </Box>
    )

};

export default DPiechart;
