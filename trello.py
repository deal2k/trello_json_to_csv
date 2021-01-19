# script to export Trello JSON to CSV format
# data to capture: name (card), status, label, activity (data, user, info)
import pandas as pd
import json

# read JSON file
with open('Hi43Zpsm.json', 'r') as json_file:
    json_data = json.load(json_file)

# get list of buckets(lists of cards) to DataFrame
buckets = pd.DataFrame(json_data['lists']).loc[:, ['id', 'name']].set_index('id')

# cards to DataFrame
columns = ['id', 'idList', 'closed', 'desc', 'name', 'labels']
cards = pd.DataFrame(json_data['cards']).loc[:, columns].set_index('id')
cards_num = len(cards['labels'].values)     # get total number of cards to iterate
# extract labels from dictionary
cards['labels'] = [ cards['labels'].values[i][0]['name'] for i in range(cards_num) ]

# add buckets (lists of cards) names to DataFrame 'cards'
cards = pd.merge(cards, buckets, how='left', left_on='idList', right_on='id', 
                 suffixes=('_card', '_list'), right_index=True).drop(['idList'], axis=1)

print(cards.head())

# prepare DataFrame with actions (activities)
columns = ['idMemberCreator','data','type','date']
actions = pd.DataFrame(json_data['actions']).loc[:, columns]
print(f'actions: {set(actions["type"])}')
# filter DataFrame actions and sort in chronological order
cards_actions = ['addChecklistToCard', 'commentCard', 'createCard', 'updateCard', 
                 'updateCheckItemStateOnCard']
actions = actions[actions['type'].isin(cards_actions)].reset_index(drop=True)
actions = actions.sort_values(by='date').reset_index(drop=True)

# prepare DataFrame with memebers (users)
members = pd.DataFrame(json_data['members']).loc[:, ['id', 'username']].set_index('id')
# add usernames to DataFrame 'actions'
actions = pd.merge(actions, members, how='left',
                   left_on='idMemberCreator', right_on='id',
                   suffixes=('_actions', '_members')).drop(['idMemberCreator'], axis=1)

# add actions information to DataFrame 'actions'

# prepare new columns
actions['card_id'] = ''
actions['changed'] = ''
actions['old'] = ''
actions['new'] = ''

# add info to DataFrame
for row in range(len(actions)):
    try:
        actions.loc[row, 'card_id'] = actions.loc[row, 'data']['card']['id']
        actions.loc[row, 'changed'] = list(actions.loc[row, 'data']['old'].keys())[0]
        actions.loc[row, 'old'] = list(actions.loc[row, 'data']['old'].values())
        # get value of what was changed to use it after
        changed = list(actions.loc[row, 'data']['old'].keys())[0]
        actions.loc[row, 'new'] = actions.loc[row, 'data']['card'][changed]
    except:
        pass

print(actions.head(20))

# create table for export
cards_list = []
for row in range(len(cards)):
    # prepare empty dictionary
    card = {}
    
    # add name of card (task)
    card['name'] = cards.iloc[row,2]
    
    # add status
    card['status'] = 'Open'
    if cards.iloc[row, 0] == True:
        card['status'] = 'Closed'
    
    # add name of list (bucket)
    card['list'] = cards.iloc[row, 4]
    
    # add label
    card['label'] = cards.iloc[row, 3]
    
    # add description
    card['desc'] = cards.iloc[row, 1]
    
    # add actions to card
    # get card id
    card_id = cards.index[row]
    
    # iterate over list of action to find action for this card
    counter = 0
    for action_id in range(len(actions)):
        if actions['card_id'][action_id] == card_id:
            card['activity' + str(counter)] = actions['type'][action_id]
            card['date' + str(counter)] = actions['date'][action_id][:16]
            card['user' + str(counter)] = actions['username'][action_id]
            counter += 1
    
    # add card dict to list of cards
    cards_list.append(card)
    
# prepare new DataFrame from list of dicts
df = pd.DataFrame(cards_list).set_index('name')
# export to CSV
df.transpose().to_csv('trello.csv')
            