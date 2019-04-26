# Download 10-year historical csv stock prices
# from https://www.nasdaq.com/symbol/epam/historical
# (select 10 years and click download on the bottom of the page)
# and write a program to create a graph like attached.

import matplotlib.pyplot as plt
import pandas as pd
import json

#config file to take all params
CONFIG_FILE = 'config5.json'

def main(config_file):
    ''' Create a graph showing stock prices based on the input file from config5.json'''

    #open config file and parse into dict
    with open(config_file, 'r') as config_file:
        config = json.load(config_file)
    ##print configs to console
    # print(config)

    #read input data file into pandas daat set
    data = pd.read_csv(config['data_file'])

    #if we need to convert data in to date format, let's do that
    if 'convert_to_date' in config:
        data[config['convert_to_date']] = pd.to_datetime(data[config['convert_to_date']],
                                                         infer_datetime_format=True)
    ##print out head of data set just to check
    # print(data.head())

    #take existing axes
    ax = plt.gca()
    #for each line/.chart to draw in the plot
    # (we might want to take open/close in adition to low/high)
    for plot in config['plots']:
        #add this plot to our axis
        data.plot(kind=plot['kind'],
                 x=plot['x'],
                  y=plot['y'],
                 label=plot['label'],
                color=plot['color'],
                ax=ax)

    #add all labels and print legend
    plt.xlabel(config['labels']['xlabel'])
    plt.ylabel(config['labels']['ylabel'])
    plt.title(config['labels']['title'])
    plt.legend()

    ##show chart just to check
    # plt.show()
    #dave it to file in propser format and DPI
    plt.savefig(config['result_file'],
                format=config['format'],
                dpi=int(config['DPI']))


if __name__ == '__main__':
    main(CONFIG_FILE)
