from dataclasses import dataclass

from ..constants.styles import MD

class Switchtypes():
    switch = "Switch"
    dimmer = "Dimmer"


class PeriodTypes():
    wholeDay :str = "24h Hour Period"
    timeFrame :str = "Timeframe"

@dataclass
class TimeFrameValidation():
    passed :bool
    def return_Validation_Result(self):
        if self.passed == False:
            return "<br> 🚨 <mark> Your Timeframe is SHORTER than your desired ON Time</mark> "
        else:
            return ""


@dataclass
class Config():
    switchtype :Switchtypes
    nr_of_Hours_On :int
    uninterrupted :bool
    timeframe :list[list]
    periodType : str = ""
    bestHour :str = ""
    week: int = 100
    timeFrameValidation = TimeFrameValidation(False)

    def __post_init__(self):
        def check_nr_of_Hours_not_0():
            if self.nr_of_Hours_On < 1:
                raise ValueError(f"Hey your Number of Hours On can't be zero")

        def check_TimeFrame_is_large_enogh():
            if len(self.find_Possible_Hours()) > self.nr_of_Hours_On:
                self.timeFrameValidation = TimeFrameValidation(True)
            else:
                self.timeFrameValidation = TimeFrameValidation(False)
        
        def checkLogic():
            if self.uninterrupted:
                if len(self.timeframe) > 1:
                    raise ValueError(f"Hey your Timeframe has the Attribute of Beeing uninterruped means you can't have multiple timeframes")
            if self.switchtype == Switchtypes.switch and self.nr_of_Hours_On == 24:
                raise ValueError(f"Hey if it Should be on for {self.nr_of_Hours_On} there is no need for switching")


        def check_Overlapping_Arrays():
            possible_Hours = self.find_Possible_Hours()
            if(len(set(possible_Hours)) != len(possible_Hours)):
                raise ValueError(f"Hey your Timeframes {self.timeframe} have overlapping Hours. Reduce it to one")
            
        
        check_nr_of_Hours_not_0()
        check_TimeFrame_is_large_enogh()
        checkLogic()
        #check_Overlapping_Arrays()
        
    def find_Possible_Hours(self):
        possible_Hours = []
        for timeframe in self.timeframe:
            start,end = timeframe[0],timeframe[1]
            def loop_Hours(_start,_end):
                for hour in range (_start,_end):
                    possible_Hours.append(hour)
                
            if start < end:
                loop_Hours(start,end)
            elif start > end :  # timeframe goes over Midnight
                loop_Hours(start,25)
                loop_Hours(0,end)

        if possible_Hours == []:    # If its the same start and end consider the whole day is OK
            possible_Hours = [*range(0,24)]


        return possible_Hours

def return_Setup_Explanation(config:Config):
    start,end = config.timeframe[0][0],config.timeframe[0][1]
    setup_explanation_String = MD.alinCenterStart
    setup_explanation_String += f"Your Load will be switched <mark>ON for the {config.nr_of_Hours_On} cheapest Hours "
    if config.periodType.startswith(PeriodTypes.wholeDay):
        setup_explanation_String += f"during a 24h Period. "
    else:
        setup_explanation_String += f"between {start} and {end}</mark>"
    if config.uninterrupted:
        setup_explanation_String += f"</mark>Predictions based on Arregated Data says the <mark>cheapest Hour To Start a your continous {config.nr_of_Hours_On}h Cycle in week {config.week} is {config.bestHour}:00</mark> each day"
    
    setup_explanation_String += config.timeFrameValidation.return_Validation_Result()
    setup_explanation_String += MD.alinCenterStart

    return setup_explanation_String
