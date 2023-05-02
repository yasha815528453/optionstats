import React from 'react';
import './Ratiobar.css'

const RatioBar = ({ variable1, variable2 }) => {
    const total = variable1 + variable2;
    const percentageVariable1 = (variable1 / total) * 100;
    const percentageVariable2 = (variable2 / total) * 100;
  
    return (
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
    );
  };
  
  export default RatioBar;