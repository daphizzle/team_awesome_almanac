__author__ = 'adnan'
import matplotlib
import matplotlib.pyplot as plt
import random
import time
import itertools
import math




def distance_on_unit_sphere(lat1, long1, lat2, long2):

    # Convert latitude and longitude to
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0

    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians

    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians

    # Compute spherical distance from spherical coordinates.

    # For two locations in spherical coordinates
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) =
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length

    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) +
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )

    # Remember to multiply arc by the radius of the earth
    # in your favorite set of units to get length.
    return arc*6373

#Generate all possible combination for accessing all bins and return the shortest one
def exact_TSP(cities):
    return shortest(itertools.permutations(cities))


#Return the tour with the minimum total distance
def shortest(tours):
    return min(tours, key=total_distance)


#The total distance between each pair of consecutive bins
def total_distance(tour):
    return sum(distance_on_unit_sphere(tour[i][0],tour[i][1], tour[i-1][0], tour[i-1][1]) for i in range(len(tour)))


#The distance between two points
def distance(A, B):
    return abs(A - B)


#Make a set of n bins, each with random coordinates
def bins(n):
    Bin = complex # Constructor for new cities, e.g. City(300, 400)
    return set(Bin(random.randrange(0, 10), random.randrange(0, 10)) for c in range(n))


#alltours =  # The permutation function is already defined in the itertools module

#bins = bins(5)



#path = exact_TSP(bins)


#print bins
#print path

#print(total_distance(path))





