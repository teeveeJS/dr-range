import sqlite3
import json



def save_range(name, range, actions, hero_pos, villain_pos, villain_type, previous_action, table_size, notes):
    conn = sqlite3.connect('ranges.db')
    cur = conn.cursor()

    cur.execute('''INSERT INTO ranges ( name, range, actions, hero_pos,
        villain_pos, villain_type, previous_action, table_size, notes )
        VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ? )''', (name, json.dumps(range), json.dumps(actions), hero_pos,
        villain_pos, villain_type, previous_action, table_size, notes))

    rid = cur.lastrowid

    conn.commit()
    conn.close()
    return rid


def update_range(range_id, data):
    # TODO: idk handle sql injection stuff

    # THIS IS A BAD METHOD: the range_id changes!

    conn = sqlite3.connect('ranges.db')
    cur = conn.cursor()
    cur.execute('DELETE FROM ranges WHERE range_id = ' + str(range_id))
    conn.commit()
    conn.close()


    save_range(data['name'], data['range'], data['actions'], data['hero_pos'], data['villain_pos'], data['villain_type'], data['previous_action'], data['table_size'], data['notes'])
    return


def delete_range(range_id):
    conn = sqlite3.connect('ranges.db')
    cur = conn.cursor()
    cur.execute('DELETE FROM ranges WHERE range_id = ' + str(range_id))
    conn.commit()
    conn.close()
    return


def load_ranges(filters=None, cols=None, load_one=False):
    conn = sqlite3.connect('ranges.db')
    cur = conn.cursor()


    sql_cols = "*"
    if not cols is None:
        sql_cols = ""
        for c in cols:
            sql_cols += c + ", "
        sql_cols = sql_cols[:-2]


    if filters is None or filters == {}:
        cur.execute('SELECT ' + sql_cols + ' FROM ranges')
    else:
        sql_filter = ''
        for k in filters.keys():
            if k in ["range_id", "name", "range", "actions", "hero_pos", "villain_pos", "villain_type", "previous_action", "table_size", "notes"]:
                sql_filter += k + ' = ' + '\'' + str(filters[k]) + '\'' + ' AND '
        sql_filter = sql_filter[:-5]
        print(sql_filter)

        cur.execute('SELECT ' + sql_cols + ' FROM ranges WHERE ' + sql_filter)


    if load_one:
        rows = cur.fetchone()
    else:
        rows = cur.fetchall()


    conn.commit()
    conn.close()
    return json.dumps(rows)


def export_range(range_id):
    conn = sqlite3.connect('ranges.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM ranges WHERE range_id = " + str(range_id))
    data = cur.fetchone()


    filename = data[1]
    if not filename.endswith('.txt'):
        filename += '.txt'


    try:
        fl = open(filename, "w")

        fl.write('Hero Position: ' + data[4] + '\n')
        fl.write('Villain Position: ' + data[5] + '\n')
        fl.write('Villain Type: ' + data[6] + '\n')
        fl.write('Previous Action: ' + data[7] + '\n')
        fl.write('Table Size: ' + data[8] + '\n')

        actions = json.loads(data[3])
        for i in range(len(actions)):
            fl.write(str(i) + " - " + actions[i][0] + " - " + actions[i][1] + '\n')

        poker_range = json.loads(data[2])
        for i in range(13):
            for j in range(13):
                fl.write(coord_to_hand(i, j) + '[' + str(poker_range[i][j]) + '] ')
            fl.write('\n')

        fl.close()
    except:
        conn.commit()
        conn.close()
        return "Error exporting range"

    conn.commit()
    conn.close()
    return filename


def main():

    """ RANGE DATABASE """

    conn = sqlite3.connect('ranges.db')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS ranges ( range_id INTEGER PRIMARY KEY, name TEXT, range TEXT, actions TEXT, hero_pos TEXT, villain_pos TEXT, villain_type TEXT, previous_action TEXT, table_size TEXT, notes TEXT )')

    conn.commit()
    conn.close()



if __name__ == '__main__':
    main()
