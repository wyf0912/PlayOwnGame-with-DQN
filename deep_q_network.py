#!/usr/bin/env python
from __future__ import print_function

import tensorflow as tf

import sys
import ball as game
import random
import numpy as np
from collections import deque
import tensorboard

GAME = 'PlayBall' # the name of the game being played for log files
ACTIONS = 5 # number of valid actions
GAMMA = 0.99 # decay rate of past observations
OBSERVE = 100000. # timesteps to observe before training
OBSERVE = 20000.
EXPLORE = 2000000. # frames over which to anneal epsilon
EXPLORE = 800000. # frames over which to anneal epsilon
FINAL_EPSILON = 0.001 # final value of epsilon
INITIAL_EPSILON = 1# starting value of epsilon
REPLAY_MEMORY = 200000 # numberww of previous transitions to remember
BATCH = 128 # size of minibatchwa 曾经64似乎太大了
FRAME_PER_ACTION = 1
PLAYER=0 #if player=0, Two computers are antagonistic to each other .if player=1,computer use player 1,if player=2 computer use player 2

if PLAYER:
    OBSERVE=100
    EXPLORE=100000
    INITIAL_EPSILON=0.0
    FINAL_EPSILON = 0.0

def action_trans(action,player=1):

    real_action=[0,0,0,0]
    if action[0]==1:
        return real_action
    if ACTIONS==5:
        if player==2 and action[1]==1:
            real_action[1]=1;real_action[0]=0
        elif player==2 and action[2]==1:
            real_action[0] = 1;real_action[1]=0
        else:
            real_action=action[1:]
       # print(real_action)
        return real_action
    if ACTIONS == 3:
        #print(type(action))
        real_action = np.append([0,0],action[1:])
        return real_action

def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev = 0.01)
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0.01, shape = shape)
    return tf.Variable(initial)

def conv2d(x, W, stride):
    return tf.nn.conv2d(x, W, strides = [1, stride, stride, 1], padding = "SAME")

def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize = [1, 2, 2, 1], strides = [1, 2, 2, 1], padding = "SAME")

def createNetwork():
    # network weights


    W_fc1 = weight_variable([48, 96])
    b_fc1 = bias_variable([96])
    W_fc2 = weight_variable([96, 96])
    b_fc2 = bias_variable([96])
    W_fc3 = weight_variable([96, 96])
    b_fc3 = bias_variable([96])
    W_fc4 = weight_variable([96, 96])
    b_fc4 = bias_variable([96])
    W_fc5 = weight_variable([96, 96])
    b_fc5 = bias_variable([96])
    W_fc6 = weight_variable([96, 96])
    b_fc6 = bias_variable([96])
    W_fc7 = weight_variable([96, ACTIONS])
    b_fc7 = bias_variable([ACTIONS])

    # input layer
    s = tf.placeholder("float", [None,48])


    h_fc1 = tf.nn.relu(tf.matmul(s, W_fc1) + b_fc1)
    h_fc2 = tf.nn.relu(tf.matmul(h_fc1, W_fc2) + b_fc2)
    h_fc3 = tf.nn.relu(tf.matmul(h_fc2, W_fc3) + b_fc3)
    h_fc4 = tf.nn.relu(tf.matmul(h_fc3, W_fc4) + b_fc4)
    h_fc5 = tf.nn.relu(tf.matmul(h_fc4, W_fc5) + b_fc5)
    h_fc6 = tf.nn.relu(tf.matmul(h_fc5, W_fc6) + b_fc6)
    # readout layer
    readout = tf.matmul(h_fc6, W_fc7) + b_fc7
    w_fc=[W_fc1,W_fc2,W_fc3,W_fc4,W_fc5,W_fc6,W_fc7]
    return s, readout,w_fc

def trainNetwork(s, readout, sess,w_fc):
    # define the cost function
    a = tf.placeholder("float", [None, ACTIONS])
    y = tf.placeholder("float", [None]) #y是q值
    readout_action = tf.reduce_sum(tf.multiply(readout, a), reduction_indices=1)

    regularcost = tf.contrib.layers.l2_regularizer(0.001)(w_fc[0]) #L2正则化
    cost = tf.reduce_mean(tf.square(y - readout_action))+regularcost

    train_step = tf.train.AdamOptimizer(1e-6).minimize(cost)

    # open up a game state to communicate with emulator
    ball_state1, ball_state2, state1, state2, reward1, reward2,state1_ob,state2_ob,terminal = game.GameState()

    # store the previous observations in replay memory
    D1 = deque()
    D2 = deque()
    # printing
    #a_file = open("logs_" + GAME + "/readout.txt", 'w')
    #h_file = open("logs_" + GAME + "/hidden.txt", 'w')

    # get the first state by doing nothing and preprocess the image to 80x80x4
    ball_state1, ball_state2, state1, state2, reward1, reward2, state1_ob, state2_ob,terminal =game.GameState(train=1,action1=[0,0,0,0],action2=[0,0,0,0])
    x1_t=[ball_state1,state1,state2_ob]
    x2_t = [ball_state2, state2, state1_ob]
    s1_t = np.stack((x1_t, x1_t, x1_t, x1_t), axis=2)
    s2_t = np.stack((x2_t, x2_t, x2_t, x2_t), axis=2)
    s1_t = np.resize(s1_t, [1, 48])
    s2_t =np.resize(s2_t,[1,48])
    #s_t=np.asmatrix(s_t)
    # saving and loading networks
    saver = tf.train.Saver()
    checkpoint = tf.train.get_checkpoint_state("saved_networks")

    summary_writer=tf.summary.FileWriter('./logs', sess.graph)
    QMAX_val=tf.Variable(0.0)
    tf.summary.scalar('QMAX_val', QMAX_val)
    merged_summary_op = tf.summary.merge_all()

    sess.run(tf.initialize_all_variables())

    if checkpoint and checkpoint.model_checkpoint_path:
        saver.restore(sess, checkpoint.model_checkpoint_path)
        print("Successfully loaded:", checkpoint.model_checkpoint_path)
    else:
        print("Could not find old network weights")



    # start training
    epsilon = INITIAL_EPSILON
    t = 0
    while "flappy bird" != "angry bird":
        # choose an action epsilon greedily

        readout1_t = readout.eval(feed_dict={s : s1_t})[0]
        readout2_t = readout.eval(feed_dict={s: s2_t})[0]
        a1_t = np.zeros([ACTIONS])
        a2_t = np.zeros([ACTIONS])
        action_index = 0
        if t % FRAME_PER_ACTION == 0:
            if random.random() <= epsilon:
                print("----------Random Action----------")
                action_index = random.randrange(ACTIONS)
                a1_t[random.randrange(ACTIONS)] = 1
            else:
                action_index = np.argmax(readout1_t)
                a1_t[action_index] = 1
        else:
            a1_t[0] = 1 # do nothing

        if t % FRAME_PER_ACTION == 0:
            if random.random() <= epsilon:
                print("----------Random Action----------")
                action_index = random.randrange(ACTIONS)
                a2_t[random.randrange(ACTIONS)] = 1
            else:
                action_index = np.argmax(readout2_t)
                a2_t[action_index] = 1
        else:
            a1_t[0] = 1 # do nothing
            a2_t[0] = 1

        # scale down epsilon
        if epsilon > FINAL_EPSILON and t > OBSERVE :
            epsilon -= (INITIAL_EPSILON - FINAL_EPSILON) / EXPLORE

        # run the selected action and observe next state and reward
        if PLAYER==0:
            ball_state1, ball_state2, state1, state2, reward1, reward2,state1_ob,state2_ob,terminal = game.GameState(train=1,action1=action_trans(a1_t),action2=action_trans(a2_t,player=2))
        elif PLAYER==1:
            ball_state1, ball_state2, state1, state2, reward1, reward2,state1_ob,state2_ob,terminal = game.GameState(train=1,
                                                                                        action1=action_trans(a1_t),)
        else:
            ball_state1, ball_state2, state1, state2, reward1, reward2,state1_ob,state2_ob,terminal = game.GameState(train=1,
                                                                                        action2=action_trans(
                                                                                            a1_t,player=2))
        x_t1=ball_state1+state1+state2_ob
        x_t2 = ball_state2 + state2 + state1_ob
        #s1_t1 = np.append(x_t1, s1_t[:,:,1:], axis = 2)
        s1_t1 = np.append(x_t1, s1_t[0][:36])
        s1_t1=[s1_t1]
        s2_t1 = np.append(x_t2, s2_t[0][:36])
        s2_t1=[s2_t1]
        #s1_t1=np.asmatrix(s1_t1)
        # store the transition in D
        D1.append((s1_t[0], a1_t, reward1, s1_t1[0],terminal))    #上一次状态 这一次的动作 得到的奖励 到达的新的状态
        D2.append((s2_t[0], a2_t, reward2, s2_t1[0],terminal))
        if len(D1) > REPLAY_MEMORY:
            D1.popleft()
            D2.popleft()

        # only train if done observing
        if t > OBSERVE:
            # sample a minibatch to train on
            minibatch1 = random.sample(D1, BATCH)
            minibatch2 = random.sample(D2, BATCH)

            # get the batch variables
            s1_j_batch = [d[0] for d in minibatch1]
            a1_batch = [d[1] for d in minibatch1]
            r1_batch = [d[2] for d in minibatch1]
            s1_j1_batch = [d[3] for d in minibatch1] #得到的新的状态

            s2_j_batch = [d[0] for d in minibatch2]
            a2_batch = [d[1] for d in minibatch2]
            r2_batch = [d[2] for d in minibatch2]
            s2_j1_batch = [d[3] for d in minibatch2]


            y1_batch = []
            y2_batch = []
            readout1_j1_batch = readout.eval(feed_dict = {s : s1_j1_batch})
            readout2_j1_batch = readout.eval(feed_dict={s: s2_j1_batch})


            for i in range(0, len(minibatch1)):
                # if terminal, only equals reward
                terminal1 = minibatch1[i][4]
                terminal2 = minibatch2[i][4]
                if terminal1:
                    y1_batch.append(r1_batch[i])
                else:
                    y1_batch.append(r1_batch[i] + GAMMA * np.max(readout1_j1_batch[i])) #得到抽取的batch的Q值
                if terminal2:
                    y2_batch.append(r2_batch[i])
                else:
                    y2_batch.append(r2_batch[i] + GAMMA * np.max(readout2_j1_batch[i]))

            # perform gradient step
            if PLAYER==2:
                train_step.run(feed_dict = {
                    y : y1_batch,
                    a : a1_batch,
                    s : s1_j_batch}   #s1_j_batch是旧的状态
                )
            if PLAYER == 1:
                train_step.run(feed_dict={
                    y: y2_batch,
                    a: a2_batch,
                    s: s2_j_batch}
                )

            if PLAYER == 0:
                train_step.run(feed_dict={
                    y: y2_batch,
                    a: a2_batch,
                    s: s2_j_batch}
                )
                train_step.run(feed_dict = {
                    y : y1_batch,
                    a : a1_batch,
                    s : s1_j_batch}   #s1_j_batch是旧的状态
                )
            print("/Player1 Lost", cost.eval(feed_dict={
                y: y1_batch,
                a: a1_batch,
                s: s1_j_batch}))
            print("/Player1 Lost", cost.eval(feed_dict={
                y: y2_batch,
                a: a2_batch,
                s: s2_j_batch}))

        # update the old values
        s1_t = s1_t1
        s2_t = s2_t1
        t += 1

        # save progress every 10000 iterations
        if t % 10000 == 0 and PLAYER==0:
            saver.save(sess, 'saved_networks/' + GAME + '-dqn', global_step = t)

        if t % 100 == 0:
            data = sess.run(merged_summary_op)
            summary_writer.add_summary(data, t)

        # print info
        state = ""
        if t <= OBSERVE:
            state = "observe"
        elif t > OBSERVE and t <= OBSERVE + EXPLORE:
            state = "explore"
        else:
            state = "train"

        print("TIMESTEP", t, "/ STATE", state, \
            "/ EPSILON", epsilon, "/ ACTION", action_index, "/ REWARD", reward1, \
            "/ Q_MAX %e" % np.max(readout1_t))

        print( "/ ACTION", action_index, "/ REWARD", reward2, \
            "/ Q_MAX %e" % np.max(readout2_t))

        print("regularcost", regularcost.eval())
        # write info to files
        '''
        if t % 10000 <= 100:
            a_file.write(",".join([str(x) for x in readout1_t]) + '\n')
            h_file.write(",".join([str(x) for x in h_fc1.eval(feed_dict={s:[s1_t]})[0]]) + '\n')
            cv2.imwrite("logs_tetris/frame" + str(t) + ".png", x_t1)
        '''


def playGame():
    sess = tf.InteractiveSession()
    s, readout, w_fc = createNetwork()
    trainNetwork(s, readout, sess, w_fc)


def main():
    playGame()

if __name__ == "__main__":
    main()
    #print(action_trans([0,1,0,0,0],player=1))
