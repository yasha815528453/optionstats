import { useState, useEffect } from "react";
import ReactECharts from 'echarts-for-react';
import { Box } from "@mui/material";
import Header from "../../components/Header";
import { Typography, useTheme } from "@mui/material";
import { tokens } from "../../theme";
import Symbol  from "../../components/Symbolprice";
import SearchBar from "../../components/searchbar";
import { color } from "@mui/system";
import PcChart from "../../components/echarts";
import { Tabs, Tab } from "@mui/material";
import Heatmp from "../../components/heatmap";

const Expectationschart = () => {
    const [cdata, setCdata] = useState({
        chartdata: {
          ispositive: false,
          result: []
        },
        stockdata: [
          {
            category: "",
            closingprice: 0,
            description: "",
            percentchange: 0,
            pricechange: 0,
            symbol: ""
          }
        ]
      });

    const [oidata, setOidata] = useState([]);
    const [searchTerm, setSearchTerm] = useState('SPY');
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    const [selecttable, setSelectTable] = useState(0);

    useEffect(() => {
        const fetchData = async () => {
            if(searchTerm) {
                const response = await fetch(`/api/expectation/${searchTerm}`);
                const data = await response.json();
                setCdata(data);
                const response2 = await fetch(`/api/oitable/${searchTerm}`);
                const data2 = await response2.json();
                setOidata(data2);
            }
        };
        fetchData();
    }, [searchTerm]);

    const handleSearch = (searchValue) => {
        setSearchTerm(searchValue);
        // Implement your search logic here
    };
    const handleTabChange = (event, newValue) => {
        setSelectTable(newValue);
      };

    return (
        <Box m="5px">
            <Box m="10px" height="100%">
                <Box display="flex" justifyContent="space-between" alignItems="center" width="53%">
                    <Header title="Trend expectation" subtitle="Expectations of dollar movement based on options pricing" />
                </Box>
            </Box>

            {cdata.chartdata.result.length > 0 ? (
            <Box m="10px"
                sx = {{
                    display:'grid',
                    gridTemplateColumns: 'repeat(16, 1fr)',
                    gridTemplateRows: 'repeat(16, 1fr)',
                    gap: 2,
                    height: '80vh',
                }}
                >

                <Box display="flex" justifyContent="space-between"
                    sx={{
                        gridColumn: '1',
                        gridRow: '1 / span 3',
                        gridColumnEnd: 'span 4',
                    }}
                    >
                    {console.log(cdata.stockdata.percentchange)}
                    <Symbol description={cdata.stockdata[0].description} closingprice = {cdata.stockdata[0].closingprice} pricechange={cdata.stockdata[0].pricechange} percentchange={cdata.stockdata[0].percentchange} />
                </Box>

                <Box
                sx={{
                    gridColumn: '8 / span 8',
                    gridRow: '1 / span 5',
                }}>
                        <SearchBar onSearch={handleSearch} />
                </Box>

                <Box sx={{
                        gridColumn:'1',
                        gridRow: '4 / span 16',
                        gridColumnEnd: 'span 16',}}>
                        <Tabs value={selecttable} onChange={handleTabChange} textColor="secondary" indicatorColor="secondary" >
                            <Tab label="Expectation"/>
                            <Tab label="Open Interest Heatmap"/>
                        </Tabs>
                        {selecttable === 0 ? (
                                <PcChart symbol={cdata.stockdata[0].symbol} backenddata={cdata || { chartdata: { result: [] } }} h={"57vh"} w={"125vh"}/>)
                                : ( <Heatmp backenddata={oidata}/>)}
                </Box>



                <Box sx={{
                    gridColumn:'13',
                    gridRow: '6 / span 3',
                    gridColumnEnd: 'span 3',
                }}
                    border="4px solid"
                    borderColor={colors.grey[200]}
                >
                    <Typography
                        variant = "h4"
                        color={colors.grey[100]}
                        margin="10px"
                    >
                        This stock is in the category of {cdata.stockdata[0].category}
                    </Typography>


                    {cdata.chartdata.ispositive ? (
                        <Typography
                            variant = "h4"
                            color = {colors.greenAccent[700]}
                            margin="10px"
                        >
                            The overall expectation of this stock is POSITIVE

                        </Typography>
                    ) : (
                        <Typography
                            variant = "h4"
                            color = {colors.redAccent[400]}
                            margin="10px"
                        >
                            The overall expectation of this stock is NEGATIVE
                        </Typography>
                    )


                }
                </Box>
            </Box>) : (
                <Box m="50px" >
                    <Box
                sx={{
                    gridColumn: '8 / span 8',
                    gridRow: '1 / span 3',
                }}>
                        <SearchBar onSearch={handleSearch} />
                </Box>
                <Typography variant = "h3" color={colors.primary[100]}>
                    No data available for the given input. Please try again with a different symbol.
                </Typography>
                <Box marginBottom="70vh"/>
            </Box>
            )

            }
        </Box>

    )
}

export default Expectationschart;
