'''
The following snippet writes a .png for each second of data in Reddit's r/place.
'''

from PIL import Image, ImageColor
from pathlib import Path
import pandas as pd
import os
from time import time

def save_frame(timestamp, directory, frame):
    filename = '{}.png'.format(str(timestamp))
    file_path = os.path.join(directory, filename)
    frame.save(file_path, 'PNG')

def main():
    with open('sorted_tiles.csv', 'r') as rptp:
        tiles = pd.read_csv(rptp)

    colors = ['#FFFFFF',
              '#E4E4E4',
              '#888888',
              '#222222',
              '#FFA7D1',
              '#E50000',
              '#E59500',
              '#A06A42',
              '#E5D900',
              '#94E044',
              '#02BE01',
              '#00E5F0',
              '#0083C7',
              '#0000EA',
              '#E04AFF',
              '#820080',
             ]
    
    # convert colors to R,G,B
    colors = [ImageColor.getrgb(color) for color in colors]
        
    #make path in which to save frames
    frames_dir = Path('frames.02')
    if not frames_dir.exists():
        frames_dir.mkdir()
        
    save_folder = os.path.join(os.getcwd(), frames_dir)

    # make an 1000x1000 pixel image
    working_frame = Image.new("RGB", (1001, 1001), 'white')
    pix = working_frame.load()
    
    # Write all pixel placements for that timestamp
    current_second = tiles.iloc[0]['ts']
    start_time = time()

    for i in range(len(tiles)):

        # once we move to the next second of our dataset
        # Save this image file, then move on.

        if tiles.iloc[i]['ts'] != current_second:
            save_frame(current_second, save_folder, working_frame)
            current_second = tiles.iloc[i]['ts']

        x = int(tiles.iloc[i]['x'])
        y = int(tiles.iloc[i]['y'])
        color = int(tiles.iloc[i]['color'])
        pix[x,y] = colors[color]

    save_frame(current_second, save_folder, working_frame)
        
    print('All done. Took this long: {}'.format(time() - start_time))

if __name__ == '__main__':
    main()

