# FM CLI (football-manager CLI app)
Simple fun Football Manager-like app written in pure python with CLI interface.

## Features
1. Running from terminal with CLI [v. 0.1].
2. Match simulation between two chosen clubs [v. 0.1].
3. Checking details of 9k+ real players, clubs, leagues. [v. 0.2].

## Programming details
Tested with Python 3.9. Should work with Python 3.7+.

App structure:
1. Data access (DAL) [app/database + SQLite DB]
2. Data mapping (DAM) [app/resources with SQLAlchemy use]
3. Business logic (BLL) [app/models]
4. Service layer [app/services]
5. Presentation layer [app/cli with Curses]
6. Configuration layer [config.py]
7. Testing layer [app/test]


## Changelog

### v. 0.2 [in progress]
- reorganised and updated DB:
    - added 9k+ real players
    - added 28 leagues
    - added 386 real clubs associated with mentioned leagues
    - added proper nationalities
- adapted match simulating model to the new DB [in progress]
  - todo:
    - can't play matches between two same team
    - even if so - scorers should be separated
    - improve scoring times - it's not always chronological cause of rand
- calculating team power
- totally remodeled files structure for scalable app; it covers 7 basic app layers now

### v. 0.1
- project setup
- basic teams and players data stored in JSON files
- teams can play against each other; result depends on teams' power and how's the game going
- simple CLI menu
