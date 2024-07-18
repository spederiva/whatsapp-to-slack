import argparse
import sys
import csv
import time
import datetime
import pandas as pd
import whatsApp2csv as wc

def main():
    parser = argparse.ArgumentParser(prog='whatsapp2slack', description='Use whatsapp2slack to convert your exported WhatsApp chat to a slack CSV format', epilog='For reporting bugs or requesting features, please visit https://github.com/sandsturm/whatsapp-converter/ and create an issue')
    parser.add_argument('source', metavar='source', type=str, help='WhatsApp file containing the exported chat. It MUST be exported from Whatsapp App for Windows or Mac')
    parser.add_argument('resultset', help='filename of the resultset. CSV extension should be included in the filename')
    parser.add_argument('channel', help='slack channel name')

    args = parser.parse_args()

    if not str( args.source ):
        print("ERROR: needs an import file")
        sys.exit()

    if not str( args.resultset ):
        print("ERROR: output filename is missed")
        sys.exit()

    if not str( args.channel ):
        print("ERROR: needs define slack channel")
        sys.exit()

    whatsapp2slack(args.source, args.resultset, args.channel)


def whatsapp2slack(source, resultset, channel):
    print('Start WhatsApp to Slack Convertion')
    print(f'Source Filename: {source}')
    print(f'Target Filename: {resultset}')
    print(f'Slack Channel: {channel}')

    messages = wc.whatapp2csv(source)

    rows = []
    for row in messages:
        element = datetime.datetime.strptime(f'{row[0]} {row[1]}',"%d/%m/%Y %H:%M:%S")
        timestamp = datetime.datetime.timestamp(element)    

        dict={
            'timestamp': int(timestamp),
            'channel': channel,
            'username': row[2],
            'message': row[3]
        }

        rows.append(dict)


    columns = ['timestamp', 'channel', 'username', 'message']
    df = pd.DataFrame(columns=columns, data=rows)


    df.to_csv(resultset,index=False, header=False, quoting=csv.QUOTE_ALL)


if __name__ == "__main__":
    main()    