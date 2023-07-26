# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# Copyright (C) 2023 MUJIN Inc
# AUTO GENERATED FILE! DO NOT EDIT!

<%
def _SortedParams(params):
    # type: list[(str, dict[str, Any])] -> list[(str, dict[str, Any])]
    KWARG_PARAMS = ['kwargs', 'ignoredArgs']
    paramSortKey = lambda paramItem: paramItem[1].get('paramOrderingIndex', 998) if paramItem[0] not in KWARG_PARAMS else 999
    return sorted(params, key=paramSortKey)


def _ArgsForPayload(args):
    for name, data in args.items():
        if not any(map(lambda removalReason: data.get(removalReason, False),
            ['omit', 'deprecated', 'x-getFromPrepareCommandMethod', 'x-doNotAddToPayload'])):
            # We still need the name since it's used to as the key in the command.
            yield name, data


# TODO(heman.gandhi): Consider putting this in the client generators utilities.
def _TidyRawCode(code, indentationLevel, removeBlank=True, indentationString = ' '*4):
    """Indents multi-line strings to match the indentation they were interpolated at.

    As Mako interpolates the string, the first line is properly indented, but the subsequent ones
    lose initial indentation level. This code fixes the interpolation by adding the initial indent
    (specified as `indentationLevel`) to all but the first line (even if the first line is empty).

    Args:
        code (str): the multi-line string.
        indentationLevel (int): the number of indents the first line was at.
        removeBlank (bool): whether empty lines should be included. If they are included, they are unaltered.
        indentationString (str): represents the string used to move one indentation level.

    Returns:
        str: the indented string.
    """
    lines = []
    isFirstLine = True
    for line in code.splitlines():
        if not removeBlank or len(line) > 0:
            if isFirstLine or len(line) == 0:
                lines.append(line)
            else:
                lines.append(indentationLevel * indentationString + line)
        isFirstLine = False
    return '\n'.join(lines)

def _FormatParameterList(serviceData):
    # Note: using `map` and `filter` since Mako doesn't parse list comprehensions.
    sortedKeptParams = _SortedParams(filter(lambda item: not item[1].get('omit', False), serviceData['parameters'].items()))
    formattedParams = ['self'] + list(map(lambda item: FormatMethodParameter(*item), sortedKeptParams))
    if len(formattedParams) > 20:
        formattedParams[0] = ' ' * 8 + formattedParams[0]
        return '\n' + _TidyRawCode(',\n'.join(formattedParams), 2) + '\n' + ' ' * 4
    return ', '.join(formattedParams)

def _AssignmentRightSide(paramName, paramData):
    rightSideParamName = paramData.get('customParameterName', paramName)
    if 'forceCastList' in paramData:
        return "[" + paramData['forceCastList'] + "(f) for f in " + rightSideParamName + "]"
    if 'forceCast' in paramData:
        return paramData['forceCast'] + '(' + rightSideParamName + ')'
    return rightSideParamName
%>
import typing # noqa: F401 # used in type check
import time
import zmq
import ujson as json

from mujinplanningclient import zmqclient, TimeoutError

from . import ugettext as _
from . import VisionControllerClientError, VisionControllerTimeoutError

import logging
log = logging.getLogger(__name__)

class VisionClient(object):
    """Mujin Vision client for the ${clientTaskName} task"""

    _ctx = None  # type: zmq.Context # zeromq context to use
    _ctxown = None  # type: zmq.Context
    # if owning the zeromq context, need to destroy it once done, so this value is set
    hostname = None  # type: typing.Optional[str]  # hostname of vision controller
    commandport = None  # type: typing.Optional[int]  # command port of vision controller
    configurationport = None  # type: typing.Optional[int]  # configuration port of vision controller, usually command port + 2
    statusport = None  # type: typing.Optional[int]  # status publishing port of vision manager, usually command port + 3

    _commandsocket = None  # type: typing.Optional[zmqclient.ZmqClient]
    _configurationsocket = None  # type: typing.Optional[zmqclient.ZmqClient]
    
    _callerid = None # the callerid to send to vision
    _checkpreemptfn = None # called periodically when in a loop
    
    _subscriber = None # an instance of ZmqSubscriber, used for subscribing to the state

    _deprecated = None # used to mark arguments as deprecated (set argument default value to this)

    def __init__(
        self,
        ${extraConstructorArgs}hostname='127.0.0.1',
        commandport=7004,
        ctx=None,
        checkpreemptfn=None,
        reconnectionTimeout=40,
        callerid=None,
    ):
        """Connects to the vision server, initializes vision server, and sets up parameters

        Args:
            ${extraConstructorArgsDocstringLines}hostname (str, optional): e.g. visioncontroller1
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

    def SetDestroy(self):
        # type: () -> None
        if self._commandsocket is not None:
            self._commandsocket.SetDestroy()
        if self._configurationsocket is not None:
            self._configurationsocket.SetDestroy()
    
    def _PrepareCommand(self, commandName, callerid=None):
        # type: (str, typing.Optional[str]) -> typing.Dict
        """Adds common parameters to the command sent to the server 

        Args:
            commandName (str): 
            callerid (str, optional):
        """
        callerid = callerid or self._callerid
        command = {'command': commandName}
        if callerid:
            command['callerid'] = callerid
        return command

    def _ProcessResponse(self, response, command=None, recvjson=True):
        # type: (typing.Dict, typing.Optional[str], bool) -> typing.Dict
        
        def _HandleError(response):
            # type: (typing.Optional[typing.Dict]) -> None
            if isinstance(response['error'], dict):  # until vision manager error handling is resolved
                raise VisionControllerClientError(response['error'].get('desc', ''), errortype=response['error'].get('type', ''))
            else:
                raise VisionControllerClientError(_('Got unknown error from vision manager: %r') % response['error'], errortype='unknownerror')
        if recvjson:
            if 'error' in response:
                _HandleError(response)
        else:
            if len(response) > 0 and response[0] == '{' and response[-1] == '}':
                response = json.loads(response)
                if 'error' in response:
                    _HandleError(response)
            if len(response) == 0:
                raise VisionControllerClientError(_('Vision command %(command)s failed with empty response %(response)r') % {'command': command, 'response': response}, errortype='emptyresponseerror')
        return response

    def _ExecuteCommand(self, command, fireandforget=False, timeout=2.0, recvjson=True, checkpreempt=True, blockwait=True):
        # type: (typing.Dict, bool, float, bool, bool, bool) -> typing.Optional[typing.Dict]
        response = self._commandsocket.SendCommand(command, fireandforget=fireandforget, timeout=timeout, recvjson=recvjson, checkpreempt=checkpreempt, blockwait=blockwait)
        if blockwait and not fireandforget:
            return self._ProcessResponse(response, command=command, recvjson=recvjson)
        return response

    def _SendConfiguration(self, configuration, fireandforget=False, timeout=2.0, checkpreempt=True, recvjson=True):
        # type: (typing.Dict, bool, float, bool, bool) -> typing.Dict
        """Sends a configuration command.

        Args:
            configuration (dict):
            fireandforget (bool, optional): Whether we should return immediately after sending the command. If True, return value is None.
            timeout (float, optional): Time in seconds after which the command is assumed to have failed.
            checkpreempt (bool, optional): If a preempt function should be checked during execution.
            recvjson (bool, optional): If True, a json is received.
        """
        response = self._configurationsocket.SendCommand(configuration, fireandforget=fireandforget, timeout=timeout, checkpreempt=checkpreempt)
        if not fireandforget:
            return self._ProcessResponse(response, command=configuration, recvjson=recvjson)
        return response

    def _WaitForResponse(self, recvjson=True, timeout=None, command=None):
        # type: (bool, typing.Optional[float], typing.Optional[str]) -> typing.Dict
        """Waits for a response for a command sent on the RPC socket.

        Args:
            recvjson (bool, optional): If the response is json, should be the same value with `recvjson` of `SendAndReceive`. (Default: True)
            timeout (float, optional): (Default: None)
            command (dict, optional): Command sent to sensorbridge (Default: None)

        Raises:
            VisionControllerClientError
        """
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
        return self._commandsocket.IsWaitingReply()

    def WaitForGetLatestDetectionResultImages(self, timeout=2.0):
        # type: (bool, float) -> typing.Dict
        return self._WaitForResponse(recvjson=False, timeout=timeout)

    #
    # commands (Generated from the spec)
    #

    # Subscription command (subscribes to the state)
    def GetPublishedState(self, timeout=None, fireandforget=False):
        # type: (typing.Optional[float], bool) -> typing.Dict
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

% for serviceName, serviceData in spec['services'].items():
    def ${serviceName}(${_FormatParameterList(serviceData)}):
        ${_TidyRawCode(FormatDocstring(serviceData, _SortedParams), 2, removeBlank=False)}
        % if serviceData.get('x-methodStartSetup'):
        ${_TidyRawCode(serviceData['x-methodStartSetup'], 2)}
        % endif
        command = self._PrepareCommand('${serviceData.get('serversideCommandName', serviceName)}'\
${", " if any(data.get('x-getFromPrepareCommandMethod', False) for data in serviceData['parameters'].values()) else ""}\
${', '.join(name + '=' + name for name, data in serviceData['parameters'].items() if data.get('x-getFromPrepareCommandMethod', False))})
    ## The for-loop omits args in this way because it's difficult to have a "continue" statement without also having an empty line
    % for paramName, paramData in _ArgsForPayload(serviceData['parameters']):
        % if 'x-specialCase' in paramData and 'content' in paramData['x-specialCase'] and not paramData['x-specialCase'].get('omitRegularAssignment', False):
        ${_TidyRawCode(paramData['x-specialCase']['content'], 2)}
        % endif
        % if 'x-specialCase' in paramData and paramData['x-specialCase'].get('omitRegularAssignment', False):
            %if 'content' in paramData['x-specialCase']:
        ${_TidyRawCode(paramData['x-specialCase']['content'], 2)}
            % else:
            % endif
        % elif paramName == 'kwargs':
        command.update(kwargs)
        % elif paramData.get('isRequired'):
        command['${paramData.get('mapsTo', paramName)}'] = ${_AssignmentRightSide(paramName, paramData)}
        % else:
        if ${paramData.get('customParameterName', paramName)} ${'!=' if paramData.get('default') is not None else 'is not'} ${repr(paramData.get('default'))}:
            command['${paramData.get('mapsTo', paramName)}'] = ${_AssignmentRightSide(paramName, paramData)}
        % endif
    % endfor
    % if serviceData.get('x-omitRegularReturnStatement', False):
        % if serviceData.get('x-modifiedReturnStatement'):
        ${_TidyRawCode(serviceData['x-modifiedReturnStatement'], 2)}
        % endif
    % else:
        ${"return " if 'type' in serviceData.get('returns', {}) else ''}\
self.${'_SendConfiguration' if serviceData.get('usesConfigSocket', False) else '_ExecuteCommand'}\
(command, ${
    ', '.join(
        data.get('customParameterName', arg) + '=' + data.get('customParameterName', arg)
        for arg, data in serviceData['parameters'].items()
        if data.get('x-doNotAddToPayload', False)
    )
})\
${
    ".get('" + serviceData['returns']['returnPayloadField'] + "', None)" \
    if 'returnPayloadField' in serviceData.get('returns', {}) else \
    ''
}
    % endif

% endfor
% if extraClientContent:

% for line in extraClientContent.splitlines():
% if line.strip():
    ${line}
% else:

% endif
% endfor
% endif

VisionControllerClient = VisionClient
