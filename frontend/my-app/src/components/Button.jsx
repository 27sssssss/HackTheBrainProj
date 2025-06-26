import React, { Component } from 'react';
const Basicbutton = ({children, onClick}) => {
  return (
    <div>
      <button
        style={{
          marginTop: '15px',
          width: 60,
          height: 60,
          backgroundColor: 'black',
          border: 'none',
          cursor: 'pointer',
          padding: 0
        }}
        onClick={onClick}
      >
        {children}
      </button>
    </div>
  );
};

export default Basicbutton;