import random
import time

class WeatherApp:
    def __init__(self):
        self.temperature = 22.5
        self.humidity = 60
        
    def check_voltage(self):
        voltage = 3.5  # Simulated voltage
        if voltage >= 3.0:
            return True 
        else:
            return False
    
    def get_temperature(self):
        # Simulate temperature reading
        self.temperature = round(random.uniform(18.0, 30.0), 1)
        return self.temperature
    
    def get_humidity(self):
        # Simulate humidity reading  
        self.humidity = round(random.uniform(40, 80), 1)
        return self.humidity
    
    def display_weather(self):
        temp = self.get_temperature()
        humid = self.get_humidity()
        voltage_ok = self.check_voltage()
        
        print("=== Weather Station ===")
        print(f"Temperature: {temp}°C")
        print(f"Humidity: {humid}%")
        print(f"System Status: {'OK' if voltage_ok else 'LOW POWER'}")
        print("=======================")
    

    