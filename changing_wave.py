# imports
import synthtree

import wave


# important parameters
length = 12.0
framerate = 44100
num_segments = 30
resolution = 40

# define the change
def update_tree(tree, seg, x):
    tree[143: 146] = (x * 0.9 - 0.4, -x * 0.6 + 0.4, x * 0.5 - 0.3)
    tree[100 - seg: 100 - seg + 2] = ((x ** 2 / 3) + x * 0.1 - 0.2, ((x * 3) ** 2) / 11 - 0.4)

def update_tree_segment(tree, seg):
    tree[0 : 300] = 0.0
    tree[300 + seg] = 0.2
    tree[280] = 0.5 - seg / 27

# -----------

# detected parameters
total_frames = int(framerate * length)
segment_size = int(total_frames // num_segments // resolution)

tree = synthtree.SynthTree()
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
        seg = int(x * num_segments)

        update_tree(tree, seg, x)
        wfp.writeframes(stream.read(segment_size))

        if i % num_segments == (num_segments - 1):
            segment += 1
            update_tree_segment(tree, segment)
        
        print('\rProgress: ({}/{}) {:.2f}%\r'.format(i, num_segments * resolution, 100 * i / (num_segments * resolution)), end='')

    print('\rProgress: ({0}/{0}) 100.00%'.format(num_segments * resolution))

    print()
