#########################################################################
# Collection of the data from ungoing measurment by RPi pico through UART
# 
# Output from code is: rgb_data.txt, red_data_clean.txt, 
# green_data_clean.txt, blue_data_clean.txt and XX_data_KNN.csv
#
# Requirement: User must define file path and test number
#########################################################################
import serial
import time
import csv

##########################################################################
#   Shorts for filename an test definition name
##########################################################################
data_file_path = "YOURFILEPATH"            # change manually

data_file = "_rgb_data.txt"
red_file = "_red_data_clean.txt"
green_file = "_green_data_clean.txt"
blue_file = "_blue_data_clean.txt"
csv_file = "_data_KNN.csv"

# Step 0: Set test number
test = "t50"                                                                # change manually

##########################################################################
#   Read from UART and save in txt file:
#   
#   Seriell communication via UART is directly used 
#   during RPi pico print function. 
#   The RPi pico continously writes prints collected 
#   trough the port and stored in rgb_file.
##########################################################################

# Step 1: Configure the serial connection
port = "COM6"                      
baudrate = 115200

# Step 2: Check the serial port for connection
try:
    serial_connection = serial.Serial(port, baudrate)
except Exception as e:
    print(f"Failed to connect to {port}: {e}")
    exit()

rgb_file = open(data_file_path+test+data_file, "w") 

# Step 3: Read the serial port, decode and strip the data and stored in file
try:
    while True:
        if serial_connection.in_waiting:
            line = serial_connection.readline().decode('utf-8').strip()
            print(line)

            rgb_file.write(", " + line)
            
except KeyboardInterrupt:
    print("Interrupted by user, closing...")

# Step 4: Close the connection
finally:
    serial_connection.close()

#######################################################################################
#   From rgb_file collect and clean the data:
#   Three new files created 'red_file_clean', 'green_file_clean' and 'blue_file_clean'.
#   Each file is cleaned and data for specific photo-diod output.
#######################################################################################

# Step 5: Open and clean up data files
rgb_color = open(data_file_path+test+data_file, "r")
red_file_clean = open(data_file_path+test+red_file, "w")
green_file_clean = open(data_file_path+test+green_file, "w")
blue_file_clean = open(data_file_path+test+blue_file, "w")

rflag = 0
gflag = 0
bflag = 0

# Step 6: Replace character for clean output and seperated into specific file
for line_r in rgb_color:
    cleaned_line_r = line_r.translate(str.maketrans({"[": ",", "]": "", ",": " "}))
    
    line = cleaned_line_r.split()
    
    for word in line:
        if word.startswith(','):
            word = word.lstrip(',')

        if word == "'red'":
            rflag = 1
            gflag = 0
            bflag = 0
        elif word == "'green'":
            rflag = 0
            gflag = 1
            bflag = 0
        elif word == "'blue'":
            rflag = 0
            gflag = 0
            bflag = 1

        if rflag == 1 and word != "'red'" and word != "0":
            red_file_clean.write(word+ " ")
        elif gflag == 1 and word != "'green'" and word != "0":
            green_file_clean.write(word + " ")
        elif bflag == 1 and word != "'blue'" and word != "0":
            blue_file_clean.write(word+" ")
        
# Step 7: Close files
rgb_color.close()
red_file_clean.close()
green_file_clean.close()
blue_file_clean.close()

############################################################################
# Convert from txt to csv file
############################################################################

# Step 0: set file path
fp_red = data_file_path+test+red_file
fp_green = data_file_path+test+green_file
fp_blue = data_file_path+test+blue_file


# Step 8: Read data from text file path ( 'r' - read) and save content
with open(fp_red, 'r') as file:
    content_r = file.read()

with open(fp_green, 'r') as file:
    content_g = file.read()

with open(fp_blue, 'r') as file:
    content_b = file.read()


# Step 9: Split into float numbers
numbers_r = list(map(float, content_r.strip().split()))

numbers_g = list(map(float, content_g.strip().split()))

numbers_b = list(map(float, content_b.strip().split()))

min_length = min(len(numbers_b), len(numbers_g), len(numbers_r))

# Step 10: Pair into sample and value
pairs = [(numbers_r[i], numbers_g[i], numbers_b[i]) for i in range(0, min_length-1, 3)]

# Step 11: Write to CSV
with open(data_file_path+test+csv_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['red', 'green', 'blue'])  # column headers
    writer.writerows(pairs)

print("CSV file has been created as" + csv_file)
