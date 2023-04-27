import React, { useState } from 'react';
import TextField from '@mui/material/TextField';
import InputAdornment from '@mui/material/InputAdornment';
import IconButton from '@mui/material/IconButton';
import SearchIcon from '@mui/icons-material/Search';
import { Typography, useTheme } from "@mui/material";
import { tokens } from "../theme";

const SearchBar = ({ onSearch }) => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    const [searchValue, setSearchValue] = useState('');

    const handleSearchChange = (event) => {
        setSearchValue(event.target.value);
    };

    const handleKeyDown = (event) => {
        if (event.key === 'Enter') {
          onSearch(searchValue);
        }
    };

    const handleSearchClick = () => {
        onSearch(searchValue);
    };

    return (
        <TextField
        value={searchValue}
        onChange={handleSearchChange}
        placeholder="ex. SPY"
        onKeyDown={handleKeyDown}
        variant="standard"
        size="small"
        label="Ticker Symbols"
        sx={{
            // Add custom styles here
            width: '16%',
            '& .MuiInputBase-input': {
                color: colors.grey[100],
            },
            '& .MuiInputLabel-formControl': {
                color: colors.grey[200],
            }
        }}
        InputProps={{

            endAdornment: (
            <InputAdornment position="end">
                <IconButton onClick={handleSearchClick} edge="end" size="small">
                <SearchIcon />
                </IconButton>
            </InputAdornment>
            ),
        }}
        />
    );
};

export default SearchBar;
