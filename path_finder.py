class Graph:
    def __init__(self, adj_list):
        self.adj_list = adj_list

    def find_neigh(self, n):
        """
        Finds the neighbors of the current node
        :n: (string) the current node
        :return: (list having strings) list of neighbors for the current node 
        """

        if n in self.adj_list:
            return self.adj_list[n]
        else:
            return []

    # Setting the heuristic function by assigning an equal value to all the nodes
    def h(self, n):
        H = {
            'Tatooine': 1,
            'Dagobah': 1,
            'Hoth': 1,
            'Endor': 1
        }
        return H[n]

    def astar_algo(self, start, stop):
        """
        A* algorithm
        :start: (string) starting node
        :stop: the ending node
        """

        if start == stop:
            return [start]

        open_lst = set([start])
        closed_lst = set([])

        # pres has present number of says from start to all other nodes
        # the default is +infinity
        pres = {}
        pres[start] = 0

        # p_adj contains an adjac mapping of all nodes
        p_adj = {}
        p_adj[start] = start

        while len(open_lst) > 0:
            n = None

            for v in open_lst:
                if n == None or pres[v] + self.h(v) < pres[n] + self.h(n):
                    n = v

            if n == None:
                # print('Path does not exist!')
                return None

            # if the present node is the stop then start again from start
            if n == stop:
                constr_path = []

                while p_adj[n] != n:
                    constr_path.append(n)
                    n = p_adj[n]

                constr_path.append(start)

                constr_path.reverse()

                # print("Path found: ", constr_path)

                return constr_path

            # for the present node's neighbors
            for (m, weight) in self.find_neigh(n):
                # if the present node is not there in both open_lst and closed_lst add it to open_lst and note n as it's p_adj
                if m not in open_lst and m not in closed_lst:
                    open_lst.add(m)
                    p_adj[m] = n
                    pres[m] = pres[n] + weight

                # else, check if it's faster to first rreach n, then m, then update p_adj data and pres data
                # and if the node was present in the closed_lst, move it to open_lst
                else:
                    if pres[m] > pres[n] + weight:
                        pres[m] = pres[n] + weight
                        p_adj[m] = n

                        if m in closed_lst:
                            closed_lst.remove(m)
                            open_lst.add(m)

            # removing n from the open_lst, and adding it to closed_lst
            # because all of its neighbors have been examined
            open_lst.remove(n)
            closed_lst.add(n)

        # print('Path does not exist!')
        return None

    def find_days(self, path):
        """
           Finds the total number of days required to traverse the given path
           :path: input path
           :return: days: total number of days required to traverse the path, day_list: days required to travel between subsequent planets in the path
        """
        days = 0
        day_list = [0]  # start node has number of days set to 0
        # print("path in find_days: ", path)
        for (ind, node) in enumerate(path):
            if ind < len(path)-1:

                for (v, weight) in self.find_neigh(node):
                    if v == path[ind+1]:
                        days += weight
                        day_list.append(weight)

        return days, day_list


def travel_time_main(exponent, prob_cap, autonomy, current_days, level_of_fuel, remaining_path, remaining_path_days, hunt_plan, countdown):
    """
    Traverses the given path and sums up the probability of capture
    :exponent: (integer) the exponent in the formula for computing the probability of capture; it keeps updating - starts from 0
    :prob_cap: (float) probability of capture
    :autonomy: (integer) the autonomy of the Millennium Falcon
    :current_days: (integer) number of days required to reach the current planet + refuel time in the current planet + number of waiting days in the current planet
    :level_of_fuel: (integer) the level of fuel remaining
    :remaining_path: (list having strings) the remaining part of the current path that is left to traverse
    :remaining_path_days: (list having integers) the numbe of days required to traverse the remaining part of the current path that is left to traverse
    :hunt_plan: (dictionary): plan of the bounty hunters, where each entry is planet: list of days present in the planet
    :countdown: (integer) Empire's countdown for reaching the destination
    :return: days_to_reach: (integer) Days to reach the destination using the given path, prob_cap: (float) probability of capture when following the current path
    """
    assert len(
        remaining_path) >= 2, "Length of remaining path cannot be less that 2"

    if len(remaining_path) == 2:
        # The next node is the destination
       # print(f"Reach at {remaining_path[1]}") # print to uncomment when checking the path

        days_to_reach = current_days + remaining_path_days[1]
    elif len(remaining_path) == 3:
        # Find if the reaching time to the next node results in a clash with the hunters
        if remaining_path[1] in hunt_plan:

            if (current_days + remaining_path_days[1]) in hunt_plan[remaining_path[1]]:
                prob_cap += (1*(9**exponent))/(10**(exponent+1))

                exponent += 1

        if level_of_fuel - remaining_path_days[1] < remaining_path_days[2]:

            # find refueling time of the next node using the weight (days) of the edge leaving from the next node;
            # level_of_fuel is the level_of_fuel after refueling in the current_node if required
            refuel_time = 1

            if remaining_path[1] in hunt_plan:
                if (current_days + remaining_path_days[1] + refuel_time) in hunt_plan[remaining_path[1]]:
                    prob_cap += (1*(9**exponent))/(10**(exponent+1))
                    exponent += 1

            level_of_fuel = autonomy  # After refueling at the next node
            # print(f"Refuel at {remaining_path[1]}") print to uncomment when checking the path
        else:
            refuel_time = 0
            level_of_fuel = level_of_fuel - remaining_path_days[1]
            # print(f"Reach and no refuel at {remaining_path[1]}") # print to uncomment when checking the path

        current_days = current_days + remaining_path_days[1] + refuel_time
        days_to_reach, prob_cap = travel_time_main(
            exponent, prob_cap, autonomy, current_days, level_of_fuel, remaining_path[1:], remaining_path_days[1:], hunt_plan, countdown)
    else:

        if remaining_path[1] in hunt_plan:
            if (current_days + remaining_path_days[1]) in hunt_plan[remaining_path[1]]:
                prob_cap += (1*(9**exponent))/(10**(exponent+1))
                exponent += 1

        if level_of_fuel - remaining_path_days[1] < remaining_path_days[2]:
            # find refueling time of the next node;
            # level_of_fuel is the level_of_fuel after refueling in the current_node if required
            refuel_time = 1

            if remaining_path[1] in hunt_plan:
                if (current_days + remaining_path_days[1] + refuel_time) in hunt_plan[remaining_path_days[1]]:
                    prob_cap += (1*(9**exponent))/(10**(exponent+1))
                    exponent += 1

            level_of_fuel = autonomy  # After refueling at the next node
            # print(f"Refuel at {remaining_path[1]}") # print to uncomment when checking the path
        else:
            refuel_time = 0
            level_of_fuel = level_of_fuel - remaining_path_days[1]
            # print(f"Reach and no refuel at {remaining_path[1]}") # print to uncomment when checking the path
        WT, flag_cant_reach = waiting_time(prob_cap, autonomy, current_days +
                                           remaining_path_days[1], level_of_fuel, remaining_path[1:], remaining_path_days[1:], hunt_plan, countdown)
        if not flag_cant_reach:
            current_days = current_days + \
                remaining_path_days[1] + refuel_time + WT
            # print(f"Wait at {remaining_path[1]} for {WT} days") # print to uncomment when checking the path
            days_to_reach, prob_cap = travel_time_main(
                exponent, prob_cap, autonomy, current_days, level_of_fuel, remaining_path[1:], remaining_path_days[1:], hunt_plan, countdown)
        else:
            days_to_reach = None
            prob_cap = 1  # Can't reach

    return days_to_reach, prob_cap


def travel_time(prob_cap, autonomy, current_days, level_of_fuel, remaining_path, remaining_path_days, hunt_plan, countdown):
    """
    Used during recursion while computing the maximum possible waiting time after traversing the given path
    :autonomy: (integer) the autonomy of the Millennium Falcon
    :current_days: (integer) number of days required to reach the current planet + refuel time in the current planet + number of waiting days in the current planet
    :level_of_fuel: (integer) the level of fuel remaining
    :remaining_path: (list having strings) the remaining part of the current path that is left to traverse
    :remaining_path_days: (list having integers) the numbe of days required to traverse the remaining part of the current path that is left to traverse
    :hunt_plan: (dictionary): plan of the bounty hunters, where each entry is planet: list of days present in the planet
    :countdown: (integer) Empire's countdown for reaching the destination
    :return: days_to_reach: (integer) Days to reach the destination using the given path
    """
    assert len(
        remaining_path) >= 2, "Length of remaining path cannot be less that 2"

    if len(remaining_path) == 2:
        # The next node is the destination
        days_to_reach = current_days + remaining_path_days[1]
    elif len(remaining_path) == 3:

        # if level_of_fuel + remaining_path_days[2] > autonomy:
        if level_of_fuel - remaining_path_days[1] < remaining_path_days[2]:

            # find refueling time of the next node using the weight (days) of the edge leaving from the next node;
            # level_of_fuel is the level_of_fuel after refueling in the current_node if required
            refuel_time = 1
            # print("level of fuel at DG: ", level_of_fuel)
            level_of_fuel = autonomy  # After refueling at the next node
            # print(f"Refuel at {remaining_path[1]}")
        else:
            refuel_time = 0
            level_of_fuel = level_of_fuel - remaining_path_days[1]
            # print(f"Reach and no refuel at {remaining_path[1]}")

        current_days = current_days + remaining_path_days[1] + refuel_time
        days_to_reach = travel_time(
            prob_cap, autonomy, current_days, level_of_fuel, remaining_path[1:], remaining_path_days[1:], hunt_plan, countdown)
    else:

        if level_of_fuel - remaining_path_days[1] < remaining_path_days[2]:
            # find refueling time of the next node;
            # level_of_fuel is the level_of_fuel after refueling in the current_node if required
            refuel_time = 1
            level_of_fuel = autonomy  # After refueling at the next node
        else:
            refuel_time = 0
            level_of_fuel = level_of_fuel - remaining_path_days[1]
        WT, _ = waiting_time(prob_cap, autonomy, current_days +
                             remaining_path_days[1], level_of_fuel, remaining_path[1:], remaining_path_days[1:], hunt_plan, countdown)
        current_days = current_days + remaining_path_days[1] + refuel_time + WT

        days_to_reach = travel_time(
            prob_cap, autonomy, current_days, level_of_fuel, remaining_path[1:], remaining_path_days[1:], hunt_plan, countdown)

    return days_to_reach


def waiting_time(prob_cap, autonomy, day_spent, level_of_fuel, remaining_path, remaining_path_days, hunt_plan, countdown):
    """
    Computes the waiting time at the current planet 
    :prob_cap: (float) probability of capture
    :autonomy: (integer) the autonomy of the Millennium Falcon
    :days_spent: (integer) number of days required to reach the current planet (does not include waiting time at the current_node + refuel_time at the current node)
    :level_of_fuel: (integer) the level of fuel remaining
    :remaining_path: (list having strings) the remaining part of the current path that is left to traverse
    :remaining_path_days: (list having integers) the numbe of days required to traverse the remaining part of the current path that is left to traverse
    :hunt_plan: (dictionary): plan of the bounty hunters, where each entry is planet: list of days present in the planet
    :countdown: (integer) Empire's countdown for reaching the destination
    :return: WT_tentative: (integer) waiting time at the current planet, flag_cant_reach: (bool) if True, the flag to indicate that the destination cannot be reached  with the current path before countdown
    """

    flag_cant_reach = False

    if level_of_fuel - remaining_path_days[0] < remaining_path_days[1]:
        refuel_time = 1
        # print(f"Refuel at {remaining_path[0]}")
        level_of_fuel = autonomy  # After refueling

    else:
        refuel_time = 0
        level_of_fuel = level_of_fuel - remaining_path_days[0]
        # print(f"Reach and no refuel at {remaining_path[0]}")

    # Check if next neighbor requires refueling
    refuel_next = level_of_fuel - \
        (day_spent + refuel_time + remaining_path_days[1])
    if refuel_next == 0:
        refuel_time_next = 1
    elif len(remaining_path_days) > 2:
        refuel_next = level_of_fuel - \
            (day_spent + refuel_time +
             remaining_path_days[1] + remaining_path_days[2])
        if refuel_next == 0:
            refuel_time_next = 1
        else:
            refuel_time_next = 0
    else:
        refuel_time_next = 0

    # Assumption: Wait only if the next neighbor will have a bounty hunter at some point and sufficient fuel is there
    if remaining_path[1] not in hunt_plan:
        WT_tentative = 0  # next neighbor will never have a bounty hunter
        # print(f"Wait at {remaining_path[0]} for 0 days")
        return WT_tentative, flag_cant_reach
    # If next leap will not result in clash with the hunter, take the leap without waiting
    elif (day_spent + refuel_time + remaining_path_days[1]) not in hunt_plan[remaining_path[1]] and (day_spent + refuel_time + remaining_path_days[1] + refuel_time_next) not in hunt_plan[remaining_path[1]]:
        return 0, flag_cant_reach

    else:
        days_of_hunt = hunt_plan[remaining_path[1]]
        last_day = max(days_of_hunt)

        WT_permit = float('inf')

        # If the present node is in the hunt plan
        if remaining_path[0] in hunt_plan:
            days_of_hunt_current = hunt_plan[remaining_path[0]]
            days_of_hunt_current = [
                i for i in days_of_hunt_current if i > day_spent+refuel_time]
            if days_of_hunt_current:
                #    days_for_next_hunt = min(
                #        days_of_hunt_current) - (day_spent+refuel_time)

                # No use waiting if the current node has a bounty hunter on the next day after refueling
                WT_permit = min(days_of_hunt_current) - \
                    (day_spent+refuel_time)

        WT_tentative = last_day - \
            (day_spent + refuel_time +
             remaining_path_days[1]) + 1  # maximum waiting time
        if WT_tentative < 0:  # the next planet will not have a hunter after reaching the planet
            WT_tentative = 0
            return WT_tentative, flag_cant_reach
        WT_tentative = min(WT_tentative, WT_permit)

    current_days = day_spent + refuel_time + WT_tentative
    days_to_reach = travel_time(prob_cap, autonomy,
                                current_days, level_of_fuel, remaining_path, remaining_path_days, hunt_plan, countdown)

    if days_to_reach <= countdown:
        # print(f"Wait at {remaining_path[0]} for {WT_tentative} days")
        return WT_tentative, flag_cant_reach
    else:
        while days_to_reach > countdown:
            WT_tentative -= 1
            if WT_tentative < 0:
                WT_tentative = 0
                flag_cant_reach = True
                # print("Can't reach while waiting") # print to uncomment when checking the path
                return WT_tentative, flag_cant_reach
            current_days = day_spent + refuel_time + WT_tentative
            days_to_reach = travel_time(prob_cap, autonomy,
                                        current_days, level_of_fuel, remaining_path, remaining_path_days, hunt_plan, countdown)

        if current_days + remaining_path_days[1] in hunt_plan[remaining_path[1]]:
            # if remaining_path[1] is not in hunt_plan, the code would have not reached this point, there is a check before
            # No use waiting, it will anyway reach a day in the next node when a hunter is there
            WT_tentative = 0
        # print(f"Wait at {remaining_path[0]} for {WT_tentative} days")
        return WT_tentative, flag_cant_reach


def total_time(autonomy, path, path_days, hunt_plan, countdown):
    """
    Calls travel_time_main to compute the days_to_reach and prob_cap for the current path
    :autonomy: (integer) the autonomy of the Millennium Falcon
    :path: (list having strings) the current path 
    :path_days: (list having integers) the number of days required to traverse the current path
    :hunt_plan: (dictionary): plan of the bounty hunters, where each entry is planet: list of days present in the planet
    :countdown: (integer) Empire's countdown for reaching the destination
    :return: days_to_reach: (integer) Days to reach the destination using the given path, prob_cap: (float) probability of capture when following the current path
    """
    level_of_fuel = autonomy
    day_spent = 0
    refuel_time = 0
    prob_cap = 0
    exponent = 0
    flag_cant_reach = False

    # Assumption: Wait only if the next neighbor will have a bounty hunter at some point and sufficient fuel is there
    if path[1] not in hunt_plan:
        WT_tentative = 0  # next neighbor will never have a bounty hunter
        # print(f"Start at {path[0]}") # print to uncomment when checking the path
        # print(f"Wait at {path[0]} for {WT_tentative} days") # print to uncomment when checking the path
        current_days = day_spent + refuel_time + WT_tentative
        days_to_reach, prob_cap = travel_time_main(exponent, prob_cap, autonomy,
                                                   current_days, level_of_fuel, path, path_days, hunt_plan, countdown)
        return days_to_reach, prob_cap
    else:
        days_of_hunt = hunt_plan[path[1]]
        last_day = max(days_of_hunt)

        WT_tentative = last_day - \
            (day_spent + refuel_time +
             path_days[1]) + 1  # maximum waiting time

        current_days = day_spent + refuel_time + WT_tentative

        days_to_reach = travel_time(prob_cap, autonomy,
                                    current_days, level_of_fuel, path, path_days, hunt_plan, countdown)

    if days_to_reach <= countdown:
        # print(f"Wait at {path[0]} for {WT_tentative} days") # print to uncomment when checking the path
        days_to_reach, prob_cap = travel_time_main(exponent, prob_cap, autonomy,
                                                   current_days, level_of_fuel, path, path_days, hunt_plan, countdown)

        return days_to_reach, prob_cap
    else:

        while days_to_reach > countdown:
            WT_tentative -= 1
            if WT_tentative < 0:
                WT_tentative = 0
                flag_cant_reach = True
                # print to uncomment when checking the path
                # print("Can't reach")
                prob_cap = 1
                return days_to_reach, prob_cap

            current_days = day_spent + refuel_time + WT_tentative
            days_to_reach = travel_time(prob_cap, autonomy,
                                        current_days, level_of_fuel, path, path_days, hunt_plan, countdown)

    if path[1] in hunt_plan:
        if current_days + path_days[1] in hunt_plan[path[1]]:
            # No use waiting, it will anyway reach a day in the next node when a hunter is there
            WT_tentative = 0
            current_days = day_spent + refuel_time + WT_tentative
            # print(f"Wait at {path[0]} for {WT_tentative} days") # print to uncomment when checking the path
            days_to_reach, prob_cap = travel_time_main(exponent, prob_cap, autonomy,
                                                       current_days, level_of_fuel, path, path_days, hunt_plan, countdown)
    else:
        # print(f"Wait at {path[0]} for {WT_tentative} days") # print to uncomment when checking the path
        days_to_reach, prob_cap = travel_time_main(exponent, prob_cap, autonomy,
                                                   current_days, level_of_fuel, path, path_days, hunt_plan, countdown)  # Traverse the path again with the 'travel_time_main' to compute the actual probability of capture

    return days_to_reach, prob_cap


def compute_probability(autonomy, graph_1, empire_plan, path):
    """
    Computes the probability of success for the current path
    :autonomy: (integer) the autonomy of the Millennium Falcon
    :graph_1: object of Graph
    :empire_plan: (dictionary) dictionary containing the empire plan
    :path: (list having strings) the current path
    :return: prob_success: (float) probability of success in the current path
    """

    days, day_list = graph_1.find_days(path)

    countdown = empire_plan["countdown"]
    bounty_hunters = empire_plan["bounty_hunters"]
    hunt_plan = {}
    for bh in bounty_hunters:
        assert len(bh["planet"]) != 0, "planet name cannot be empty or null"

        if bh["planet"] not in hunt_plan:
            hunt_plan[bh["planet"]] = [bh["day"]]
        else:
            hunt_plan[bh["planet"]].append(bh["day"])

    if days > countdown:  # Can't reach on time
        prob_succcess = 0
    #    print("Probability of success", prob_succcess)

    else:
        prob_cap = 0  # probability of getting captured

        days_to_reach, prob_cap = total_time(
            autonomy, path, day_list, hunt_plan, countdown)
        # print("prob_cap: ", prob_cap)
        prob_succcess = (1-prob_cap)*100

    # print("total number of days_to_reach: ", days_to_reach,
    #      " prob of success: ", prob_succcess)

    return prob_succcess


def compute_prob_subgraph(graph_1, neigh_done, path_upto_start, start, empire_plan, millenium_data, prob):
    """
    Traverses different routes in the graph starting from all the neighbors of the planet 'start' through recursion and updates the probability of success 
    :graph_1: object of Graph
    :neigh_done: (string) neighbor that has been visited
    :path upto start: (list having strings): part of the route taken until the planet 'start'
    :start: (string): the planet whose neighbors are traversed
    :empire_plan: (dictionary): dictionary containing the data from the json file of empire plan
    :millenium_data: (dictionary): dictionary containing the data from the json file for the Millenium Falcon
    :prob: (float): best probability of success till now
    :return: prob: (float) updated probability of success after traversing different routes
    """

    neighbors = graph_1.find_neigh(start)

    neighbors.sort(key=lambda a: a[1])

    for (neigh, weight) in neighbors:
        #  if path_ind == 0 and neigh != path[path_ind+1]:

        # Find the shortest path for the next closest neighbor
        # neigh != neigh_done:

        # if start == 'Dagobah':
        #    print("neigh of Dagobah: ", neigh)

        # if len(path_upto_start) > 1:
        #    prev_nodes = path_upto_start[-2:]
        # else:
        #    prev_nodes = path_upto_start[-1]

        if neigh != start and neigh not in path_upto_start:

            path_new = graph_1.astar_algo(
                neigh, millenium_data['arrival'])

            path_neigh = []
            path_neigh.extend(path_upto_start)
            path_neigh.extend(path_new)

            path_neigh_days, _ = graph_1.find_days(path_neigh)
            if path_neigh or path_neigh_days <= empire_plan["countdown"]:

                prob_neigh = compute_probability(
                    millenium_data['autonomy'], graph_1, empire_plan, path_neigh)
            else:
                prob_neigh = 0

            if prob_neigh > prob:

                prob = prob_neigh
                if prob == 100:
                    break

            if neigh == millenium_data['arrival']:
                prob_neigh = prob
            else:
                prob_neigh = compute_prob_subgraph(
                    graph_1, path_neigh[1], path_upto_start+[neigh], neigh, empire_plan, millenium_data, prob)  # compute_prob_recursively for the next neighbor

            if prob_neigh > prob:

                prob = prob_neigh
                if prob == 100:
                    break

    return prob


def finding_path(db_table, millenium_data, empire_plan):
    """
    Constructs an adjacency graph from the database table, calls the A * algorithm and searches different possible routes through recursion
    :db_table: (list) the entries of the database table of the Millenium Falcon
    :millenium_data: (dictionary) data extracted from the json file for the Millenium Falcon
    :empire_plan: (dictionary) dictionary containing the data from the json file of empire plan
    return:prob: (float) Final probability of success
    """
    adjac_lis = {}
    for (source, dest, days) in db_table:

        if not isinstance(days, int):
            print(
                "Number of days for travelling is not integer: correct the millenium_falcon database")
            return None
        elif days <= 0:
            print("Number of days for travelling should be strictly positive: correct the millenium_falcon database")
            return None

        if not isinstance(source, str):
            print(
                "Source is not a string: correct the millenium_falcon database")
            return None

        if not isinstance(dest, str):
            print(
                "Destination is not a string: correct the millenium_falcon database")
            return None

        if source not in adjac_lis:
            adjac_lis[source] = [(dest, days)]
            if dest not in adjac_lis:  # Routes can be travelled in any direction
                adjac_lis[dest] = [(source, days)]
            else:
                adjac_lis[dest].append((source, days))
        else:
            adjac_lis[source].append((dest, days))
            if dest not in adjac_lis:
                adjac_lis[dest] = [(source, days)]
            else:
                adjac_lis[dest].append((source, days))

    # print("adjac_list: ", adjac_lis)

    graph_1 = Graph(adjac_lis)
    path = graph_1.astar_algo(
        millenium_data['departure'], millenium_data['arrival'])
    # path = ["Tatooine", "Dagobah", "Hoth", "Endor"]
    # path = ["Tatooine", "Hoth", "Endor"]
    if not path:
        print("Path does not exist")
        return 0
    prob = compute_probability(
        millenium_data['autonomy'], graph_1, empire_plan, path)

    prob = compute_prob_subgraph(graph_1, path[1], [
                                 millenium_data['departure']], millenium_data['departure'], empire_plan, millenium_data, prob)

    # for path_ind in range(1):
    #     neighbors = graph_1.find_neigh(path[path_ind])

    #     neighbors.sort(key=lambda a: a[1])

    #     print("Traversing other neighbors")

    #     for (neigh, weight) in neighbors:
    #         #  if path_ind == 0 and neigh != path[path_ind+1]:
    #         if neigh != path[1]:
    #             # Find the shortest path for the next closest neighbor
    #             path_new = graph_1.a_star_algorithm(
    #                 neigh, millenium_data['arrival'])
    #             path_neigh = []
    #             path_neigh.extend(path[:path_ind+1])
    #             path_neigh.extend(path_new)
    #             prob_neigh = compute_probability(
    #                 millenium_data['autonomy'], graph_1, empire_plan, path_neigh)

    #             print("new path: ", path_neigh, " prob_neigh: ", prob_neigh)

    #             if prob_neigh > prob:
    #                 print("path_neigh: ", path_neigh,
    #                       " prob_neigh", prob_neigh)
    #                 prob = prob_neigh
    #             if prob == 100:
    #                 break
    #     if prob == 100:
    #         break

    return prob
