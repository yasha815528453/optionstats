import { Box, Icon, IconButton, useTheme } from "@mui/material";
import { useContext } from "react";
import { ColorModeContext, themeSettings } from "../../theme";
import LightModeOutlinedIcon from '@mui/icons-material/LightModeOutlined';
import DarkModeIcon from '@mui/icons-material/DarkMode';
import FeedbackOutlinedIcon from '@mui/icons-material/FeedbackOutlined';


const Topbar = () => {
    const theme = useTheme();
    const colors = themeSettings()
    const colorMode = useContext(ColorModeContext);

    return <Box display="flex"  justifyContent="right" marginTop={"2vh"} marginRight={"8vh"}>
        <Box display="flex">
            <IconButton onClick={colorMode.toggleColorMode}>
                {theme.palette.mode === 'light' ? (
                    <DarkModeIcon />
                ) : (
                    <LightModeOutlinedIcon />
                )}
            </IconButton>
            <IconButton>
                <FeedbackOutlinedIcon />
            </IconButton>
        </Box>

    </Box>;
};


export default Topbar;
