import mlrose
from math import cos, asin, sqrt
import numpy as np


def travellingSales(prepared_data):
    for number_of_cars in range(len(prepared_data)):
        # Create list of city coordinates
        coords_list = []
        number_of_orders = 0
        delivery = 0

        for order in prepared_data[number_of_cars]:
            coords_list.append((order['coor'][0], order['coor'][1]))
            number_of_orders = number_of_orders + 1

        # Initialize fitness function object using coords_list
        fitness_coords = mlrose.TravellingSales(coords=coords_list)

        # Create list of distances between pairs of cities
        dist_list = [(0, 1, 3.1623), (0, 2, 4.1231), (0, 3, 5.8310), (0, 4, 4.2426),
                     (0, 5, 5.3852), (0, 6, 4.0000), (0, 7, 2.2361), (1, 2, 1.0000),
                     (1, 3, 2.8284), (1, 4, 2.0000), (1, 5, 4.1231), (1, 6, 4.2426),
                     (1, 7, 2.2361), (2, 3, 2.2361), (2, 4, 2.2361), (2, 5, 4.4721),
                     (2, 6, 5.0000), (2, 7, 3.1623), (3, 4, 2.0000), (3, 5, 3.6056),
                     (3, 6, 5.0990), (3, 7, 4.1231), (4, 5, 2.2361), (4, 6, 3.1623),
                     (4, 7, 2.2361), (5, 6, 2.2361), (5, 7, 3.1623), (6, 7, 2.2361)]

        # Initialize fitness function object using dist_list
        fitness_dists = mlrose.TravellingSales(distances=dist_list)

        problem_fit = mlrose.TSPOpt(length=number_of_orders, fitness_fn=fitness_coords, maximize=False)

        problem_no_fit = mlrose.TSPOpt(length=number_of_orders, coords=coords_list, maximize=False)

        # Solve problem using the genetic algorithm
        best_state, best_fitness = mlrose.genetic_alg(problem_fit, random_state=2)

        print('The best state found is: ', best_state)
        for i in range(number_of_orders):
            for order in prepared_data[number_of_cars]:
                if best_state[i] == prepared_data[number_of_cars].index(order):
                    order['delivery'] = delivery
                    delivery = delivery + 1

        print('The fitness at the best state is: ', best_fitness)

    return prepared_data


def travelSalesMan(orders):
    if len(orders) == 0:
        best_state, best_fitness = [0], 0
    else:

        # Create list of city coordinates
        # coords_list = [(1, 1), (4, 2), (5, 2), (6, 4), (4, 4), (3, 6), (1, 5), (2, 3)]
        coordinates = []
        for order in orders:
            coordinates.append((order.coordinate['lat'], order.coordinate['lon']))
        number_of_orders = len(coordinates)

        dist_list = []
        for i, order1 in enumerate(orders):
            for j, order2 in enumerate(orders):
                if i < j:
                    dist_list.append((i, j, computeDistance(order1.coordinate['lat'], order1.coordinate['lon'],
                                                            order2.coordinate['lat'], order2.coordinate['lon'])))

        # Initialize fitness function object using coords_list
        # fitness_coords = mlrose.TravellingSales(distances=dist_list)

        # Create list of distances between pairs of cities
        # dist_list = [(0, 1, 3.1623), (0, 2, 4.1231), (0, 3, 5.8310), (0, 4, 4.2426),
        #              (0, 5, 5.3852), (0, 6, 4.0000), (0, 7, 2.2361), (1, 2, 1.0000),
        #              (1, 3, 2.8284), (1, 4, 2.0000), (1, 5, 4.1231), (1, 6, 4.2426),
        #              (1, 7, 2.2361), (2, 3, 2.2361), (2, 4, 2.2361), (2, 5, 4.4721),
        #              (2, 6, 5.0000), (2, 7, 3.1623), (3, 4, 2.0000), (3, 5, 3.6056),
        #              (3, 6, 5.0990), (3, 7, 4.1231), (4, 5, 2.2361), (4, 6, 3.1623),
        #              (4, 7, 2.2361), (5, 6, 2.2361), (5, 7, 3.1623), (6, 7, 2.2361)]

        # print(dist_list)
        # Initialize fitness function object using dist_list
        fitness_dists = mlrose.TravellingSales(distances=dist_list)
        # fitness_coords = mlrose.TravellingSales(coords=coordinates)

        problem_fit = mlrose.TSPOpt(length=number_of_orders, fitness_fn=fitness_dists, maximize=False)
        # problem_fit = mlrose.TSPOpt(length=number_of_orders, fitness_fn=fitness_coords, maximize=False)

        # coords_list = [(1, 1), (4, 2), (5, 2), (6, 4), (4, 4), (3, 6),
        #            (1, 5), (2, 3)]
        # problem_no_fit = mlrose.TSPOpt(length = number_of_orders, maximize=False)
        # problem_no_fit = mlrose.TSPOpt(length = number_of_orders, coords = coordinates, maximize=False)

        # Solve problem using the genetic algorithm
        best_state, best_fitness = mlrose.genetic_alg(problem_fit, random_state=2)

    print('The best state found is: ', best_state)
    print('The fitness at the best state is: ', best_fitness)
    print('*******************************************************')
    return best_fitness


def computeDistance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295  # Pi/180
    a = 0.5 - cos((lat2 - lat1) * p) / 2 + cos(lat1 * p) * \
        cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    return 12742 * asin(sqrt(a))  # 2*R*asin... as km.


def path_distance(routes, cities):
    distances = 0

    for r in range(len(routes)):
        currentNode = cities[routes[r - 1]]
        nextNode = cities[routes[r]]

        c_dist = computeDistance(currentNode[0], currentNode[1], nextNode[0], nextNode[1])

        distances += c_dist

    return distances


# Reverse the order of all elements from element i to element k in array r.
two_opt_swap = lambda r, i, k: np.concatenate((r[0:i], r[k:-len(r) + i - 1:-1], r[k + 1:len(r)]))


def two_opt(orders, improvement_threshold):  # 2-opt Algorithm adapted from https://en.wikipedia.org/wiki/2-opt
    if len(orders) < 2:
        return 0
    cities = []
    for order in orders:
        cities.append((order.coordinate['lat'], order.coordinate['lon']))
    number_of_orders = len(cities)
    cities = np.array(cities)
    route = np.arange(cities.shape[0])  # Make an array of row numbers corresponding to cities.
    improvement_factor = 1  # Initialize the improvement factor.
    best_distance = path_distance(route, cities)  # Calculate the distance of the initial path.
    # print(f'best distance: {best_distance}')
    while improvement_factor > improvement_threshold:  # If the route is still improving, keep going!
        distance_to_beat = best_distance  # Record the distance at the beginning of the loop.
        for swap_first in range(1, len(route) - 2):  # From each city except the first and last,
            for swap_last in range(swap_first + 1, len(route)):  # to each of the cities following,
                new_route = two_opt_swap(route, swap_first, swap_last)  # try reversing the order of these cities
                new_distance = path_distance(new_route, cities)  # and check the total distance with this modification.
                # print(f'new distance: {new_distance}')
                if new_distance < best_distance:  # If the path distance is an improvement,
                    route = new_route  # make this the accepted best route
                    best_distance = new_distance  # and update the distance corresponding to this route.
        improvement_factor = 1 - best_distance / distance_to_beat  # Calculate how much the route has improved.
    return best_distance # When the route is no longer improving substantially, stop searching and return the route.
