import argparse
import sys
import os
import csv
import datetime
from colorama import Fore, Back, Style
import pandas as pd
import whatsApp2csv as wc

def main():
    parser = argparse.ArgumentParser(prog='whatsapp2slack', description='Use whatsapp2slack to convert your exported WhatsApp chat to a slack CSV format', epilog='For reporting bugs or requesting features, please visit https://github.com/spederiva/whatsapp-to-slack and create an issue')
    parser.add_argument('-source', type=str, help='WhatsApp file containing the exported chat. It MUST be exported from Whatsapp Mobile App')
    parser.add_argument('-resultset', required=False, help='Filename of the resultset. CSV extension should be included in the filename')
    parser.add_argument('-channel', help='Slack channel name')
    parser.add_argument('-datesep', default='/', help='Specifies the separator character that appears between the year, month, and day')
    parser.add_argument('-formatdatetime', required=False, help='Full DateTime Format. Must define \'datesep\' as well. Default: %%m/%%d/%%y %%H:%%M')

    args = parser.parse_args()

    if not str( args.source ):
        print("ERROR: needs an import file")
        sys.exit()

    # Check 
    fname = ''
    try:
        with open(args.source, "r", encoding="utf-8") as f:
            fname = f.name
    except:
        print('File does NOT exists. Please check file path')
        exit()

    resultset = args.resultset
    if resultset == None:
        folder_name = os.path.dirname(fname)
        file_name = os.path.basename(fname).rpartition('.')[0]

        resultset = f'{folder_name}/OUTPUT-{file_name}.csv'

        print(Fore.GREEN + f"NOTE: output filename parameter is missed. Output file will be located at: {resultset}\n" + Style.RESET_ALL)

    if not str( args.channel ):
        print("ERROR: needs define slack channel")
        sys.exit()

    datesep = args.datesep
    date_format = f"%m{datesep}%d{datesep}%y"
    time_format = "%H:%M"
    datetime_format = f"{date_format} {time_format}" if args.formatdatetime is None else args.formatdatetime

    whatsapp2slack(args.source, resultset, args.channel, datesep, datetime_format)


def whatsapp2slack(source, resultset, channel, datesep, datetime_format):
    print(Fore.BLUE + 'Start WhatsApp to Slack Convertion\n' + Style.RESET_ALL)
    print(f'Source Filename: {source}')
    print(f'Target Filename: {resultset}')
    print(f'Slack Channel: {channel}')
    print(f'DateTime Format: {datetime_format}')
    print(f'Using Date Separator: {datesep}')

    messages = wc.whatapp2csv(source, datesep)

    try:
        rows = []
        for row in messages:
            element = datetime.datetime.strptime(f'{row[0]} {row[1]}', datetime_format)
            timestamp = datetime.datetime.timestamp(element)    

            dict={
                'timestamp': int(timestamp),
                'channel': channel,
                'username': row[2],
                'message': row[3]
            }

            rows.append(dict)
    except ValueError:
        print(Fore.RED + '\nTime Format was not define propertly')
        exit()
    except Exception as error:
        print(f'\nSome error occured: {error}')
        exit()

    columns = ['timestamp', 'channel', 'username', 'message']
    df = pd.DataFrame(columns=columns, data=rows)

    df.to_csv(resultset,index=False, header=False, quoting=csv.QUOTE_ALL)
    print(f'\nFile was succesfully saved at: {resultset}')


if __name__ == "__main__":
    main()