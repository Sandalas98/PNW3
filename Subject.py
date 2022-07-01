
    
class Subject:
    def __init__(self, genotype: int) -> None:
        self._genotype = genotype
        self.fitness = 0
        self.speed = 0
        self.is_braking = False
        self.change_speed = 0

    def show_yourself(self):
        print(self._genotype)
        #return self._genotype

    def shift_speed(self, amount: int = 0):
        if self.speed+amount >= 0:
            self.speed += amount
        else:
            self.speed = 0


    def calculate_turn(self, obs):
        if obs[0] > obs[4]:
            turn_coeff = (obs[4] / obs[0])
            turn_coeff = abs(1-turn_coeff)
            turn_coeff = -1 * turn_coeff
        else:
            turn_coeff = (obs[0] / obs[4])
            turn_coeff = abs(1-turn_coeff)
        
        if obs[1] > obs[3]:
            turn_coeff_2 = (obs[3] / obs[1])
            turn_coeff_2 = abs(1-turn_coeff_2)
            turn_coeff_2 = -1 * turn_coeff_2
        else:
            turn_coeff_2 = (obs[1] / obs[3])
            turn_coeff_2 = abs(1-turn_coeff_2)
            
        '''print(self._genotype[0])
        print(turn_coeff)
        print(self._genotype[1])
        print(turn_coeff_2)
        print('------------------------')'''
        turn_ratio = (self._genotype[0]*turn_coeff + self._genotype[1]*turn_coeff_2)/2


        return turn_ratio

    def calculate_speed(self, obs):
        _max_foward_distance = 74
        
        dist = obs[2]

        dist_to_range_coef = dist / _max_foward_distance

        max_current_speed = dist_to_range_coef * self._genotype[2]

        if self.speed > max_current_speed:
            return 0, 0.1*self._genotype[3]
        else: # self.speed < max_current_speed:
            return 0.1*self._genotype[4], 0
        
            
    def calculate_decision(self, obs: list):
        turning_ratio = self.calculate_turn(obs)
        speed_ratio, brake_ratio = self.calculate_speed(obs)

        if turning_ratio != 0 :
            speed_ratio = 0

        if brake_ratio == 0:
            self.shift_speed(speed_ratio)
        else:
            self.shift_speed(-1*self._genotype[5]*brake_ratio)


        return [turning_ratio, speed_ratio, brake_ratio]