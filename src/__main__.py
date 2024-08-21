import argparse
import sys
import os
import csv
import time
import datetime
import pandas as pd
import whatsApp2csv as wc

def main():
    parser = argparse.ArgumentParser(prog='whatsapp2slack', description='Use whatsapp2slack to convert your exported WhatsApp chat to a slack CSV format', epilog='For reporting bugs or requesting features, please visit https://github.com/sandsturm/whatsapp-converter/ and create an issue')
    parser.add_argument('-source', metavar='source', type=str, help='WhatsApp file containing the exported chat. It MUST be exported from Whatsapp Mobile App')
    parser.add_argument('-resultset', required=False, help='filename of the resultset. CSV extension should be included in the filename')
    parser.add_argument('-channel', help='slack channel name')

    args = parser.parse_args()

    if not str( args.source ):
        print("ERROR: needs an import file")
        sys.exit()

    resultset = args.resultset
    if resultset == None:
        with open(args.source, "r", encoding="utf-8") as f:
            folder_name = os.path.dirname(f.name)
            file_name = os.path.basename(f.name)

            resultset = f'{folder_name}/OUTPUT-{file_name}'

            print(f"NOTE: output filename parameter is missed. You can find the output at: {resultset}")

    if not str( args.channel ):
        print("ERROR: needs define slack channel")
        sys.exit()

    whatsapp2slack(args.source, resultset, args.channel)


def whatsapp2slack(source, resultset, channel):
    print('Start WhatsApp to Slack Convertion')
    print(f'Source Filename: {source}')
    print(f'Target Filename: {resultset}')
    print(f'Slack Channel: {channel}')

    messages = wc.whatapp2csv(source)

    rows = []
    for row in messages:
        element = datetime.datetime.strptime(f'{row[0]} {row[1]}',"%m/%d/%y %H:%M")
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

    # source = 'files/WhatsApp Chat - Alon_Cathy_Sebastian.txt'
    # resultset = 'files/OUTPUT2-WhatsApp Chat - Alon_Cathy_Sebastian.csv'
    # channel = 'XXX'

    # whatsapp2slack(source, resultset, channel)