import React from 'react';
import './Ratiobar.css'
import { Typography, Box, useTheme } from "@mui/material";


const RatioBar = ({ variable1, variable2 }) => {

    const total = variable1 + variable2;
    const percentageVariable1 = (variable1 / total) * 100;
    const percentageVariable2 = (variable2 / total) * 100;
    let rightside = 0;
    let leftside = 0;
    if (variable1 > variable2) {
      rightside = 1.0
      leftside = Math.round(variable1/variable2 * 10)/10;
    }
    else {
      leftside = 1.0
      rightside = Math.round(variable2/variable1 * 10)/10;
    }
    return (
      <div>
        <div className="progress-bar">
          <div
            className="progress-variable1"
            style={{ width: `${percentageVariable1}%` }}
          ></div>
          <div
            className="progress-variable2"
            style={{ width: `${percentageVariable2}%` }}
          ></div>
        </div>
        <div>
          <Typography variant="h6">
            {leftside} : {rightside}
          </Typography>
        </div>
      </div>



    );
  };

  export default RatioBar;
