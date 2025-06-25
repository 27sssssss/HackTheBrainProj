import './App.css';
import Basic from './pages/Basic'
import Main from './pages/Main'
import Poligon from './pages/Poligons'
import { BrowserRouter, Route, Routes, Navigate } from 'react-router-dom';
function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Basic></Basic>}>
        </Route>
        <Route path="/asd" element={<Main></Main>}>
        </Route>
        <Route path="/polig" element={<Poligon></Poligon>}></Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
