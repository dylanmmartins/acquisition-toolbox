


import argparse

import acq


def stim(stimulus_name, screen_id):

    if stimulus_name=='gratings':

        gt_props = {
            'num_orientations': 8,
            'sf_list': [0.01, 0.02, 0.04],
            'tf_list': [1, 2, 4],
            'shuffle': True,
            'num_repeats': 1,
            'on_time': 2,
            'off_time': 0.5
        }
        stimobj = acq.DriftingGratings(gt_props, screen_id=screen_id)
        stimobj.make_stim_stack()
        stimobj.show()

def stim_from_arg():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-st',
        '--stim',
        type='str',
        default='gratings',
        choices=[
            'gratings',
            'checkerboard',
            'whitenoise',
            'natmovie',
            'natimgs',
            'sparsenoise'
        ]
    )
    parser.add_argument(
        '-sc',
        '--screen',
        type=str,
        default='3'
    )
    args = parser.parse_args()

    stimulus_name = args.stim
    screen_id = int(args.screen)

    stim(stimulus_name, screen_id)


if __name__ == '__main__':
    
    stim_from_arg()