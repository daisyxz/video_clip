class Caption:
    def __init__(self, cap_dict):
        self.id = cap_dict["id"] if "id" in cap_dict.keys() else -1
        self.text = cap_dict["text"] if "text" in cap_dict.keys() else ""
        self.start_time = cap_dict["start_time"] if "start_time" in cap_dict.keys() else ""
        self.end_time = cap_dict["end_time"] if "end_time" in cap_dict.keys() else ""
        self.start_time_sec = sum(x * int(t) for x, t in zip([3600, 60, 1], self.start_time.split(",")[0].split(':')))\
                    + float(self.start_time.split(",")[1])/1000
        self.end_time_sec =  sum(x * int(t) for x, t in zip([3600, 60, 1], self.end_time.split(",")[0].split(':')))\
                    + float(self.end_time.split(",")[1])/1000

        self.duration_sec = self.end_time_sec - self.start_time_sec





    


