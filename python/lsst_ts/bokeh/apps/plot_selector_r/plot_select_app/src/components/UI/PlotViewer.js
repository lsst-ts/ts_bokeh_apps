import classes from './PlotViewer.module.css';

const PlotViewer = (props) => {
    return <div className={classes.plot_viewer}>
        {props.children}
    </div>
}

export default PlotViewer;