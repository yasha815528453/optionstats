import { Box, Typography, useTheme} from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import { tokens } from "../../theme";
import { React, useEffect, useState } from "react";
import Header from "../../components/Header"
import { Tabs, Tab } from "@mui/material";


const Rankings = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const [data, setData] = useState([]);
  const [selectedComponent, setSelectedComponent] = useState(1);

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
      minWidth: 200,
      renderCell: (params) => (
        <div
          className="MuiDataGrid-cellWrap"
          style={{ width: "100%", height: "100%",color: colors.blueAccent[300]}}
        >
          {params.value}
        </div>
      ),
    },
    { field: "category", headerName: "Category", minWidth:200,
      renderCell: (params) => (
        <div className="MuiDataGrid-medium"
        style={{ width: "100%", height:"100%", color: colors.blueAccent[300]}}
        >
          {params.value}
        </div>
      )},
    { field: "closingprice", headerName: "Closing price",
      renderCell: (params) => (

      <div className="MuiDataGrid-large"
      style={{ width: "100%", height:"100%", color: params.row.percentchange < 0 ? colors.redAccent[400] : colors.greenAccent[400]}}
      >
        {params.value} $
      </div>
    )},
    { field: "percentchange", headerName: "Percent change",
    renderCell: (params) => (
      <div className="MuiDataGrid-medium"
      style={{ width: "100%", height:"100%", color: params.value < 0 ? colors.redAccent[400] : colors.greenAccent[400]}}
      >
        {params.value >= 0 ? `+${params.value}` : params.value}%
      </div>
    )},
    { field: "pricechange", headerName: "Price change",
    renderCell: (params) => (
      <div className="MuiDataGrid-medium"
      style={{ width: "100%", height:"100%", color: params.value < 0 ? colors.redAccent[400] : colors.greenAccent[400]}}
      >
         {params.value >= 0 ? `+${params.value}` : params.value} $
        </div>
      )},
    { field: "variable1", headerName: "variable2",
    renderCell: (params) => (
      <div className="MuiDataGrid-medium"
      style={{ width: "100%", height:"100%", color: params.value < 0 ? colors.redAccent[400] : colors.greenAccent[400]}}
      >
        {params.value >= 0 ? `+${params.value}` : params.value}%
      </div>
    )},
      { field: "strikeprice", headerName: "Strike price",
    renderCell: (params) => (
      <div className="MuiDataGrid-large"
      style={{ width: "100%", height:"100%", color: colors.grey[100]}}
      >
        {params.value}
      </div>
    ) },
    { field: "strikedate", headerName: "Strike date", minWidth: 150,
    renderCell: (params) => (
      <div className="MuiDataGrid-large"
      style={{ width: "100%", height:"100%"}}
      >
        {params.value}
      </div>
    ) },

    { field: "variable3", headerName: "variable4",
    renderCell: (params) => (
      <div className="MuiDataGrid-medium"
      style={{ width: "100%", height:"100%"}}
      >
        {params.value}
      </div>
    ) },
    { field: "volume", headerName: "Trade volume",
    renderCell: (params) => (
      <div className="MuiDataGrid-medium"
      style={{ width: "100%", height:"100%"}}
      >
        {params.value}
      </div>
    ) },
    { field: "avgvolume", headerName: "Average volume",
    renderCell: (params) => (
      <div className="MuiDataGrid-medium"
      style={{ width: "100%", height:"100%"}}
      >
        {params.value}
      </div>
    ) },
  ];

  const apiEndpoints = [
    "/api/top100bcperf",
    "/api/top100bpperf",
    "/api/top100wcperf",
    "/api/top100wpperf",
  ];

  const variableMapping = [
    {
      variable1: "bcallperf",
      variable2: "Best performance today",
      variable3: "bcalldate",
      variable4: "Purchase date ",
    },
    {
      variable1: "bputperf",
      variable2: "Best performance today",
      variable3: "bputdate",
      variable4: "Purchase date",
    },
    {
      variable1: "wcallperf",
      variable2: "Worst performance today",
      variable3: "wcalldate",
      variable4: "Sell date",
    },
    {
      variable1: "wputperf",
      variable2: "Worst performance today",
      variable3: "wputdate",
      variable4: "Sell date ",
    },
  ];

  useEffect(() => {
    fetchData(selectedComponent);
  }, [selectedComponent]);

  function fetchData(componentNumber) {
    const savedData = sessionStorage.getItem(`data-${componentNumber}`);
    if (savedData) {
      setData(JSON.parse(savedData));
    } else {
      fetch(apiEndpoints[componentNumber - 1])
        .then((response) => response.json())
        .then((data) => {
          setData(data);
          sessionStorage.setItem(`data-${componentNumber}`, JSON.stringify(data));
        })
        .catch((error) => console.error(error));
    }
  }

  function showComponent(componentNumber) {
    setSelectedComponent(componentNumber);
  }
  const handleTabChange = (event, newValue) => {
    setSelectedComponent(newValue + 1);
  };

  const columns = generalColumns.map((column) => {
    if (column.field in variableMapping[selectedComponent - 1]) {
      return {
        ...column,
        field: variableMapping[selectedComponent - 1][column.field],
        headerName: variableMapping[selectedComponent - 1][column.headerName],

      };
    }
    return column;
  });

  return (
    <Box m="20px">
      <Header title="RANKINGS" subtitle="Options Ranking" />
      <Typography
        m="-20px 0 0 0"
        variant="h6"
        color={colors.grey[300]}>
           Last Updated 2023-01-02 03:03 PDT End of day quote
      </Typography>
      <Box m="10px 0 0 50px" height="75vh" width="160vh">
        <Tabs value={selectedComponent - 1} onChange={handleTabChange} textColor="secondary" indicatorColor="secondary">
          <Tab label="Buyside calls" sx={{color:colors.grey[100]}}/>
          <Tab label="Buyside puts" sx={{color:colors.grey[100]}}/>
          <Tab label="Sellside calls" sx={{color:colors.grey[100]}}/>
          <Tab label="Sellside puts" sx={{color:colors.grey[100]}}/>
        </Tabs>
        <DataGrid
          getRowId={(row) => row.SYMBOLS}
          rows={data}
          columns={columns}
          rowHeight={100}
          headerHeight={70}
        />
      </Box>
    </Box>
    );
    };

  export default Rankings;
