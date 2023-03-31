import React, {useState} from 'react';
import classes from "./CenteredLayout.module.css"

const CenteredLayout = (props) => {
    return (
        <React.Fragment>
            <div className={classes.outerdiv}>
                <div className={classes.innerdiv}>
                    {props.children}
                </div>
            </div>
        </React.Fragment>
    )
}

export default CenteredLayout;