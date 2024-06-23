from Counters import Time

class Clock:

    def getTime(self):
        return Time.getTime()

    def setTime(self, timetuple):
        Time.setTime(timetuple)    
   

    def getHour(self):
        # return the current hour as an int

        timetuple = Time.getTime()
        return timetuple[3]

    def setHour(self, hour):
        # sets the RTC hour to the hour parameter    
        # first get the current time from the system
        timetuple = Time.getTime()
        # convert the tuple into a list
        timelist = list(timetuple)
        #change the hour to the new hour
        timelist[3] = hour
        # save it back to the system
        Time.setTime(timelist)

    def getMinute(self):
        # return the current minute
        timetuple = Time.getTime()
        return timetuple[4]

    def setMinute(self, minute):
        timetuple = Time.getTime()
        timelist = list(timetuple)
        timelist[4] = minute
        Time.setTime(timelist)    

    def getmonth(self):    # returns the current month as an int
        timetuple = Time.getTime()
        return timetuple[1] 

    def setmonth(self, month):         
        timetuple = Time.getTime()       # retrives current month from the system
        timelist = list(timetuple)      # converts the tuple into list
        timelist[1] = month             # updates the month
        Time.setTime(timelist)         # saves it back to the system

    
    def getdate(self):
        timetuple = Time.getTime()
        return timetuple[2]

    def setdate(self, date):
        timetuple = Time.getTime()    # retrives current date from the system
        timelist = list(timetuple)    # converts the tuple into list
        timelist[2] = date           # updates the date
        Time.setTime(timelist)      # saves it back to the system
             