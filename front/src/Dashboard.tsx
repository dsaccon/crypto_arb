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
import {FormControl, TableSortLabel} from "@material-ui/core";
import InputLabel from "@material-ui/core/InputLabel";
import Select from "@material-ui/core/Select";
import MenuItem from "@material-ui/core/MenuItem";
import Typography from "@material-ui/core/Typography";
import BCH from './assets/BCH.png';
import BNB from './assets/BNB.png';
import BSV from './assets/BSV.png';
import BTC from './assets/BTC.png';
import EOS from './assets/EOS.png';
import ETH from './assets/ETH.png';
import LTC from './assets/LTC.png';
import USDT from './assets/USDT.png';
import XRP from './assets/XRP.png';
import XTZ from './assets/XTZ.png';
import {allExchanges, serverHost} from './utils';
import {coinImages} from "./coinImages";

interface Column {
    id: string;
    label: string;
    minWidth?: number;
    align?: 'right';
    format?: (value: any) => any;
    className?: any;
}

const granularities = ['1s', '5s', '10s', '30s', '1mi', '2mi', '5mi', '10mi', '15mi', '30mi', '1h', '2h', '4h',
    '12h', '1d', '3d', '1w', '2w', '1mo', '3mo', '6mo', '1y'];

const logos = {
    BCH,
    BNB,
    BSV,
    BTC,
    // CNY,
    EOS,
    ETH,
    // EUR,
    // JPY,
    LTC,
    // USD,
    USDT,
    XRP,
    XTZ,
}

const getSymbol = (ccy: string, coinPriceLogoClass: any) => {
    switch (ccy) {
        case 'btc':
            return '₿ ';
        case 'usd':
            return '$ ';
        case 'gbp':
            return '£ ';
        case 'eur':
            return '€ ';
        case 'eth':
            return 'Ξ ';
        case 'jpy':
            return '¥ ';
        case 'cny':
            return '¥ ';
        case 'usdt':
            return '₮ ';
        default:
            return (
                <img
                    // @ts-ignore
                    src={coinImages[ccy]}
                    className={coinPriceLogoClass}
                    alt={'logo'}
                />
            )

    }
}

const getColumns: (classes: any, priceCurrencyLocal: string) => Column[] = (classes, priceCurrencyLocal) => ([
    {
        id: 'coin',
        label: 'Coin',
        minWidth: 170,
        format: (coin) => (
            <>
                <img
                    // @ts-ignore
                    src={coinImages[coin.toLowerCase()]}
                    className={classes.coinLogo}
                    alt={'logo'}
                />
                {coin}
            </>
        ),
        className: () => classes.coin,
    },
    {
        id: 'price',
        label: 'Price',
        minWidth: 145,
        format: (value: number) => {
            return (
                <>
                    {getSymbol(priceCurrencyLocal.toLowerCase(), classes.coinPriceLogo)}
                    {!!value ? value.toFixed(value > 100 ? 2 : (value < 1 ? 6 : 4)) : 0}
                </>
            );
        },
        className: (value: number, prevValue: number) => {
            console.log(value, prevValue);
            return (value < prevValue ? classes.red : classes.green);
        },
    },
    ...granularities.map(granularity => ({
        id: 'price_' + granularity,
        label: 'Price % ' + granularity,
        format: (value: number) => value && ((100 * value).toFixed(2) + '%'),
        className: (value: number) => value < 0 ? classes.red : classes.green,
    })),
    ...granularities.map(granularity => ({
        id: 'volume_' + granularity,
        label: 'Volume % ' + granularity,
        format: (value: number) => value && (100 * value).toFixed(1) + '%',
        className: (value: number) => value < 0 ? classes.red : classes.green,
    })),
]);

const useStyles = makeStyles({
    root: {
        width: '100%',
    },
    container: {
        // maxHeight: 440,
        '-ms-overflow-style': 'none',
        '&::-webkit-scrollbar': {
            display: 'none',
        }
    },
    filterContainer: {
        display: 'flex',
        flexDirection: 'row',
    },
    filter: {
        display: 'flex',
        marginLeft: 'auto',
        justifyContent: 'space-between',
        paddingBottom: 20,
        width: 500,
    },
    red: {
        color: 'red',
        animation: `$fadeOutRed 1000ms ease-out`,
    },
    green: {
        color: 'green',
        animation: `$fadeOutGreen 1000ms ease-out`,
    },
    coin: {
        display: 'flex',
    },
    coinLogo: {
        height: 20,
        marginRight: 10,
    },
    coinPriceLogo: {
        height: 20,
        marginBottomm: -5,
    },
    '@keyframes fadeOutRed': {
        from: {
            backgroundColor: "rgba(100,100,100,0.3)",
        },
        to: {
            backgroundColor: 'white'
        }
    },
    '@keyframes fadeOutGreen': {
        from: {
            backgroundColor: "rgba(100,100,100,0.3)",
        },
        to: {
            backgroundColor: 'white'
        }
    }
});

const initialVisibleColumns = ['coin', 'price', 'price_30s', 'price_1mi', 'price_2mi', 'price_5mi', 'price_10mi',
    'price_1h', 'price_1d'];

const allPriceCurrencies = ['BCH', 'BNB', 'BSV', 'BTC', 'CNY', 'EOS', 'ETH', 'EUR', 'JPY', 'LTC', 'USD', 'USDT',
    'XRP', 'XTZ'];
const refreshInterval = 1000;

let isLoading = false;

const loadData = (options: any, onSuccess: (response: any) => any) => {
    if (isLoading) {
        return;
    }
    isLoading = true;
    fetch(serverHost + 'dashboard', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(options)
    })
        .then(response => response.json())
        .then((resp) => {
            isLoading = false;
            onSuccess(resp.sort((a: any, b: any) => (a.coin > b.coin) ? 1 : ((b.coin > a.coin) ? -1 : 0)));
        })
        .catch(err => {
            isLoading = false;
            console.log(err);
        });
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

const ORDER_ASC = 'asc', ORDER_DESC = 'desc';

export default function Dashboard() {
    const classes = useStyles();
    const [page, setPage] = React.useState(0);
    const [rowsPerPage, setRowsPerPage] = React.useState(10);
    const [visibleColumnIds, setVisibleColumnIds] = React.useState(initialVisibleColumns);
    const [selectedExchanges, setSelectedExchanges] = React.useState(['COINBASE']);
    const [priceCurrency, setPriceCurrency] = React.useState('USD');
    const [rows, setRows] = React.useState([]);
    const [orderBy, setOrderBy] = React.useState('coin');
    const [order, setOrder] = React.useState<'asc' | 'desc' | undefined>('asc');
    const orderByRef = useRef(orderBy);
    const orderRef = useRef(order);
    const columns = getColumns(classes, priceCurrency);
    const prevRowValuesRef = useRef({});
    const lastChangedValuesRef = useRef<any>({});
    for (let row of rows) {
        // @ts-ignore
        if (prevRowValuesRef.current[row.coin] !== row.price) {
            // @ts-ignore
            lastChangedValuesRef.current[row.coin] = prevRowValuesRef.current[row.coin];
        }
        // @ts-ignore
        prevRowValuesRef.current[row.coin] = row.price
    }


    // @ts-ignore
    const rowsWithImage = rows.filter(row => !!coinImages[row.coin.toLowerCase()]).sort((a: any, b: any) => {
        const orderSign = order === ORDER_DESC ? -1 : 1;
        return orderSign * (a[orderBy] < b[orderBy] ? -1 : (a[orderBy] === b[orderBy] ? 0 : 1));
    });

    const handleSortClick = (column: any) => (event: any) => {
        if (orderByRef.current === column) {
            const newOrder = orderRef.current === ORDER_ASC ? ORDER_DESC : ORDER_ASC
            setOrder(newOrder);
            orderRef.current = newOrder;
        } else {
            setOrderBy(column);
            setOrder(ORDER_ASC);
        }
        orderByRef.current = column;
    }

    useEffect(() => loadData(
        {visibleColumns: visibleColumnIds, exchanges: selectedExchanges, priceCurrency},
        (rows) => setRows(rows),
    ), []);
    useInterval(() => loadData(
        {visibleColumns: visibleColumnIds, exchanges: selectedExchanges, priceCurrency},
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

    const handlePriceCurrencyChange = (event: React.ChangeEvent<{ value: unknown }>) => {
        setPriceCurrency(event.target.value as any);
    };

    const visibleColumns = columns.filter(column => visibleColumnIds.indexOf(column.id) > -1);


    return (
        <>
            <div className={classes.filterContainer}>
                <Typography variant="h4">
                    Dashboard
                </Typography>
                <div className={classes.filter}>
                    <FormControl>
                        <InputLabel id="columns">VisibleColumns</InputLabel>
                        <Select
                            labelId="columns"
                            id="columns"
                            value={visibleColumnIds}
                            onChange={handleChangeVisibleColumns}
                            multiple
                            renderValue={() => 'Visible Columns'}
                        >
                            {columns.map((column) => (
                                <MenuItem value={column.id}>{column.label}</MenuItem>
                            ))}
                        </Select>
                    </FormControl>

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
                                <MenuItem value={exchange}>{exchange}</MenuItem>
                            ))}
                        </Select>
                    </FormControl>

                    <FormControl>
                        <InputLabel id="priceCurrency">Price</InputLabel>
                        <Select
                            labelId="priceCurrency"
                            id="priceCurrency"
                            value={priceCurrency}
                            onChange={handlePriceCurrencyChange}
                        >
                            {allPriceCurrencies.map((priceCurrency) => (
                                <MenuItem value={priceCurrency}>{priceCurrency}</MenuItem>
                            ))}
                        </Select>
                    </FormControl>
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
                                        <TableSortLabel
                                            active={orderBy === column.id}
                                            direction={orderBy === column.id ? order : 'asc'}
                                            onClick={handleSortClick(column.id)}
                                        >
                                            {column.label}
                                        </TableSortLabel>
                                    </TableCell>
                                ))}
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {rowsWithImage.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage).map((row) => {
                                const coin = (row as any).coin;
                                // @ts-ignore
                                const prevPrice = lastChangedValuesRef.current[coin];
                                return (coinImages as any)[coin.toLowerCase()] === null
                                    ? null
                                    : (
                                        <TableRow hover role="checkbox" tabIndex={-1} key={coin}>
                                            {visibleColumns.map((column) => {
                                                // @ts-ignore
                                                const value = row[column.id];

                                                return (
                                                    <TableCell
                                                        key={column.id}
                                                        align={column.align}
                                                        className={column.className && column.className(value, prevPrice)}
                                                    >
                                                        {column.format ? column.format(value) : value}
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
                    count={rowsWithImage.length}
                    rowsPerPage={rowsPerPage}
                    page={page}
                    onChangePage={handleChangePage}
                    onChangeRowsPerPage={handleChangeRowsPerPage}
                />
            </Paper>
        </>
    );
}
