import numpy as np
import math

class Mapper:
    _car_pos_y = 47
    _car_pos_x = 73
    _road_threshold = 150
    _frame_size = 95

    prev_pixel_val = 0
    current_pixel_val = 0

    def __init__(self) -> None:
        pass

    def calculate_distances(self, state: np.array):
        distances = [0] * 5

        i = 0
        # streigth distance
        while state[self._car_pos_x - i][self._car_pos_y] < self._road_threshold and \
                self._car_pos_x - i != 0:
            distances[2] += 1
            i += 1

        i = 0
        # left distance
        while state[self._car_pos_x - i][self._car_pos_y - i] < self._road_threshold and \
                self._car_pos_y - i != 0:
            distances[0] = math.sqrt((self._car_pos_x - self._car_pos_x - i)**2 + (self._car_pos_y - self._car_pos_y - i)**2)
            #distances[0] += 1
            i += 1

        i = 0
        # right distance
        while state[self._car_pos_x - i][self._car_pos_y + i] < self._road_threshold and \
                self._car_pos_y + i != 95:
            distances[4] = math.sqrt((self._car_pos_x - self._car_pos_x - i)**2 + (self._car_pos_y - self._car_pos_y - i)**2)
            #distances[4] += 1
            i += 1

        i = 0
        # left corner distance
        while state[(self._car_pos_x - 2*i)%self._frame_size][(self._car_pos_y - i)%self._frame_size] < self._road_threshold and \
            -1*self._frame_size < self._car_pos_x - 2*i and -1*self._frame_size < self._car_pos_y - i: 
            lc_x = self._car_pos_x - 2*i
            lc_y = self._car_pos_y - i
            i += 1
        distances[1] = math.sqrt((self._car_pos_x - lc_x)**2 + (self._car_pos_y - lc_y)**2)
            

        i = 0
        # right corner distance
        while state[(self._car_pos_x - 2*i)%self._frame_size][(self._car_pos_y + i)%self._frame_size] < self._road_threshold and \
            -1*self._frame_size < self._car_pos_x - 2*i and self._car_pos_y + i < self._frame_size:
            lc_x = self._car_pos_x - 2*i
            lc_y = self._car_pos_y + i
            i += 1
        distances[3] = math.sqrt((self._car_pos_x - lc_x)**2 + (self._car_pos_y - lc_y)**2)

        return distances


    def is_car_on_grass(self, state: np.array):
        if state[self._car_pos_x - 10][self._car_pos_y] > 110:
            return True
        else:
            return False

    def distance_fitness(self, state: np.array):
        if 99 < state[self._car_pos_x - 30][self._car_pos_y] and state[self._car_pos_x - 30][self._car_pos_y] < 110:
            self.current_pixel_val =  state[self._car_pos_x - 30][self._car_pos_y]

            if self.current_pixel_val != self.prev_pixel_val:
                self.prev_pixel_val = self.current_pixel_val
                return True
            else:
                return False
        else:
            return False




