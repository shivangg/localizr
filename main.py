# The function localize takes the following arguments:
#
# colors:
#        2D list, each entry either 'R' (for red cell) or 'G' (for green cell)
#
# measurements:
#        list of measurements taken by the robot, each entry either 'R' or 'G'
#
# motions:
#        list of actions taken by the robot, each entry of the form [dy,dx],
#        where dx refers to the change in the x-direction (positive meaning
#        movement to the right) and dy refers to the change in the y-direction
#        (positive meaning movement downward)
#        NOTE: the *first* coordinate is change in y; the *second* coordinate is
#              change in x
#
# sensor_right:
#        float between 0 and 1, giving the probability that any given
#        measurement is correct; the probability that the measurement is
#        incorrect is 1-sensor_right
#
# p_move:
#        float between 0 and 1, giving the probability that any given movement
#        command takes place; the probability that the movement command fails
#        (and the robot remains still) is 1-p_move; the robot will NOT overshoot
#        its destination in this exercise
#
# The function should RETURN (not just show or print) a 2D list (of the same
# dimensions as colors) that gives the probabilities that the robot occupies
# each cell in the world.
#
# Compute the probabilities by assuming the robot initially has a uniform
# probability of being in any cell.
#
# Also assume that at each step, the robot:
# 1) first makes a movement,
# 2) then takes a measurement.
#
# Motion:
#  [0,0] - stay
#  [0,1] - right
#  [0,-1] - left
#  [1,0] - down
#  [-1,0] - up

def localize(colors, measurements, motions, sensor_right, p_move):
    # initializes p to a uniform distribution over a grid of the same dimensions as colors
    pinit = 1.0 / float(len(colors)) / float(len(colors[0]))
    p = [[pinit for row in range(len(colors[0]))] for col in range(len(colors))]

    # >>> Insert your code here <<<
    # sense
    for i in range(len(motions)):


        # move right
        U = motions[i][1]
        p = mover_right(p, U, p_move)
        normalize(p)
        # show(p)

        # move down
        U = motions[i][0]
        p = mover_down( p, U, p_move)
        normalize(p)
        # show(p)

        U = measurements[i]
        p = sense(p, U, sensor_right, colors)
        normalize(p)
        # show(p)

    return p

def sense(p, U, sensor_right, colors):

    summer = 0
    for x in range(len(colors)):
        for y in range(len(colors[0])):
            hit = (colors[x][y] == U)
            p[x][y] = p[x][y] * (sensor_right * hit + (1 - hit) * (1 - sensor_right))
        summer += sum(p[x])
    for x in range(len(colors)):
        for y in range(len(colors[0])):
            p[x][y] /= summer

    return p

def mover_down(p1, U, p_move):
    p2 = [[0 for row in range(len(p1[0]))] for col in range(len(p1))]
    for y in range(len(p1[0])):
        q = [p1[k][y] for k in range(len(p1[0]))]
        q = move(q, U, p_move)
        #     array in the down direction
        for k in range(len(p1)):
            p2[k][y] = q[k]
    return p2

def mover_right(p,U,p_move):
    p1 = [[0 for row in range(len(p[0]))] for col in range(len(p))]
    for x in range(len(p)):
        q = [p[x][y] for y in range(len(p[x]))]
        q = move(q, U, p_move)

        for k in range(len(p1)):
            p1[x][k] = q[k]

    return p1

def move(arr, U, p_move):
    q= []
    for i in range(len(arr)):
        s = p_move * arr[(i - U) % len(arr)]
        s += (1 - p_move) * arr[(i - U + 1) % len(arr)]

        q.append(s)

    # for x in range(len(q)):
    #     q[x] /= summer

    return q

def normalize(p):
    summer = 0
    for x in range(len(p)):
        for y in range(len(p[0])):
            summer +=p[x][y]

    for x in range(len(p)):
        for y in range(len(p[0])):
            p[x][y] /= summer

    return p


def show(p):
    rows = ['[' + ','.join(map(lambda x: '{0:.5f}'.format(x), r)) + ']' for r in p]
    print('[' + ',\n '.join(rows) + ']')


#############################################################
# For the following test case, your output should be
# [[0.01105, 0.02464, 0.06799, 0.04472, 0.02465],
#  [0.00715, 0.01017, 0.08696, 0.07988, 0.00935],
#  [0.00739, 0.00894, 0.11272, 0.35350, 0.04065],
#  [0.00910, 0.00715, 0.01434, 0.04313, 0.03642]]
# (within a tolerance of +/- 0.001 for each entry)

# colors = [['R','G','G','R','R'],
#           ['R','R','G','R','R'],
#           ['R','R','G','G','R'],
#           ['R','R','R','R','R']]
# measurements = ['G','G','G','G','G']
# motions = [[0,0],[0,1],[1,0],[1,0],[0,1]]
colors = [['G', 'G', 'G'],
          ['G', 'R', 'R'],
          ['G', 'G', 'G']]
measurements = ['R', 'R']
motions = [[0,0], [0,1]]
sensor_right = 1.0
p_move = 1.0
p = localize(colors,measurements,motions,sensor_right,p_move)
# p = localize(colors,measurements,motions,sensor_right = 0.7, p_move = 0.8)
show(p)  # displays your answer
# p = [[0,0,0],
#      [0, 1,0,],
#      [0, 0, 0]]
# motions = [[0,1], [0,1]]
# show(mover_right(p,motions,p_move))

# problem in only p_move
# row 1 should have the same numbers. Why is it not so when 0 < p_move < 1.0
