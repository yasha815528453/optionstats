import { useState } from "react";
import { ProSidebar, Menu, MenuItem, SidebarFooter } from "react-pro-sidebar";
import 'react-pro-sidebar/dist/css/styles.css';
import { Box, IconButton, Typography, useTheme } from '@mui/material';
import { Link } from "react-router-dom";
import { tokens } from "../../theme";
import FeedbackOutlinedIcon from '@mui/icons-material/FeedbackOutlined';
import MenuOutlinedIcon from '@mui/icons-material/MenuOutlined';
import FirstPageOutlinedIcon from '@mui/icons-material/FirstPageOutlined';
import AppsOutlinedIcon from '@mui/icons-material/AppsOutlined';
import AssessmentOutlinedIcon from '@mui/icons-material/AssessmentOutlined';
import TableChartOutlinedIcon from '@mui/icons-material/TableChartOutlined';
import ShowChartOutlinedIcon from '@mui/icons-material/ShowChartOutlined';
import PublicOutlinedIcon from '@mui/icons-material/PublicOutlined';
import QuestionAnswerOutlinedIcon from '@mui/icons-material/QuestionAnswerOutlined';


const Item = ({ title, to, icon, selected, setSelected }) => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    return (
      <MenuItem
        active={selected === title}
        style={{
          color: colors.grey[100],
        }}
        onClick={() => setSelected(title)}
        icon={icon}
      >
        <Typography>{title}</Typography>
        <Link to={to} />
      </MenuItem>
    );
  };


const Sidebar = () => {

    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    const [isCollapsed, setIsCollapsed] = useState(false);
    const [selected, setSelected] = useState("overview");

    return (
        <Box
            sx={{
                "& .pro-sidebar-inner": {
                    background: `${colors.primary[900]} !important`,
                },
                "& .pro-icon-wrapper": {
                    backgroundColor: "transparent !important",
                },
                "& .pro-inner-item": {
                    padding: "5px 35px 5px 20px !important",
                },
                "& .pro-inner-item:hover": {
                    color: "#868dfb !important",
                },
                "& .pro-menu-item.active": {
                    color: "#6870fa !important",
                },
                height: "100%",

            }}
        >
            <ProSidebar collapsed={isCollapsed}>
                <Menu iconShape="square">
                    <MenuItem
                        onClick={() => setIsCollapsed(!isCollapsed)}
                        icon={isCollapsed ? <MenuOutlinedIcon  fontSize="large"/> : undefined}
                        style={{
                            margin: "10px 0 10px 5px",
                            color: colors.grey[100],
                        }}
                    >
                        {!isCollapsed && (
                            <Box
                            display="flex"
                            justifyContent="space-between"
                            alignItems="center"
                            ml="15px"
                            >
                                <Typography variant="h5" color={colors.grey[100]}>
                                    OPTION VISUALIZER
                                </Typography>
                                <IconButton onClick={() => setIsCollapsed(!isCollapsed)}>
                                    <FirstPageOutlinedIcon  fontSize="large"/>

                                </IconButton>
                            </Box>
                        )}

                    </MenuItem>
                <Box paddingLeft={isCollapsed ? undefined : "10%"} height={"82vh"}>
                    <Item
                        title="Overview"
                        to="/"
                        icon={<AppsOutlinedIcon fontSize="large"/>}
                        selected={selected}
                        setSelected={setSelected}
                    />
                    <Item
                        title = "Option Ranking"
                        to="/rankings"
                        icon={<AssessmentOutlinedIcon fontSize="large"/>}
                        selected={selected}
                        setSelected={setSelected}
                    />
                    <Typography
                    variant="h6"
                    color={colors.grey[300]}
                    sx={{ m: "15px 0 5px 20px" }}
                    >
                        Insights
                    </Typography>
                    <Item
                        title="Sector performance"
                        to="/sectorranking"
                        icon={<TableChartOutlinedIcon fontSize="large"/>}
                        selected={selected}
                        setSelected={setSelected}
                    />
                    <Item
                        title="Expectations"
                        to="/expectations"
                        icon={<ShowChartOutlinedIcon fontSize="large"/>}
                        selected={selected}
                        setSelected={setSelected}
                    />
                    <Item
                        title="Visualize"
                        to="/country"
                        icon={<PublicOutlinedIcon fontSize="large"/>}
                        selected={selected}
                        setSelected={setSelected}
                    />

                </Box>
                <SidebarFooter>
                    <Menu>
                        <MenuItem>
                            <Item
                                title="FAQ page"
                                to="/FAQ"
                                icon={<QuestionAnswerOutlinedIcon fontSize="medium"/>}
                                selected={selected}
                                setSelected={setSelected}
                            />
                        </MenuItem>
                    </Menu>

                </SidebarFooter>


                </Menu>
            </ProSidebar>







        </Box>
    )
}


export default Sidebar;
