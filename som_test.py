def test_som(sumo_wrestlers_height=None,sumo_wrestlers_weight=None,basketball_players_height=None,basketball_players_weight=None,label1=None,label2=None,xlabel=None,ylabel=None):
    if sumo_wrestlers_height is None:
        sumo_wrestlers_height = [ 4, 2, 2, 3, 4 ]
        sumo_wrestlers_weight = [ 8, 6, 2, 5, 7 ]
        basketball_players_height = [ 3, 4, 5, 5, 3 ]
        basketball_players_weight = [ 2, 5, 3, 7, 3 ]
    import pylab as pl
    f,ax = pl.subplots()
    if label1 is None:
        label1 = "Sumo wrestlers"
    if label2 is None:
        label2 = "Basketball players"
    if xlabel is None:
        xlabel = 'Height'
    if ylabel is None:
        ylabel = 'Weight'
    ax.plot(sumo_wrestlers_height, sumo_wrestlers_weight, 'ro',
           linewidth=2, label=label1)
    ax.plot(basketball_players_height, basketball_players_weight, 'bx',
           linewidth=2, label=label2)
    ax.set_xlim(0, max(max(sumo_wrestlers_height),max(basketball_players_height)))
    ax.set_ylim(0, max(max(sumo_wrestlers_weight),max(basketball_players_weight)))
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    pl.legend()
    import numpy as np

    # transpose to have observations along the first axis
    sumo_data = np.vstack((sumo_wrestlers_height,
                          sumo_wrestlers_weight)).T
    # same for the baskball data
    basketball_data = np.vstack((basketball_players_height,
                                basketball_players_weight)).T
    # now stack them all together
    all_data = np.vstack((sumo_data, basketball_data))
    # creates: [  1,  1,  1,  1,  1, -1, -1, -1, -1, -1]
    all_desired_output = np.array([1]*len(sumo_wrestlers_weight)+[-1]*len(basketball_players_weight))
    zero_meaned_data = all_data - all_data.mean(axis=0)
    # compute pseudo-inverse as a matrix
    pinv = np.linalg.pinv(np.mat(zero_meaned_data))
    # column-vector of observations
    y = all_desired_output[np.newaxis].T

    weights = pinv * y
    gridspec = np.linspace(-1, 1, 20)
    input_space_X, input_space_Y = np.meshgrid(gridspec, gridspec)

    # for the rest it is easier to have `weights` as a simple array, instead
    # of a matrix
    weights = weights.A

    weighted_output_Z = input_space_X * weights[0] + input_space_Y * weights[1]
    pl.figure()
    pl.pcolor(input_space_X, input_space_Y, weighted_output_Z,
             cmap=pl.cm.Spectral)
    pl.plot(zero_meaned_data[all_desired_output == 1, 0],
           zero_meaned_data[all_desired_output == 1, 1],
           'ro', linewidth=2, label=label1)
    pl.plot(zero_meaned_data[all_desired_output == -1, 0],
           zero_meaned_data[all_desired_output == -1, 1],
           'bx', linewidth=2, label=label2)
    pl.xlim(-1, 1)
    pl.ylim(-1, 1)
    pl.colorbar()
    pl.xlabel('Demeaned '+label1)
    pl.ylabel('Demeaned '+label2)
    pl.title('Decision output')
    pl.legend()


    pl.show()
