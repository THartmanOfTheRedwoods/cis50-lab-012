#!/usr/bin/env python3

import os
import validators
import sqlalchemy
from datetime import datetime
from datetime import timedelta
from urllib.parse import urlparse
from bijective import Bijective


class UrlHelper(object):

    def __init__(self, *args, **kwargs):

        self._short_fqdn = os.environ.get('SHORT_FQDN')
        if 'short_fqdn' in kwargs:
            self._short_fqdn = kwargs['short_fqdn']

        connection_str = os.environ.get('SA_CONNECTION_STR')
        if 'connection_str' in kwargs:
            connection_str = kwargs['connection_str']

        if connection_str:
            self._engine = sqlalchemy.create_engine(connection_str)
        else:
            drivername = os.environ.get('SA_DRIVERNAME')
            if 'divername' in kwargs:
                drivername = kwargs['divername']

            username = os.environ.get('SA_USERNAME')
            if 'username' in kwargs:
                username = kwargs['username']

            password = os.environ.get('SA_PASSWORD')
            if 'password' in kwargs:
                password = kwargs['password']

            database = os.environ.get('SA_DATABASE')
            if 'database' in kwargs:
                database = kwargs['database']

            instance_id = os.environ.get('SA_INSTANCE_ID')
            if 'instance_id' in kwargs:
                database = kwargs['instance_id']

            self._engine = sqlalchemy.create_engine(
                sqlalchemy.engine.url.URL(
                    drivername=drivername,
                    username=username,
                    password=password,
                    database=database,
                    query={
                        'unix_socket': '/cloudsql/{}'.format(instance_id)
                    }
                ),
            )

    def validateUrl(self, url):
        if validators.url(url):
            return True
        raise Exception('Unacceptable URL')

    def longUrl(self, short_url):
        self.validateUrl(short_url)

        path = "".join(urlparse(short_url).path.split('/'))
        if path:
            connection = self._engine.connect()
            metadata = sqlalchemy.MetaData()
            urls = sqlalchemy.Table('cr_urls', metadata, autoload_with=self._engine)
            # self._engine.echo = True  # We want to see the SQL we're creating

            b = Bijective()
            query = sqlalchemy.select(urls).where(urls.columns.id == b.decode(path))
            ResultProxy = connection.execute(query)
            ResultSet = ResultProxy.fetchone()
            if ResultSet:  # ResultSet is empty, so we should insert.
                return ResultSet.url

        raise Exception('Url not found.')

    def shortenUrl(self, long_url: str, expires=None):
        self.validateUrl(long_url)

        connection = self._engine.connect()
        metadata = sqlalchemy.MetaData()
        # urls = sqlalchemy.Table('cr_urls', metadata, autoload=True, autoload_with=self._engine)
        urls = sqlalchemy.Table('cr_urls', metadata, autoload_with=self._engine)
        # self._engine.echo = True  # We want to see the SQL we're creating

        # query = sqlalchemy.select([urls]).where(urls.columns.url == long_url)
        query = sqlalchemy.select(urls).where(urls.columns.url == long_url)
        ResultProxy = connection.execute(query)
        ResultSet = ResultProxy.fetchone()
        url_id = None
        if not ResultSet:  # ResultSet is empty, so we should insert.
            timestamp = (datetime.now() + timedelta(days=36525)).strftime(
                '%Y-%m-%d %H:%M:%S')  # Approximately 100 years in the future.
            if expires:
                timestamp = (datetime.now() + timedelta(days=int(expires))).strftime('%Y-%m-%d %H:%M:%S')

            stmt = urls.insert().values({'url': long_url, 'expires_at': timestamp})
            result = connection.execute(stmt)
            url_id = result.lastrowid
            connection.commit()
        else:
            url_id = ResultSet.id

        if url_id:
            b = Bijective()
            s = b.encode(url_id)

        return "{0}{1}".format(self._short_fqdn, s)


def main():
    print("Class test started...")
    uri = UrlHelper()
    short_url = uri.shortenUrl(
        'https://hydrobuilder.com/hydroponics/water-chillers-and-water-heaters/active-aqua-chiller-with-power-boost.html')
    print("Short Url: {0}".format(short_url))

    long_url = uri.longUrl(short_url)
    print("Long Url: {0}".format(long_url))


if __name__ == "__main__":
    main()
