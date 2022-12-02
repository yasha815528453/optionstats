import logo from './logo.svg';
import React, { useState, useEffect } from "react";
import './App.css';

function App() {
  
  const [optiondata, setoptiondata] = useState({
    bid: 0,
    ask: 0,
    lowest: 0,
    lel: 0,
  });
  
  useEffect(() => {
    fetch("/").then((res) =>
    res.json().then((data) => {
      setoptiondata({
        bid: data.bid,
        ask: data.ask,
        lowest: data.lowest,
        lel: data.highest,
      });
    })
    );
  })

  

  return (
    <div className="App">
      <header className="App-header">
      
      <p>the bid is {optiondata.bid}</p>
      <p>the ask is {optiondata.ask}</p>
      <p>the lowest is {optiondata.lowest}</p>
      <p>the highest is {optiondata.lel}</p>
      
      
      
      </header>
    </div>
  );
}

export default App;
