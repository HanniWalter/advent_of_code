
from cellular_automata import Automata
from cellular_automata import state_number_encoder



def create_pattern(input, patternfilename, refAutomata):
    #read input
    with open(input, 'r') as f:
        lines = f.readlines()
    outputlines = []

    #outputlines.append("x= " + str(len(lines[0]))+ ", y= " + str(len(lines)) + ", rule = " + refAutomata.name)
    temp_pattern = []

    for line in lines:
        line = line.strip()
        pattern = ""
        for char in line:
            if char in "0123456789":
                charnumber = refAutomata.state_number[char]
            elif char == " ":
                charnumber = 0
            elif char not in refAutomata.state_number:
                print("ERROR: "+ char +" not in states")
                exit()
            charchar = state_number_encoder(charnumber)
            pattern+=charchar
        temp_pattern.append(pattern)
        #pattern+="$"
    #pattern = pattern[:-1] + "!"
    max_pattern_length = 0
    for line in temp_pattern:
        if len(pattern) > max_pattern_length:
            max_pattern_length = len(pattern)
    #make every pattern the same lenght
    emptychar = state_number_encoder(0)
    for i in range(len(temp_pattern)):
        while len(temp_pattern[i]) < max_pattern_length:
            temp_pattern[i] += emptychar
    pattern = ""
    for line in temp_pattern:
        pattern += line + "$"
    pattern = pattern[:-1] + "!"
    
    outputlines.append("x= " + str(max_pattern_length)+ ", y= " + str(len(lines)) + ", rule = " + refAutomata.name)
    outputlines.append(pattern)

    #write to file:
    with open("Rules/" + patternfilename + ".rle", 'w') as f:
        for line in outputlines:
            f.write(line + '\n')

def main():
    rulename = "aoc2024_2_1"

    A = Automata(rulename)
    A.add_state("0", color=[0,0,30])
    A.add_state("1", color=[0,0,55])
    A.add_state("2", color=[0,0,80])
    A.add_state("3", color=[0,0,105])
    A.add_state("4", color=[0,0,130])
    A.add_state("5", color=[0,0,155])
    A.add_state("6", color=[0,0,180])
    A.add_state("7", color=[0,0,205])
    A.add_state("8", color=[0,0,230])
    A.add_state("9", color=[0,0,255])

    #transform 2digits to single digit
    for i in range(100):
        A.add_state("A_"+str(i), color=[0,0,i*2])
    for i in range(10):
        A.transform_when_E_W(str(i), "A_"+str(i), "EMPTY", "EMPTY")
    for i in range(10):
        for j in range(10):
            combined = i*10+j
            A.transform_when_W(str(j), "A_"+str(combined), str(i))
            A.transform_when_E(str(i), "A_"+str(combined), str(j))

    for i in range(100):
        A.just_transform("A_"+str(i), "EMPTY")

    A.add_state("wrong", color=[255,255,255])
    A.add_state("smaller", color=[155,0,155])
    A.add_state("higher", color=[255,0,255])
    for w in range(100):
        for e in range(100):
            cell_new = "wrong"
            diff = e-w
            if 0<diff<4 :
                cell_new = "smaller"
            elif -4<diff<0:
                cell_new = "higher"
            
            A.transform_when_E_W("EMPTY" ,cell_new ,"A_"+str(w), "A_"+str(e))
    A.add_state("left_marker", color=[0,255,255])
    for i in range(10):
        A.transform_when_E_W("EMPTY", "left_marker", str(i), "EMPTY")

    for i in range(4):
        A.add_state("left_smaller_"+str(i), color=[0,255,255])
        A.add_state("left_higher_"+str(i), color=[0,255,255])
        A.add_state("left_wrong_"+str(i), color=[0,255,255]) 

        A.transform_when_E("left_smaller_"+str(i),"left_wrong_0" ,"wrong")
        A.transform_when_E("left_smaller_"+str(i),"left_wrong_0" ,"higher")
        A.transform_when_E("left_smaller_"+str(i),"left_smaller_0" ,"smaller")
        A.transform_when_E("left_higher_"+str(i),"left_wrong_0" ,"wrong")
        A.transform_when_E("left_higher_"+str(i),"left_wrong_0" ,"smaller")
        A.transform_when_E("left_higher_"+str(i),"left_higher_0" ,"higher")
        A.transform_when_E("left_wrong_"+str(i), "left_wrong_0" ,"wrong")
        A.transform_when_E("left_wrong_"+str(i), "left_wrong_0" ,"smaller")
        A.transform_when_E("left_wrong_"+str(i), "left_wrong_0" ,"higher")

    A.transform_when_E("left_marker", "left_smaller_0", "smaller")
    A.transform_when_E("left_marker", "left_higher_0", "higher")
    A.transform_when_E("left_marker", "left_wrong_0", "wrong")
    
    for i in range(3):
        A.just_transform("left_smaller_"+str(i), "left_smaller_"+str(i+1))
        A.just_transform("left_higher_"+str(i), "left_higher_"+str(i+1))
        A.just_transform("left_wrong_"+str(i), "left_wrong_"+str(i+1))

    A.add_state("Token", color=[255,0,255])
    A.add_state("No_Token", color=[155,0,155])
    A.just_transform("left_smaller_3", "Token")
    A.just_transform("left_higher_3", "Token")
    A.just_transform("left_wrong_3", "No_Token")

    A.just_transform("wrong", "EMPTY")
    A.just_transform("smaller", "EMPTY")
    A.just_transform("higher", "EMPTY")
    A.transform_when_E("EMPTY", "wrong", "wrong")
    A.transform_when_E("EMPTY", "smaller", "smaller")
    A.transform_when_E("EMPTY", "higher", "higher")    
    
   

    #counting
    for i in range(11):
        A.add_state("c_"+str(i), color=[0,25*i,25*i])
    A.transform_when_S("EMPTY", "c_0", "left_marker")
    for i in range(10):
        A.transform_when_E("c_"+str(i), "c_"+str(i+1), "c_10")
    A.transform_when_E("EMPTY", "c_1", "c_10")
    A.just_transform("c_10", "c_0")
    for i in range(10):
        A.transform_when_S("c_"+str(i), "c_"+str(i+1), "Token")
    
    #moving up
    A.transform_when_S("EMPTY", "Token", "Token")
    A.transform_when_S("EMPTY", "No_Token", "No_Token")
    A.transform_when_N("Token", "EMPTY", "EMPTY")
    A.transform_when_N("No_Token", "EMPTY", "EMPTY")
    
    for i in range(11):
        A.transform_when_N("Token", "EMPTY", "c_"+str(i))
        A.transform_when_N("No_Token", "EMPTY", "c_"+str(i)) 
    #finish

    A.create_rule("Rules/" +rulename+".rule")
    A.print_states()
    input = "input"
    patternfilename = "aoc2024_test"
    create_pattern(input, patternfilename,A)

if __name__ == '__main__':
    main()