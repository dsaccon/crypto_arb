import React, {useEffect, useRef} from 'react';
import {makeStyles} from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TablePagination from '@material-ui/core/TablePagination';
import TableRow from '@material-ui/core/TableRow';
import {FormControl} from "@material-ui/core";
import InputLabel from "@material-ui/core/InputLabel";
import Select from "@material-ui/core/Select";
import MenuItem from "@material-ui/core/MenuItem";
import Typography from "@material-ui/core/Typography";
import TextField from "@material-ui/core/TextField";
import Slider from "@material-ui/core/Slider";
import {allExchanges, formatTimestamp, serverHost} from "./utils";

interface Column {
    id: string;
    label: string;
    minWidth?: number;
    align?: 'right';
    format?: (value: number) => string;
    className?: any;
}

const getColumns: (classes: any) => Column[] = (classes) => ([
    {id: 'timestamp', label: 'Date', minWidth: 170, format: formatTimestamp},
    {id: 'exchange', label: 'Exchange', minWidth: 100},
    {id: 'pair', label: 'Currency Pair', minWidth: 100},
    {id: 'price', label: 'Price', minWidth: 100},
    {id: 'amount', label: 'Volume', minWidth: 100},
    {id: 'side', label: 'Type', minWidth: 100,
        className: (value: string) => value === 'sell' ? classes.red : classes.green},
]);


const useStyles = makeStyles({
    root: {
        width: '100%',
    },
    container: {
        // maxHeight: 440,
    },
    filterContainer: {
        display: 'flex',
        flexDirection: 'row',
    },
    filter: {
        display: 'flex',
        marginLeft: 20,
        justifyContent: 'space-between',
        paddingBottom: 20,
        flex: 1,
    },
    red: {
        color: 'red',
    },
    green: {
        color: 'green',
    },
    select: {
        width: 85,
    },
    slider: {
        width: 150,
        textAlign: 'center',
    },
    input: {
        width: 85,
    },
});

const initialVisibleColumns = ['timestamp', 'exchange', 'pair', 'price', 'amount', 'side'];
const allPriceCurrencies = ['BCH', 'BNB', 'BSV', 'BTC', 'CNY', 'EOS', 'ETH', 'EUR', 'JPY', 'LTC', 'USD', 'USDT',
    'XRP', 'XTZ'];
const refreshInterval = 1000;

const loadData = (options: any, onSuccess: (response: any) => any) => {
    fetch(serverHost + 'trades', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(options)
    })
        .then(response => response.json())
        .then((resp) => {
            onSuccess(resp);
        })
        .catch(console.log);
}

function useInterval(callback: any, delay: number) {
    const savedCallback: any = useRef();

    // Remember the latest callback.
    useEffect(() => {
        savedCallback.current = callback;
    }, [callback]);

    // Set up the interval.
    useEffect(() => {
        function tick() {
            savedCallback.current();
        }

        if (delay !== null) {
            let id = setInterval(tick, delay);
            return () => clearInterval(id);
        }
    }, [delay]);
}

const MIN_PRICE = 0, MAX_PRICE = 8000, MIN_VOLUME = 0, MAX_VOLUME = 500;
const TRADE_TYPES = ['all', 'buy', 'sell'];

const padNumber = (n: number) => {
    return n > 9 ? n : '0' + n;
}

const formatTs = (ts: number) => {
    let d = new Date(ts);
    const date = `${d.getFullYear()}-${padNumber(d.getMonth()+1)}-${padNumber(d.getDate())}`;
    const time = `T${padNumber(d.getHours())}:${padNumber(d.getMinutes())}`;
    return date + time;
}

export default function Trades() {
    const classes = useStyles();
    const columns = getColumns(classes);
    const [page, setPage] = React.useState(0);
    const [rowsPerPage, setRowsPerPage] = React.useState(10);
    const [visibleColumnIds, setVisibleColumnIds] = React.useState(initialVisibleColumns);
    const [selectedExchanges, setSelectedExchanges] = React.useState(['COINBASE']);
    const [baseCurrency, setBaseCurrency] = React.useState(['BTC']);
    const [quoteCurrency, setQuoteCurrency] = React.useState(['USD']);
    const [rows, setRows] = React.useState([]);
    const [priceRange, setPriceRange] = React.useState<number[]>([MIN_PRICE, MAX_PRICE]);
    const [minPrice, setMinPrice] = React.useState<number | null>(null);
    const [maxPrice, setMaxPrice] = React.useState<number | null>(null);
    const [minAmount, setMinAmount] = React.useState<number | null>(null);
    const [maxAmount, setMaxAmount] = React.useState<number | null>(null);
    const [volumeRange, setVolumeRange] = React.useState<number[]>([MIN_VOLUME, MAX_VOLUME]);
    const [fromTs, setFromTs] = React.useState(null);
    const [toTs, setToTs] = React.useState(null);
    const [side, setSide] = React.useState(TRADE_TYPES[0]);

    useEffect(() => loadData(
        {
            exchanges: selectedExchanges,
            currencies1: baseCurrency,
            currencies2: quoteCurrency,
            fromTs: fromTs,
            toTs : toTs,
            minPrice,
            maxPrice,
            minAmount,
            maxAmount,
            side,
        },
        (rows) => setRows(rows),
    ), []);
    useInterval(() => loadData(
        {
            exchanges: selectedExchanges,
            currencies1: baseCurrency,
            currencies2: quoteCurrency,
            fromTs,
            toTs,
            minPrice,
            maxPrice,
            minAmount,
            maxAmount,
            side,
        },
        (rows) => setRows(rows),
    ), refreshInterval);

    const handleChangePage = (event: unknown, newPage: number) => {
        setPage(newPage);
    };

    const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
        setRowsPerPage(+event.target.value);
        setPage(0);
    };

    const handleChangeVisibleColumns = (event: React.ChangeEvent<{ value: unknown }>) => {
        setVisibleColumnIds(event.target.value as any);
    };

    const handleChangeExchanges = (event: React.ChangeEvent<{ value: unknown }>) => {
        setSelectedExchanges(event.target.value as any);
    };

    const handleChangeSide = (event: React.ChangeEvent<{ value: unknown }>) => {
        setSide(event.target.value as any);
    };

    const handleBaseCurrencyChange = (event: React.ChangeEvent<{ value: unknown }>) => {
        setBaseCurrency(event.target.value as any);
    };

    const handleQuoteCurrencyChange = (event: React.ChangeEvent<{ value: unknown }>) => {
        setQuoteCurrency(event.target.value as any);
    };

    const handlePriceRangeChange = (event: any, newValue: number | number[]) => {
        setPriceRange(newValue as number[]);
    };

    const handleMinPriceChange = (event: any) => {
        setMinPrice(event.target.value);
    };

    const handleMaxPriceChange = (event: any) => {
        setMaxPrice(event.target.value);
    };

    const handleMinAmountChange = (event: any) => {
        setMinAmount(event.target.value);
    };

    const handleMaxAmountChange = (event: any) => {
        setMaxAmount(event.target.value);
    };

    const handleVolumeRangeChange = (event: any, newValue: number | number[]) => {
        setVolumeRange(newValue as number[]);
    };

    const handleFromTsChange = (event: React.ChangeEvent<HTMLTextAreaElement | HTMLInputElement>) => {
        // @ts-ignore
        setFromTs(event.target.valueAsNumber / 1000 + new Date().getTimezoneOffset() * 60);
    }

    const handleToTsChange = (event: React.ChangeEvent<HTMLTextAreaElement | HTMLInputElement>) => {
        // @ts-ignore
        setToTs(event.target.valueAsNumber / 1000 + new Date().getTimezoneOffset() * 60);
    }

    const visibleColumns = columns.filter(column => visibleColumnIds.indexOf(column.id) > -1);

    return (
        <>
            <div className={classes.filterContainer}>
                <Typography variant="h4">
                    Trades
                </Typography>
                <div className={classes.filter}>

                    <FormControl>
                        <InputLabel id="exchanges">Exchanges</InputLabel>
                        <Select
                            labelId="exchanges"
                            id="exchanges"
                            value={selectedExchanges}
                            onChange={handleChangeExchanges}
                            multiple
                        >
                            {allExchanges.map((exchange) => (
                                <MenuItem key={exchange} value={exchange}>{exchange}</MenuItem>
                            ))}
                        </Select>
                    </FormControl>

                    <FormControl>
                        <InputLabel id="baseCurrency">BaseCurrency</InputLabel>
                        <Select
                            labelId="baseCurrency"
                            id="baseCurrency"
                            value={baseCurrency}
                            onChange={handleBaseCurrencyChange}
                            multiple
                            className={classes.select}
                        >
                            {allPriceCurrencies.map((currency) => (
                                <MenuItem key={currency} value={currency}>{currency}</MenuItem>
                            ))}
                        </Select>
                    </FormControl>

                    <FormControl>
                        <InputLabel id="quoteCurrency">QuoteCurrency</InputLabel>
                        <Select
                            labelId="quoteCurrency"
                            id="quoteCurrency"
                            value={quoteCurrency}
                            onChange={handleQuoteCurrencyChange}
                            multiple
                            className={classes.select}
                        >
                            {allPriceCurrencies.map((currency) => (
                                <MenuItem key={currency} value={currency}>{currency}</MenuItem>
                            ))}
                        </Select>
                    </FormControl>

                    <FormControl>
                        <InputLabel id="side">Side</InputLabel>
                        <Select
                            labelId="side"
                            id="side"
                            value={side}
                            onChange={handleChangeSide}
                            className={classes.select}
                        >
                            {TRADE_TYPES.map((side) => (
                                <MenuItem key={side} value={side}>{side}</MenuItem>
                            ))}
                        </Select>
                    </FormControl>

                    <TextField
                        id="datetime-local"
                        label="From"
                        type="datetime-local"
                        onChange={handleFromTsChange}
                        defaultValue={formatTs(new Date() as any - 3600000)}
                        InputLabelProps={{
                            shrink: true,
                        }}
                    />

                    <TextField
                        id="datetime-local"
                        label="To"
                        type="datetime-local"
                        onChange={handleToTsChange}
                        defaultValue={formatTs(new Date() as any + 0)}
                        InputLabelProps={{
                            shrink: true,
                        }}
                    />

                    <TextField
                        id="min-price"
                        label="Price From"
                        onChange={handleMinPriceChange}
                        className={classes.input}
                        InputLabelProps={{
                            shrink: true,
                        }}
                    />

                    <TextField
                        id="max-price"
                        label="To"
                        onChange={handleMaxPriceChange}
                        className={classes.input}
                        InputLabelProps={{
                            shrink: true,
                        }}
                    />

                    <TextField
                        id="min-amount"
                        label="Vol From"
                        onChange={handleMinAmountChange}
                        className={classes.input}
                        InputLabelProps={{
                            shrink: true,
                        }}
                    />

                    <TextField
                        id="max-amount"
                        label="To"
                        onChange={handleMaxAmountChange}
                        className={classes.input}
                        InputLabelProps={{
                            shrink: true,
                        }}
                    />

                    {false && <div className={classes.slider}>
                        <Typography id="discrete-slider-custom" gutterBottom>
                            Price
                        </Typography>
                        <Slider
                            value={priceRange}
                            onChange={handlePriceRangeChange}
                            aria-labelledby="discrete-slider-custom"
                            min={MIN_PRICE}
                            step={10}
                            max={MAX_PRICE}
                            valueLabelDisplay="on"
                            marks={[{
                                value: MIN_PRICE,
                                label: MIN_PRICE,
                            }, {
                                value: MAX_PRICE,
                                label: MAX_PRICE,
                            },]}
                        />
                    </div>}

                    {false && <div className={classes.slider}>
                        <Typography id="discrete-slider-custom" gutterBottom>
                            Volume
                        </Typography>
                        <Slider
                            value={volumeRange}
                            onChange={handleVolumeRangeChange}
                            aria-labelledby="discrete-slider-custom"
                            min={MIN_VOLUME}
                            step={10}
                            max={MAX_VOLUME}
                            valueLabelDisplay="on"
                            marks={[{
                                value: MIN_VOLUME,
                                label: MIN_VOLUME,
                            }, {
                                value: MAX_VOLUME,
                                label: MAX_VOLUME,
                            },]}
                        />
                    </div>}

                </div>
            </div>

            <Paper elevation={3} className={classes.root}>
                <TableContainer className={classes.container}>
                    <Table stickyHeader aria-label="sticky table">
                        <TableHead>
                            <TableRow>
                                {visibleColumns.map((column) => (
                                    <TableCell
                                        key={column.id}
                                        align={column.align}
                                        style={{minWidth: column.minWidth}}
                                    >
                                        {column.label}
                                    </TableCell>
                                ))}
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {rows.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage).map((row, index) => {
                                return (
                                    <TableRow hover role="checkbox" tabIndex={-1} key={index}>
                                        {visibleColumns.map((column) => {
                                            // @ts-ignore
                                            const value = row[column.id];
                                            return (
                                                <TableCell
                                                    key={column.id}
                                                    align={column.align}
                                                    className={column.className && column.className(value)}
                                                >
                                                    {column.format && typeof value === 'number' ? column.format(value) : value}
                                                </TableCell>
                                            );
                                        })}
                                    </TableRow>
                                );
                            })}
                        </TableBody>
                    </Table>
                </TableContainer>
                <TablePagination
                    rowsPerPageOptions={[10, 25, 100]}
                    component="div"
                    count={rows.length}
                    rowsPerPage={rowsPerPage}
                    page={page}
                    onChangePage={handleChangePage}
                    onChangeRowsPerPage={handleChangeRowsPerPage}
                />
            </Paper>
        </>
    );
}
