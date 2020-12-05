# imports
import synthtree

import math
import wave


# important parameters
length = 12.0
framerate = 44100
num_segments = 50
resolution = 40
sine_speed = 0.6 # periods per segment_size

# define the change
def update_tree(tree, seg, x, y):
    tree[153: 156] = (y * 0.9 - 0.4, -y * 0.6 + 0.4, y * 0.5 - 0.3)
    tree[135: 137] = ((y ** 2 / 3) + y * 0.1 - 0.2, ((y * 3) ** 2) / 11 - 0.4)
    tree[80] = y / (x + 1)
    tree[81] = y ** 2 / (x + 1)
    tree[82] = y / math.sqrt((x + 1))

def update_tree_segment(tree, seg):
    #tree[0 : 400] = 0.0
    pass

# -----------

# detected parameters
total_frames = int(framerate * length)
segment_size = int(total_frames // num_segments // resolution)
sine_factor = math.tau * sine_speed * num_segments

tree = synthtree.SynthTree(resolution=512)
stream = synthtree.PCMStream(tree, signed=True)

# export
with wave.open('changing_wave.wav', 'wb') as wfp:
    wfp.setnchannels(1)
    wfp.setsampwidth(2) 
    wfp.setframerate(framerate)
    wfp.setnframes(total_frames)

    segment = 0
    
    for i in range(num_segments * resolution):
        x = i / num_segments / resolution
        y = math.sin(x * sine_factor)
        seg = int(x * num_segments)

        update_tree(tree, seg, x, y)
        wfp.writeframes(stream.read(segment_size))

        if i % num_segments == (num_segments - 1):
            segment += 1
            update_tree_segment(tree, segment)
        
        print('\rProgress: ({}/{}) {:.2f}%\r'.format(i, num_segments * resolution, 100 * i / (num_segments * resolution)), end='')

    print('\rProgress: ({0}/{0}) 100.00%'.format(num_segments * resolution))

    print()
