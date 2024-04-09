import time
import board
import adafruit_ina260

i2c = board.I2C()  # uses board.SCL and board.SDA
ina260 = adafruit_ina260.INA260(i2c)

# Battery Values
warning_voltage = 11.5 # warn the user when voltage drops below this
shutoff_voltage = 11 # shutoff or sternly warn when the voltage drops below this

# Constants
sample_time_delay = 1 # read every 1 second
voltage_sample_size = 10 # store and check last 10 voltage readings


# Initialize lists to store data
time_data = []
voltage_data = []

voltage_data_index =  0

while true:
   voltage_data[voltage_data_index] = ina260.voltage # store the voltage reading at the desired index
   
   voltage_data_index = (voltage_data_index + 1) % voltage_sample_size  # Increment the index to wrap around
   
   if check_for_low_battery:   # check if the battery is low and if so we gotta send a warning
      low_battery_warning
      
   if check_for_dead_battery: # check for a dead battery
      dead_battery_warning
      
   time.sleep(sample_time_delay) # pause for the delay between readings
   
   except KeyboardInterrupt:
            # Save the final plot when interrupted by the user
            plt.savefig('voltage_plot.png')
            print("Program stopped by user. Saving final plot as 'voltage_plot.png'.")
            break


def check_for_low_battery:
   for voltage in voltage_data:
      if voltage > warning_voltage:  # look for any voltage exceeding the minimum
         return false
   
   return true # return true if the battery is low (all samples are below the cutoff)
   
def check_for_dead_battery:
   for voltage in voltage_data:
      if voltage > shutoff_voltage: # look for any voltage exceeding the minimum
         return false
   
   return true    # return true if the battery is low (all samples are below the cutoff)
   
def low_battery_warning # warn the user that the battery is low
   print("Hey man your battery is low")
   
def dead_battery_warning # warn the user that the battery is dead
   print("your battery is dead bro")
   
