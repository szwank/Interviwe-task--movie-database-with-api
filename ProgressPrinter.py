

class ProgressPrinter:
    def __init__(self, total):
        if total == 0:
            raise ValueError("Total can't be 0")
        self.total = total
        self.actual_position = 0
        self.__init_progress_bar()


    def __init_progress_bar(self):
        print("Progress {}%".format(self.actual_position / self.total * 100), end='\r', flush=True)



    def update(self):
        self.actual_position += 1

        if self.actual_position < self.total:
            print("Progress {}%".format(round(self.actual_position / self.total * 100, 2)), end='\r', flush=True)

        elif self.actual_position == self.total:
            print("Progress 100%", flush=True)
            print("\nDone!")

