import sqlite3


# получили полный список групп-подгрупп для комбобоксов
def get_subgroups():
    with sqlite3.connect('app.db') as db:
        cursor = db.cursor()
        query = """
                SELECT group_id, subgroup 
                FROM subgroups
                """
        cursor.execute(query)
    subgroups = {}
    for res in cursor:
        if res[0] in subgroups:
            subgroups[res[0]] += (res[1],)
        else:
            subgroups[res[0]] = (res[1],)
    return subgroups


def get_sets(group_id, subgroup):
    with sqlite3.connect('app.db') as db:
        cursor = db.cursor()
        query = """
                SELECT DISTINCT (set_n) 
                FROM dictionary
                WHERE group_part = :group_id and subgroup = :subgroup
                ORDER BY set_n
                """
        cursor.execute(query, {'group_id': group_id, 'subgroup': subgroup})

    set_n = []
    for res in cursor:
        set_n.append(str(res[0]))
    return set_n