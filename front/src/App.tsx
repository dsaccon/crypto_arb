import React from 'react';
import './App.css';
import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import Typography from "@material-ui/core/Typography";
import Button from "@material-ui/core/Button";
import {makeStyles} from '@material-ui/core/styles';
import {MemoryRouter as Router, Route, Switch} from 'react-router';
import {Link as RouterLink} from 'react-router-dom';
import CustomPaginationActionsTable from "./Dashboard";
import Trades from './Trades';

const useStyles = makeStyles((theme) => ({
    root: {
        flexGrow: 1,
    },
    menuButton: {
        marginRight: theme.spacing(2),
    },
    title: {
        flexGrow: 1,
    },
    buttonRoot: {
        color: '#fff',
        textDecoration: 'none',
    },
    contentContainer: {
        padding: 20,
    }
}));


function App() {
    const classes = useStyles();
    return (
        <Router>
            <AppBar position="static">
                <Toolbar>
                    <Typography variant="h6" className={classes.title}>
                        Crypto Data
                    </Typography>

                    <Button color="inherit">
                        <RouterLink to="/" className={classes.buttonRoot}>
                            Dashboard
                        </RouterLink>
                    </Button>

                    <Button color="inherit">
                        <RouterLink to="/trades" className={classes.buttonRoot}>
                            Trades
                        </RouterLink>
                    </Button>

                </Toolbar>
            </AppBar>

            <div className={classes.contentContainer}>
            <Switch>
                <Route path="/trades">
                    <Trades/>
                </Route>
                <Route path="/">
                    <CustomPaginationActionsTable/>
                </Route>
            </Switch>
            </div>

        </Router>
    );
}

export default App;
