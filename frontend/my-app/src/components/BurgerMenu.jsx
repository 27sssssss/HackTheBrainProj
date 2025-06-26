import React from 'react';
const BurgerMenu = ({ open, onClick }) => {
  return (
    <div
      onClick={onClick}
      style={{
        width: 40,
        height: 24,
        cursor: 'pointer',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-between',
        zIndex: 30
      }}
    >
      <span style={{
        height: 3,
        width: '100%',
        backgroundColor: 'white',
        borderRadius: 2,
        transition: '0.3s',
        transform: open ? 'rotate(45deg) translate(7.3px, 7.3px)' : 'none'
      }} />
      <span style={{
        height: 3,
        width: '100%',
        backgroundColor: 'white',
        borderRadius: 2,
        opacity: open ? 0 : 1,
        transition: '0.3s'
      }} />
      <span style={{
        height: 3,
        width: '100%',
        backgroundColor: 'white',
        borderRadius: 2,
        transition: '0.3s',
        transform: open ? 'rotate(-45deg) translate(7.3px, -7.3px)' : 'none'
      }} />
    </div>
  );
};
export default BurgerMenu