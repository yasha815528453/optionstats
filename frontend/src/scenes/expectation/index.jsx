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
    const [searchTerm, setSearchTerm] = useState('SPY');
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);

    useEffect(() => {
        const fetchData = async () => {
            if(searchTerm) {
                const response = await fetch(`/api/expectation/${searchTerm}`);
                const data = await response.json();
                console.log(data)
                setCdata(data);
            }
        };
        fetchData();
    }, [searchTerm]);

    const handleSearch = (searchValue) => {
        setSearchTerm(searchValue);
        // Implement your search logic here
    };

    return (
        <Box m="5px">
            <Box m="10px" height="100%">
                <Box display="flex" justifyContent="space-between" alignItems="center" width="53%">
                    <Header title="Trend expectation" subtitle="Expectations of dollar movement based on options pricing" />
                    <SearchBar onSearch={handleSearch} />
                </Box>
            </Box>
            {cdata.chartdata.result.length > 0 ? (
            <Box m="20px"
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
                <Box sx={{
                    gridColumn:'4',
                    gridRow: '2 / span 16',
                    gridColumnEnd: 'span 16',
                    flexGrow: 1, overflow: 'auto', m:"30px"}}>

                    <PcChart symbol={cdata.stockdata[0].symbol} backenddata={cdata || { chartdata: { result: [] } }} />

                    </Box>

                <Box sx={{
                    gridColumn:'1',
                    gridRow: '6 / span 2',
                    gridColumnEnd: 'span 3',
                }}
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
            </Box> ) : (
                <Box m="50px" >
                    <Typography variant = "h3" color={colors.primary[100]}>
                        No data available for the given input. Please try again with a different symbol.
                    </Typography>
                </Box>
            )

            }
        </Box>

    )
}

export default Expectationschart;
