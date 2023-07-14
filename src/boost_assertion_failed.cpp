#ifdef BOOST_ENABLE_ASSERT_HANDLER

#include <boost/format.hpp>
#include <mujinvisioncontrollerclient/visioncontrollerclient.h>

namespace boost {

__attribute__((visibility("hidden"))) void assertion_failed(char const* expr, char const* function, char const* file, long line)
{
    throw mujinvisioncontrollerclient::VisionControllerClientException(
        (boost::format("[%s:%d] -> %s, expr: %s")%file%line%function%expr).str(), mujinvisioncontrollerclient::VisionControllerClientException::VCCEC_Assert);
}

#if BOOST_VERSION > 104600
__attribute__((visibility("hidden"))) void assertion_failed_msg(char const* expr, char const* msg, char const* function, char const* file, long line)
{
    throw mujinvisioncontrollerclient::VisionControllerClientException(
        (boost::format("[%s:%d] -> %s, expr: %s, msg: %s")%file%line%function%expr%msg).str(), mujinvisioncontrollerclient::VisionControllerClientException::VCCEC_Assert);
}
#endif

}; // namespace boost

#endif
