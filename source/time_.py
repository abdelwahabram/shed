import time, math

class Time:
    def __init__(self):
        
        self.time = time.time()
        
        self.time_zone_offset = None
        
        self.set_time_zone_offset()
    
    def get_time(self):
        
        return int(time.time())
    
    
    def set_time_zone_offset(self):
        timeOffsetInSeconds = time.localtime().tm_gmtoff

        timeOffsetInHours = timeOffsetInSeconds / 3600

        westOfGMT = True if timeOffsetInHours < 0 else False

        timeOffsetInHours = abs(timeOffsetInHours)
        
        fraction, whole = math.modf(timeOffsetInHours)

        hours = int(whole)
        minutes = int(fraction * 60)

        HH = f"{hours}" if hours > 9 else f"0{hours}"
        MM = f"{minutes}" if minutes > 9 else f"0{minutes}"

        self.time_zone_offset = "-" + HH + MM if westOfGMT else "+" + HH + MM
    
    
    def get_time_zone_offset(self):
        return self.time_zone_offset