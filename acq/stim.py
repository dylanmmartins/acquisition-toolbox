


import argparse

import acq


def stim(stimulus_name, screen_id=2):

    if stimulus_name=='gratings':

        gt_props = {
            'num_orientations': 8,
            'sf_list': [0.04], # [0.01, 0.02, 0.04],
            'tf_list': [1], # [1, 2, 4], # not currently used
            'shuffle': True,
            'num_repeats': 1,
            'on_time': 2,
            'off_time': 0.5
        }
        stimobj = acq.DriftingGratings(gt_props, screen_id=screen_id)
        stimobj.make_stim_stack() # this is defined in gratings.py
        stimobj.show()            # this function is defined in gratings.py

        return stimobj  # moves stimobj from local scope to global scope
                        # temporary solution to be able to look up attributes

    else:
        print('You might have made a typo, or this stimulus type is \
              not available yet.')

def stim_from_arg(): # this specifies what flags we can set in the terminal
                     # to play the stimuli

    parser = argparse.ArgumentParser()
    parser.add_argument( # 1st flag, defining the type of stimulus
        '-st',
        '--stim',
        type=str,
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
    parser.add_argument( # 2nd flag, defining projection screen
        '-sc',
        '--screen',
        type=str,
        default=1
    )
    args = parser.parse_args()

    stimulus_name = args.stim
    screen_id = int(args.screen)

    stim(stimulus_name, screen_id)

    print('stimulus: ' + stimulus_name + '\n' + 'screen nr: ' + str(screen_id))


if __name__ == '__main__':
    
    stim_from_arg()