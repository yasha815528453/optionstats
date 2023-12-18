import { Box, Typography, useTheme } from "@mui/material";
import { useState, useEffect } from "react";
import { DataGrid } from "@mui/x-data-grid";
import { tokens } from "../../theme";
import Header from "../../components/Header";
import RatioBar from "../../components/ratiobar/Ratiobar";
import './overview.css'
import { Tabs, Tab } from "@mui/material";
import PcChart from "../../components/echarts";

const Overview = () => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    const [selectorValue1, setSelectorValue1] = useState("highest");
    const [selectorValue2, setSelectorValue2] = useState(1);
    const [data, setData] = useState([]);
    const [statdata, setStatdata] = useState(null);
    const [selectedIndices, setIndicesComponent] = useState(0);
    const handleSelectorChange1 = (e) => {
        setSelectorValue1(e.target.value);
    }

    const handleSelectorChange2 = (e) => {
        setSelectorValue2(parseInt(e.target.value));
    }

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
      const [timestamp, setTimestamp] = useState("");

      useEffect(() => {
          const fetchforData = async () => {
              const response = await fetch(`/api/timestamp`);
              const data = await response.json();
              console.log(data);
              setTimestamp(data[0]);
          };
          fetchforData();
      }, []);

      useEffect(() => {
        const fetchData = async () => {
            const response = await fetch(`/api/expectation/${indices[selectedIndices]}`);
            const data = await response.json();
            console.log(data)
            setCdata(data);
        };
        fetchData();
    }, [selectedIndices]);

    useEffect(() => {
        const fetchforData = async () => {
            const response = await fetch(`/api/stats/${indices[selectedIndices]}`);
            const data = await response.json();
            setStatdata(data);
        };
        fetchforData();
    }, [selectedIndices]);

    const generalColumns = [
        { field: "SYMBOLS", headerName: "Ticker symbol",
          renderCell: (params) => (
            <div className="MuiDataGrid-large"
            style={{ width: "100%", height:"100%", color: colors.blueAccent[300]}}
            >
              {params.value}
            </div>
          )},
        {
          field: "description",
          headerName: "Description",
          minWidth: 280,
          renderCell: (params) => (
            <div
              className="MuiDataGrid-small"
              style={{ width: "100%", height: "100%",color: colors.blueAccent[300]}}
            >
              {params.value}
            </div>
          ),
        },
        { field: "closingprice", headerName: "Closing price",
          renderCell: (params) => (

          <div className="MuiDataGrid-large"
          style={{ width: "100%", height:"100%", color: params.row.percentchange < 0 ? colors.redAccent[400] : colors.greenAccent[400]}}
          >
            {params.value} $
          </div>
        )},
        { field: "variable1", headerName: "variable2",
        renderCell: (params) => (
            <div className="MuiDataGrid-large"
            style={{ width: "100%", height:"100%", color: colors.primary[100]}}
            >
              {params.value}
            </div>
          )},
      ];


    const endpoints = ["otmitmcratio", "otmitmpratio", "otmitmcoiratio", "otmitmpoiratio", "cpratio"];
    const indices = ["SPY", "DIA", "QQQ"];


    const variableMapping = [
        {
            variable1:"otmitmcratio",
            variable2:"ITM/OTM ratio - Call Volume",
        },
        {
            variable1:"otmitmpratio",
            variable2:"ITM/OTM ratio - Put Volume",
        },
        {
            variable1:"otmitmcoiratio",
            variable2:"ITM/OTM ratio - Call OI",
        },
        {
            variable1:"otmitmpoiratio",
            variable2:"ITM/OTM ratio - Put OI",
        },
        {
            variable1:"cpratio",
            variable2:"call put ratio",
        },
    ]


    useEffect(() => {
        fetchData(selectorValue1, selectorValue2);
        }, [selectorValue1, selectorValue2]);

    function fetchData(componentNumber1, componentNumber2) {
        const key = `data-${componentNumber1}-${componentNumber2}`;
        const savedData = sessionStorage.getItem(key);
        if (savedData) {
            setData(JSON.parse(savedData));
        } else {
            const apiEndpoint = `api/top10/${componentNumber1}/${endpoints[componentNumber2 - 1]}`;
            fetch(apiEndpoint)
            .then((response) => response.json())
            .then((data) => {
                setData(data);
                sessionStorage.setItem(key, JSON.stringify(data));
            })
            .catch((error) => console.error(error));
        }
        }

    const columns = generalColumns.map((column) => {
        if (column.field in variableMapping[selectorValue2 - 1]) {
            return {
            ...column,
            field: variableMapping[selectorValue2 - 1][column.field],
            headerName: variableMapping[selectorValue2 - 1][column.headerName],

            };
        }
        return column;
    });

    const handleTabChange = (event, newValue) => {
        setIndicesComponent(newValue);
      };



    return(
        <Box m={4}>
            <Box m="10px" height = "100%">
                <Box display="flex" justifyContent="space-between" alignItems="center">
                    <Header title="Overview" subtitle="Welcome to options insights" />
                </Box>
            </Box>
            <Typography
                variant = "h6"
                color={colors.grey[300]}>
                Last Updated {timestamp.timestamp} PDT End of day quote
            </Typography>
            <Box m="10px" display="flex" height = "100%">
                <Box width="60%" >
                    <Tabs value={selectedIndices} onChange={handleTabChange} textColor="secondary" indicatorColor="secondary">
                        <Tab label="SPDR 500" sx={{color:colors.grey[100]}}/>
                        <Tab label="Dow Jones" sx={{color:colors.grey[100]}}/>
                        <Tab label="Nasdaq" sx={{color:colors.grey[100]}}/>
                    </Tabs>
                    <PcChart symbol={cdata.stockdata[0].symbol} backenddata={cdata || { chartdata: { result: [] } }} h={"63vh"} w={"103vh"}/>

                </Box>
                <Box width = "40%" height = "100%" display = "flex" flexDirection="column">

                    <Box height="40%">
                    <div className="option-summary">
                        <h2>Option Summary Today</h2>
                        <hr />


                        <div className="content">
                            {statdata === null ? (
                            <div> Loading...</div>
                            ) : (
                            <div style={{ display: 'flex', justifyContent: 'space-between', minHeight: '28vh' }}>
                            {/* <RatioBar variable1={variable1} variable2={variable2} /> */}

                            <div style={{ paddingRight: '10px', borderRight: '1px solid', width:"50%" }}>

                                <table className="table-container">
                                    <thead>
                                        <tr>
                                            <th scope="col" class="first-col"></th>
                                            <th scope="col" class="sec-col">Calls</th>
                                            <th scope="col" class="third-col"></th>
                                            <th scope="col" class="fourth-col">Puts</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <th class="first-col">
                                                Total Volume
                                            </th>
                                            <td class="sec-col">
                                                {statdata.callvolume}
                                            </td>
                                            <td class="third-col">
                                                <RatioBar variable1={statdata.callvolume} variable2={statdata.putvolume}/>
                                            </td>
                                            <td class="fourth-col">
                                                {statdata.putvolume}
                                            </td>
                                        </tr>
                                        <tr>
                                            <th class="first-col">
                                                Total Open Interest
                                            </th>
                                            <td class="sec-col">
                                                {statdata.calloi}
                                            </td>
                                            <td class="third-col">
                                                <RatioBar variable1={statdata.calloi} variable2={statdata.putoi}/>
                                            </td>
                                            <td class="fourth-col">
                                                {statdata.putoi}
                                            </td>
                                        </tr>
                                        <tr>
                                            <th class="first-col">
                                                ITM Volume
                                            </th>
                                            <td class="sec-col">
                                                {statdata.itmcallvolume}
                                            </td>
                                            <td class="third-col">
                                                <RatioBar variable1={statdata.itmcallvolume} variable2={statdata.itmputvolume}/>
                                            </td>
                                            <td class="fourth-col">
                                                {statdata.itmputvolume}
                                            </td>
                                        </tr>
                                        <tr>
                                            <th class="first-col">
                                                OTM Volume
                                            </th>
                                            <td class="sec-col">
                                                {statdata.otmcallvolume}
                                            </td>
                                            <td class="third-col">
                                                <RatioBar variable1={statdata.otmcallvolume} variable2={statdata.otmputvolume}/>
                                            </td>
                                            <td class="fourth-col">
                                                {statdata.otmputvolume}
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                            <div style={{ paddingRight: '10px', minWidth: "50%", paddingLeft: '5px'}}>
                                <table className="table-container" >
                                    <thead>
                                        <tr>
                                            <th scope="col" class="first-col"></th>
                                            <th scope="col" class="sec-col">Calls</th>
                                            <th scope="col" class="third-col"></th>
                                            <th scope="col" class="fourth-col">Puts</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <th class="first-col">
                                                Avg Volume
                                            </th>
                                            <td class="sec-col">
                                                {statdata.volume}
                                            </td>
                                            <td class="third-col">
                                                <RatioBar variable1={statdata.volume} variable2={statdata.avgvolume}/>
                                            </td>
                                            <td class="fourth-col">
                                                {statdata.avgvolume}
                                            </td>
                                        </tr>
                                        <tr>
                                            <th class="first-col">
                                                Avg Open Interest
                                            </th>
                                            <td class="sec-col">
                                                {statdata.oi}
                                            </td>
                                            <td class="third-col">
                                                <RatioBar variable1={statdata.oi} variable2={statdata.avgoi}/>
                                            </td>
                                            <td class="fourth-col">
                                                {statdata.avgoi}
                                            </td>
                                        </tr>
                                        <tr>
                                            <th class="first-col">
                                                Volatility
                                            </th>
                                            <td class="sec-col">
                                                {statdata.volatility}
                                            </td>
                                            <td class="third-col">
                                                <RatioBar variable1={statdata.volatility} variable2={statdata.avgvola}/>
                                            </td>
                                            <td class="fourth-col">
                                                {statdata.avgvola}
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div> )}
                        <hr />
                        <div className="top-10s">
                            <Box height="5vh" display="flex">
                                <h3>Today's Top 10s</h3>
                                <Box display="flex" justifyContent="right" marginLeft="10px" marginTop="20px">
                                    <Box marginRight="10px">
                                        <select value={selectorValue1} onChange={handleSelectorChange1}>
                                            <option value="highest">Highest</option>
                                            <option value="lowest">Lowest</option>
                                        </select>
                                    </Box>
                                    <Box>
                                        <select value={selectorValue2} onChange={handleSelectorChange2}>
                                            <option value="1">ITM/OTM ratio - Call Volume</option>
                                            <option value="2">ITM/OTM ratio - Put Volume</option>
                                            <option value="3">ITM/OTM ratio - Call OI</option>
                                            <option value="4">ITM/OTM ratio - Put OI</option>
                                            <option value="5">Call-Put ratio</option>
                                        </select>
                                    </Box>

                                </Box>


                            </Box>
                            <Box height="332px">
                                <DataGrid
                                        getRowId={(row) => row.SYMBOLS}
                                        rows={data}
                                        columns={columns}
                                        rowHeight={30}
                                        headerHeight={30}
                                        hideFooter={true}
                                    />
                            </Box>

                        </div>
                        </div>
                        </div>
                    </Box>

                </Box>
            </Box>
        </Box>
    )
}


export default Overview;
