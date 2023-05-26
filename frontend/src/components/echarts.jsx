import ReactECharts from 'echarts-for-react';
import { Box } from "@mui/material";
import { tokens } from "../theme";
import { Typography, useTheme } from "@mui/material";

const PcChart = ({symbol, backenddata, h, w}) => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    const options = {
        title: {
            text: symbol,
            top: 0,
            right: "center",
            textStyle: {
                color: colors.grey[100]
            }
        },
        tooltip : {
            trigger: 'axis',
            axisPointer: { type: 'cross'}
        },
        legend: {
            data: ["today's projections", "projections 10 days ago", 'Call Volume', 'Put Volume'],
            orient: 'horizontal',
            right: 'center',
            top: 30,
            itemGap: 20,
            textStyle: {
                color: colors.grey[100],
            }
        },
        toolbox: {
            top: 0,
            right: 160,
            orient: 'horizontal',
            feature: {
                saveAsImage: {
                    show:true,
                }
            }
        },
        grid: {
            left: '4%',
            right: '10%',
            top: '10%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: [
            {
                axisTick: {
                    alignWithLabel: true
                },
                axisLabel: {
                    rotate: 20
                },
                type: 'category',
                boundaryGap : true,
                data : backenddata.chartdata.result.map((item) => item.compiledate),
                axisline: {
                    symbol: 'none',
                    lineStyle: {
                        type: 'solid',
                        color: colors.grey[100],
                    }
                }
            }
        ],
        yAxis : [
            {
                type: 'value',
                name: 'Option Volume',
                position:'right',
                splitLine: {
                    show: false,
                },
                axisLine: {
                    show: 'true',
                    symbol: 'none',
                    lineStyle: {
                        type: 'solid',
                        color: colors.grey[100],
                    }
                }
            },
            {
                type:'value',
                name:'Expected Dollar Movement',
                position:'left',
                axisLabel: {
                    formatter:' {value} $'
                },
                splitLine: {
                    show: false,
                },
                axisLine: {
                    show: 'true',
                    symbol: 'none',
                    lineStyle: {
                        type: 'solid',
                        color: colors.grey[100],
                    }
                }
            }
        ],
        series : [
            {
                name: "today's projections",
                type: 'line',
                yAxisIndex: 1,
                color: colors.primary[100],
                data : backenddata.chartdata.result.map((item) => item['pcdiff'])
            },
            {
                name: 'projections 10 days ago',
                type: 'line',
                yAxisIndex: 1,
                color: colors.blueAccent[600],
                data: backenddata.chartdata.result.map((item) => item['10pcdiff'])
            },
            {
                name: 'Call Volume',
                type: 'bar',
                yAxisIndex: 0,
                color: colors.greenAccent[600],
                data: backenddata.chartdata.result.map((item) => item.callvol)
            },
            {
                name: 'Put Volume',
                type: 'bar',
                yAxisIndex: 0,
                color: colors.redAccent[600],
                data: backenddata.chartdata.result.map((item) => item.putvol)
            }
        ]
    };

    return (
        <Box>
            <ReactECharts option={options}
                style = {{width:w, height: h}}
            />
            {}
        </Box>
    )
}


export default PcChart;
