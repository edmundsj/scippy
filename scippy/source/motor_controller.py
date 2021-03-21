import time

class MotorController:

    @property
    def motor_position(self):
        self.write_line('MOTOR:POSITION?')
        position = int(self.read_line())
        return position

    @motor_position.setter
    def motor_position(self, motorPosition):
        """
        Sets the motor position to a desired value.

        :param motorPosition: Integer value of number of steps motor has taken
        """
        self.write_line('MOTOR:POSITION ' + str(motorPosition))


    @property
    def motor_direction(self):
        """
        Gets the motor direction of the motor.

        :returns motorDirection: The direction of the motor, either 0 (clockwise) or 1 (counterclockwise)
        """
        self.write_line('MOTOR:DIRECTION?')
        direction = int(self.read_line())
        return direction

    @motor_direction.setter
    def motor_direction(self, motor_direction):
        """
        Sets the direction of the motor to 0 (clockwise) or 1 (counterclockwise)

        :param motor_direction: A boolean or 0/1 valued integer with the direction of the motor
        """
        self.write_line('MOTOR:DIRECTION ' + str(int(bool(motor_direction))))

    @property
    def motor_rotating(self):
        """
        Checks whether the motor is currently rotating or not.

        :returns rotation: boolean value of whether the motor is currently rotating or not
        """
        self.write_line('MOTOR:ROTATE?')
        rotation_text = self.read_line()
        rotation = bool(int(rotation_text))
        return rotation

    def wait_for_motor(self):
        time.sleep(0.05)
        while(self.motor_rotating == True):
            time.sleep(0.05)

    def rotate_motor(self, n_steps):
        """
        Rotates the stepper motor by some integer number of steps.

        :param n_steps: The number of stepper motor steps to take. Positive = clockwise, negative = counterclockwise.
        """
        if self.motor_enable== False:
            self.motor_enable = True
            time.sleep(0.01)
        if(n_steps < 0):
            self.motorDirection = 1
        else:
            self.motorDirection = 0

        self.write_line('MOTOR:ROTATE ' + str(n_steps))

        # Not having this here was causing endless headaches. 
        # Better to just make this a blocking event.
        self.wait_for_motor()

    @property
    def motor_enable(self):
        self.write_line('MOTOR:ENABLED?')
        enabled = bool(int(self.read_line()))
        return enabled

    @motor_enable.setter
    def motor_enable(self, motorEnable):
        if motorEnable == True:
            self.write_line('MOTOR:ENABLE')
        elif motorEnable == False:
            self.write_line('MOTOR:DISABLE')

    @property
    def motor_period(self):
        self.write_line('MOTOR:PERIOD?')
        motorPeriod = int(self.read_line())
        return motorPeriod

    @motor_period.setter
    def motor_period(self, period):
        self.write_line('MOTOR:PERIOD ' + str(int(period)))
