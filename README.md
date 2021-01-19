# trello_json_to_csv
Export Trello JSON to CSV with Python's Pandas

## Background
Trello is a collaboration tool that helps people and teams to organize  projects into boards. While Trello support free export to JSON format, export to CSV is available only for upgraded accounts.

## Challenge: One-to-many data structures
One of the difficulties with making Trello's JSON human-readable is that in many cases, there are multiple pieces of information nested within a single structure. For example, for a single card, you can have information about what's currently on the card, a history of what was previously on the card, information about changes that have been made to the card (moves between lists), and information about structures that are themselves nested (like checklist items within a checklist on a single card). 

That information is hard to represent e.g. in a single row in Excel, since some of it contains information about actions over time (movement) and some contains information about static information (the content of new checklist items, for example). That nesting and one-to-many nature of the data is why some of this information isn't included on Trello's CSV export.

## Solution
Trello.py script use Python's library Pandas to export from JSON file selected keys with required information to DataFrame structure. Resulted CSV file has vertical structure where each column is a separate task (card) with different information bellow: name, description, label, actions, dates, usernames, etc. Date exported to CSV file can be used for storrage or further formatting using Excel, Numbers, Google sheets or similar apps.
