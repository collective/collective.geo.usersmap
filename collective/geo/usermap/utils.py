# -*- coding: utf-8 -*-


def coordinate_transform(coordinate, unique_coordinates):
    '''
    Takes a coordinate (a tuple of two floats) and a list of unique
    coordinates. If the coordinate does not exist in the list, it is
    added to the list and returned
    If the coordinate already exists in the list, compute a new coordinate
    with a small offset that is unique, add it to the list and return it.
    The list is modified within the function!
    If the coordinate is not
    '''
    # make sure we have a two float tuple
    if (not isinstance(coordinate, (tuple, list)) or
        len(coordinate) != 2 or
        not isinstance(coordinate[0], float) or
        not isinstance(coordinate[1], float)):
        return (None, None)

    step = 0.01  # distance for a step in decimal degrees

    # draw a star around a central coordinate with 4 points building an
    # inner square and 4 point building an outer square rotated 45°
    steps = [
        lambda coord, start:(coord[0] + (start + 1) * step,
                             coord[1] + (start + 1) * step),
        lambda coord, start:(coord[0] - (start + 1) * step,
                             coord[1] + (start + 1) * step),
        lambda coord, start:(coord[0] - (start + 1) * step,
                             coord[1] - (start + 1) * step),
        lambda coord, start:(coord[0] + (start + 1) * step,
                             coord[1] - (start + 1) * step),
        lambda coord, start:(coord[0] + (start + 2) * step,
                             coord[1]),
        lambda coord, start:(coord[0],
                             coord[1] + (start + 2) * step),
        lambda coord, start:(coord[0] - (start + 2) * step,
                             coord[1]),
        lambda coord, start:(coord[0],
                             coord[1] - (start + 2) * step),
        ]

    unique = coordinate
    start = 0
    index = 0
    while unique in unique_coordinates:
        unique = steps[index](coordinate, start)
        index = index + 1
        if index == 8:
            index = 0
            start = start + 2
    # modifies the list that is passed in without returning it!
    unique_coordinates.append(unique)
    return unique
