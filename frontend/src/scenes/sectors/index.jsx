import { Box, Typography, useTheme} from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import { tokens } from "../../theme";
import { React, useEffect, useState } from "react";
import Header from "../../components/Header"
import { Tabs, Tab } from "@mui/material";
import DPiechart from "../../components/pie";
import Halfpie from "../../components/Halfpie";

const Sectors = () => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    const [data, setData] = useState([]);
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

    const generalColumns = [
        {
          field: "INDUSTRY",
          headerName: "Categories",
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

        { field: "avgperf", headerName: "Average Performance",
          minWidth: 130,
          renderCell: (params) => (

          <div className="MuiDataGrid-large"
          style={{ width: "100%", height:"100%", color: params.row.avgperf < 0 ? colors.redAccent[400] : colors.greenAccent[400]}}
          >
            {params.value >= 0 ? `+${params.value}` : params.value}%
          </div>
        )},
          { field: "oi", headerName: "Open Interest",
          minWidth: 100,
        renderCell: (params) => (
          <div className="MuiDataGrid-large"
          style={{ width: "100%", height:"100%", color: colors.grey[100]}}
          >
            {params.value}
          </div>
        ) },
        { field: "avgoi", headerName: "Average OI",
        renderCell: (params) => (
          <div className="MuiDataGrid-large"
          style={{ width: "100%", height:"100%"}}
          >
            {params.value}
          </div>
        ) },

        { field: "volume", headerName: "Volume",
        renderCell: (params) => (
          <div className="MuiDataGrid-medium"
          style={{ width: "100%", height:"100%"}}
          >
            {params.value}
          </div>
        ) },
        { field: "avgvolume", headerName: "Average Volume",
        renderCell: (params) => (
          <div className="MuiDataGrid-medium"
          style={{ width: "100%", height:"100%"}}
          >
            {params.value}
          </div>
        ) },
        { field: "volatility", headerName: "Volatility",
        renderCell: (params) => (
          <div className="MuiDataGrid-medium"
          style={{ width: "100%", height:"100%"}}
          >
            {params.value}
          </div>
        ) },
        { field: "avgvola", headerName: "Average Volatility",
        renderCell: (params) => (
          <div className="MuiDataGrid-medium"
          style={{ width: "100%", height:"100%"}}
          >
            {params.value}
          </div>
        ) },
      ];

    useEffect(() => {
        fetch('/api/sectors').then((response) => response.json()).then((data) => {
            setData(data);
        }).catch((error) => console.error(error));
    }, []);


    return(
        <Box m={4}>
            <Header title="Sector Performance"/>
            <Typography
                m="-20px 0 0 0"
                variant="h6"
                color={colors.grey[300]}>
                Last Updated {timestamp.timestamp} PDT End of day quote
            </Typography>

            <Box m="10px 0 0 0px" height="75vh" width="100%" display="flex">
              <Box height="75vh" width="115vh">
                <DataGrid
                  getRowId={(row) => row.INDUSTRY}
                  rows={data}
                  columns={generalColumns}
                  rowHeight={100}
                  headerHeight={70}
              />
              </Box>
              <Box height="75vh" width="60vh">

                <Box height="75vh" width="100%" m="0 0 0 20px">
                  <Halfpie backenddata={data}/>
                </Box>

              </Box>
            </Box>

        </Box>
    );
};

export default Sectors;
