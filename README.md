# whatsapp-to-slack

### Introduction
whatsapp-to-slack is a tool that converts your exported WhatsApp chat (must be exported from the mobile app) to a CSV file that can be imported into Slack.

Note: The conversion is done locally. No data is shared with the internet!

### Setup
Ensure Python 3.x is installed on your computer. It's recommended to create a virtual Python environment to install the dependencies.

Once you have Python installed, it is a good practice to create a virtual python environment to install the dependencies.

To create a virtual environment:

```
python -m venv venv
```

Once you’ve created the virtual environment, you need to activate it. On Windows, run:

```
venv\Scripts\activate
```

On Unix or MacOS, run:

```
source venv/bin/activate
```

Now, install the dependencies

```
pip install pandas colorama
```

Everything should work correctly now.

### Help

For an overview of available arguments, use:

```
python src/main.py -h
```

This will display:
```
  -h, --help            Show this help message and exit
  -source               WhatsApp file containing the exported chat. It MUST be exported from Whatsapp Mobile App
  -resultset            Filename of the resultset. CSV extension should be included in the filename
  -channel              Slack channel name
  -datesep              Specifies the separator character that appears between the year, month, and day
  -formatdatetime       Full DateTime Format. Must define 'datesep' as well. Default: %m/%d/%y %H:%M  
```

### Usage

Example command to convert the sample:

```
python src/main.py -source samples/conversations.txt -channel SAMPLE
```


```
// Exmaple including datetime formating
python src/main.py -source samples/conversations.txt -channel SAMPLE -datesep=. -formatdatetime=%d.%m.%Y\ %H:%M
```

Both examples create a file named `OUTPUT-conversations.csv` in the 'samples' folder, which can be imported to Slack.

### How to Import

Note: You need to be the workspace administrator.

1. Go to https://sodyo.slack.com/admin
1. Login with an administrator
1. Click on "Settings & Permissions"
1. Click on "Import/Export Data"
1. Then click on 'Import' CSV
1. Click on 'choose file' and select you converted file
1. Start Import
1. After this phase is done, you will get an email updating you how to move to the next phase

Reference: https://slack.com/help/articles/360035354694-Move-data-to-Slack-using-a-CSV-or-text-file#:~:text=Upload%20your%20file%20to%20Slack,next%20to%20CSV%2FText%20File.

----
Acknowledgment: This project uses parts of the code from [whatsapp-converter](https://github.com/sandsturm/whatsapp-converter/).
