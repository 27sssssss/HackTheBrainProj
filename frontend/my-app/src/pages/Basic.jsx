import React, { useEffect, useRef, useState } from 'react';
import Globe from 'globe.gl';

const GlobeComponent = () => {
  const globeEl = useRef(null);
  const globeInstanceRef = useRef(null);
  const [currentTexture, setCurrentTexture] = useState(0);

  const textures = [
    '//cdn.jsdelivr.net/npm/three-globe/example/img/earth-blue-marble.jpg',
    '//cdn.jsdelivr.net/npm/three-globe/example/img/earth-dark.jpg',
    '//cdn.jsdelivr.net/npm/three-globe/example/img/earth-night.jpg'
  ];

  useEffect(() => {
    if (!globeEl.current || globeInstanceRef.current) return;

    const globeInstance = Globe()(globeEl.current);

    globeInstance
      .globeImageUrl(textures[currentTexture])
      .backgroundColor('rgba(0,0,0,0)')
      .showAtmosphere(false)
      .labelLat(d => d.lat)
      .labelLng(d => d.lng)
      .labelText(() => '')
      .labelDotRadius(0.7)
      .labelColor(() => 'red')
      .labelsData([
        { lat: 55.7558, lng: 37.6173, name: "Москва" },
        { lat: 48.8566, lng: 2.3522, name: "Париж" },
        { lat: 40.7128, lng: -74.0060, name: "Нью-Йорк" },
        { lat: 35.6895, lng: 139.6917, name: "Токио" }
      ]);

    globeInstanceRef.current = globeInstance;
  }, [globeEl]);

  const handleSwitchTexture = () => {
    if (!globeInstanceRef.current) return;

    const next = (currentTexture + 1) % textures.length;
    globeInstanceRef.current.globeImageUrl(textures[next]);
    setCurrentTexture(next);
  };

  return (
    <div>
      <header>
        <nav>
          <button onClick={handleSwitchTexture}>Switch View</button>
        </nav>
        <h1>CLIMATE<br />DISASTERS</h1>
      </header>
      <div className="frame" style={{ width: '100%', height: '600px' }}>
        <div ref={globeEl} style={{ width: '100%', height: '100%' }} />
      </div>
    </div>
  );
};

export default GlobeComponent;
