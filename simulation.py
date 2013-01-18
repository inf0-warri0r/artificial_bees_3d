"""
Author : tharindra galahena (inf0_warri0r)
Project: artificial bees simulation using neural networks - part 2
Blog   : http://www.inf0warri0r.blogspot.com
Date   : 18/01/2013
License:

     Copyright 2013 Tharindra Galahena

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version. This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
details.

* You should have received a copy of the GNU General Public License along with
This program. If not, see http://www.gnu.org/licenses/.

"""

import ga
import neural_gen
import random
import sys
import display


class world:

    def __init__(self, n_bees, n_flowers, width, height, depth):
        self.bee_count = 40
        self.flower_count = 80
        self.width = width
        self.height = height
        self.depth = depth
        self.hive = (width / 2, height / 2, depth / 2)
        self.total = 1
        self.bee = list()
        self.bee_old = list()
        self.flower = list()
        self.bee_net = list()
        self.fit = list()
        self.gen_count = 0
        self.timer = 0
        self.disp = display.display(width, height)

        for i in range(0, self.bee_count):
            self.fit.append(0.0)

        for i in range(0, self.flower_count):
            x = random.randrange(50, self.width - 50)
            z = random.randrange(50, self.depth - 50)
            self.flower.append((x, self.hive[1] - 60, z, 0))

    def set_bees(self, nu1, nu2, crossover, mutation):

        for i in range(0, self.bee_count):
            self.bee_net.append(
                (neural_gen.neural(nu1[0], nu1[1], nu1[2], nu1[3]),
                neural_gen.neural(nu2[0], nu2[1], nu2[2], nu2[3])))
            self.bee.append(
                (random.uniform(0, self.width),
                random.uniform(0, self.height),
                random.uniform(0, self.depth), 0))
            self.bee_old.append(
                (random.uniform(0, self.width),
                random.uniform(0, self.height),
                random.uniform(0, self.depth), 0))
            self.bee_net[i][0].init()
            self.bee_net[i][1].init()

        self.w_num1 = self.bee_net[0][0].get_num_weights()
        self.w_num2 = self.bee_net[0][1].get_num_weights()

        self.pop = ga.population(self.bee_count, self.w_num1 + self.w_num2,
            crossover, mutation)
        self.chro = self.pop.genarate()

        for i in range(0, self.bee_count):
            l = self.split_list(self.chro[i])
            for j in range(0, 2):
                self.bee_net[i][j].put_weights(l[j])

    def distence(self, b):
        min_d = float(sys.maxint)
        min_i = 0
        for i in range(0, self.flower_count):
            d = float((self.bee[b][0] - self.flower[i][0])) ** 2.0
            d = d + float((self.bee[b][1] - self.flower[i][1])) ** 2.0
            d = d + float((self.bee[b][2] - self.flower[i][2])) ** 2.0
            if d < min_d:
                min_d = d
                min_i = i

        return self.flower[min_i]

    def split_list(self, a):
        l = list()
        l.append(list())
        l.append(list())
        for i in range(0, self.w_num1):
            l[0].append(a[i])
        for i in range(self.w_num1, self.w_num1 + self.w_num2):
            l[1].append(a[i])
        return l

    def decode(self, a, b, c):

        if a < 0.5:
            if b < 0.5:
                if c < 0.5:
                    return -5.0
                else:
                    return -3.0
            else:
                if c < 0.5:
                    return -2.0
                else:
                    return -1.0
        else:
            if b < 0.5:
                if c < 0.5:
                    return 1.0
                else:
                    return 2.0
            else:
                if c < 0.5:
                    return 3.0
                else:
                    return 5.0

    def move(self, b, output):
        x = self.bee[b][0]
        y = self.bee[b][1]
        z = self.bee[b][2]
        f = self.bee[b][3]

        dx = self.decode(output[0], output[1], output[2])
        dy = self.decode(output[3], output[4], output[5])
        dz = self.decode(output[6], output[7], output[8])

        x = x + dx
        y = y + dy
        z = z + dz

        if x < -10:
            x = 600
        if x > 610:
            x = 0
        if y < -10:
            y = 600
        if y > 610:
            y = 0
        if z < -10:
            z = 600
        if z > 610:
            z = 0

        self.bee[b] = (x, y, z, f)

    def out(self, b):
        f = self.bee[b][3]
        inputs = list()
        inputs.append(float(f))
        output = self.bee_net[b][1].update(inputs)
        if output[0] < 0.5:
            d = self.distence(b)
            inputs[0] = float(d[0] - float(self.bee[b][0]))
            inputs.append(d[1] - self.bee[b][1])
            inputs.append(d[2] - self.bee[b][2])
            output2 = self.bee_net[b][0].update(inputs)
            self.move(b, output2)
        else:
            inputs[0] = (self.hive[0] - self.bee[b][0])
            inputs.append(self.hive[1] - self.bee[b][1])
            inputs.append(self.hive[2] - self.bee[b][2])
            output2 = self.bee_net[b][0].update(inputs)
            self.move(b, output2)

    def copy(self):
        for i in range(0, self.bee_count):
            self.bee_old[i] = self.bee[i]

    def fitness(self, b):

        x = self.bee[b][0]
        y = self.bee[b][1]
        z = self.bee[b][2]
        f = self.bee[b][3]

        for i in range(0, self.flower_count):
            d = (x - self.flower[i][0]) ** 2.0
            d = d + (y - self.flower[i][1]) ** 2.0
            d = d + (z - self.flower[i][2]) ** 2.0
            d = d ** 0.5
            if d < 20.0 and d > -20.0:
                if f == 0:
                    self.flower[i] = (self.flower[i][0], self.flower[i][1],
                        self.flower[i][2], self.flower[i][3] + 1)
                    self.bee[b] = (x + 10, y + 10, z + 10, 1)
                    return 0.0
                else:
                    return 0.0

        d = (x - self.hive[0]) ** 2.0
        d = d + (y - self.hive[1]) ** 2.0
        d = d + (z - self.hive[2]) ** 2.0
        d = d ** 0.5
        if d < 60.0 and d > -60.0:
                self.bee[b] = (x, y, z, 0)
                if f == 1:
                    self.total = self.total + 1
                    return 100.0
                else:
                    return 0.0
        return 0.0

    def record(self):

        file1 = open('total.data', 'a')
        file1.write(str(self.gen_count) + ' ' + str(self.total) + '\n')
        file1.close()

    def new_genaration(self):

        for i in range(0, self.bee_count):
            self.fit[i] = self.bee_net[i][0].get_fitness()

        bf = self.pop.cal_b_fit(self.fit)
        print " generation        : ", self.gen_count
        print " best fitness      : ", self.fit[int(bf)]
        print " total honey count : ", self.total

        self.record()

        self.chro = self.pop.new_gen(self.fit)
        for i in range(0, self.bee_count):
            l = self.split_list(self.chro[i])
            for j in range(0, 2):
                self.bee_net[i][j].reset_fitness()
                self.bee_net[i][j].put_weights(l[j])

        for i in range(0, self.bee_count):
            self.bee[i] = ((random.uniform(0, self.width),
                random.uniform(0, self.height),
                random.uniform(0, self.depth), 0))
        self.gen_count = self.gen_count + 1
        self.total = 0
        print "---------------------------------------"

    def simulate(self):
        dw = self.width / 25.0
        dh = self.height / 25.0
        dd = self.depth / 25.0
        k = 12.5
        self.disp.set_cod(1.7)
        file1 = open('total.data', 'w')
        file1.close()
        print "---------------------------------------"
        while 1:
            self.disp.key_bord()
            if self.timer > 600:
                self.new_genaration()
                self.timer = 0

            self.disp.set_display()
            self.timer = self.timer + 1
            self.copy()
            for i in range(0, self.bee_count):
                self.out(i)

            for i in range(0, self.bee_count):
                fi = self.fitness(i)
                self.bee_net[i][0].update_fitness(fi)
                self.bee_net[i][1].update_fitness(fi)

            for i in range(0, self.bee_count):

                if self.bee[i][3] == 0:
                    self.disp.cube(float(self.bee[i][0]) / dw - k,
                        float(self.bee[i][1]) / dh - k,
                        float(self.bee[i][2]) / dd - k, (1.0, 0.0, 0.0), 0.1)
                else:
                    self.disp.cube(float(self.bee[i][0]) / dw - k,
                        float(self.bee[i][1]) / dh - k,
                        float(self.bee[i][2]) / dd - k, (0.0, 0.0, 1.0), 0.1)

            for i in range(0, self.flower_count):
                if self.flower[i][3] > 8:
                    x = random.randrange(50, self.width - 50)
                    z = random.randrange(50, self.depth - 50)
                    self.flower[i] = x, 240, z, 0

            for i in range(0, self.flower_count):
                if self.flower[i][3] < 5:
                    self.disp.cube(float(self.flower[i][0]) / dw - k,
                        float(self.flower[i][1]) / dh - k,
                        float(self.flower[i][2]) / dd - k,
                        (0.0, 1.0, 0.0), 0.1)
                else:
                    self.disp.cube(float(self.flower[i][0]) / dw - k,
                        float(self.flower[i][1]) / dh - k,
                        float(self.flower[i][2]) / dd - k,
                        (0.0, 1.0, 1.0), 0.1)

            self.disp.set_cod(1.7)
            self.disp.spear(float(self.hive[0]) / dw - k,
                float(self.hive[1]) / dh - k,
                float(self.hive[2]) / dd - k, (1.0, 0.0, 1.0))

            self.disp.flip()
