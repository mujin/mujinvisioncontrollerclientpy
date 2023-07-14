// -*- coding: utf-8 -*-
// Copyright (C) 2022 Mujin,Inc.
#ifndef MUJIN_VISIONCONTROLLERCLIENT_H
#define MUJIN_VISIONCONTROLLERCLIENT_H

#include <vector>

#include <mujincontrollercommon/datapool.h>
#include <mujincontrollercommon/mujincontrollercommon.h>
#include <mujincontrollercommon/mujinjson.h>
#include <mujincontrollercommon/zmq.hpp>
#include <mujincontrollercommon/zmqclient.h>

#include <mujinvisioncontrollerclient/config.h>

#include <rapidjson/document.h>
#include <rapidjson/memorybuffer.h>
#include <boost/function.hpp>
#include <boost/thread/tss.hpp>

namespace mujinvisioncontrollerclient {

class MUJINVISIONCONTROLLERCLIENT_API VisionControllerClientException : public mujincontrollercommon::MujinExceptionBase
{
public:
    enum VisionControllerClientErrorCode : uint32_t
    {
        // TODO(heman.gandhi): Fix the error masks below
        VCCEC_Failed = mujincontrollercommon::MECM_SensorBridgeClientErrorMask | 0,
        VCCEC_Assert = mujincontrollercommon::MECM_SensorBridgeClientErrorMask | 1,
        VCCEC_FailedToSendZMQRequest = mujincontrollercommon::MECM_SensorBridgeClientErrorMask | 2,       ///< failed to send a zmq command
        VCCEC_InvalidZMQResponse = mujincontrollercommon::MECM_SensorBridgeClientErrorMask | 3,    ///< invalid or unexpected data got received from the command
        VCCEC_CallTimeout = mujincontrollercommon::MECM_SensorBridgeClientErrorMask | 4,  ///< did not get the sensorbridge response
        VCCEC_ZMQRecvError = mujincontrollercommon::MECM_SensorBridgeClientErrorMask | 5, ///< failed to recv
        VCCEC_InvalidArgument = mujincontrollercommon::MECM_SensorBridgeClientErrorMask | 6, ///< invalid argument
        VCCEC_UnexpectedReturnData = mujincontrollercommon::MECM_SensorBridgeClientErrorMask | 7, ///< unexpected return data
    };

    static MUJINVISIONCONTROLLERCLIENT_API const char* GetVisionControllerClientErrorCodeString(VisionControllerClientErrorCode error);

    VisionControllerClientException(
        const std::string& s,
        VisionControllerClientErrorCode code = VCCEC_Failed,
        const std::string& countermeasure = std::string())
    {
        _s = "MujinVisionControllerClient (" + (GetVisionControllerClientErrorCodeString(code) + ("): " + s));
        _code = code;
        _countermeasure = countermeasure;
    }

    virtual ~VisionControllerClientException() throw() {}

    const char *GetCodeString() const override {
        return GetVisionControllerClientErrorCodeString(static_cast<VisionControllerClientErrorCode>(_code));
    }
};


class MUJINVISIONCONTROLLERCLIENT_API VisionControllerClient
{

public:
    VisionControllerClient(
        boost::shared_ptr<zmq::context_t>& context,
        const std::string& host = std::string("127.0.0.1"),
        const uint16_t port = 5718,
        const uint64_t timeoutMS = 200,
        const std::string& callerId = std::string());
    virtual ~VisionControllerClient();

    VisionControllerClient(VisionControllerClient const &) = delete;
    VisionControllerClient & operator=(VisionControllerClient const &) = delete;
    VisionControllerClient & operator=(VisionControllerClient &&) = delete;

    void SetConnectionInfo(const std::string& host, const uint16_t port);

    void SetCallerId(const char* callerId) {
        _callerId = callerId;
    }

    void SetCallerId(const std::string& callerId) {
        _callerId = callerId;
    }

% for socketType in ('command', 'config'):
    /// \brief Send a command to sensorbridge ${socketType} socket and receive the result
    void SendAndReceive${socketType.title()}(
        const std::string& command,
        const rapidjson::Value& rParameterValue,
        rapidjson::Value& rReturnValue,
        rapidjson::Document::AllocatorType& rReturnAlloc,
        double timeout)
    {
        _SendAndReceiveFromSocket(_current${socketType.title()}Socket, command, rParameterValue, rReturnValue, rReturnAlloc, timeout);
    }

% endfor

    // GENERATED API

% for serviceName, serviceData in spec['services'].items():
<%include file="/cppHeaderMethodDeclTemplate.h.mako" args="serviceName=serviceName,serviceData=serviceData,FormatOutParams=FormatOutParams,FormatMethodParameter=FormatMethodParameter,ShouldUseOptionsStruct=ShouldUseOptionsStruct,JsonSchemaToCppType=JsonSchemaToCppType,TypeNeedsJsonAlloc=TypeNeedsJsonAlloc" />
% endfor

    // END GENERATED API

private:
    typedef std::pair<rapidjson::MemoryBuffer, VisionControllerClient *> SendDataEntry; /// holds the memory buffer and a pointer to a send buffer

    void _EnsureSocket(boost::shared_ptr<zmq::socket_t> socket);

    void _SendAndReceiveFromSocket(
        boost::shared_ptr<zmq::socket_t> socket,
        const std::string& command,
        const rapidjson::Value& rParameterValue,
        rapidjson::Value& rReturnValue,
        rapidjson::Document::AllocatorType& rReturnAlloc,
        double timeout);

    /// @brief Send command. Tries reconnecting once.
    void _SendCommand(boost::shared_ptr<zmq::socket_t> socket, zmq::message_t& message, const char* commandString, uint64_t timeoutMS);

    /// @brief Receive response.
    void _ReceiveResponse(boost::shared_ptr<zmq::socket_t> socket, zmq::message_t& message, const char* commandString, uint64_t timeoutMS);

    /// @brief Send JSON command.
    void _SendCommandJSON(boost::shared_ptr<zmq::socket_t> socket, rapidjson::Value& rCommand, rapidjson::Document::AllocatorType& rAlloc, const char* commandString, uint64_t timeoutMS);

    /// @brief Receive and deserialize JSON response in rapidjson::Value.
    void _ReceiveResponseJSON(boost::shared_ptr<zmq::socket_t> socket, rapidjson::Document& rResponse, const char* commandString, uint64_t timeoutMS);

    static void _ReleaseSendBuffer(void* mbSendSendBufferData, void* sendDataEntry);

    // don't change the order
    mutable boost::shared_ptr<zmq::context_t> _context;
    std::string _host = "127.0.0.1";
    uint16_t _port = 5718;
    uint64_t _timeoutMS = 200;
    std::string _callerId; ///< 'callerid' passed into all the sensorbridge commands

% for socketType in ('command', 'config'):
    boost::shared_ptr<mujincontrollercommon::ZmqSocketPool> _${socketType}SocketPool; ///< pool to create ${socketType} sockets
    boost::shared_ptr<zmq::socket_t> _current${socketType.title()}Socket;                     ///< current created ${socketType} socket
% endfor

    std::vector<uint8_t> _vRapidJsonBuffer;                      ///< for internal rapidjson documents
    boost::shared_ptr<rapidjson::MemoryPoolAllocator<>> _rAlloc; ///< allocator for command rapidjson documents

    boost::shared_ptr<mujincontrollercommon::DataPool<SendDataEntry>> _sendDataPool;
};

typedef boost::shared_ptr<VisionControllerClient> VisionControllerClientPtr;

} // end namespace mujinsensorbridgeclient

#endif // MUJIN_VISIONCONTROLLERCLIENT_H