def get_game_chooser_info_from_boardname(sm, boardname):
    board = sm.get_screen(boardname).children[0].board
    gameinfo = board.collectionsgf.info_for_button()
    if 'wname' in gameinfo:
        wname = gameinfo['wname']
    else:
        wname = 'Unknown'
    if 'bname' in gameinfo:
        bname = gameinfo['bname']
    else:
        bname = 'Unknown'
    if 'filepath' in gameinfo:
        filepath = gameinfo['filepath']
    else:
        filepath = 'Not yet saved'
    if 'date' in gameinfo:
        date = gameinfo['date']
    else:
        date = '---'
    return {
        'boardname': boardname,
        'wname': wname,
        'bname': bname,
        'filepath': filepath,
        'date': date
    }
