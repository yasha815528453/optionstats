import { Box, Icon, IconButton, useTheme, Typography } from "@mui/material";
import { useContext } from "react";
import { tokens } from "../../theme";
import { ColorModeContext, themeSettings } from "../../theme";
const Disclaimer = () => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);

    return (
        <Box
            id="disclaimer"
            sx={{
                marginTop:"5vh",
                backgroundColor: colors.background || '#0c0d0d', // replace with your chosen color
                color: colors.text || '#ffffff', // replace with your chosen color
                height: '20vh', // to make it cover the full height
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                textAlign: 'center',
            }}
        >
            <Typography
                variant="h6"
                color="#e0e0e0"
                >
                 This website is a personal project and is for informational purposes only.<br />
                It is not intended as financial advice. <br />
                Any information contained herein should not be relied upon for making financial decisions.

            </Typography>

        </Box>
    );
}

export default Disclaimer;
