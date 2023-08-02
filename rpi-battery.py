import gammu
import time
from renogymodbus import RenogySmartBattery

# Setup RenoGYModbus
battery = RenogySmartBattery("/dev/ttyUSB0", 48)

def send_sms(number, message):
    # Create object for talking with phone
    sm = gammu.StateMachine()
    sm.ReadConfig()
    sm.Init()

    # Prepare message
    msg = {
        'Text': message, 
        'SMSC': {'Location': 1}, 
        'Number': number,
    }

    # Actually send the message
    sm.SendSMS(msg)

def main():
    while True:
        try:
            # Get battery voltage
            voltage = battery.get_voltage()
            bms_temperature = battery.get_bms_temperature()
            environment_temperature = battery.get_environment_temperatures()
            heater_temperature = battery.get_heater_temperatures()
            current = battery.get_current()
            remaining_capacity = battery.get_remaining_capacity()
            state_of_charge = battery.get_state_of_charge()
            message = f"voltage: {voltage}, bms_temperature: {bms_temperature}, environment_temperature: {environment_temperature}, heater_temperature: {heater_temperature}, current: {current}, remaining_capacity: {remaining_capacity}, state_of_charge: {state_of_charge}"

            # Send battery voltage info
            send_sms('6043595796', message)

            # If successful, send another SMS
            #send_sms('6049899010', '#PWD123456#OUT6=OFF')

            # Break the loop if the messages are sent successfully
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            # Wait for 60 seconds before retrying
            time.sleep(60)

if __name__ == "__main__":
    main()
