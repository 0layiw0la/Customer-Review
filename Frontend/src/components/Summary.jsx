import React from "react";

const Summary = ({ subhead,content }) => {
    return(
        <div class="large-text">
            <span>
                {subhead}:              
            </span>
            <span>
                {content}
            </span>
        </div>
    )
}

export default Summary;