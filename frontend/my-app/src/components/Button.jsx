import React, { Component } from 'react';
const Basicbutton = ({children}) => {
  return (
    <div>
      <button
        style={{
          width: 60,
          height: 60,
          backgroundColor: 'black',
          border: 'none',
          cursor: 'pointer',
          padding: 0
        }}
      >
        {children}
      </button>
    </div>
  );
};

export default Basicbutton;