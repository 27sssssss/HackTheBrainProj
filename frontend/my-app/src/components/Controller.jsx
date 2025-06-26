import React, { useState } from 'react';
import AvalancheIcon from '../assets/Avalanche.svg';
import DroughtIcon from '../assets/drought.svg';
import EarthquakeIcon from '../assets/Earthquake.svg';
import FloodIcon from '../assets/Flood.svg';
import ForestFireIcon from '../assets/ForestFire.svg';
import HurricaneIcon from '../assets/Hurricane.svg';
import TornadoIcon from '../assets/Tornado.svg';
import TsunamiIcon from '../assets/Tsunami.svg';
import VolcanoIcon from '../assets/Volcano.svg';


const initialDisasters = [
  { id: 'hurricanes', name: 'Hurricanes', icon: HurricaneIcon, active: true },
  { id: 'tsunamis', name: 'Tsunamis', icon: TsunamiIcon, active: true },
  { id: 'volcanoes', name: 'Volcanic Eruptions', icon: '', active: false },
  { id: 'floods', name: 'Floods', icon: '', active: true },
  { id: 'wildfires', name: 'Wildfires', icon: '', active: true },
  { id: 'droughts', name: 'Droughts', icon: '', active: true },
  { id: 'avalanches', name: 'Avalanches', icon: '', active: false },
  { id: 'tornadoes', name: 'Tornadoes', icon: '', active: false },
  { id: 'earthquakes', name: 'Earthquakes', icon: '', active: false },
];

const DisasterToolbar = ({ onToggle }) => {
  const [disasters, setDisasters] = useState(initialDisasters);

  const handleToggle = (id) => {
    const updated = disasters.map(d =>
      d.id === id ? { ...d, active: !d.active } : d
    );
    setDisasters(updated);
    onToggle?.(updated);
  };

  return (
    <div
      style={{
        position: 'absolute',
        top: 40,
        left: 40,
        padding: 20,
        borderRadius: 20,
        backgroundColor: 'rgba(255,255,255,0.06)',
        backdropFilter: 'blur(10px)',
        border: '1px solid rgba(255,255,255,0.2)',
        display: 'flex',
        flexDirection: 'column',
        gap: 12,
        zIndex: 20,
      }}
    >
      {disasters.map((disaster) => (
        <div
          key={disaster.id}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: 12,
            color: 'white',
            fontSize: 14,
            fontFamily: 'Open Sans, sans-serif'
          }}
        >
          {/* Toggle */}
          <label style={{ position: 'relative', width: 38, height: 20, display: 'inline-block' }}>
            <input
              type="checkbox"
              checked={disaster.active}
              onChange={() => handleToggle(disaster.id)}
              style={{
                opacity: 0,
                width: 0,
                height: 0
              }}
            />
            <span
              style={{
                position: 'absolute',
                top: 0,
                left: 0,
                right: 0,
                bottom: 0,
                backgroundColor: disaster.active ? '#2ecc71' : '#ccc',
                borderRadius: 20,
                transition: '0.3s'
              }}
            />
            <span
              style={{
                position: 'absolute',
                content: '""',
                height: 16,
                width: 16,
                left: disaster.active ? 20 : 2,
                bottom: 2,
                backgroundColor: 'white',
                borderRadius: '50%',
                transition: '0.3s'
              }}
            />
          </label>

          {/* Icon */}
          {disaster.icon && (
            <img
              src={disaster.icon}
              alt=""
              style={{
                width: 20,
                height: 20,
                filter: 'invert(1)'
              }}
            />
          )}

          {/* Label */}
          <span style={{ whiteSpace: 'nowrap' }}>{disaster.name}</span>
        </div>
      ))}
    </div>
  );
};

export default DisasterToolbar;
