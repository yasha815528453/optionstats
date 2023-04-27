import { useState } from "react";
import ReactECharts from 'echarts-for-react';
import React from 'react';
import SearchBar from '../../components/searchbar';

const Countrymap = () => {
    const handleSearch = (searchValue) => {
        console.log('Search value:', searchValue);
        // Implement your search logic here
      };

      return (
        <div>
          <h1>React MUI Search Bar Example</h1>
          <SearchBar onSearch={handleSearch} />
          {/* Other components */}
        </div>
      );
}

export default Countrymap;
