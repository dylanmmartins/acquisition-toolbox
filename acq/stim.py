import argparse
import acq

def stim(stimulus_name, screen_id=1): # should include calibrated monitor name

    if stimulus_name == 'gratings':

        stimobj = acq.DriftingGratings(screen_id=screen_id)
        stimobj.make_stim_stack()
        stimobj.show()

        return stimobj  # moves stimobj from local scope to global scope
                        # temporary solution to be able to look up attributes

    elif stimulus_name == 'checkerboard':

        stimobj = acq.Checkerboard(screen_id=screen_id)
        stimobj.make_stim_stack()
        stimobj.show()

        return stimobj

def stim_from_arg(): # should include calibrated monitor name

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
    
    print('stimulus: ' + stimulus_name + '\n' + 'screen nr: ' + str(screen_id))

    stim(stimulus_name, screen_id)


if __name__ == '__main__':
    
    stim_from_arg()