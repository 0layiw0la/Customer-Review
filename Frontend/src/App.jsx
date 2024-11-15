import React from 'react';
import {BrowserRouter, Routes,Route} from 'react-router-dom';
import routes from './utils/routes';
import './App.css';

function App() {


  return (
    <BrowserRouter>
        <Routes>
            {routes.map((route,index)=>(
                <Route path = {route.path} element={route.element} key={index} />
            ))}
        </Routes>
    </BrowserRouter>
  )
}

export default App;
