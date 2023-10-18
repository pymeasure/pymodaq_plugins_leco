pymodaq_plugins_leco (LECO protocol)
##########################################

.. the following must be adapted to your developped package, links to pypi, github  description...


.. image:: https://github.com/pymeasure/pymodaq_plugins_leco/workflows/Upload%20Python%20Package/badge.svg
   :target: https://github.com/pymeasure/pymodaq_plugins_leco
   :alt: Publication Status

Set of PyMoDAQ plugins for controlling instruments via the Laboratory Experiment Control Protocol (`LECO <https://leco-laboratory-experiment-control-protocol.readthedocs.io/en/latest/>`_).


Authors
=======

* Benedikt Burger  (benedikt.burger@physik.tu-darmstadt.de)


Instruments
===========

Below is the list of instruments included in this plugin

Actuators
+++++++++

* **LECO_Trinamic**: Control of Trinamic motion control stepper motor cards
* **LECO_Director**: Control as a Director any actor

Viewer0D
++++++++

* **0DViewer_LECO_LISTENER**: Control of a single variable 0D detector


PID Models
==========


Extensions
==========


Infos
=====

The Actuators and Viewers of this plugin use the LECO protocol to control or read devices.

As LECO is still under development, there is not yet a PyPI package of PyLECO.
See `PyLECO <https://github.com/pymeasure/pyleco/>`_ for installation information.

