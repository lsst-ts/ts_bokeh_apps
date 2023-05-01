import React, {useState} from 'react';
import classes from './PlotCard.module.css'

const PlotCard = (props) => {
    return (<React.Fragment>
        <div className={classes.plot_card}>{props.children}</div>
    </React.Fragment>);
}

export default PlotCard;