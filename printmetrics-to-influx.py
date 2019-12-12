import sys
import datetime as dt
from influxdb import InfluxDBClient, SeriesHelper


host = 'localhost'
db = 'ldm'
port = 8086

class HubEntry(SeriesHelper):
    class Meta:
        series_name = 'printmetrics'
        fields = ['time',
                  'load_1',
                  'load_5',
                  'load_15',
                  'local_ports',
                  'remote_ports',
                  'queue_age',
                  'queue_count',
                  'queue_bytes',]
        tags = []


def main():
    db_client = InfluxDBClient(host=host, port=port, database=db)
    db_client.create_database(db)
    HubEntry.Meta.client = db_client
    raw_metrics = sys.stdin.readlines()[0].split('\n')[0].split()
    report_time = dt.datetime.utcnow()
    HubEntry(
        time = report_time,
        load_1 = float(raw_metrics[1]),
        load_5 = float(raw_metrics[2]),
        load_15 = float(raw_metrics[3]),
        local_ports = int(raw_metrics[4]),
        remote_ports = int(raw_metrics[5]),
        queue_age = int(raw_metrics[6]),
        queue_count = int(raw_metrics[7]),
        queue_bytes = int(raw_metrics[8])
        )
    HubEntry.commit()


if __name__ == '__main__':
    main()
