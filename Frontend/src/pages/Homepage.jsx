import React from 'react';
import Header from '../components/Header';
import './Homepage.css';

function HomePage(){
    return(
        <div class="wrapper">
            <Header headertext="Should you go?"/>
                <form className="homepage-flex">
                    <input type ="text" placeholder="Business Name" />
                    <input type ="text" placeholder="Location" />
                    <button type='submit'>Submit</button>
                </form>
        </div>
    )
}

export default HomePage;