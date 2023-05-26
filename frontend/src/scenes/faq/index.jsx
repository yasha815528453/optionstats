import { Typography, useTheme } from "@mui/material";
import { Box } from "@mui/material";
import { tokens } from "../../theme";


const Faq = () => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);


    return (
        <Box height="90vh"
            sx={{
                color: colors.grey[100],
            }}
        >
            <Box marginLeft="50vh" marginTop="5vh" marginBottom="5vh">
                <Typography variant="h2" fontWeight="bold">
                    Frequently Asked Questions
                </Typography>
            </Box>


            <Box margin="8vh" marginRight="16vh">
                <Typography variant="h3" gutterBottom>
                    How are the options ranked?
                </Typography>
                <br></br>
                <Typography variant="h5" gutterBottom>
                    Options are ranked by the maximum gain/loss possible, for both
                    the buy side and sell side.
                    Gain/loss is calculated by getting the highest high and lowest low it has ever been
                </Typography>
            </Box>

            <Box margin="8vh" marginRight="16vh">
                <Typography variant="h3" gutterBottom>
                    How does the expectation chart work?
                </Typography>
                <Typography variant="h5" gutterBottom>
                    The projections are calculated by offsetting the pricing of
                    call and put option contracts against each other, taking into account
                    of interest rate and implied volatility, how much of a difference of pricing
                    are there between the contracts with same $ distance.
                </Typography>
            </Box>

            <Box margin="8vh" marginRight="16vh">
                <Typography variant="h3" gutterBottom>
                    How does the open interst heatmap work?
                </Typography>
                <Typography variant="h5" gutterBottom>
                    In the heatmap, the green represents call options, and red represents put options.
                    The y-axis represents the out/in the money from the stock price, with the middle being
                    at the money. For call options, higher number means out the money; while put options,
                    the higher number means in the money. The total difference between the number of
                    open interest of call and put options are the OI values. The y-axis is not
                    a representation of relations to the stock price.
                </Typography>
            </Box>

            {/* Add more FAQs as needed */}
        </Box>
    );
}

export default Faq;
