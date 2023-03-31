import PlotViewer from './components/UI/PlotViewer.js'
import PlotSelector from './components/PlotSelector/PlotSelector'
import CenteredLayout from './components/UI/CenteredLayout.js'


function App() {

    const cards_available = 6;
    let cards = []
    for(let index = 0; index< cards_available; index++)
        cards.push(<PlotSelector></PlotSelector>);
    return (
      <CenteredLayout>
          <PlotViewer>
              {cards}
          </PlotViewer>
      </CenteredLayout>
      );
}

export default App;
