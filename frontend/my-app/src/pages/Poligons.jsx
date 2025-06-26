import React, { useEffect, useRef, useState } from 'react';
import Globe from 'globe.gl';
import CountryGeoJson from '../assets/geojson_files/ne_110m_admin_0_countries.geojson'
import VolcanoJson from '../assets/geojson_files/volcano.json'
import WorldPolygons from '../assets/geojson_files/world_polygons_only.geojson'
import Stars from '../assets/8k_stars.jpg'
import Menu from '../assets/menu123.svg'
import Rain from '../assets/earthdisaster.svg'
import BasicButton from '../components/Button.jsx'
import Controller from '../components/Controller.jsx'
import BurgerMenu from '../components/BurgerMenu.jsx';

const disasterLocations = [
  { date: '2025-06-23T00:00:00', event_type: 'Wildfire', color: '#CC0000', severity: 'Orange', lat: 38.3927, lng: 26.1153 },
  { date: '2025-06-22T00:00:00', event_type: 'Drought', color: '#9933FF', severity: 'Orange', lat: -12.854, lng: -48.14 },
  { date: '2025-06-20T03:00:00', event_type: 'Tropical Cyclone', color: '#00CCCC', severity: 'Red', lat: 18.0, lng: -100.8 },
  { date: '2025-06-17T09:45:00', event_type: 'Volcano', color: '#FF9933', severity: 'Orange', lat: -8.542, lng: 122.775 },
  { date: '2025-06-08T13:08:06', event_type: 'Earthquake', color: '#FF3333', severity: 'Orange', lat: 4.5125, lng: -73.1444 },
];



const DisasterGlobe = () => {
  const [disastersList, setDisastersList] = useState(false);
  const toggleDisasters = () => setDisastersList(prev => !prev)

  const globeRef = useRef();

  useEffect(() => {
    const world = Globe()(globeRef.current)
      .globeImageUrl('//cdn.jsdelivr.net/npm/three-globe/example/img/earth-dark.jpg')
      .backgroundImageUrl(Stars)
      .backgroundColor('#000')
      .labelLat(d => d.lat)
      .labelLng(d => d.lng)
      .labelText(d => d.event_type)
      .labelSize(3)
      .labelDotRadius(0.7)
      .labelColor(d => d.color)
      .labelsData(disasterLocations);
      console.log("Rain:", Rain);
    fetch(CountryGeoJson)
      .then(res => res.json())
      .then(countries => {
        world
          .hexPolygonsData(countries.features)
          .hexPolygonResolution(3)
          .hexPolygonMargin(0.3)
          .hexPolygonUseDots(true)
          .hexPolygonColor(() => '#444');
      })
      .catch(err => console.error("GeoJSON load error:", err));
  }, []);

  return (
    <div className="frame" style={{ width: '100%', height: '100vh', position:'relative' }}>
      <div
        style={{
          width:'300px',
          position: 'absolute',
          top: '40px',
          left: '90%',
          transform: 'translateX(-50%)',
          color: 'white',
          fontSize: '3rem',
          fontWeight: 'bold',
          zIndex: 10,
          display:'flex',
          flexDirection:'column',
          justifyContent:'space-evenly',
        }}
    >
    <div style={{display:'flex', flexDirection:'row', justifyContent:'space-evenly', alignItems:'center'}}>
      <BasicButton>
        <img
        src={Rain}
        alt="Rain icon"
        style={{ width: '100%', height: '100%' }}
      />
      </BasicButton>
      <BurgerMenu open={disastersList} onClick={toggleDisasters} />
      </div>
      <div
        style={{
          transition: 'opacity 0.3s ease, transform 0.3s ease',
          opacity: disastersList ? 1 : 0,
          transform: disastersList ? 'translateY(0)' : 'translateY(-20px)',
          pointerEvents: disastersList ? 'auto' : 'none' // чтобы не кликался в скрытом виде
        }}
      >
    <Controller />
</div>
    </div>
      <div ref={globeRef} style={{ width: '100%', height: '100%' }} />
    </div>
  );
};

export default DisasterGlobe;
