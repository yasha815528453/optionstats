import { Box } from "@mui/material";
import Header from "../../components/Header"
const Overview = () => {
    return(
        <Box m="5px">
            <Box m="10px" height = "100%">
                <Box display="flex" justifyContent="space-between" alignItems="center">
                    <Header title="Overview" subtitle="Welcome to options insights" />
                </Box>
            </Box>
            <Box m="20px" display="flex" height = "100%">
                <Box width="65%" >
                    indices charts
                </Box>
                <Box width = "35%" height = "100%" display = "flex" flexDirection="column">
                    <Box height="60%">
                        top10
                    </Box>

                    <Box height="40%">
                        overall option stats
                    </Box>

                </Box>
            </Box>
        </Box>
    )
}


export default Overview;
