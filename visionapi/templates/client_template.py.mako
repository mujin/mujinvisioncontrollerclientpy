# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# Mujin vision controller client for bin picking task
# Copyright (C) 2023 MUJIN Inc
# AUTO GENERATED FILE! DO NOT EDIT!

# system imports
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Any, Callable, Dict, List, Optional, Tuple, Union # noqa: F401 # used in type check

# mujin imports
from mujinplanningclient import zmqclient, zmqsubscriber, TimeoutError
from . import VisionControllerClientError, VisionControllerTimeoutError
from . import json
from . import zmq
from . import ugettext as _

try:
    import mujincommon.i18n
    ugettext, ungettext = mujincommon.i18n.GetDomain('mujinvisioncontrollerclientpy').GetTranslationFunctions()
except ImportError:
    def ugettext(message):
        return message

    def ungettext(singular, plural, n):
        return singular if n == 1 else plural

_ = ugettext


try:
    import ujson as json  # noqa: F401
except ImportError:
    import json  # noqa: F401

import zmq  # noqa: F401 # TODO: stub zmq
import six

@six.python_2_unicode_compatible
class VisionControllerClientError(Exception):
    _type = None  # type: six.text_type # In PY2, it is unicode; in PY3, it is str
    _desc = None  # type: six.text_type # In PY2, it is unicode; In PY3, it is str

    def __init__(self, errordesc, errortype='unknownerror'):
        # type: (Union[six.text_type, str], Union[six.text_type, str]) -> None
        if errortype is not None and not isinstance(errortype, six.text_type):
            # Then errortype is str, and we need to decode it back to unicode:
            # noinspection PyUnresolvedReferences
            errortype = errortype.decode('utf-8', 'ignore')
        if errordesc is not None and not isinstance(errordesc, six.text_type):
            # noinspection PyUnresolvedReferences
            errordesc = errordesc.decode('utf-8', 'ignore')

        self._type = errortype
        self._desc = errordesc

    def __str__(self):
        # type: () -> str
        # By doing this we are implicitly not doing any translation
        # To enable translation, need to import mujincommon
        return "%s: %s, %s" % (self.__class__.__name__, self._type, self._desc)

    def __repr__(self):
        # type: () -> str
        return "<%r(%r, %r)>" % (self.__class__.__name__, self._type, self._desc)

    def __hash__(self):
        # type: () -> int
        return hash((self._type, self._desc))

    def __eq__(self, r):
        # type: (VisionControllerClientError) -> bool
        return self._type == r._type and self._desc == r._desc

    def __ne__(self, r):
        # type: (VisionControllerClientError) -> bool
        return self._type != r._type or self._desc != r._desc

class VisionControllerTimeoutError(VisionControllerClientError):
    pass

# logging
import logging
log = logging.getLogger(__name__)

class VisionClient(object):
    """Mujin Vision client for the ${clientTaskName} tasks."""

    _ctx = None  # type: Optional[zmq.Context] # zeromq context to use
    _ctxown = None  # type: Optional[zmq.Context]
    # if owning the zeromq context, need to destroy it once done, so this value is set
    hostname = None  # type: Optional[str] # hostname of vision controller
    commandport = None  # type: Optional[int] # command port of vision controller
    configurationport = None  # type: Optional[int] # configuration port of vision controller, usually command port + 2
    statusport = None  # type: Optional[int] # status publishing port of vision manager, usually command port + 3

    _commandsocket = None  # type: Optional[zmqclient.ZmqClient]
    _configurationsocket = None  # type: Optional[zmqclient.ZmqClient]
    
    _callerid = None # the callerid to send to vision
    _checkpreemptfn = None # called periodically when in a loop
    
    _subscriber = None # an instance of ZmqSubscriber, used for subscribing to the state

    _deprecated = None # used to mark arguments as deprecated (set argument default value to this)

    def __init__(self, hostname='127.0.0.1', commandport=7004, ctx=None, checkpreemptfn=None, reconnectionTimeout=40, callerid=None):
        # type: (str, int, Optional[zmq.Context], Optional[Callable], float, Optional[str]) -> None
        """Connects to the vision server, initializes vision server, and sets up parameters

        Args:
            hostname (str, optional): e.g. visioncontroller1
            commandport (int, optional): e.g. 7004
            ctx (zmq.Context, optional): The ZMQ context
            checkpreemptfn (Callable, optional): Called periodically when in a loop. A function handle to preempt the socket. The function should raise an exception if a preempt is desired.
            reconnectionTimeout (float, optional): Sets the "timeout" parameter of the ZmqSocketPool instance
            callerid (str, optional): The callerid to send to vision.
        """
        self.hostname = hostname
        self.commandport = commandport
        self.configurationport = commandport + 2
        self.statusport = commandport + 3
        self._callerid = callerid
        self._checkpreemptfn = checkpreemptfn

        if ctx is None:
            self._ctxown = zmq.Context()
            self._ctxown.linger = 100
            self._ctx = self._ctxown
        else:
            self._ctx = ctx

        self._commandsocket = zmqclient.ZmqClient(self.hostname, commandport, ctx=self._ctx, limit=3, checkpreemptfn=checkpreemptfn, reusetimeout=reconnectionTimeout)
        self._configurationsocket = zmqclient.ZmqClient(self.hostname, self.configurationport, ctx=self._ctx, limit=3, checkpreemptfn=checkpreemptfn, reusetimeout=reconnectionTimeout)
        self._validationQueue = None
        self._lastCommandCall = None
        if os.environ.get('MUJIN_VALIDATE_APIS', False):
            from mujinapispecvalidation.apiSpecServicesValidation import ValidationQueue, ParameterIgnoreRule
            try:
                from mujinvisioncontrollerclient.visionapi import visionControllerClientSpec
            except ImportError:
                log.warn('Could not import spec, using JSON instead')
                import json
                installDir = os.environ.get('MUJIN_INSTALL_DIR', 'opt')
                specExportPath = os.path.join(installDir, 'share', 'apispec', 'en_US.UTF-8', 'mujinrobotbridgeapi.spec_robotbridge.robotBridgeSpec.json')
                visionControllerClientSpec = json.load(open(specExportPath))
            ignoreParametersConfigs = [ParameterIgnoreRule(parameter=p) for p in ['command', 'callerid', 'sendTimeStamp', 'queueid']]
            self._validationQueue = ValidationQueue(apiSpec=visionControllerClientSpec, parameterIgnoreRules=ignoreParametersConfigs, clientName='VisionControllerClient')

    def __del__(self):
        self.Destroy()

    def Destroy(self):
        # type: () -> None
        self.SetDestroy()

        if self._commandsocket is not None:
            try:
                self._commandsocket.Destroy()
                self._commandsocket = None
            except Exception as e:
                log.exception('problem destroying commandsocket: %s', e)

        if self._configurationsocket is not None:
            try:
                self._configurationsocket.Destroy()
                self._configurationsocket = None
            except Exception as e:
                log.exception('problem destroying configurationsocket: %s', e)

        if self._subscriber is not None:
            self._subscriber.Destroy()
            self._subscriber = None
        
        if self._ctxown is not None:
            try:
                self._ctxown.destroy()
                self._ctxown = None
            except Exception as e:
                log.exception('problem destroying ctxown: %s', e)

        self._ctx = None
        if self._validationQueue:
            self._validationQueue.StopValidationProcess()

    def SetDestroy(self):
        # type: () -> None
        if self._commandsocket is not None:
            self._commandsocket.SetDestroy()
        if self._configurationsocket is not None:
            self._configurationsocket.SetDestroy()

    def _ExecuteCommand(self, command, fireandforget=False, timeout=2.0, recvjson=True, checkpreempt=True, blockwait=True):
        # type: (Dict, bool, float, bool, bool, bool) -> Any
        """Executes given command.

        Args:
            configuration (dict): Command in json format.
            fireandforget (bool, optional): Whether we should return immediately after sending the command. If True, return value is None.
            timeout (float, optional): Time in seconds after which the command is assumed to have failed.
            recvjson (bool, optional): If True, a json is received.
            checkpreempt (bool, optional): If a preempt function should be checked during execution.
            blockwait (bool, optional): If True, will block and wait until function is done. Otherwise user will have to call _ProcessResponse on their own. (Default: True)
        """
        assert self._commandsocket is not None
        if self._callerid:
            command['callerid'] = self._callerid
        if self._validationQueue:
            self._lastCommandCall = command
        response = self._commandsocket.SendCommand(command, fireandforget=fireandforget, timeout=timeout, recvjson=recvjson, checkpreempt=checkpreempt, blockwait=blockwait)
        if blockwait and not fireandforget:
            return self._ProcessResponse(response, command=command, recvjson=recvjson)
        return response

    def _ProcessResponse(self, response, command=None, recvjson=True):
        # type: (Any, Optional[Dict], bool) -> Any

        def _HandleError(response):
            # type: (Dict) -> None
            if isinstance(response['error'], dict):  # until vision manager error handling is resolved
                raise VisionControllerClientError(response['error'].get('desc', ''), errortype=response['error'].get('type', ''))
            else:
                raise VisionControllerClientError(_('Got unknown error from vision manager: %r') % response['error'], errortype='unknownerror')
        if recvjson:
            if 'error' in response:
                _HandleError(response)
            elif self._validationQueue:
                if command is None:
                    log.warn('Cannot validate! Got response=' + str(response))
                else:
                    self._validationQueue.Add(command['command'], command, response)
        else:
            if len(response) > 0 and response[0] == '{' and response[-1] == '}':
                response = json.loads(response)
                if 'error' in response:
                    _HandleError(response)
                elif self._validationQueue:
                    if command is None:
                        log.warn('Cannot validate! Got response=' + str(response))
                    else:
                        self._validationQueue.Add(command['command'], command, response)
            if len(response) == 0:
                raise VisionControllerClientError(_('Vision command %(command)s failed with empty response %(response)r') % {'command': command, 'response': response}, errortype='emptyresponseerror')
        return response

    def _WaitForResponse(self, recvjson=True, timeout=None, command=None):
        # type: (bool, Optional[float], Optional[Dict]) -> Dict
        """Waits for a response for a command sent on the RPC socket.

        Args:
            recvjson (bool, optional): If the response is json, should be the same value with `recvjson` of `SendAndReceive`. (Default: True)
            timeout (float, optional): (Default: None)
            command (dict, optional): Command sent to sensorbridge (Default: None)

        Raises:
            VisionControllerClientError
        """
        assert self._commandsocket is not None
        commandName = ''
        if command is not None and isinstance(command, dict):
            commandName = command.get('command') or ''

        if not self._commandsocket.IsWaitingReply():
            raise VisionControllerClientError(_('Waiting on command "%(commandName)s" when wait signal is not on') % {
                'commandName': commandName,
            }, errortype='invalidwait')

        try:
            response = self._commandsocket.ReceiveCommand(timeout=timeout, recvjson=recvjson)
        except TimeoutError as e:
            raise VisionControllerTimeoutError(_('Timed out after %.03f seconds to get response message %s from %s:%d: %s') % (timeout, commandName, self.hostname, self.commandport, e), errortype='timeout')
        except Exception as e:
            raise VisionControllerClientError(_('Problem receiving response from the last vision manager async call %s: %s') % (commandName, e), errortype='unknownerror')
        return self._ProcessResponse(response, command=command, recvjson=recvjson)

    def IsWaitingResponse(self):
        # type: () -> bool
        """Returns whether the client is waiting for response on the command socket, and caller should call WaitForResponse().
        """
        assert self._commandsocket is not None
        return self._commandsocket.IsWaitingReply()

    def WaitForGetLatestDetectionResultImages(self, timeout=2.0):
        # type: (float) -> Dict
        """Waits for response to GetLatestDetectionResultImages command

        Args:
            timeout (float, optional): Time in seconds after which the command is assumed to have failed. (Default: 2.0)
        """
        return self._WaitForResponse(recvjson=False, timeout=timeout)

    def _SendConfiguration(self, configuration, fireandforget=False, timeout=2.0, checkpreempt=True, recvjson=True):
        # type: (Dict, bool, float, bool, bool) -> Any
        """Sends a configuration command.

        Args:
            configuration (dict): Configuration to send in json format.
            fireandforget (bool, optional): Whether we should return immediately after sending the command. If True, return value is None.
            timeout (float, optional): Time in seconds after which the command is assumed to have failed.
            checkpreempt (bool, optional): If a preempt function should be checked during execution.
            recvjson (bool, optional): If True, a json is received.
        """
        assert self._configurationsocket is not None
        if self._callerid:
            configuration['callerid'] = self._callerid
        response = self._configurationsocket.SendCommand(configuration, fireandforget=fireandforget, timeout=timeout, checkpreempt=checkpreempt)
        if not fireandforget:
            return self._ProcessResponse(response, command=configuration, recvjson=recvjson)
        return response

    #
    # Commands (generated from the spec)
    #

% for serviceName, serviceData in services.items():
    <%include file="/serviceTemplate.py.mako" args="serviceName=serviceName,serviceData=serviceData,usePrepareCommand=False" />
% endfor

    # Subscription command (subscribes to the state)
    def GetPublishedState(self, timeout=None, fireandforget=False):
        # type: (Optional[float], bool) -> Optional[Dict]
        """
        Args:
            timeout (float, optional):
            fireandforget (bool, optional): (Default: False)

        Returns:
            dict: An unstructured dictionary.
        """
        if self._subscriber is None:
            self._subscriber = zmqsubscriber.ZmqSubscriber('tcp://%s:%d' % (self.hostname, self.statusport), ctx=self._ctx)
        rawState = self._subscriber.SpinOnce(timeout=timeout, checkpreemptfn=self._checkpreemptfn)
        if rawState is not None:
            return json.loads(rawState)
        return None


VisionControllerClient = VisionClient
