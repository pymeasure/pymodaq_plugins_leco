from pymodaq.control_modules.move_utility_classes import DAQ_Move_base, comon_parameters_fun, main, DataActuatorType,\
    DataActuator  # common set of parameters for all actuators
from pymodaq.utils.daq_utils import ThreadCommand # object used to send info back to the main thread
from pymodaq.utils.parameter import Parameter

from pyleco.directors.motor_director import MotorDirector


class DAQ_Move_LECO_Trinamic(DAQ_Move_base):
    """Plugin for the Trinamic motor cards via LECO protocol

    This object inherits all functionality to communicate with PyMoDAQ Module through inheritance via DAQ_Move_base
    It then implements the particular communication with the instrument

    Attributes:
    -----------
    controller: object
        The particular object that allow the communication with the hardware, in general a python wrapper around the
         hardware library
    # TODO add your particular attributes here if any

    """
    _controller_units = 'steps'
    is_multiaxes = True
    axes_names = {'Axis0': 0, 'Axis1': 1, 'Axis2': 2, 'Axis3': 3, 'Axis4': 4, 'Axis5': 5}
    _epsilon = 1
    data_actuator_type = DataActuatorType['float']  # wether you use the new data style for actuator otherwise set this
    # as  DataActuatorType['float']  (or entirely remove the line)

    params = [
        # TODO for your custom plugin: elements to be added here as dicts in order to control your custom stage
        {'title': 'Actor name:', 'name': 'actor_name', 'type': 'str', 'value': "actor_name", 'text': 'Name of the actor to communicate with.'},
        {'title': 'Use units:', 'name': "use_units", 'type': "bool", 'value': False, 'text': "Use the units given by the motor card."}
    ] + comon_parameters_fun(is_multiaxes, axes_names, epsilon=_epsilon)

    def ini_attributes(self):
        self.controller: MotorDirector = None

    def get_actuator_value(self):
        """Get the current value from the hardware with scaling conversion.

        Returns
        -------
        float: The position obtained after scaling conversion.
        """
        if self.settings["use_units"]:
            pos = self.controller.get_actual_units(self.settings['multiaxes', 'axis'])
        else:
            pos = self.controller.get_actual_position(self.settings['multiaxes', 'axis'])
            pos = self.get_position_with_scaling(pos)
        return pos

    def close(self):
        """Terminate the communication protocol"""
        self.controller.close()

    def commit_settings(self, param: Parameter):
        """Apply the consequences of a change of value in the detector settings

        Parameters
        ----------
        param: Parameter
            A given parameter (within detector_settings) whose value has been changed by the user
        """
        if param.name() == "actor_name":
           self.controller.actor = param.value()
        elif param.name() == "use_units":
            self._controller_units = "units" if param.value() else "steps"
        else:
            pass

    def ini_stage(self, controller=None):
        """Actuator communication initialization

        Parameters
        ----------
        controller: (object)
            custom object of a PyMoDAQ plugin (Slave case). None if only one actuator by controller (Master case)

        Returns
        -------
        info: str
        initialized: bool
            False if initialization failed otherwise True
        """
        communicator = controller.communicator if controller is not None else None

        self.controller = self.ini_stage_init(
            old_controller=controller,
            new_controller=MotorDirector(actor=self.settings["actor_name"],
                                         communicator=communicator))

        info = "Whatever info you want to log"
        initialized = True  # TODO return whether communication works
        return info, initialized

    def move_abs(self, value: DataActuator):
        """ Move the actuator to the absolute target defined by value

        Parameters
        ----------
        value: (float) value of the absolute target positioning
        """

        value = self.check_bound(value)  #if user checked bounds, the defined bounds are applied here
        self.target_value = value
        value = self.set_position_with_scaling(value)  # apply scaling if the user specified one

        if self.setting["use_units"]:
            self.controller.move_to_units(self.settings['multiaxes', 'axis'], value)
        else:
            self.controller.move_to(self.settings['multiaxes', 'axis'], value)

        return
        ## TODO for your custom plugin
        self.emit_status(ThreadCommand('Update_Status', ['Some info you want to log']))

    def move_rel(self, value: DataActuator):
        """ Move the actuator to the relative target actuator value defined by value

        Parameters
        ----------
        value: (float) value of the relative target positioning
        """
        value = self.check_bound(self.current_position + value) - self.current_position
        self.target_value = value + self.current_position
        value = self.set_position_relative_with_scaling(value)

        if self.setting["use_units"]:
            self.controller.move_by_units(self.settings['multiaxes', 'axis'], value)
        else:
            self.controller.move_by(self.settings['multiaxes', 'axis'], value)

        return
        ## TODO for your custom plugin
        self.emit_status(ThreadCommand('Update_Status', ['Some info you want to log']))


    def move_home(self):
        """Call the reference method of the controller"""

        ## TODO for your custom plugin
        raise NotImplemented  # when writing your own plugin remove this line
        self.controller.your_method_to_get_to_a_known_reference()  # when writing your own plugin replace this line
        self.emit_status(ThreadCommand('Update_Status', ['Some info you want to log']))

    def stop_motion(self):
        """Stop the actuator and emits move_done signal"""

        self.controller.stop(self.settings['multiaxes', 'axis'])

        return
        ## TODO for your custom plugin
        self.emit_status(ThreadCommand('Update_Status', ['Some info you want to log']))


if __name__ == '__main__':
    main(__file__)
