import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';

const disasters = [
  { lat: 38, lng: -120, name: "California Wildfires", year: 2022 },
  { lat: 10, lng: -70, name: "Venezuela Floods", year: 2021 },
  { lat: 15, lng: 20, name: "Sahel Drought", year: 2023 },
  { lat: -30, lng: 35, name: "South Africa Heatwave", year: 2022 },
  { lat: 0, lng: -20, name: "Atlantic Hurricanes", year: 2023 }
];

const EarthScene = () => {
  const containerRef = useRef();
  const labelContainerRef = useRef();

  useEffect(() => {
    let camera, scene, renderer, globe, controls;
    let spaceSphere = null;
    const markerMeshes = [];
    const labelElements = [];

    // INIT
    camera = new THREE.PerspectiveCamera(25, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(4.5, 2, 3);

    scene = new THREE.Scene();

    const sun = new THREE.DirectionalLight(0xffffff, 2);
    sun.position.set(0, 0, 3);
    scene.add(sun);

    scene.add(new THREE.AmbientLight(0x404040));

    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    containerRef.current.appendChild(renderer.domElement);

    controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.minDistance = 1.5;
    controls.maxDistance = 10;

    // Load textures
    const loader = new THREE.TextureLoader();
    const dayTex = loader.load('https://cdn.jsdelivr.net/npm/three-globe/example/img/earth-blue-marble.jpg');
    const nightTex = loader.load('https://cdn.jsdelivr.net/npm/three-globe/example/img/earth-night.jpg');
    const bumpTex = loader.load('https://cdn.jsdelivr.net/npm/three-globe/example/img/earth-topology.png');
    const spaceTex = loader.load('https://cdn.jsdelivr.net/npm/three-globe/example/img/night-sky.png', texture => {
      createSpace(texture);
      createEarth();
      createMarkers();
      animate();
    });

    function createSpace(texture) {
      const geometry = new THREE.SphereGeometry(1000, 60, 60);
      const material = new THREE.MeshBasicMaterial({ map: texture, side: THREE.BackSide });
      spaceSphere = new THREE.Mesh(geometry, material);
      scene.add(spaceSphere);
    }

    function createEarth() {
      const material = new THREE.MeshStandardMaterial({
        map: dayTex,
        bumpMap: bumpTex,
        bumpScale: 0.05,
        metalness: 0.1,
        roughness: 0.7
      });
      const geometry = new THREE.SphereGeometry(1, 64, 64);
      globe = new THREE.Mesh(geometry, material);
      scene.add(globe);
    }

    function createMarkers() {
      disasters.forEach(disaster => {
        const phi = (90 - disaster.lat) * (Math.PI / 180);
        const theta = (disaster.lng + 180) * (Math.PI / 180);
        const r = 1.02;

        const x = -Math.sin(phi) * Math.cos(theta) * r;
        const y = Math.cos(phi) * r;
        const z = Math.sin(phi) * Math.sin(theta) * r;

        const markerGeo = new THREE.SphereGeometry(0.03, 16, 16);
        const markerMat = new THREE.MeshBasicMaterial({ color: 0xff0000 });
        const marker = new THREE.Mesh(markerGeo, markerMat);
        marker.position.set(x, y, z);
        scene.add(marker);
        markerMeshes.push(marker);

        // HTML label
        const label = document.createElement('div');
        label.className = 'disaster-label';
        label.textContent = `${disaster.name} (${disaster.year})`;
        label.style.position = 'absolute';
        label.style.color = 'red';
        label.style.fontSize = '14px';
        labelContainerRef.current.appendChild(label);
        labelElements.push({ label, marker });
      });
    }

    function updateLabels() {
      const vector = new THREE.Vector3();
      labelElements.forEach(({ label, marker }) => {
        vector.copy(marker.position).project(camera);
        const x = (vector.x * 0.5 + 0.5) * window.innerWidth;
        const y = (-(vector.y * 0.5) + 0.5) * window.innerHeight;
        label.style.transform = `translate(${x}px, ${y}px)`;
        label.style.display = vector.z > 1 ? 'none' : 'block';
      });
    }

    function animate() {
      requestAnimationFrame(animate);
      controls.update();
      updateLabels();
      if (spaceSphere) spaceSphere.position.copy(camera.position);
      renderer.render(scene, camera);
    }

    function onResize() {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    }

    window.addEventListener('resize', onResize);
    return () => {
      window.removeEventListener('resize', onResize);
      renderer.dispose();
    };
  }, []);

  return (
    <>
      <div ref={containerRef} style={{ width: '100%', height: '100vh', position: 'relative' }} />
      <div ref={labelContainerRef} style={{ position: 'absolute', top: 0, left: 0, pointerEvents: 'none' }} />
    </>
  );
};

export default EarthScene;
