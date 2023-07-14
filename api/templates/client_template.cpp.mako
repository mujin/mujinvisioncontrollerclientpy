// -*- coding: utf-8 -*-
// Copyright (C) 2022 Mujin,Inc.
#include <mujinvisioncontrollerclient/visioncontrollerclient.h>

#include <mujincontrollercommon/i18n.h>
#include <mujincontrollercommon/logging.h>

MUJIN_LOGGER("mujin.visioncontrollerclient.client");

// define _ for translations
#define _(msgid) mujincontrollercommon::GetLocalizedTextForDomain("sensorbridgeclient", msgid)

namespace mujinvisioncontrollerclient {

namespace {

uint64_t _GetMilliTime64()
{
    uint32_t sec, nsec;
    struct timespec start;
    clock_gettime(CLOCK_REALTIME, &start);
    sec = start.tv_sec;
    nsec = start.tv_nsec;
    return static_cast<uint64_t>(sec) * 1000 + static_cast<uint64_t>(nsec) / 1000000;
}

}  // end anonymous namespace

const char* VisionControllerClientException::GetVisionControllerClientErrorCodeString(VisionControllerClientErrorCode error)
{
    switch (error)
    {
    // TODO(heman.gandhi): determine if we should standardize these strings
    case VCCEC_Assert:
        return "Assert";
    case VCCEC_Failed:
        return "Failed";
    case VCCEC_FailedToSendZMQRequest:
        return "VCCEC_FailedToSendZMQRequest";
    case VCCEC_InvalidZMQResponse:
        return "VCCEC_InvalidZMQResponse";
    case VCCEC_CallTimeout:
        return "VisionControllerCallTimeout";
    case VCCEC_ZMQRecvError:
        return "VisionControllerZMQRecvError";
    case VCCEC_InvalidArgument:
        return "InvalidArgument";
    case VCCEC_UnexpectedReturnData:
        return "UnexpectedReturnData";
    }
    return "";
}

VisionControllerClient::VisionControllerClient(
    boost::shared_ptr<zmq::context_t>& context,
    const std::string& host,
    const uint16_t port,
    const uint64_t timeoutMS,
    const std::string& callerId)
{
    _context = context;
    _timeoutMS = timeoutMS;
    _vRapidJsonBuffer.resize(100000);
    _rAlloc = boost::make_shared<rapidjson::MemoryPoolAllocator<> >(&_vRapidJsonBuffer[0], _vRapidJsonBuffer.size());
    _sendDataPool = boost::make_shared<mujincontrollercommon::DataPool<SendDataEntry> >(2, std::string("sendData"));
    _callerId = callerId;
    if (_callerId.empty()) {
        _callerId = boost::str(boost::format("sensorbridgeclientcpp/%s (pid %d)")%MUJINVISIONCONTROLLERCLIENT_VERSION_STRING%getpid());
    }
    SetConnectionInfo(host, port);
}

VisionControllerClient::~VisionControllerClient() {}

void VisionControllerClient::SetConnectionInfo(const std::string& host, const uint16_t port)
{
    if (host == _host && port == _port) {
        return; // no change
    }

    _host = host;
    _port = port;
    _currentCommandSocket.reset();
    _commandSocketPool.reset();
}

void VisionControllerClient::_SendAndReceiveFromSocket(boost::shared_ptr<zmq::socket_t> socket, const std::string& command, const rapidjson::Value& rParameterValue, rapidjson::Value& rReturnValue, rapidjson::Document::AllocatorType& rReturnAlloc, double timeout)
{
    _EnsureSocket(socket);
    rapidjson::Document rCommand(_rAlloc.get());
    rCommand.SetObject();
    
    if (rParameterValue.IsObject()) {
        mujinjson::UpdateJson(rCommand, rParameterValue);
    }
    const uint64_t startTimeMS = _GetMilliTime64();
    const uint64_t timeoutMS = timeout * 1000.0;
    _SendCommandJSON(socket, rCommand, rCommand.GetAllocator(), command.c_str(), timeoutMS);
    _rAlloc->Clear();

    rapidjson::Document rResponse(_rAlloc.get());
    const uint64_t timeSpentSendingMS = _GetMilliTime64() - startTimeMS;
    _ReceiveResponseJSON(socket, rResponse, command.c_str(), timeoutMS-timeSpentSendingMS);

    rReturnValue.CopyFrom(rResponse, rReturnAlloc);
}

void VisionControllerClient::_SendCommandJSON(boost::shared_ptr<zmq::socket_t> socket, rapidjson::Value& rCommand, rapidjson::Document::AllocatorType& rAlloc, const char* commandString, uint64_t timeoutMS)
{
    mujinjson::SetJsonValueByKey(rCommand, "command", commandString, rAlloc);
    if (!_callerId.empty()) {
        mujinjson::SetJsonValueByKey(rCommand, "callerid", _callerId, rAlloc);
    }
    mujinjson::SetJsonValueByKey(rCommand, "sendTimeStamp", _GetMilliTime64(), rAlloc);

    SendDataEntry *sendDataEntry = _sendDataPool->AllocateRaw();
    sendDataEntry->second = this; // initialize
    rapidjson::MemoryBuffer& mbSendBuffer = sendDataEntry->first;
    mbSendBuffer.Clear();
    using OutputStream = rapidjson::EncodedOutputStream<rapidjson::UTF8<>, rapidjson::MemoryBuffer>;
    OutputStream os(mbSendBuffer, false); // no utf-8 bom
    rapidjson::Writer<OutputStream> writer(os);
    rCommand.Accept(writer);

    zmq::message_t message((void *)mbSendBuffer.GetBuffer(), mbSendBuffer.GetSize(), _ReleaseSendBuffer, sendDataEntry);
    _SendCommand(socket, message, commandString, timeoutMS);
}

void VisionControllerClient::_SendCommand(boost::shared_ptr<zmq::socket_t> socket, zmq::message_t& message, const char* commandString, uint64_t timeoutMS)
{
    const uint64_t startTime = _GetMilliTime64();

    // Try sending. Recreate client once on error.
    bool recreatedOnce = false;
    while (_GetMilliTime64() - startTime < timeoutMS) {
        _EnsureSocket(socket);

        try {
            socket->send(message, zmq::send_flags::none);
            return;
        }
        catch (const zmq::error_t& e) {
            if (!recreatedOnce) {
                MUJIN_LOG_WARN_FORMAT("failed to send command '%s' to sensorbridges. Re-initializing socket once. Error: %s", commandString%e.what());
                if (!!socket) {
                    socket->close();
                    socket.reset();
                }
                recreatedOnce = true;
            }
            else {
                MUJIN_LOG_ERROR_FORMAT("failed to send command '%s' to sensorbridges even after re-creating socket: %s", commandString%e.what());
                throw VisionControllerClientException(boost::str(boost::format(_("Failed to send '%s' command to sensorbridges: %s"))%commandString%e.what()), VisionControllerClientException::VCCEC_Failed);
            }
        }
    }

    const uint64_t elapsedTime = _GetMilliTime64() - startTime;
    MUJIN_LOG_ERROR_FORMAT("Timed out sending command '%s' to sensorbridges for command '%s' after %d milliseconds", commandString%elapsedTime);
    throw VisionControllerClientException(boost::str(boost::format(_("Timed out sending command '%s' to sensorbridges after %d milliseconds"))%commandString%elapsedTime), VisionControllerClientException::VCCEC_CallTimeout);
}

void VisionControllerClient::_ReceiveResponse(boost::shared_ptr<zmq::socket_t> socket, zmq::message_t& message, const char* commandString, uint64_t timeoutMS)
{
    const uint64_t startTime = _GetMilliTime64();
    while ((_GetMilliTime64() - startTime < timeoutMS)) {
        try {
            zmq::pollitem_t pollitems[] = {
                { (void*)*socket, 0, ZMQ_POLLIN, 0 },
            };
            zmq::poll(pollitems, 1, std::chrono::milliseconds{50}); // wait ms for message
            if (pollitems[0].revents & ZMQ_POLLIN) {
                zmq::recv_result_t success = socket->recv(message, zmq::recv_flags::dontwait);
                if (!success) {
                    throw VisionControllerClientException(boost::str(boost::format(_("Received no data in response for command '%s' from sensorbridges"))%commandString), VisionControllerClientException::VCCEC_InvalidZMQResponse);
                }
                return;
            }
        }
        catch (const zmq::error_t& e) {
            MUJIN_LOG_ERROR_FORMAT("Failed to receive response for command '%s': %s", commandString%e.what());
            throw VisionControllerClientException(boost::str(boost::format(_("Failed to receive response for command '%s': %s"))%commandString%e.what()), VisionControllerClientException::VCCEC_CallTimeout);
        }
    }
    const uint64_t elapsedTime = _GetMilliTime64() - startTime;
    MUJIN_LOG_ERROR_FORMAT("Timed out receiving response from sensorbridges for command '%s' after %d milliseconds", commandString%elapsedTime);
    throw VisionControllerClientException(boost::str(boost::format(_("Timed out receiving response for command '%s' from sensorbridges after %d milliseconds"))%commandString%elapsedTime), VisionControllerClientException::VCCEC_CallTimeout);
}


void VisionControllerClient::_ReceiveResponseJSON(boost::shared_ptr<zmq::socket_t> socket, rapidjson::Document& rResponse, const char* commandString, uint64_t timeoutMS)
{
    zmq::message_t message;
    _ReceiveResponse(socket, message, commandString, timeoutMS);

    if (rResponse.Parse((const char*)message.data(), message.size()).HasParseError()) {
        throw VisionControllerClientException(boost::str(boost::format(_("Failed to parse json response for command '%s' from sensorbridges, (offset %u): %s, data=%s"))%commandString%((unsigned)rResponse.GetErrorOffset())%GetParseError_En(rResponse.GetParseError())%std::string((const char*)message.data(), message.size())), VisionControllerClientException::VCCEC_InvalidZMQResponse);
    }
}

void VisionControllerClient::_ReleaseSendBuffer(void *mbSendBufferData, void *vSendDataEntry)
{
    // sensorBridgeClient should be alive during this time...
    SendDataEntry *sendDataEntry = (SendDataEntry *)vSendDataEntry;
    rapidjson::MemoryBuffer& mbSendBuffer = sendDataEntry->first;
    VisionControllerClient *sensorBridgeClient = sendDataEntry->second;
    if (mbSendBuffer.GetBuffer() != mbSendBufferData) {
        MUJIN_LOG_ERROR_FORMAT("Problem with getting correct release data. sendDataEntry=%x (MemoryBuffer=%x, VisionControllerClient=%x), mbSendBufferData=%x != MemoryBuffer::GetBuffer()=%x", (uintptr_t)sendDataEntry%(uintptr_t)(&mbSendBuffer)%(uintptr_t)sensorBridgeClient%(uintptr_t)mbSendBufferData%(uintptr_t)mbSendBuffer.GetBuffer());
    }
    if (!!sensorBridgeClient->_sendDataPool) {
        sensorBridgeClient->_sendDataPool->Recycle(sendDataEntry);
    }
    else {
        MUJIN_LOG_WARN_FORMAT("VisionControllerClient=%x pool is empty", sensorBridgeClient);
    }
}

void VisionControllerClient::_EnsureSocket(boost::shared_ptr<zmq::socket_t> socket)
{
    if (!!socket) {
        return; // already has a socket
    }

    bool isCommandSocket = (socket == _currentCommandSocket);
    boost::shared_ptr<mujincontrollercommon::ZmqSocketPool> pool = isCommandSocket ? _commandSocketPool : _configSocketPool;

    if (!pool) {
        const std::string endpoint = boost::str(boost::format("tcp://%s:%d")%_host%(_port + (isCommandSocket ? 1 : 2)));
        const int maxNumSockets = 2; // need at least 2 when destructing old socket
        pool = boost::make_shared<mujincontrollercommon::ZmqSocketPool>(_context, endpoint, maxNumSockets, 0.001 * _timeoutMS);
        MUJIN_LOG_DEBUG_FORMAT("initialized command socket pool to connect to \"%s\", caller id \"%s\"", endpoint%_callerId);
    }
    socket = pool->AcquireSocket();
}

// THE REST OF THIS NAMESPACE IS GENERATED IMPLEMENTATION

% for serviceName, serviceData in spec['services'].items():
<%include file="/cppImplServiceTemplate.cpp.mako" args="clientName='VisionControllerClient',serviceName=serviceName,serviceData=serviceData,FormatOutParams=FormatOutParams,FormatMethodParameter=FormatMethodParameter,ShouldUseOptionsStruct=ShouldUseOptionsStruct,JsonSchemaToCppType=JsonSchemaToCppType,TypeNeedsJsonAlloc=TypeNeedsJsonAlloc" />
% endfor

} // end namespace mujinvisioncontrollerclient
