import argparse
import json
import sqlite3
import os
import pathlib
from path_finder import finding_path


def create_connection(file_db):
    """ creates a connection to the SQLite database as specified by the file_db
    :param file_db: database file
    :return: Connection object or None
    """
    conn = None

    try:
        conn = sqlite3.connect(file_db)
    except Exception as e:
        print("Error in creating a connection to the database: ", e)

    return conn


def read_table(conn):
    """
        Fetch all rows from the database table (universe.db)
        :param conn: Connection object
        :return :all rows of the database table
    """
    cur_obj = conn.cursor()
    try:
        cur_obj.execute('SELECT * FROM ROUTES')
    except Exception as e:
        print("No table with the name ROUTES in the database file ")
        return None

    return cur_obj.fetchall()


def cli():
    """ computes the probability of success by taking as input the two json files from command line
        :return: Probability of success
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('json_file1', type=str, default=None,
                        help='millenium_falcon json file')
    parser.add_argument('json_file2', type=str,
                        default=None, help='empire json file')
    args = parser.parse_args()

    millenium_falcon = args.json_file1
    empire = args.json_file2

    if not millenium_falcon.endswith(".json"):
        print("The millenium_falcon file is not a json file. ")
        return None

    if not empire.endswith(".json"):
        print("The file uploaded is not a json file. ")
        return None

    try:
        if millenium_falcon:
            with open(millenium_falcon) as jsonFile:
                millenium_data = json.load(jsonFile)
                ####### Checking the fields #########
      #          if not isinstance(millenium_data, dict):
      #              print(
      #                  "The json file for millenium_falcon is not correctly formatted")
      #              return None
                keys = millenium_data.keys()
                if "autonomy" not in keys:
                    print(
                        "The json file for millenium falcon does not have the field `autonomy' ")
                    return None
                else:
                    value = millenium_data["autonomy"]
                    if not isinstance(value, int):
                        print("The value of the field `autonomy' is not an integer")
                        return None

                if "departure" not in keys:
                    print(
                        "The json file for millenium falcon does not have the field `departure' ")
                    return None
                else:
                    value = millenium_data["departure"]
                    if not isinstance(value, str):
                        print("The value of the field `departure' is not an string")
                        return None

                if "arrival" not in keys:
                    print(
                        "The json file for millenium falcon does not have the field `arrival' ")
                    return None
                else:
                    value = millenium_data["arrival"]
                    if not isinstance(value, str):
                        print("The value of the field `arirval' is not an string")
                        return None

                if "routes_db" not in keys:
                    print(
                        "The json file for millenium falcon does not have the field `routes_db' ")
                    return None
                else:
                    value = millenium_data["routes_db"]
                    if not isinstance(value, str):
                        print("The value of the field `routes_db' is not an string")
                        return None

        else:
            print("No file entered")
    except Exception as e:
        print("The json file containing the database is not correctly formatted: ", e)
        return None

    try:
        if empire:
            with open(empire) as jsonFile:
                empire_plan = json.load(jsonFile)

                ####### Checking the fields #########
                if not isinstance(empire_plan, dict):
                    print("The json file uploaded is not correctly formatted")
                    return None
                keys = empire_plan.keys()
                if "countdown" not in keys:
                    print(
                        "The json file uploaded does not have the field 'countdown' ")
                    return None
                else:
                    value = empire_plan["countdown"]
                    if not isinstance(value, int):
                        print("The value of the field 'countdown' is not an integer")
                        return None
                    elif value < 0:

                        return 0

                if "bounty_hunters" not in keys:
                    print(
                        "The json file uploaded does not have the field 'bounty_hunters' ")
                    return None
                else:
                    value = empire_plan["bounty_hunters"]
                    if not isinstance(value, list):
                        print("The value of the field 'bounty_hunters' is not a list")
                        return None
                    else:
                        for entry in value:
                            if not isinstance(entry, dict):
                                print(
                                    "The value of a field in 'bounty_hunters' is not a dictionary")
                                return None
                            else:
                                if len(entry) != 2:
                                    print(
                                        "The uploaded file is not correctly formatted: an entry for the empire's plan has more or less than 2 items in the dictionary")
                                    return None
                                keys_entry = entry.keys()
                                if "planet" not in keys_entry:
                                    print(
                                        "The field planet is not present in an entry in the uploaded file")
                                    return None
                                else:
                                    val_entry = entry["planet"]
                                    if not val_entry:
                                        print(
                                            "The field planet in the uploaded file is empty")
                                        return None
                                    elif not isinstance(val_entry, str):
                                        print(
                                            "The field planet in the uploaded file is not a string")
                                        return None

                                if "day" not in keys_entry:
                                    print(
                                        "The field day is not present in an entry in the uploaded file")
                                    return None
                                else:
                                    val_entry = entry["day"]
                                    if not isinstance(val_entry, int):
                                        print(
                                            "The field day in the uploaded file is not an integer")
                                        return None

        else:
            print("No file entered")
    except Exception as e:
        print("The json file containing the empire's plans is not correctly formatted ", e)
        return None

    try:
        sqlite_file = millenium_data['routes_db']
    except Exception as e:
        print("The file containing millenium falcon's details does not have the field 'routes_db ", e)
        return None

    # Finding the path of the millenium_falcon file to append it with the sqlite database file
    # normalize the path, e.g. forward slash is converted
    # millenium_path = os.path.normpath(millenium_falcon)¶
    millenium_falcon = str(pathlib.PureWindowsPath(r'%s' %
                                                   millenium_falcon).as_posix())  # In case, the OS is different, converting it to posix path. This should also work if the path is not a Windows path

    path_ind = millenium_falcon.rfind("/")
    path_folder = millenium_falcon[:path_ind+1]
    sqlite_file = path_folder+sqlite_file

    conn = create_connection(sqlite_file)
    db_table = read_table(conn)
    if not db_table:
        return None

    conn.close()

    prob = finding_path(db_table, millenium_data, empire_plan)
    return prob


if __name__ == '__main__':
    prob = cli()
    if prob is not None:
        print(prob)
