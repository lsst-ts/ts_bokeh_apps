
import classes from './PlotSelector.module.css'
import PlotCard from "../UI/PlotCard";


const PlotSelector = (props) => {
    return (
        <PlotCard>
            <div className={classes.plus}></div>
        </PlotCard>
    );
}

export default PlotSelector;