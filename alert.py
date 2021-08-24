class Alert:
    """
    Alert that stores state between checks
    """

    def __init__(self, threshold: float) -> None:
        self.threshold = threshold
        self.active = False
        self.previous_state = False

    def raised(self) -> bool:
        if self.active and not self.previous_state:
            return True
        return False

    def recovered(self) -> bool:
        if not self.active and self.previous_state:
            return True
        return False

    def check(self, requests_per_second: float) -> None:
        """
        Check if the value crosses the threshold and raise or recover the alert
        """
        self.previous_state = self.active
        if not self.active and requests_per_second > self.threshold:
            self.active = True
        elif self.active and requests_per_second <= self.threshold:
            self.active = False
