from collections import deque
import sys
import os
import math
import numpy as np
import pandas as pd
import datetime
import time

lenStateCOunt = 0
resultEpisode = {}
appName = "canva"

def time_convert(sec):
  mins = sec // 60
  sec = sec % 60
  hours = mins // 60
  mins = mins % 60
  print("Time Lapsed = {0}:{1}:{2}".format(int(hours),int(mins),sec))

def saveEpisodeResult(timeStart,timeEnd,noEp, noState):
    timeEp = timeStart - timeEnd
    resultEpisode[noEp] = [timeEp, noState]

def saveEpToCSV():
    st = pd.DataFrame.from_dict(resultEpisode, orient = "index")
    if not os.path.exists('Episode.csv'):
        st.to_csv(str("Episode.csv"))
    else: # else it exists so append without writing the header
        y = 1
        yy ="("+ str(y) +")Episode.csv"
        while os.path.exists(yy):
            y += 1
            yy ="("+ str(y) +")Episode.csv"
        st.to_csv(yy)
   



def save_rewards_csv(average_reward_per_100_episodes, best_average_reward_per_100_episodes):
    episodes = np.arange(1, len(average_reward_per_100_episodes) + 1)
    reward_per_episode_df = pd.DataFrame({
        'average_reward_per_100_episodes': average_reward_per_100_episodes,
        'best_average_reward_per_100_episodes': best_average_reward_per_100_episodes,
        'episodes': episodes
    })
    reward_per_episode_df.to_csv('rewards_plot_data.csv')


def interact(env, agent, num_episodes=30, window=1):
    """ Monitor agent's performance.
    
    Params
    ======
    - env: instance of OpenAI Gym's Taxi-v1 environment
    - agent: instance of class Agent (see Agent.py for details)
    - num_episodes: number of episodes of agent-environment interaction
    - window: number of episodes to consider when calculating average rewards

    Returns
    =======
    - avg_rewards: deque containing average rewards
    - best_avg_reward: largest value in the avg_rewards deque
    """
    # initialize average rewards
    average_reward_per_100_episodes = []
    best_average_reward_per_100_episodes = []
    avg_rewards = deque(maxlen=num_episodes)
    # initialize best average reward
    best_avg_reward = -math.inf
    # initialize monitor for most recent rewards
    samp_rewards = deque(maxlen=window)


    answer = input("Load QTable? (y/n) ?")
    if answer == "y":
    # Do this.
        an = input("Name ?")
        agent.q_table.readQ(an)
        agent.q_table.readStateList(an)
        agent.observation_space = np.size(agent.q_table.q, 0)
        agent.q_table.stateCount = len(agent.q_table.stateList)
        #print("files not found")
    elif answer == "n":
    # Do that.
        pass
    else:
        print("Please enter y or n")

    start_time = time.time()
    # for each episode
    for i_episode in range(1, num_episodes+1):
        # begin the episode
        state_array,state, state_with_act = env.reset()
        #if  state <= agent.q_table.observation_space -1:
            #print('next state is in q table')
        y =  agent.q_table.addStateList(state_with_act[state][4], state_with_act[state][1], state_with_act[state][2])
        if y != -1:
            print ("state is in the stateList")
        else : 
            #agent.addState(state)
            y= agent.q_table.stateCount
        # initialize the sampled reward
        samp_reward = 0
        while True:
            #print("new action starts")
            # agent selects an action
            action = agent.select_action(y)
            # agent performs the selected action
            next_state, reward,done, indices, stateENV, action_count = env.step(action)
            time.sleep(0.3)
            #print("indices =")
            #print(indices)
            # agent performs internal updates based on sampled experience
            
            #if  next_state <= agent.q_table.observation_space -1:
                #print('next state is in q table')
            x =  agent.q_table.addStateList(stateENV[next_state][4], stateENV[next_state][1], stateENV[next_state][2])
            if x != -1:
               print ("state is in the stateList")
            else : 
                #agent.addState(state)
                x= agent.q_table.stateCount
            #print ("next state ="+str(next_state))
            #print ("observation_space" + str(agent.q_table.observation_space-1))
            #agent.step(state, action, reward, next_state, indices)
            agent.step(y, action, reward, x, indices)
            #print('stateList = ')
            #print(agent.q_table.stateList)
            # update the sampled reward
            samp_reward += reward
            # update the state (s <- s') to next time step
            y = x
            agent.update_epsilon()
            if done:
                # save final sampled reward
                samp_rewards.append(samp_reward)
                break
        
        lenStateCOunt = len(agent.q_table.stateList)
        time_end = time.time()
        saveEpisodeResult(start_time,time_end,i_episode, lenStateCOunt)


        

        if (i_episode >= 100):
            # get average reward from last 100 episodes
            avg_reward = np.mean(samp_rewards)
            # append to deque
            avg_rewards.append(avg_reward)
            # update best average reward
            print('episode average reward {}'.format(avg_reward))
            average_reward_per_100_episodes.append(avg_reward)
            best_average_reward_per_100_episodes.append(best_avg_reward)
            if avg_reward > best_avg_reward:
                best_avg_reward = avg_reward
        print ("State with activities =")
        for key,value in stateENV.items():
            print(str(key) + '. ')
            print(str(stateENV[key][0]) + ', ' + str(stateENV[key][1])+ ', ' + str(stateENV[key][2]) + ', ' + str(stateENV[key][4]))
            
        # monitor progress
        print("\rEpisode {}/{} || Best average reward {} || eps {} ".format(i_episode, num_episodes, best_avg_reward, agent.epsilon), end="")
        sys.stdout.flush()
        
        # check if task is solved (according to OpenAI Gym)
        if best_avg_reward >= 9.7:
            print('\nEnvironment solved in {} episodes.'.format(i_episode), end="")
            agent.q_table.saveQ(best_avg_reward,appName)
            agent.q_table.saveStateList(appName)
            print("width = "+ str(action_count))
            saveEpToCSV()
            save_rewards_csv(average_reward_per_100_episodes, best_average_reward_per_100_episodes)
            break
        if i_episode == num_episodes: 
            agent.q_table.saveQ(best_avg_reward,appName)
            agent.q_table.saveStateList(appName)
            print("width = "+ str(action_count))
            saveEpToCSV()
            save_rewards_csv(average_reward_per_100_episodes, best_average_reward_per_100_episodes)
            print('\n')

    end_time = time.time()
    time_lapsed = end_time - start_time
    time_convert(time_lapsed)
    return avg_rewards, best_avg_reward
    print("width = "+ str(action_count))