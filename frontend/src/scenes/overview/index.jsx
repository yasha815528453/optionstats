import { Box } from "@mui/material";
import { useState } from "react";
import Header from "../../components/Header";
import RatioBar from "../../components/ratiobar/Ratiobar";

const Overview = () => {

    const [selectorValue, setSelectorValue] = useState('a');

    const handleSelectorChange = (event) => {
      setSelectorValue(event.target.value);
    };

    const [variable1, setVariable1] = useState(5);
    const [variable2, setVariable2] = useState(10);

    return(
        <Box m="5px">
            <Box m="10px" height = "100%">
                <Box display="flex" justifyContent="space-between" alignItems="center">
                    <Header title="Overview" subtitle="Welcome to options insights" />
                </Box>
            </Box>
            <Box m="20px" display="flex" height = "100%">
                <Box width="60%" >
                    indices charts
                </Box>
                <Box width = "40%" height = "100%" display = "flex" flexDirection="column">
                    
                    <Box height="40%">
                    <div className="option-summary">
                        <h2>Option Summary Today</h2>
                        <hr />
                        <div className="content">
                            <div>
                            <RatioBar variable1={variable1} variable2={variable2} />
                            </div>
                            <hr />
                            <p>Today's Total Dollar Traded: {98765}</p>
                            <hr />
                            <div className="top-10s">
                            <h3>Today's Top 10s</h3>
                            <select value={selectorValue} onChange={handleSelectorChange}>
                                <option value="a">Option A</option>
                                <option value="b">Option B</option>
                                <option value="c">Option C</option>
                                <option value="d">Option D</option>
                            </select>
                            <ul>
                                {/* Replace this with the actual data from your database */}
                                {Array.from({ length: 10 }, (_, index) => (
                                <li key={index}>Item {index + 1}</li>
                                ))}
                            </ul>
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
