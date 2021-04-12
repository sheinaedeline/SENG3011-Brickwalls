import './styles/App.css';
import {
    BrowserRouter as Router,
    Switch,
    Route,
} from "react-router-dom";
import Login from "./pages/Login.js"
import Main from "./pages/Main.js"

function App() {
  return (
    <div className="App">
        <Router>
            <Switch>
                <Route exact path="/">
                    <Login></Login>
                </Route>
                <Route path="/main">
                    <Main></Main>
                </Route>
            </Switch>
        </Router>
        
    </div>
  );
}

export default App;
