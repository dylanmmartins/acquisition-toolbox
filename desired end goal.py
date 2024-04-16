## what the end goal is supposed to look like:
## open terminal on the experimental PC, run these

$ python -m acq.stim # this will import stim.py as a module, which we
                     # have installed in our environment with .yml file

# this is what we want to have to type into the terminal to play the stimulus

$ conda activate acq1
$ python -m acq.stim --screen 3 --stim gratings

# then it should play the specified stimulus