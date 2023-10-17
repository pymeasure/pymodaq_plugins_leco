import numpy as np
from pymodaq.utils.daq_utils import ThreadCommand
from pymodaq.utils.data import DataFromPlugins, DataToExport
from pymodaq.control_modules.viewer_utility_classes import DAQ_Viewer_base, comon_parameters, main
from pymodaq.utils.parameter import Parameter

from pyleco.utils.listener import Listener


class DAQ_0DViewer_LECO_Listener(DAQ_Viewer_base):
    """Viewer for data published via LECO data protocol.

    Note: This viewer uses the not yet defined data protocol, which will change most probably in the future.
    """
    params = comon_parameters+[
        {'title': 'Variable:', 'name': 'variable', 'type': 'str', 'value': "variable", 'text': 'Variable to listen to.'},
        {'title': 'Listener name', 'name': 'listener_name', 'type': 'str', 'value': "listener"},
        ## TODO for your custom plugin: elements to be added here as dicts in order to control your custom stage
        ]
    live_mode_available = True

    def ini_attributes(self):
        #  TODO declare the type of the wrapper (and assign it to self.controller) you're going to use for easy
        #  autocompletion
        self.controller: QtListener = None

        #TODO declare here attributes you want/need to init with a default value
        pass

    def commit_settings(self, param: Parameter):
        """Apply the consequences of a change of value in the detector settings

        Parameters
        ----------
        param: Parameter
            A given parameter (within detector_settings) whose value has been changed by the user
        """
        ## TODO for your custom plugin
        if param.name() == "variable":
           self.controller.unsubscribe_all()
           self.controller.subscribe([param.value()])

    def ini_detector(self, controller=None):
        """Detector communication initialization

        Parameters
        ----------
        controller: (object)
            custom object of a PyMoDAQ plugin (Slave case). None if only one actuator/detector by controller
            (Master case)

        Returns
        -------
        info: str
        initialized: bool
            False if initialization failed otherwise True
        """

        self.ini_detector_init(old_controller=controller,
                               new_controller=Listener(name=self.settings['listener_name']))
        self.controller.start_listen()
        self.controller.message_handler.handle_subscription_data = self.show_received_data
        self._live_state = False

        variable = self.settings["variable"]

        self.controller.subscribe([variable])

        info = "Whatever info you want to log"
        initialized = True  # self.controller.a_method_or_atttribute_to_check_if_init()  # TODO
        return info, initialized

    def close(self):
        """Terminate the communication protocol"""
        self.controller.stop_listen()

    def show_received_data(self, data):
        """Show the data received on the Viewer emitting an appropriate signal."""
        for key, value in data.items():
            self.dte_signal.emit(DataToExport(name=key, data=[DataFromPlugins(
                name=key,
                data=[np.array([value])],
                dim='Data0D',
                )]))
        if self._live_state is False:
            self.controller.unsubscribe_all()

    def grab_data(self, Naverage=1, live=False, **kwargs):
        """Start a grab from the detector

        Parameters
        ----------
        Naverage: int
            Number of hardware averaging (if hardware averaging is possible, self.hardware_averaging should be set to
            True in class preamble and you should code this implementation)
        kwargs: dict
            others optionals arguments
        """
        self._live_state = live
        variable = self.settings["variable"]
        self.controller.subscribe([variable])

    def stop(self):
        """Stop the current grab hardware wise if necessary"""
        self.controller.unsubscribe_all()
        self.emit_status(ThreadCommand('Update_Status', ['Some info you want to log']))
        ##############################
        return ''


if __name__ == '__main__':
    main(__file__)
