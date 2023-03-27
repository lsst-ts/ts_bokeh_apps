 .. py:currentmodule:: lsst.ts.bokeh.apps

.. _lsst.ts.bokeh.apps:

##################
lsst.ts.bokeh.apps
##################

.. Paragraph that describes what this Python module does and links to related modules and frameworks.

.. .. _lsst.ts.bokeh.apps-using:

.. Using lsst.ts.bokeh.apps
.. ========================

.. toctree linking to topics related to using the module's APIs.

.. .. toctree::
..    :maxdepth: 1

.. _lsst.ts.bokeh.apps-contributing:

Contributing
============

``lsst.ts.bokeh.apps`` is developed at https://github.com/lsst-ts/ts_bokeh_apps.
You can find Jira issues for this module under the `ts_bokeh_apps <https://jira.lsstcorp.org/issues/?jql=project%20%3D%20DM%20AND%20component%20%3D%20ts_bokeh_apps>`_ component.

.. If there are topics related to developing this module (rather than using it), link to this from a toctree placed here.

.. .. toctree::
..    :maxdepth: 1

.. .. _lsst.ts.bokeh.apps-scripts:

.. Script reference
.. ================

.. .. TODO: Add an item to this toctree for each script reference topic in the scripts subdirectory.

.. .. toctree::
..    :maxdepth: 1

.. .. _lsst.ts.bokeh.apps-pyapi:

Python API reference
====================

.. automodapi:: lsst.ts.bokeh.apps
   :no-main-docstr:
   :no-inheritance-diagram:

Testing Applications
===================
*Applications must be served using the bokeh serve execution, nowadays they cannot be launched inside a notebook due to a CORS error.*

Data plotted by bokeh is being taken from DBB which can be only accessed from limited locations in this case we created the testing environment inside the USDF which has permissions to access to those DB.

The first step to enter to the USDF environment is ssh to `s3dflogin.slac.stanford.edu` with username and password assigned, from that bastion server we can enter to other servers.

In this example we decided to  install the full appication inside rubin-devl server which can be ssh-accessed from this server with same username and password.
Inside rubin-devl it may be needed to create a full development environment which may be created following instructions in https://developer.lsst.io/stack/lsstsw.html, which will download and install all software needed inside a conda environment, which should be activated in order to be used, using the command lsstsw/bin/envconfig

Once inside the environment some dependencies must be installed:

.. code-block:: bash
    pip install -r requirements.txt


With the environment ready the installation of this package can be done, executing from root package folder:

.. code-block:: bash
    pip install -e .*

Now the IP of each server(*) (s3dflogin and rubin-devl) is needed, for example using ifconfig command.

With this values the bokeh server can be launched:

(*) IP may change for every connection so checking the IPs must be done each time the bokeh server is launched.

Server is ready to be launched!

For example to serve the torque viewer, moving to the folder python/lsst/ts/bokeh/apps/auxtel/ execute:

bokeh serve torque --allow-websocket-origin=<s3dflogin_ip>:<external_port>

By default bokeh port is launched in port 5006 but this can be changed launching the command with the argument: --port=<new_port_number>

The server is ready now for attending petitions, there is still one last step to make the server available to our own browser, creating the ssh tunnel, this is done in s3dflogin server, executing:

ssh -v -L <s3df_ip_server>:<external_port>:<rubin-dev_ip>:<bokeh_port> rubin-dev_ip

Now browsing to address <s3df_ip_server>:<external_port>/torques should be enough to connect to bokeh server in rubin-devl




