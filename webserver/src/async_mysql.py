import aiomysql


class MySQLClient:
    def __init__(self, loop):
        self.pool = loop.run_until_complete(aiomysql.create_pool(
		host='mysql',
		user='root',
                password='root',
		db='crypto',
                maxsize=50,
		loop=loop))

        self.TABLES = {
            'Arb': (  # add account_id
                'ask_price',
                'bid_price',
                'volume',
                'base_currency',
                'quote_currency',
                'instrument_pair',
                'ask_exchange',
                'bid_exchange',
		'arb',
		'arb_type',
		'profit',
                'timestamp',
            ),
        }

    def send_queries(self, queries, values):
        pass

    async def get_last_arb_id(self):
        query = 'SELECT arb_id FROM Arb ORDER BY CONVERT(arb_id, UNSIGNED) DESC LIMIT 1'
        result = await self.query(query, num_rows=1)
        return result

    async def reset_table(self):
        query = 'DROP TABLE Arb'
        result = await self.query(query)
        #
        query = (
            f'CREATE TABLE Arb('
                f'arb_id VARCHAR(64),'
                f'ask_price VARCHAR(64),'
                f'bid_price VARCHAR(64),'
                f'volume VARCHAR(64),'
                f'base_currency VARCHAR(32),'
                f'quote_currency VARCHAR(32),'
                f'instrument_pair VARCHAR(32),'
                f'ask_exchange VARCHAR(32),'
                f'bid_exchange VARCHAR(32),'
                f'arb VARCHAR(64),'
                f'arb_type VARCHAR(32),'
                f'profit VARCHAR(64),'
                f'timestamp VARCHAR(64),'
                f'PRIMARY KEY ( arb_id ))')
        result = await self.query(query)
        return result

    async def query(self, query, num_rows=1):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query)
                if num_rows == 'all':
                    result = await cursor.fetchall()
                    return result

                for row in range(num_rows):
                    result = await cursor.fetchone()
                    return result

    async def insert_dict(self, table, row):
        names = []
        value_types = []
        values = []
        for k, v in row.items():
            names.append('`' + k + '`')
            values.append(v)
            value_types.append('%s')

        value_types = ','.join(value_types)
        names = ','.join(names)
        query = f'INSERT INTO `{table}` ({names}) VALUES ({value_types})'

        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, values)
            await conn.commit()

    async def insert_dicts(self, table, rows):
        # Insert data for multiple rows in one command
        # rows - list of dicts: [{..}, .. {..}]
        names = []
        value_types = []
        values = []
        # Assumes all dicts have same set of keys
        for i, row in enumerate(rows):
            values.append([])
            for k, v in row.items():
                if i == 0:
                    names.append('`' + k + '`')
                    value_types.append('%s')
                values[i].append(v)
        value_types = ','.join(value_types)
        names = ','.join(names)
        query = f'INSERT INTO `{table}` ({names}) VALUES ({value_types})'

        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.executemany(query, values)
            await conn.commit()

    async def insert(self, table, values):
        query = f'INSERT INTO `{table}` ('
        _fields = ''
        for f in self.TABLES[table]:
            _fields += '`' + f + '`, '
        _fields = _fields[:-2] + ')'
        query += _fields + ' VALUES ('
        _values = ''
        for v in values:
            _values += '%s, '
        _values = _values[:-2] + ')'
        query += _values

        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, values)
            await conn.commit()

    async def read(self, table, num_rows=1):
        _fields = ''
        for f in self.TABLES[table]:
            _fields += f'`{f}`, '
        _fields = _fields[:-2]
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                query = f'SELECT {_fields} FROM `{table}`'
                cursor.execute(query)
                if num_rows == 'all':
                    result = cursor.fetchall()
                    return result

                for row in range(num_rows):
                    result = cursor.fetchone()
                    return result

    async def close(self):
        await self.pool.wait_closed()
