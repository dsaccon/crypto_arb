import requests

host, db, redis_host = 'http://localhost:8086', 'crypto', '127.0.0.1'

BITFINEX = ['BTC-USD', 'LTC-USD', 'LTC-BTC', 'ETH-USD', 'ETH-BTC', 'ETC-BTC', 'ETC-USD', 'RRT-USD', 'ZEC-USD',
            'ZEC-BTC', 'XMR-USD', 'XMR-BTC', 'DASH-USD', 'DASH-BTC', 'BTC-EUR', 'BTC-JPY', 'XRP-USD', 'XRP-BTC',
            'IOTA-USD', 'IOTA-BTC', 'IOTA-ETH', 'EOS-USD', 'EOS-BTC', 'EOS-ETH', 'SAN-USD', 'SAN-BTC', 'SAN-ETH',
            'OMG-USD', 'OMG-BTC', 'OMG-ETH', 'NEO-USD', 'NEO-BTC', 'NEO-ETH', 'ETP-USD', 'ETP-BTC', 'ETP-ETH',
            'QTUM-USD', 'QTUM-BTC', 'AVT-USD', 'EDO-USD', 'EDO-BTC', 'EDO-ETH', 'BTG-USD', 'BTG-BTC', 'DATA-USD',
            'DATA-BTC', 'DATA-ETH', 'QASH-USD', 'YYW-USD', 'GNT-USD', 'GNT-BTC', 'GNT-ETH', 'SNT-USD', 'SNT-BTC',
            'SNT-ETH', 'IOTA-EUR', 'BAT-USD', 'BAT-BTC', 'BAT-ETH', 'MNA-USD', 'MNA-BTC', 'FUN-USD', 'FUN-ETH',
            'ZRX-USD', 'ZRX-BTC', 'ZRX-ETH', 'TNB-USD', 'TNB-BTC', 'TNB-ETH', 'SPK-USD', 'TRX-USD', 'TRX-BTC',
            'TRX-ETH', 'RCN-USD', 'RLC-USD', 'RLC-BTC', 'AID-USD', 'SNG-USD', 'REP-USD', 'REP-BTC', 'REP-ETH',
            'ELF-USD', 'NEC-USD', 'NEC-BTC', 'NEC-ETH', 'BTC-GBP', 'ETH-EUR', 'ETH-JPY', 'ETH-GBP', 'NEO-EUR',
            'NEO-JPY', 'NEO-GBP', 'EOS-EUR', 'EOS-JPY', 'EOS-GBP', 'IOTA-JPY', 'IOTA-GBP', 'IOS-USD', 'IOS-BTC',
            'IOS-ETH', 'AIO-USD', 'AIO-BTC', 'REQ-USD', 'RDN-USD', 'LRC-USD', 'LRC-BTC', 'WAX-USD', 'WAX-BTC',
            'DAI-USD', 'DAI-BTC', 'DAI-ETH', 'AGI-USD', 'BFT-USD', 'BFT-BTC', 'MTN-USD', 'ODE-USD', 'ODE-BTC',
            'ODE-ETH', 'ANT-USD', 'ANT-BTC', 'ANT-ETH', 'DTH-USD', 'MIT-USD', 'STJ-USD', 'XLM-USD', 'XLM-EUR',
            'XLM-GBP', 'XLM-BTC', 'XLM-ETH', 'XVG-USD', 'XVG-BTC', 'MKR-USD', 'MKR-BTC', 'MKR-ETH', 'KNC-USD',
            'KNC-BTC', 'POA-USD', 'LYM-USD', 'UTK-USD', 'VEE-USD', 'DAD-USD', 'ORS-USD', 'AUC-USD', 'POY-USD',
            'FSN-USD', 'CBT-USD', 'ZCN-USD', 'SEN-USD', 'NCA-USD', 'CND-USD', 'CND-ETH', 'CTX-USD', 'PAI-USD',
            'SEE-USD', 'ESS-USD', 'ATM-USD', 'HOT-USD', 'DTA-USD', 'IQX-USD', 'IQX-EOS', 'WPR-USD', 'ZIL-USD',
            'BNT-USD', 'ABS-USD', 'XRA-USD', 'MAN-USD', 'NIO-USD', 'NIO-ETH', 'DGX-USD', 'DGX-ETH', 'VET-USD',
            'VET-BTC', 'UTN-USD', 'TKN-USD', 'GOT-USD', 'GOT-EUR', 'GOT-ETH', 'XTZ-USD', 'XTZ-BTC', 'CNN-USD',
            'BOX-USD', 'TRX-EUR', 'TRX-GBP', 'TRX-JPY', 'MGO-USD', 'RTE-USD', 'YGG-USD', 'MLN-USD', 'WTC-USD',
            'CSX-USD', 'OMN-USD', 'OMN-BTC', 'INT-USD', 'DRN-USD', 'PNK-USD', 'PNK-ETH', 'DGB-USD', 'DGB-BTC',
            'BSV-USD', 'BSV-BTC', 'BAB-USD', 'BAB-BTC', 'WLO-USD', 'VLD-USD', 'ENJ-USD', 'ONL-USD', 'RBT-USD',
            'RBT-BTC', 'UST-USD', 'EUT-EUR', 'EUT-USD', 'GSD-USD', 'UDC-USD', 'TSD-USD', 'PAX-USD', 'RIF-USD',
            'RIF-BTC', 'PAS-USD', 'VSY-USD', 'VSY-BTC', 'MKR-DAI', 'BTT-USD', 'BTT-BTC', 'BTC-UST', 'ETH-UST',
            'CLO-USD', 'CLO-BTC', 'IMP-USD', 'LTC-UST', 'EOS-UST', 'BAB-UST', 'SCR-USD', 'GNO-USD', 'GEN-USD',
            'ATO-USD', 'ATO-BTC', 'ATO-ETH', 'WBT-USD', 'XCH-USD', 'EUS-USD', 'WBT-ETH', 'XCH-ETH', 'LEO-USD',
            'LEO-BTC', 'LEO-UST', 'LEO-EOS', 'LEO-ETH', 'AST-USD', 'FOA-USD', 'UFR-USD', 'ZBT-USD', 'OKB-USD',
            'USK-USD', 'GTX-USD', 'KAN-USD', 'OKB-UST', 'OKB-BTC', 'USK-UST', 'USK-ETH', 'USK-BTC', 'USK-EOS',
            'GTX-UST', 'KAN-UST', 'AMP-USD', 'ALG-USD', 'ALG-BTC', 'ALG-UST', 'BTC-XCH', 'SWM-USD', 'TRI-USD',
            'LOO-USD', 'AMP-UST', 'DUSK:USD', 'DUSK:BTC', 'UOS-USD', 'UOS-BTC', 'RRB-USD', 'RRB-UST', 'DTX-USD',
            'AMP-BTC', 'FTT-USD', 'FTT-UST', 'PAX-UST', 'UDC-UST', 'TSD-UST', 'BTC:CNHT', 'UST:CNHT', 'CNH:CNHT',
            'CHZ-USD', 'CHZ-UST', 'XAUT:USD', 'XAUT:BTC', 'XAUT:UST']
BITMEX = ['XBTUSD', 'ETHUSD', 'XRPUSD']
BINANCE = ['BTC-USDT', 'ETH-USDT', 'BNB-USDT', 'LINK-USDT', 'ETH-BTC', 'BTC-BUSD', 'BUSD-USDT', 'BNB-BTC', 'BCH-USDT',
           'XRP-USDT', 'LTC-USDT', 'EOS-USDT', 'BTC-USDC', 'LINK-BTC', 'XTZ-USDT', 'USDC-USDT', 'XMR-USDT', 'SOL-BTC',
           'BTC-PAX', 'XMR-BTC', 'ETC-USDT', 'XRP-BTC', 'PAX-USDT', 'VET-USDT', 'BCH-BTC', 'TUSD-USDT', 'TRX-USDT',
           'BTC-TUSD', 'DASH-USDT', 'ADA-USDT', 'ZEC-USDT', 'XTZ-BTC', 'EOS-BTC', 'ATOM-USDT', 'XLM-USDT', 'LTC-BTC',
           'ETH-BUSD', 'ARK-BTC', 'ALGO-USDT', 'ENJ-BTC', 'BAT-USDT', 'NEO-USDT', 'VET-BTC', 'BAND-BTC', 'WRX-USDT',
           'MATIC-USDT', 'BAND-USDT', 'ETH-USDC', 'ONT-USDT', 'QTUM-USDT', 'TOMO-BTC', 'KAVA-BTC', 'GVT-BTC', 'BNB-ETH',
           'KAVA-USDT', 'WAVES-BTC', 'LSK-BTC', 'WRX-BTC', 'TRX-BTC', 'LTO-BTC', 'ADA-BTC', 'ENJ-USDT', 'SOL-BUSD',
           'BTT-USDT', 'ALGO-BTC', 'ZEC-BTC', 'ETC-BTC', 'IOTA-USDT', 'ATOM-BTC', 'BAT-BTC', 'BNB-BUSD', 'BCH-USDC',
           'LINK-ETH', 'MATIC-BTC', 'BTC-NGN', 'STRAT-BTC', 'STPT-BTC', 'IOST-USDT', 'NEO-BTC', 'TOMO-USDT',
           'WAVES-USDT', 'DASH-BTC', 'BUSD-NGN', 'ARN-BTC', 'WIN-USDT', 'CTXC-BTC', 'ICX-USDT', 'RVN-BTC', 'BTC-EUR',
           'NAS-BTC', 'OGN-BTC', 'OGN-USDT', 'XLM-BTC', 'BTG-BTC', 'ETH-TUSD', 'IOTA-BTC', 'TRX-ETH', 'NKN-BTC',
           'COTI-BTC', 'ETH-PAX', 'HBAR-BTC', 'BNB-TUSD', 'KMD-BTC', 'LSK-USDT', 'CDT-BTC', 'AION-USDT', 'ONT-BTC',
           'HBAR-USDT', 'XRP-USDC', 'QTUM-BTC', 'KNC-BTC', 'EOS-ETH', 'ICX-BTC', 'USDT-TRY', 'FET-USDT', 'NKN-USDT',
           'RVN-USDT', 'SOL-BNB', 'XRP-BUSD', 'TROY-BTC', 'LINK-BUSD', 'GXS-BTC', 'MITH-BTC', 'CTXC-USDT', 'FTT-BTC',
           'MCO-BTC', 'DATA-BTC', 'PERL-BTC', 'VIB-BTC', 'BCH-BUSD', 'REN-BTC', 'NAV-BTC', 'LEND-BTC', 'AION-BTC',
           'XRP-ETH', 'CHZ-BTC', 'FET-BTC', 'DOGE-USDT', 'NANO-BTC', 'STEEM-BTC', 'MTL-BTC', 'ZRX-BTC', 'LINK-USDC',
           'PERL-USDT', 'TROY-USDT', 'VET-ETH', 'AE-BTC', 'CELR-BTC', 'CHZ-USDT', 'OAX-BTC', 'EOS-USDC', 'EVX-BTC',
           'COTI-USDT', 'ZIL-USDT', 'MITH-USDT', 'MANA-BTC', 'QKC-BTC', 'XRP-BNB', 'EOS-BNB', 'ANKR-BTC', 'ARPA-USDT',
           'MTL-USDT', 'LTC-USDC', 'EDO-BTC', 'TRX-BNB', 'LTC-TUSD', 'BCH-TUSD', 'FTM-BTC', 'ANKR-USDT', 'ARPA-BTC',
           'TRX-XRP', 'TRX-USDC', 'BTC-TRY', 'USDT-RUB', 'LTC-BNB', 'DCR-BTC', 'BNB-USDC', 'BCH-BNB', 'SNT-BTC',
           'XRP-TUSD', 'STORJ-BTC', 'WTC-BTC', 'ONE-BTC', 'BQX-BTC', 'XEM-BTC', 'OMG-BTC', 'TNT-BTC', 'ENJ-ETH',
           'TRX-BUSD', 'EOS-BUSD', 'MBL-USDT', 'XZC-BTC', 'NANO-USDT', 'OMG-USDT', 'LEND-ETH', 'LTC-BUSD', 'PIVX-BTC',
           'LTO-USDT', 'LOOM-BTC', 'MDA-BTC']
BINANCE_US = ['BTC-USD', 'BTC-USDT', 'LINK-USD', 'ETH-USD', 'XRP-USD', 'USDT-USD', 'BNB-USD', 'LTC-USD', 'ETH-USDT',
              'VET-USD', 'ALGO-USD', 'XRP-USDT', 'ADA-USD', 'BNB-USDT', 'BCH-USD', 'VET-USDT', 'BTC-BUSD', 'LTC-USDT',
              'ZEC-USD', 'BCH-USDT', 'BNB-BTC', 'ETH-BTC', 'ENJ-USD', 'BUSD-USD', 'NEO-USD', 'XLM-USD', 'ICX-USD',
              'ETC-USD', 'ZRX-USD', 'BAT-USD', 'ATOM-USD', 'XRP-BTC', 'ADA-USDT', 'RVN-USD', 'ZIL-USD', 'IOTA-USD',
              'BNB-BUSD', 'DASH-USD', 'LTC-BTC', 'ETC-USDT', 'BCH-BTC', 'NANO-USD', 'ZRX-USDT', 'XLM-USDT', 'ETH-BUSD',
              'ONT-USD', 'DOGE-USDT', 'XRP-BUSD', 'ZIL-BUSD', 'NEO-USDT', 'WAVES-USD', 'QTUM-USDT', 'ALGO-BUSD',
              'BAT-USDT', 'QTUM-USD', 'ONT-USDT', 'ATOM-USDT']
BITSTAMP = ['BTC-USD', 'XRP-USD', 'BTC-EUR', 'XRP-EUR', 'ETH-USD', 'ETH-EUR', 'BCH-USD', 'LTC-USD', 'ETH-BTC',
            'LTC-EUR', 'BCH-EUR', 'BCH-BTC', 'LTC-BTC', 'XRP-BTC']
BITTREX = ['BTC-USD', 'BTC-USDT', 'BCH-USD', 'ETH-BTC', 'ETH-USD', 'USDT-USD', 'CTC-BTC', 'ETH-USDT', 'TUSD-BTC',
           'MOF-USDT', 'BSV-USDT', 'BSV-USD', 'BOA-BTC', 'DGB-BTC', 'LINK-BTC', 'XRP-BTC', 'BSV-BTC', 'ABBC-BTC',
           'LTC-BTC', 'ARK-BTC', 'ADA-BTC', 'BCH-BTC', 'XTP-BTC', 'ENJ-BTC', 'WAXP-BTC', 'BOA-USDT', 'XRP-USD',
           'LSK-BTC', 'LTC-USD', 'GAME-BTC', 'STC-BTC', 'WAXP-USDT', 'WAXP-USD', 'QNT-BTC', 'MOF-BTC', 'LINK-USD',
           'XRP-USDT', 'XMR-BTC', 'NMR-BTC', 'STEEM-BTC', 'MRPH-BTC', 'KMD-BTC', 'TUSD-USD', 'FXC-BTC', 'NMR-USDT',
           'STRAT-BTC', 'DMT-BTC', 'TRX-BTC', 'HBAR-USD', 'NEO-BTC', 'VTC-BTC', 'ELAMA-BTC', 'LINK-USDT', 'LTC-USDT',
           'OCEAN-BTC', 'NMR-ETH', 'XTZ-BTC', 'ANT-ETH', 'TUSD-USDT', 'TRX-USD', 'XLM-USDT', 'DCR-BTC', 'SXP-BTC',
           'RVN-BTC', 'BAT-USDT', 'HIVE-BTC', 'OCEAN-USDT', 'BCH-USDT', 'AEON-BTC', 'HBAR-BTC', 'LBC-BTC', 'BAT-BTC',
           'DAI-USDT', 'ANT-BTC', 'ZEC-BTC', 'DGB-ETH', 'ADA-USDT', 'XMR-USDT', 'ADA-USD', 'XLM-BTC', 'SOLVE-BTC',
           'XTZ-USD', 'TRX-USDT', 'ETC-BTC', 'PIVX-BTC', 'WICC-USDT', 'BTC-EUR', 'EOS-BTC', 'XHV-BTC', 'DGB-USDT',
           'CRO-BTC', 'DGB-USD', 'RDD-BTC', 'IGNIS-BTC', 'FCT-BTC', 'LTC-ETH', 'NEO-USDT', 'ZEC-USDT', 'DAI-BTC',
           'CPC-BTC']
BYBIT = ['BTC-USD', 'ETH-USD', 'XRP-USD', 'EOS-USD']
COINBASE = ['BTC-USD', 'ETH-USD', 'LINK-USD', 'BTC-EUR', 'XRP-USD', 'BTC-USDC', 'LTC-USD', 'BCH-USD', 'XTZ-USD',
            'BTC-GBP', 'ETH-EUR', 'ETH-USDC', 'ETH-BTC', 'XLM-USD', 'OXT-USD', 'BAT-USDC', 'DAI-USDC', 'ETH-GBP',
            'EOS-USD', 'XRP-EUR', 'LTC-EUR', 'KNC-USD', 'XRP-BTC', 'BCH-BTC', 'ALGO-USD', 'BCH-EUR', 'ZEC-USDC',
            'ETC-USD', 'ZRX-USD', 'LINK-ETH', 'DASH-USD', 'ATOM-USD', 'XTZ-BTC', 'LTC-BTC', 'REP-USD', 'BCH-GBP',
            'LTC-GBP', 'XLM-EUR', 'EOS-BTC', 'ZEC-BTC', 'XLM-BTC', 'BAT-ETH', 'ZRX-BTC', 'ATOM-BTC', 'ETH-DAI',
            'EOS-EUR', 'ZRX-EUR', 'DASH-BTC', 'ETC-EUR', 'KNC-BTC', 'ETC-BTC', 'REP-BTC', 'ETC-GBP', 'MANA-USDC',
            'CVC-USDC', 'LOOM-USDC', 'GNT-USDC', 'DNT-USDC']
COINBENE = ['ETC-USDT', 'BTC-USDT', 'BCH-USDT', 'ETH-USDT', 'ETH-BTC', 'EOS-USDT', 'EOS-BTC', 'BSV-USDT', 'DASH-USDT',
            'LTC-USDT', 'LTC-BTC', 'XRP-USDT', 'NEO-USDT', 'BSV-BTC', 'BNB-USDT', 'TRX-USDT', 'ETC-BTC', 'ZEC-USDT',
            'QTUM-BTC', 'BAT-BTC', 'XRP-BTC', 'OKB-USDT', 'NEO-BTC', 'TRX-BTC', 'XMR-BTC', 'HT-USDT', 'BNT-BTC',
            'ZEC-BTC', 'QTUM-USDT', 'LINK-BTC', 'CONI-USDT', 'PAX-USDT', 'XLM-BTC', 'NANO-BTC', 'KMD-BTC', 'TWEE-USDT',
            'ZRX-BTC', 'DGD-BTC', 'BTNT-BTC', 'LAMB-USDT', 'STORJ-BTC', 'ABBC-BTC', 'REP-BTC', 'EQUAD-BTC', 'IOST-BTC',
            'OMG-BTC', 'AION-BTC', 'ELF-BTC', 'GVT-BTC', 'CS-USDT', 'AE-BTC', 'ADN-BTC', 'HTDF-USDT', 'CVC-BTC',
            'POLY-BTC', 'YAP-BTC', 'PPT-BTC', 'SKM-ETH', 'LOOM-BTC', 'HNB-USDT', 'ABBC-USDT', 'YAP-USDT', 'XSR-USDT',
            'MOAC-USDT', 'RIF-BTC', 'ADK-BTC', 'PLF-USDT', 'SBT-USDT', 'LBK-BTC', 'CTCN-USDT', 'SEN-BTC', 'VSC-ETH',
            'CUST-USDT', 'MXM-USDT', 'WBX-USDT', 'PAT-ETH', 'CCC-ETH', 'LUX-BTC', 'IVY-ETH', 'VSF-BTC', 'APL-ETH',
            'MINX-BTC', 'MXM-ETH', 'ETN-BTC', 'FAB-ETH', 'GDC-ETH', 'MINX-ETH', 'CPC-BTC', 'BTC-BRL', 'YTA-USDT',
            'MIB-BTC', 'SMART-USDT', 'CRN-BTC', 'SCC-BTC', 'TOSC-BTC', 'XNK-ETH', 'KBC-BTC', 'TMTG-BTC', 'XRP-BRL',
            'AIDOC-BTC', 'OVC-ETH', 'KBC-USDT', 'XEM-BTC', 'GDC-BTC', 'NBAI-ETH', 'NPXS-ETH', 'WFX-BTC', 'WBL-BTC',
            'AIDUS-BTC', 'NPXS-USDT', 'MZG-USDT', 'MTC-BTC', 'ETK-BTC', 'TRUE-ETH', 'SRCOIN-BTC', 'ACDC-BTC',
            'ACDC-USDT', 'CREDO-ETH', 'SMARTUP-USDT', 'DTA-ETH', 'FND-ETH', 'ALX-ETH', 'CAN-ETH', 'MVL-ETH', 'EDR-ETH',
            'EBC-ETH', 'TEN-BTC', 'MTN-ETH', 'SIM-BTC', 'AIT-USDT', 'CTXC-ETH', 'RBTC-BTC', 'COSM-ETH', 'ABYSS-ETH',
            'SWTC-USDT', 'SMARTUP-ETH', 'PMA-ETH', 'VME-BTC', 'TCT-BTC', 'CEDEX-ETH', 'SKB-BTC', 'BETHER-ETH',
            'BAAS-BTC', 'GDC-USDT', 'SLT-ETH', 'NTY-ETH', 'OMX-ETH', 'SRCOIN-ETH', 'PLAY-BTC', 'CENT-BTC', 'QKC-BTC',
            'PSM-BTC', 'CNN-BTC', 'ADI-ETH', 'GRN-BTC', 'KST-BTC', 'CMT-USDT', 'KNT-ETH', 'FNKOS-ETH', 'CNN-ETH',
            'CS-ETH', 'CMT-ETH', 'ISR-ETH', 'ECA-BTC', 'BSTN-ETH', 'LTC-BRL', 'GUSD-USDT', 'COSM-BTC', 'ETH-BRL',
            'FTT-BTC', 'DENT-BTC', 'INCX-ETH', 'ATX-BTC', 'CXP-BTC', 'SHE-BTC', 'MT-ETH', 'GETX-ETH', 'AE-USDT',
            'BOA-USDT', 'ALI-ETH', 'CNN-USDT', 'MT-USDT', 'ABT-USDT', 'NOBS-BTC', 'FXT-ETH', 'BEZ-BTC', 'ABT-ETH',
            'UNI-USDT', 'TEMCO-USDT', 'HDAC-BTC', 'UTNP-BTC', 'EBC-USDT', 'TEN-ETH', 'VME-ETH']
DERIBIT = ['BTC-PERPETUAL', 'ETH-PERPETUAL']
GEMINI = ['BTC-USD', 'ETH-USD', 'BCH-USD', 'LTC-USD', 'ZEC-USD', 'ETH-BTC', 'BCH-BTC', 'LTC-BTC', 'ZEC-BTC', 'LTC-ETH',
          'LTC-BCH', 'BCH-ETH', 'ZEC-LTC', 'ZEC-ETH', 'ZEC-BCH']
HITBTC = ['BTC-USD', 'ETH-USD', 'BCH-USD', 'ETH-BTC', 'BSV-USD', 'EOS-USD', 'LTC-USD', 'BCH-BTC', 'ETC-ETH', 'ETC-USD',
          'BSV-BTC', 'XRP-BTC', 'DASH-USD', 'LTC-BTC', 'EOS-BTC', 'XMR-USD', 'ZEC-USD', 'ETC-BTC', 'XMR-BTC', 'TRX-USD',
          'QTUM-USD', 'TRX-BTC', 'ONT-USD', 'NEO-USD', 'ICX-USD', 'XLM-USD', 'ADA-BTC', 'ADA-USD', 'NEO-BTC', 'ZEC-BTC',
          'DASH-BTC', 'XTZ-USD', 'EOS-ETH', 'VET-BTC', 'ETH-DAI', 'QTUM-BTC', 'IOST-USD', 'XLM-BTC', 'ROOBEE-BTC',
          'BTG-BTC', 'ONT-BTC', 'TRX-ETH', 'STRAT-BTC', 'IOTA-USD', 'LSK-BTC', 'LSK-USD', 'IOTA-BTC', 'ICX-BTC',
          'KMD-BTC', 'IOST-BTC', 'XEM-USD', 'DGTX-BTC', 'OMG-BTC', 'ZRX-BTC', 'BNT-USD', 'DASH-ETH', 'ONT-ETH',
          'XTZ-BTC', 'GNT-USD', 'BTC-USDC', 'DOGE-BTC', 'STEEM-BTC', 'WAVES-BTC', 'OMG-USD', 'NXT-BTC', 'DOGE-USD',
          'XVG-BTC', 'XZC-BTC', 'ADK-BTC', 'REP-BTC', 'ZEC-ETH', 'BNB-BTC', 'BTM-USD', 'ADA-ETH', 'QTUM-ETH',
          'BTC-TUSD', 'BNB-USD', 'IOTA-ETH', 'CENNZ-BTC', 'BTM-ETH', 'ZRX-USD', 'EMRX-BTC', 'TNT-BTC', 'ZIL-USD',
          'XEM-BTC', 'NWC-USD', 'XMR-ETH', 'LINK-BTC', 'MAID-BTC', 'EOS-DAI', 'TNT-USD', 'GRIN-BTC', 'XLM-ETH',
          'VRA-BTC', 'GNT-BTC', 'MTL-BTC', 'BTS-BTC', 'ZEN-USD', 'DGB-BTC', 'ENJ-BTC', 'BET-BTC', 'NWC-BTC', 'BTG-USD',
          'LSK-ETH', 'NEBL-BTC', 'SC-BTC', 'BTC-PAX', 'KMD-USD', 'SOLO-USD', 'ZEN-BTC', 'DOGE-ETH', 'MKR-BTC',
          'BNT-BTC', 'MKR-USD', 'BTC-DAI', 'MAID-USD', 'ICX-ETH', 'DCN-ETH', 'KMD-ETH', 'NANO-BTC', 'REM-BTC',
          'SHIP-BTC', 'SMART-USD', 'CHSB-BTC', 'NXT-USD', 'XTZ-ETH', 'CHSB-ETH', 'GRIN-USD', 'SHIP-ETH', 'SMART-BTC',
          'ZIL-BTC', 'XZC-USD', 'DGTX-USD', 'BTM-BTC', 'ETP-USD', 'BTC-GUSD', 'ZRC-BTC', 'MKR-ETH', 'CRO-BTC',
          'ZRX-ETH', 'EDO-USD', 'ARDR-BTC', 'OMG-ETH', 'XVG-ETH', 'MAID-ETH', 'XEM-ETH', 'DGTX-ETH', 'CPT-BTC',
          'NXT-ETH', 'SMART-ETH', 'GRIN-ETH', 'NANO-USD', 'REP-ETH', 'REM-ETH', 'STORJ-BTC', 'BTG-ETH', 'NEXO-BTC',
          'EDO-BTC', 'ETP-BTC', 'HEDG-BTC', 'SLV-BTC', 'ARPA-BTC', 'BTC-EURS', 'NMR-BTC', 'ATOM-BTC', 'DCN-USD',
          'XRP-ETH', 'LA-ETH', 'TNT-ETH', 'NEBL-ETH', 'XVG-USD', 'REM-USD', 'MANA-BTC', 'GNT-ETH', 'DATA-BTC',
          'TUSD-USDC', 'LRC-BTC', 'AE-BTC', 'BAT-BTC', 'IPX-USD', 'BTT-BTC', 'PRE-BTC', 'DASH-BCH', 'LTC-ETH',
          'ETH-USDC', 'RAISE-BTC', 'CRPT-BTC', 'ZEN-ETH', 'DGB-USD', 'BET-ETH', 'ABTC-BTC', 'RCN-BTC', 'MANA-USD',
          'LINK-USD', 'HBAR-BTC', 'AVA-ETH', 'DRG-BTC', 'NIM-BTC', 'RAISE-ETH', 'IQ-USD']
HUOBI = ['BTC-USDT', 'ETH-USDT', 'EOS-USDT', 'USDT-HUSD', 'BCH-USDT', 'HT-USDT', 'BSV-USDT', 'XRP-USDT', 'LINK-USDT',
         'LTC-USDT', 'SEELE-USDT', 'SEELE-BTC', 'ETC-USDT', 'ETH-BTC', 'HT-BTC', 'DASH-USDT', 'ZEC-USDT', 'TRX-USDT',
         'BCH-BTC', 'XRP-BTC', 'BSV-BTC', 'EOS-BTC', 'ATOM-USDT', 'HT-ETH', 'XMR-USDT', 'ADA-USDT', 'XTZ-USDT',
         'ALGO-USDT', 'XMR-BTC', 'ONT-USDT', 'BTC-HUSD', 'HPT-USDT', 'NEXO-BTC', 'BTT-USDT', 'IOST-USDT', 'MCO-BTC',
         'QTUM-USDT', 'CRO-BTC', 'NEXO-ETH', 'LTC-BTC', 'EOS-ETH', 'CTXC-USDT', 'CVNT-BTC', 'DASH-BTC', 'USDC-HUSD',
         'ETC-BTC', 'ZEC-BTC', 'NEO-USDT', 'BHT-USDT', 'KCASH-BTC', 'CKB-USDT', 'TRX-BTC', 'XLM-USDT', 'LAMB-USDT',
         'TUSD-HUSD', 'UIP-USDT', 'EKT-USDT', 'TT-USDT', 'MDS-USDT', 'AE-USDT', 'BTM-USDT', 'STEEM-USDT', 'CKB-BTC',
         'NKN-USDT', 'CVNT-ETH', 'MX-USDT', 'CRO-USDT', 'HPT-BTC', 'HB10-USDT', 'RSR-USDT', 'CTXC-BTC', 'LINK-BTC',
         'HPT-HT', 'SNC-BTC', 'EOS-HT', 'OST-BTC', 'NEO-BTC', 'KCASH-ETH', 'NAS-USDT', 'VET-USDT', 'LXT-USDT',
         'CRE-USDT', 'ETH-HUSD', 'HT-HUSD', 'VET-BTC', 'MXC-BTC', 'VSYS-USDT', 'HC-USDT', 'OMG-USDT', 'KAN-USDT',
         'PAX-HUSD', 'WICC-USDT', 'GXC-USDT', 'ALGO-BTC', 'STORJ-USDT', 'XTZ-BTC', 'FOR-USDT', 'IOTA-USDT', 'CTXC-ETH',
         'NODE-USDT', 'ITC-USDT', 'TRX-ETH', 'ACT-USDT', 'ARPA-USDT', 'VIDY-USDT', 'EM-USDT', 'LAMB-ETH', 'YCC-BTC',
         'BCH-HT', 'BIX-USDT', 'UUU-USDT', 'MT-ETH', 'DATX-BTC', 'YCC-ETH', 'SNC-ETH', 'BSV-HUSD', 'TOPC-ETH',
         'DOGE-USDT', 'LINK-ETH', 'NEW-USDT', 'ZIL-USDT', 'ATOM-BTC', 'ONE-USDT', 'MDS-BTC', 'LET-USDT', 'EOS-HUSD',
         'PAI-USDT', 'XZC-USDT', 'RSR-BTC', 'ZJLT-BTC', 'KAN-ETH', 'EVX-BTC', 'FTT-USDT', 'LET-ETH', 'LET-BTC',
         'XRP-HT', 'FSN-USDT', 'LXT-BTC', 'WAVES-USDT', 'RUFF-USDT', 'OGO-USDT', 'WAXP-BTC', 'DCR-USDT', 'KAN-BTC',
         'BIX-BTC', 'AE-BTC', 'BTS-USDT', 'BAT-USDT', 'UTK-ETH', 'LBA-USDT', 'XLM-BTC', 'NKN-BTC', 'LOL-USDT',
         'UTK-BTC', 'ADA-BTC', 'KCASH-HT', 'BTG-BTC', 'TRIO-BTC', 'SKM-USDT', 'CNNS-USDT', 'BTT-TRX', 'REN-USDT',
         'AAC-BTC', 'ELA-USDT', 'MT-BTC', 'GT-USDT', 'WAN-BTC', 'BOX-BTC', 'UC-BTC', 'SNT-USDT', 'QTUM-ETH', 'ATP-USDT',
         'UC-ETH', 'VSYS-BTC', 'TOP-USDT', 'FTT-BTC', 'DBC-BTC', 'BTT-BTC', 'BHT-BTC', 'KNC-ETH', 'GXC-BTC', 'SMT-USDT',
         'TT-BTC', 'OCN-USDT', 'BTM-BTC', 'KMD-BTC', 'WXT-USDT', 'IOST-BTC', 'WAVES-BTC', 'ZRX-USDT', 'DOGE-BTC',
         'DAC-BTC', 'IOTA-BTC', 'BCD-BTC', 'BIX-ETH', 'MANA-USDT', 'THETA-USDT', 'FAIR-BTC', 'FAIR-ETH', 'UIP-ETH']
KRAKEN = ['XBT-EUR', 'XBT-USD', 'ETH-EUR', 'ETH-USD', 'USDT-USD', 'ETH-XBT', 'USDT-EUR', 'XRP-USD', 'XRP-EUR',
          'USDC-EUR', 'XTZ-USD', 'USDC-USD', 'XTZ-EUR', 'BCH-USD', 'LINK-USD', 'BCH-EUR', 'XBT-GBP', 'LTC-USD',
          'PAXG-EUR', 'XMR-EUR', 'XTZ-XBT', 'EOS-EUR', 'LINK-EUR', 'XBT-USDT', 'XMR-XBT', 'LTC-EUR', 'XBT-CAD',
          'XMR-USD', 'EOS-USD', 'USDC-USDT', 'ETH-USDT', 'PAXG-XBT', 'XRP-XBT', 'PAXG-USD', 'XBT-CHF', 'ETH-CAD',
          'XLM-EUR', 'DAI-USD', 'DAI-EUR', 'ADA-EUR', 'LINK-XBT', 'ATOM-EUR', 'ETC-EUR', 'LSK-XBT', 'XLM-USD',
          'DAI-USDT', 'DASH-EUR', 'BCH-XBT', 'LTC-XBT', 'ALGO-USD', 'LSK-EUR', 'ADA-XBT', 'DASH-USD', 'ATOM-USD',
          'BAT-USD', 'ZEC-USD', 'ZEC-EUR', 'XBT-USDC', 'XBT-DAI', 'QTUM-USD', 'ZEC-XBT', 'ADA-USD', 'TRX-USD',
          'LINK-ETH', 'REP-EUR', 'WAVES-EUR', 'ALGO-EUR', 'ALGO-XBT', 'DASH-XBT', 'NANO-EUR', 'ICX-EUR', 'ICX-XBT',
          'XTZ-ETH', 'USDT-GBP', 'EOS-XBT', 'ICX-USD', 'LSK-USD', 'BAT-EUR', 'NANO-XBT', 'SC-EUR', 'BAT-XBT', 'ETH-CHF',
          'USDT-CAD', 'XDG-XBT', 'TRX-EUR', 'ALGO-ETH', 'ETH-GBP', 'REP-USD', 'WAVES-XBT', 'XRP-CAD', 'ETC-XBT',
          'PAXG-ETH', 'ETC-USD', 'BAT-ETH', 'ETH-USDC', 'OMG-EUR', 'EOS-ETH', 'XLM-XBT', 'GNO-EUR', 'MLN-ETH',
          'XDG-EUR', 'ATOM-XBT', 'LSK-ETH', 'NANO-USD', 'GNO-ETH', 'ADA-ETH', 'REP-XBT', 'QTUM-EUR', 'ICX-ETH',
          'GNO-USD', 'NANO-ETH', 'GNO-XBT', 'ETH-DAI', 'WAVES-USD', 'SC-XBT', 'MLN-EUR', 'QTUM-XBT', 'SC-ETH',
          'ATOM-ETH', 'OMG-XBT', 'SC-USD', 'QTUM-ETH', 'REP-ETH', 'XDG-USD', 'OMG-USD', 'TRX-XBT', 'MLN-XBT', 'XBT-JPY',
          'WAVES-ETH', 'ETC-ETH', 'TRX-ETH', 'ETH-JPY', 'MLN-USD', 'OMG-ETH', 'XRP-JPY']
OKCOIN = ['BTC-USD', 'USDT-USD', 'ETH-USD', 'BTC-EUR', 'LTC-USD', 'BCH-USD', 'USDC-USD', 'BCH-EUR', 'ETH-EUR',
          'HBAR-USD', 'XRP-USD', 'BSV-USD', 'USDK-USD', 'BTC-USDT', 'TUSD-USD', 'EURS-EUR', 'BTC-EURS', 'TRX-USD',
          'ETC-USD', 'DAI-USD', 'EOS-USD', 'PAX-USD']
OKEX = ['BTC-USDT', 'ETH-USDT', 'OKB-USDT', 'OKB-ETH', 'MCO-BTC', 'ETC-BTC', 'TRUE-BTC', 'HDAO-USDK', 'EOS-USDT',
        'BSV-USDT', 'OKB-BTC', 'ETC-ETH', 'BCH-USDT', 'TRX-BTC', 'ETC-USDT', 'MOF-USDT', 'DEP-USDT', 'DEP-USDK',
        'TRX-ETH', 'BSV-BTC', 'LTC-USDT', 'BCH-BTC', 'HDAO-USDT', 'KNC-USDT', 'XTZ-USDT', 'EOS-ETH', 'ETH-BTC',
        'XRP-USDT', 'PAX-USDT', 'SWFTC-ETH', 'TRUE-ETH', 'GTO-ETH', 'KNC-BTC', 'BCH-USDK', 'LINK-USDT', 'ETC-USDK',
        'EOS-BTC', 'SWFTC-BTC', 'XTZ-BTC', 'MCO-USDT', 'QTUM-USDT', 'IOTA-USDT', 'YOU-ETH', 'TRUE-USDT', 'ATOM-USDT',
        'ITC-USDT', 'BSV-USDK', 'ONT-USDT', 'DASH-USDT', 'BTC-USDK', 'ZEC-BTC', 'EOS-OKB', 'ABT-USDT', 'LTC-BTC',
        'BTG-USDT', 'TRX-USDT', 'APM-USDT', 'BTM-BTC', 'USDT-USDK', 'GTO-BTC', 'ZEC-USDT', 'IOST-BTC', 'CTXC-BTC',
        'YOU-USDT', 'ROAD-USDT', 'XMR-BTC', 'NEO-ETH', 'XMR-USDT', 'LRC-USDT', 'IOST-USDT', 'MDT-USDT', 'XRP-ETH',
        'LTC-OKB', 'KCASH-USDT', 'ATOM-BTC', 'XRP-BTC', 'KCASH-BTC', 'BCD-USDT', 'ATOM-ETH', 'NEO-BTC', 'NEO-USDT',
        'QTUM-BTC', 'MANA-USDT', 'SWFTC-USDT', 'NULS-USDT', 'EC-USDT', 'CTXC-ETH', 'CVC-USDT', 'YOU-BTC', 'GAS-USDT',
        'ETC-OKB', 'ICX-USDT', 'CVC-BTC', 'XLM-USDT', 'MDT-BTC', 'ONT-BTC', 'ABT-ETH', 'ELF-BTC', 'VITE-BTC',
        'MANA-BTC', 'BTM-USDT', 'OMG-BTC', 'ORS-ETH', 'NULS-ETH', 'PAX-BTC', 'RNT-USDT', 'TUSD-BTC', 'XUC-USDT',
        'GAS-ETH', 'NAS-USDT', 'ETH-USDK', 'WXT-BTC', 'NULS-BTC', 'HBAR-USDK', 'MITH-BTC', 'TRIO-ETH', 'INT-USDT',
        'XEM-USDT', 'PAY-USDT', 'SNT-BTC', 'ONT-ETH', 'CTXC-USDT', 'BAT-USDT', 'CVT-BTC', 'DASH-BTC', 'TRIO-BTC',
        'PAY-BTC', 'CVT-USDT', 'CRO-USDT', 'ELF-ETH', 'LTC-ETH', 'PPT-USDT', 'ZIL-USDT', 'LINK-BTC', 'EOS-USDK',
        'BCD-BTC', 'INT-BTC', 'PMA-USDK', 'WTC-USDT', 'BTM-ETH', 'HBAR-USDT', 'ACT-USDT', 'MDT-ETH', 'MCO-ETH',
        'SNT-USDT', 'AAC-USDT', 'CVC-ETH', 'TUSD-USDT', 'INT-ETH', 'APM-BTC', 'GAS-BTC', 'GTO-USDT', 'DOGE-USDT',
        'PST-BTC', 'EC-USDK', 'XLM-BTC', 'LEO-USDT', 'NAS-BTC', 'CRO-BTC', 'NAS-ETH', 'WXT-USDT', 'WTC-ETH', 'OKB-USDK',
        'LBA-USDT', 'PST-USDT', 'LSK-USDT', 'ICX-BTC', 'USDC-BTC', 'ORS-BTC', 'STORJ-USDT', 'ZEC-OKB', 'ARK-USDT',
        'NEO-OKB', 'MKR-BTC', 'ELF-USDT', 'WTC-BTC', 'HBAR-BTC', 'ALGO-USDT', 'IOTA-BTC', 'MITH-USDT', 'USDC-USDT',
        'GNT-USDT', 'FAIR-USDT', 'QTUM-ETH', 'DASH-OKB', 'PMA-BTC', 'KCASH-ETH', 'EGT-ETH', 'BNT-USDT', 'ABT-BTC',
        'LSK-BTC', 'UTK-USDT', 'BTG-BTC', 'DGB-USDT', 'ZRX-BTC', 'DGB-BTC', 'ZEN-USDT', 'XMR-ETH', 'LRC-BTC',
        'BLOC-USDT']
POLONIEX = ['BTC-USDT', 'BTC-USDC', 'ETH-USDT', 'TRX-USDT', 'ETH-BTC', 'XRP-BTC', 'ETH-USDC', 'MATIC-USDT', 'BEAR-USDT',
            'XMR-BTC', 'LTC-BTC', 'BTT-USDT', 'XRP-USDT', 'BULL-USDT', 'USDT-USDC', 'BCHABC-BTC', 'XMR-USDT',
            'LTC-USDT', 'ZEC-BTC', 'MATIC-BTC', 'BCHSV-BTC', 'XRP-TRX', 'TRXBULL-USDT', 'ZEC-USDT', 'BCHSV-USDT',
            'EOS-USDC', 'DASH-BTC', 'BCHABC-USDT', 'SNX-USDT', 'TRX-BTC', 'LTC-USDC', 'ETC-BTC', 'BCHSV-USDC',
            'STR-USDT', 'ETHBULL-USDT', 'SNX-BTC', 'STORJ-BTC', 'XEM-BTC', 'DASH-USDT', 'EOS-USDT', 'TRXBEAR-USDT',
            'ETC-USDT', 'STR-BTC', 'EOS-BTC', 'ATOM-BTC', 'BTC-USDJ', 'TRX-USDJ', 'ATOM-USDT', 'ETH-TRX', 'NMR-BTC',
            'ETC-ETH', 'GRIN-BTC', 'LSK-BTC', 'ETHBEAR-USDT', 'BTT-TRX', 'ARDR-BTC', 'LSK-USDT', 'XRP-USDC',
            'STRAT-BTC', 'LPT-BTC', 'XMR-USDC', 'LINK-BTC', 'ZEC-USDC', 'BCHABC-USDC', 'SC-BTC', 'DOGE-BTC',
            'BCHBEAR-USDT', 'DOGE-USDT', 'QTUM-BTC', 'TRX-USDC', 'STR-USDC', 'ZEC-ETH', 'QTUM-USDT', 'XTZ-USDT',
            'MANA-BTC', 'PAX-USDT', 'ETC-USDC', 'GRIN-USDT', 'MATIC-TRX', 'GNT-BTC', 'DASH-USDC', 'NXT-BTC', 'BTC-PAX',
            'GRIN-USDC', 'BAT-USDT', 'BAT-BTC', 'ATOM-USDC', 'STEEM-BTC', 'XTZ-BTC', 'BTT-BTC', 'WIN-USDT', 'NXT-USDT',
            'GAS-BTC', 'CVC-BTC', 'WIN-TRX', 'SNX-TRX', 'KNC-BTC', 'OMG-BTC', 'REP-USDT', 'DCR-BTC', 'BCN-BTC',
            'FOAM-BTC', 'EOS-ETH', 'BTS-BTC', 'BAT-ETH', 'MANA-USDT', 'ZRX-BTC', 'POLY-BTC', 'BNT-BTC', 'GNT-USDT',
            'ZRX-USDT', 'ZRX-ETH', 'STEEM-TRX', 'REP-BTC', 'ETHBNT-BTC', 'SNT-BTC', 'DOGE-USDC', 'LOOM-BTC', 'LINK-TRX',
            'REP-ETH', 'BCHBULL-USDT', 'SC-USDT', 'XTZ-TRX', 'ETH-PAX']
BITMAX = ['BTC-USDT', 'ETH-USDT', 'BCH-USDT', 'EOS-USDT', 'BNB-USDT', 'ETC-USDT', 'BCHSV-USDT', 'ETH-BTC', 'LINK-USDT',
          'XRP-USDT', 'BNB-BTC', 'BTMX-USDT', 'HT-USDT', 'LTC-USDT', 'BNB-ETH', 'BTMX-BTC', 'EOS-BTC', 'XRP-BTC',
          'DAD-USDT', 'BTMX-PAX', 'ATOM-USDT', 'TRX-USDT', 'DASH-USDT', 'XTZ-USDT', 'ZEC-USDT', 'ETC-BTC', 'ALGO-USDT',
          'BCH-BTC', 'XLM-USDT', 'BTCBEAR-USDT', 'FTT-USDT', 'TRX-ETH', 'XNS-USDT', 'XNS-BTC', 'EOS-ETH', 'ONE-USDT',
          'BTC-USDC', 'BNBBEAR-USDT', 'HT-BTC', 'ALGO-BTC', 'BNBBULL-USDT', 'BCHSV-BTC', 'OKB-USDT', 'ADA-USDT',
          'INFT-USDT', 'BAT-BTC', 'ELF-USDT', 'ETHBEAR-USDT', 'FTT-BTC', 'ETHBULL-USDT', 'ATOM-BTC', 'ONT-USDT',
          'ELF-BTC', 'FRM-USDT', 'QTUM-USDT', 'CHR-USDT', 'ERD-USDT', 'LINK-ETH', 'IOST-BTC', 'BTC-PAX', 'OKB-ETH',
          'DOGE-BTC', 'LINK-BTC', 'BOLT-BTC', 'CET-USDT', 'BAT-USDT', 'RUNE-USDT', 'INFT-BTC', 'LTO-USDT', 'BXA-USDT',
          'IOST-USDT', 'KCS-USDT', 'DOS-USDT', 'BOLT-USDT', 'ANKR-BTC', 'EOSBULL-USDT', 'OKB-BTC', 'PAX-USDT',
          'BTT-USDT', 'XRP-ETH', 'ZEC-BTC', 'LTO-BTC', 'CELR-USDT', 'FTM-USDT', 'RVN-USDT', 'CHX-USDT', 'STPT-USDT',
          'RNT-USDT', 'DASH-BTC', 'ERD-BTC', 'BTCBULL-USDT', 'ZIL-BTC', 'KAVA-USDT', 'ONT-ETH', 'NEO-ETH', 'KAVA-BTC',
          'GT-BTC', 'FET-BTC', 'ANKR-USDT', 'KCS-BTC', 'GT-USDT', 'FRM-BTC', 'ZIL-USDT', 'CHX-ETH', 'TRX-BTC', 'GT-ETH',
          'STPT-BTC', 'VET-USDT', 'DOGE-USDT', 'IOST-ETH', 'ELF-ETH', 'CHR-BTC', 'ONT-BTC', 'MHC-USDT', 'HT-ETH',
          'ZRX-BTC', 'AERGO-USDT', 'AERGO-ETH', 'ONE-BTC', 'CHZ-USDT', 'CELR-BTC', 'COTI-USDT', 'COVA-USDT', 'ZRX-USDT',
          'LTC-BTC', 'MIX-USDT', 'XLM-BTC', 'EOSBEAR-USDT', 'FTM-BTC', 'VET-BTC', 'UAT-USDT', 'AERGO-BTC', 'BTT-BTC',
          'BTM-BTC', 'CHX-BTC', 'QCX-BTC', 'QCX-USDT', 'USDC-USDT', 'XEM-BTC', 'RVN-BTC', 'OLT-USDT', 'ATOM-ETH',
          'LTCBULL-USDT', 'UAT-BTC', 'NEO-BTC', 'NEO-USDT', 'BTM-USDT', 'ABBC-USDT', 'ABBC-BTC', 'TOKO-USDT',
          'CKB-USDT', 'XTZ-BTC', 'XRPBULL-USDT', 'XRPBEAR-USDT', 'LTC-ETH', 'ADA-BTC', 'LAMB-USDT', 'COTI-BTC',
          'LAMB-BTC', 'XEM-USDT', 'MATIC-USDT', 'ONG-USDT', 'QTUM-BTC', 'ALTBEAR-USDT', 'ADA-ETH', 'MATIC-BTC',
          'FET-USDT', 'ALTBULL-USDT', 'XLM-ETH', 'FLEX-USDT', 'LBA-USDT', 'LBA-BTC', 'HPB-USDT', 'EXCHBULL-USDT',
          'COVA-BTC', 'EXCHBEAR-USDT', 'ETZ-USDT', 'LTCBEAR-USDT', 'FSN-USDT', 'DREP-USDT', 'WAN-USDT', 'PROM-USDT',
          'VALOR-USDT', 'LTO-ETH', 'FLEX-BTC', 'MITX-USDT', 'DUO-USDT', 'HPB-BTC', 'CET-BTC']
UPBIT = ['BTC-KRW', 'ETH-KRW', 'XRP-KRW', 'BSV-KRW', 'ARK-KRW', 'BCH-KRW', 'BTG-KRW', 'EOS-KRW', 'IGNIS-KRW', 'LSK-KRW',
         'VTC-KRW', 'HBAR-KRW', 'TRX-KRW', 'ADA-KRW', 'STPT-KRW', 'MLK-KRW', 'DMT-KRW', 'STRAT-KRW', 'TT-KRW',
         'TTC-KRW', 'ETC-KRW', 'ENJ-KRW', 'RVN-BTC', 'QTUM-KRW', 'ANKR-KRW', 'MTL-KRW', 'BAT-KRW', 'STEEM-KRW',
         'MBL-KRW', 'BORA-BTC', 'BTT-KRW', 'XLM-KRW', 'ICX-KRW', 'IOTA-KRW', 'GTO-KRW', 'STORJ-KRW', 'DCR-KRW',
         'LTC-KRW', 'ARDR-KRW', 'GAS-KRW', 'ATOM-KRW', 'GRS-KRW', 'KMD-KRW', 'ONT-KRW', 'UPP-KRW', 'COSM-KRW',
         'META-BTC', 'LOOM-KRW', 'ONG-KRW', 'TSHP-KRW', 'WAXP-KRW', 'QKC-KRW', 'IOST-KRW', 'POLY-KRW', 'MANA-KRW',
         'RFR-KRW', 'CRE-KRW', 'WAVES-KRW', 'MED-KRW', 'KNC-KRW', 'NEO-KRW', 'ORBS-KRW', 'IQ-KRW', 'AERGO-KRW',
         'ZRX-KRW', 'THETA-KRW', 'EDR-KRW', 'LUNA-BTC', 'OST-KRW', 'TFUEL-KRW', 'MFT-KRW', 'SOLVE-KRW', 'MOC-KRW',
         'ZIL-KRW', 'CVC-KRW', 'POWR-KRW', 'GNT-KRW', 'SRN-KRW', 'OMG-KRW', 'SNT-KRW', 'EMC2-KRW', 'XEM-KRW',
         'STORM-KRW', 'ELF-KRW', 'OGN-BTC', 'VET-KRW', 'MCO-KRW', 'REP-KRW', 'ADX-KRW', 'SC-KRW', 'XRP-BTC', 'NPXS-KRW',
         'SBD-KRW', 'ETH-BTC', 'SPND-BTC', 'CHZ-BTC', 'LBA-BTC', 'TRX-BTC', 'XVG-BTC', 'IGNIS-BTC', 'TTC-BTC',
         'RCN-BTC', 'BTU-BTC', 'STORJ-BTC', 'NMR-BTC', 'PMA-BTC', 'ARK-BTC', 'SYS-BTC', 'MLK-BTC', 'SC-USDT', 'SC-BTC',
         'ARDR-BTC', 'BTC-USDT', 'EOS-BTC', 'XLM-BTC', 'NPXS-BTC', 'NXT-BTC', 'QTUM-BTC', 'POWR-BTC', 'XEM-BTC',
         'SPC-BTC']

SPOT = 1
FUTURES = 2

exchanges = [
    [BITFINEX, 'BITFINEX', SPOT],
    [BITMEX, 'BITMEX', FUTURES],
    [BINANCE, 'BINANCE', SPOT],
    [BINANCE_US, 'BINANCE_US', SPOT],
    [BITSTAMP, 'BITSTAMP', SPOT],
    [BITTREX, 'BITTREX', SPOT],
    [BYBIT, 'BYBIT', SPOT],
    [COINBASE, 'COINBASE', SPOT],
    [COINBENE, 'COINBENE', SPOT],
    [DERIBIT, 'DERIBIT', FUTURES],
    [GEMINI, 'GEMINI', SPOT],
    [HITBTC, 'HITBTC', SPOT],
    [HUOBI, 'HUOBI', SPOT],
    [KRAKEN, 'KRAKEN', SPOT],
    [OKCOIN, 'OKCOIN', SPOT],
    [OKEX, 'OKEX', SPOT],
    [POLONIEX, 'POLONIEX', SPOT],
    [BITMAX, 'BITMAX', SPOT],
    [UPBIT, 'UPBIT', SPOT],
]

exchange_names = [exchange[1] for exchange in exchanges]
futures_exchange_names = [exchange[1] for exchange in exchanges if exchange[2] == FUTURES]
spot_exchange_names = [exchange[1] for exchange in exchanges if exchange[2] == SPOT]

currencies = "BCH,BNB,BSV,BTC,CNY,EOS,ETH,EUR,JPY,LTC,USD,USDT,XRP,XTZ".split(',')


def get_currencies_in_pair(pair):
    if 'PERPETUAL' in pair:
        return pair.replace('-PERPETUAL', ''), 'USD'
    if '-' in pair:
        return tuple(pair.split('-'))
    if len(pair) == 6:
        return pair[0:3].replace('XBT', 'BTC'), pair[3:6]
    else:
        raise Exception('unknown currency pair')


def get_pair_from_currencies(exchange, ccy1, ccy2):
    if exchange == 'DERIBIT':
        return ccy1 + '-PERPETUAL'
    if exchange == 'BITMEX':
        return ccy1.replace('BTC', 'XBT') + ccy2
    return f'{ccy1}-{ccy2}'


def get_all_coins():
    all_currencies = set()
    for exchange in exchanges:
        pairs = exchange[0]
        for pair in pairs:
            if '-' in pair:
                ccy1, ccy2 = pair.split('-')
                if ccy1 != 'XBT':
                    all_currencies.add(ccy1.lower())
                all_currencies.add(ccy2.lower())
    return all_currencies


def get_pic_link(coin):
    try:
        r = requests.get('https://www.cryptocompare.com/coins/' + coin + '/overview')
        url = r.text.split('<meta ng-meta-update-content="pageInfo.getOgImage()" name="twitter:image" content="')[1].split(
            '" />')[0]
        print(url)
        return url
    except Exception as e:
        print(coin, e)


def get_coin_pictures():
    coins = list(get_all_coins())
    pics = {coin: get_pic_link(coin) for coin in coins}
    pics['eur'] = 'https://ro.m.wikipedia.org/wiki/Fi%C8%99ier:Euro_symbol_black.svg'
    pics['gbp'] = 'https://image.flaticon.com/icons/svg/33/33917.svg'
    pics['usd'] = 'http://icon-library.com/images/usd-icon/usd-icon-5.jpg'
    pics['cny'] = 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/ed/Yuan_sign_single.svg/1200px-Yuan_sign_single.svg.png'
    pics['jpy'] = 'http://icons.iconarchive.com/icons/icons8/ios7/256/Finance-Jpy-icon.png'

# x = get_coin_pictures()
