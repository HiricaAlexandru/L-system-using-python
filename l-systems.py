from math import nan, sin, cos, radians
import matplotlib.pyplot as plt

class Lsystem:
    def __init__(self):
        self.states = dict()   #dictionary for holding the states
        self.variables = []    #dictionary for holding all the variables
        self.axiom = ''
        self.angle = 0
        self.generated_string = ''

    def strip_enter(self, line):
        return line.rstrip('\n')

    def read_variables(self,file):
        line_read = file.readline()
        line_read = self.strip_enter(line_read)
        line_read = line_read.split()
        
        for character in line_read:
            #put every character into the variable list
            self.variables.append(character)
        line_read = file.readline() #to read the End from file

    def read_states(self,file):
        line_read = file.readline()
        
        #add into the dictionary the states
        while 'End' not in line_read:
            line_read = self.strip_enter(line_read)
            self.states[line_read[0]] = line_read[3:]
            line_read = file.readline()


    def read_axiom(self,file):
        line_read = file.readline()
        line_read = self.strip_enter(line_read)
        self.axiom = line_read
        line_read = file.readline()
    
    def read_angle(self,file):
        line_read = file.readline()
        line_read = self.strip_enter(line_read)
        self.angle = int(line_read)
        line_read = file.readline()

    def read(self, file_name):
        file = open(file_name,'r')
        line_read = file.readline()
        while line_read:
            if 'Variables:' in line_read:
                self.read_variables(file)
            if 'States:' in line_read:
                self.read_states(file)
            if 'Axiom:' in line_read:
                self.read_axiom(file)
            if 'angle:' in line_read:
                self.read_angle(file)
            line_read = file.readline()

    def print(self):
        print("The variables are: ",self.variables)
        print("The states are: ",self.states)
        print("The axiom is: ",self.axiom)
        print("The angle is: ",self.angle)
        print("Generated string: ",self.generated_string)

    def generate(self, number_of_iterations: int):
        generated_copy = self.axiom  #at the beginning the generated string only contains the axiom
        for i in range(number_of_iterations):
            self.generated_string = ''
            for character in generated_copy:
                #if i == 1:
                #    print(character)
                #for every value that has a state, generate the corresponding string
                if character in self.states.keys():
                    self.generated_string = self.generated_string + self.states[character]
                else:
                    self.generated_string = self.generated_string+character


            generated_copy = self.generated_string # we make a copy of the generated string
            #print(generated_copy)
            
class Turtle:
    #x' = x + d*cos(angle)
    #y' = y + d*sin(angle)
    distance = 10

    def __init__(self):
        self.current_angle = 0
        self.angle_increment = 0
        self.current_sentence = ''
        self.saved_states = []
        self.coord_x_current = 0.0
        self.coord_y_current = 0.0
        self.step = 0            #current number of points. it's intialized with 1 because it will be used with a -1 value to get
        self.points = []
        self.stack_for_points = []
        self.current_length = 0 #the number of generated points
        self.recently_deleted =  -1      #if it is -1 then no element from stack_for_points was deleted
        #every constant will be stored in a dictionary with 
        self.constants = dict()
        self.constants["+"] = self.increment_angle    #+ will increment the current angle with the and move to the new location
        self.constants["-"] = self.decrement_angle
        self.constants["["] = self.save_state
        self.constants["]"] = self.delete_state
        self.constants["F"] = self.move_forward


    
    def move_forward(self):
        #x' = x + d*cos(angle)
        #y' = y + d*sin(angle)
        cosine = cos(radians(self.current_angle))
        cosine = round(cosine,2)

        sinus = sin(radians(self.current_angle))
        sinus = round(sinus,2)

        #print(sinus,cosine)

        self.coord_x_current = self.coord_x_current + (Turtle.distance * cosine)
        self.coord_y_current = self.coord_y_current + (Turtle.distance * sinus)

        if self.recently_deleted == -1:
            self.step += 1  #the number of points is incremented by one
           
        #print(self.step)
        #save the new position into the points list for plotting
        #print(self.step)

        tuplu = (self.coord_x_current,self.coord_y_current,self.step)
        self.points.append(tuplu)

        self.recently_deleted = -1
        self.current_length += 1

        self.step = self.current_length
        

    def delete_state(self):
        #To_do
        self.coord_x_current, self.coord_y_current, self.current_angle = self.saved_states.pop()
        self.recently_deleted = self.step
        
        self.step = self.stack_for_points.pop()+1
        
    def save_state(self):
        #to_do
        tuplul_starilor = (self.coord_x_current, self.coord_y_current,self.current_angle)
        self.saved_states.append(tuplul_starilor)
        self.stack_for_points.append(self.step)
        #print(self.stack_for_points)

    def increment_angle(self):
        #
        self.current_angle += self.angle_increment
        #self.move_forward()

    def decrement_angle(self):
        self.current_angle -= self.angle_increment
        #self.move_forward()

    def construct_points(self, sentence, angle_increment):
        
        self.angle_increment = angle_increment
        constant_symbols = list(self.constants.keys())
        tuplu = (self.coord_x_current,self.coord_y_current,0)
        self.points.append(tuplu) #

        for letter in sentence:
            
            if letter in constant_symbols:
                self.constants[letter]()    #we call the function corresponding to the constant
             #

        return self.points


a = Lsystem()
a.read("levy_curve.in")
a.generate(17)
a.print()
b = Turtle()
multime_pct = b.construct_points(a.generated_string,a.angle)
x_values = [x[0] for x in multime_pct]
y_values = [x[1] for x in multime_pct]
ord = [x[2] for x in multime_pct]   #the order of the points
#print(x_values,y_values)

#print(multime_pct)
#print(b.points)
print("Reprezint punctele")
for i in range(1,len(x_values)):
    #plt.plot((x_values[i-1], x_values[i]), (y_values[i-1], y_values[i]))
    plt.plot((x_values[i], x_values[ord[i]-1]), (y_values[i], y_values[ord[i]-1]))

plt.savefig('levy_curve1.svg')
#plt.show()
