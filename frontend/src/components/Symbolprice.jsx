import { Box, IconButton, Typography, useTheme } from '@mui/material';
import { tokens } from "../theme";

const Symbol = ({ description, closingprice, pricechange, percentchange }) => {
    const theme = useTheme();
    console.log(percentchange)
    const colors = tokens(theme.palette.mode);
    pricechange = Math.abs(pricechange)
    const stockcolor = percentchange < 0 ? colors.redAccent[500] : colors.greenAccent[900];
    const sign = percentchange < 0 ? '-' : '+';

    percentchange = Math.abs(percentchange)

    return (
        <Box width="45vh" >
            <Box borderBottom="1px solid" borderColor={colors.grey[500]}>
                <Typography
                    variant="h3"
                    color={colors.grey[100]}
                    fontWeight='300'
                    fontFamily={"inherit, monospace"}
                    sx={{ mb: "15px"}}
                >
                    {description}
                </Typography>
            </Box>
            <Box marginTop={1} display="flex" justifyContent="left">
                <Typography
                    variant="h3"
                    color={colors.grey[100]}
                    fontWeight='100'
                    sx = {{fontFamily: 'Raleway, monospace', mb: "5px"}}
                >
                    {closingprice}
                </Typography>

                <Box display="flex" marginTop="7px" marginLeft="2vh" flexDirection="row" justifyContent="space-around" width="12vh">
                    <Typography
                        variant="h5"
                        color={stockcolor}
                        fontWeight='100'
                        sx = {{ fontFamily: 'Raleway, monospace'}}
                    >
                        {sign}{pricechange}
                    </Typography>
                    <Typography
                        variant="h5"
                        color={stockcolor}
                        fontWeight='100'
                        sx = {{ fontFamily: 'Raleway, monospace'}}
                    >
                        {sign}{percentchange}%
                    </Typography>


                </Box>

            </Box>
            <Typography
                        variant = "h6"
                        color={colors.grey[300]}
                    >
                        Last Updated 2023-01-02 03:03 PDT
                        End of day quote
                    </Typography>
        </Box>
    )
}

export default Symbol;