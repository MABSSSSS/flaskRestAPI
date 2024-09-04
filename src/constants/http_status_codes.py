# http_status_code.py

# 1xx: Informational responses (codes that indicate the request was received and understood, and the process is continuing)
CONTINUE = 100  # The server has received the request headers, and the client should proceed to send the request body.
SWITCHING_PROTOCOLS = 101  # The requester has asked the server to switch protocols, and the server is acknowledging that it will do so.
PROCESSING = 102  # The server has received the WebDAV request and is processing, but no response is available yet.

# 2xx: Successful responses (codes that indicate the request was successfully received, understood, and accepted)
OK = 200  # The request was successful, and the server has returned the requested resource.
CREATED = 201  # The request was successful, and a new resource has been created as a result.
ACCEPTED = 202  # The request has been accepted for processing, but the processing has not been completed.
NON_AUTHORITATIVE_INFORMATION = 203  # The request was successful, but the response contains modified information from a third-party source.
NO_CONTENT = 204  # The request was successful, but the server is not returning any content.
RESET_CONTENT = 205  # The request was successful, and the user-agent should reset the document view.
PARTIAL_CONTENT = 206  # The server is delivering only part of the resource due to a range header sent by the client.
MULTI_STATUS = 207  # The message body contains multiple separate responses (used for WebDAV).
IM_USED = 226  # The server has fulfilled a GET request for the resource and the response is a representation of the result of one or more instance-manipulations applied to the current instance.

# 3xx: Redirection messages (codes that indicate further action needs to be taken by the user-agent to fulfill the request)
MULTIPLE_CHOICES = 300  # The request has more than one possible response, and the user-agent should choose one.
MOVED_PERMANENTLY = 301  # The requested resource has been permanently moved to a new URL.
FOUND = 302  # The requested resource resides temporarily under a different URL.
SEE_OTHER = 303  # The server is redirecting to a different resource, which should be retrieved using a GET request.
NOT_MODIFIED = 304  # Indicates that the resource has not been modified since the last request.
USE_PROXY = 305  # The requested resource must be accessed through the proxy given by the Location field.
TEMPORARY_REDIRECT = 307  # The requested resource resides temporarily under a different URL, but the method should not change.
PERMANENT_REDIRECT = 308  # The request and all future requests should be repeated using another URL.

# 4xx: Client error responses (codes that indicate the request contains bad syntax or cannot be fulfilled)
BAD_REQUEST = 400  # The server could not understand the request due to invalid syntax.
UNAUTHORIZED = 401  # The client must authenticate itself to get the requested response.
PAYMENT_REQUIRED = 402  # Reserved for future use; this status code is rarely used.
FORBIDDEN = 403  # The client does not have access rights to the content.
NOT_FOUND = 404  # The server can not find the requested resource.
METHOD_NOT_ALLOWED = 405  # The request method is known by the server but has been disabled and cannot be used.
NOT_ACCEPTABLE = 406  # The server cannot produce a response matching the list of acceptable values defined in the request's proactive content negotiation headers.
PROXY_AUTHENTICATION_REQUIRED = 407  # The client must first authenticate itself with the proxy.
REQUEST_TIMEOUT = 408  # The server timed out waiting for the request.
CONFLICT = 409  # The request could not be processed because of conflict in the current state of the resource.
GONE = 410  # The content requested has been permanently deleted from the server, with no forwarding address.
LENGTH_REQUIRED = 411  # The server refuses to accept the request without a defined Content-Length header.
PRECONDITION_FAILED = 412  # The client has indicated preconditions in its headers which the server does not meet.
PAYLOAD_TOO_LARGE = 413  # The request is larger than the server is willing or able to process.
URI_TOO_LONG = 414  # The URI requested by the client is longer than the server is willing to interpret.
UNSUPPORTED_MEDIA_TYPE = 415  # The media format of the requested data is not supported by the server.
RANGE_NOT_SATISFIABLE = 416  # The range specified by the Range header field in the request cannot be fulfilled by the server.
EXPECTATION_FAILED = 417  # The server cannot meet the requirements of the Expect request-header field.
IM_A_TEAPOT = 418  # The server refuses to brew coffee because it is, permanently, a teapot (an April Fools' joke response).
MISDIRECTED_REQUEST = 421  # The request was directed at a server that is not able to produce a response.
UNPROCESSABLE_ENTITY = 422  # The request was well-formed but could not be followed due to semantic errors.
LOCKED = 423  # The resource being accessed is locked.
FAILED_DEPENDENCY = 424  # The request failed due to failure of a previous request.
UPGRADE_REQUIRED = 426  # The server refuses to perform the request using the current protocol but might do so after the client upgrades to a different protocol.
PRECONDITION_REQUIRED = 428  # The origin server requires the request to be conditional.
TOO_MANY_REQUESTS = 429  # The user has sent too many requests in a given amount of time ("rate limiting").
REQUEST_HEADER_FIELDS_TOO_LARGE = 431  # The server is unwilling to process the request because its header fields are too large.
UNAVAILABLE_FOR_LEGAL_REASONS = 451  # The user-agent requested a resource that cannot legally be provided.

# 5xx: Server error responses (codes that indicate the server failed to fulfill an apparently valid request)
INTERNAL_SERVER_ERROR = 500  # The server encountered an unexpected condition that prevented it from fulfilling the request.
NOT_IMPLEMENTED = 501  # The server does not recognize the request method, or it lacks the ability to fulfill the request.
BAD_GATEWAY = 502  # The server was acting as a gateway or proxy and received an invalid response from the upstream server.
SERVICE_UNAVAILABLE = 503  # The server is not ready to handle the request, commonly due to maintenance or overload.
GATEWAY_TIMEOUT = 504  # The server was acting as a gateway or proxy and did not receive a timely response from the upstream server.
HTTP_VERSION_NOT_SUPPORTED = 505  # The server does not support the HTTP protocol version used in the request.
VARIANT_ALSO_NEGOTIATES = 506  # The server has an internal configuration error; the chosen variant resource is configured to engage in transparent content negotiation itself, and therefore is not a proper endpoint in the negotiation process.
INSUFFICIENT_STORAGE = 507  # The server is unable to store the representation needed to complete the request.
LOOP_DETECTED = 508  # The server detected an infinite loop while processing a request with multiple redirects.
NOT_EXTENDED = 510  # Further extensions to the request are required for the server to fulfill it.
NETWORK_AUTHENTICATION_REQUIRED = 511  # The client needs to authenticate to gain network access (used for network-specific login pages).

def get_success_status_message(status_code):
    """Return a message for successful responses."""
    success_messages = {  # Dictionary mapping status codes to their respective messages.
        OK: "OK",
        CREATED: "Created",
        ACCEPTED: "Accepted",
        NON_AUTHORITATIVE_INFORMATION: "Non-Authoritative Information",
        NO_CONTENT: "No Content",
        RESET_CONTENT: "Reset Content",
        PARTIAL_CONTENT: "Partial Content",
        MULTI_STATUS: "Multi-Status",
        IM_USED: "IM Used",
    }
    return success_messages.get(status_code, "Unknown Success Status Code")
    # Retrieve the message for the given status code; return "Unknown Success Status Code" if the code is not found.

def get_redirection_status_message(status_code):
    """Return a message for redirection responses."""
    redirection_messages = {  # Dictionary mapping status codes to their respective messages.
        MULTIPLE_CHOICES: "Multiple Choices",
        MOVED_PERMANENTLY: "Moved Permanently",
        FOUND: "Found",
        SEE_OTHER: "See Other",
        NOT_MODIFIED: "Not Modified",
        USE_PROXY: "Use Proxy",
        TEMPORARY_REDIRECT: "Temporary Redirect",
        PERMANENT_REDIRECT: "Permanent Redirect",
    }
    return redirection_messages.get(status_code, "Unknown Redirection Status Code")
    # Retrieve the message for the given status code; return "Unknown Redirection Status Code" if the code is not found.

def get_client_error_status_message(status_code):
    """Return a message for client error responses."""
    client_error_messages = {  # Dictionary mapping status codes to their respective messages.
        BAD_REQUEST: "Bad Request",
        UNAUTHORIZED: "Unauthorized",
        PAYMENT_REQUIRED: "Payment Required",
        FORBIDDEN: "Forbidden",
        NOT_FOUND: "Not Found",
        METHOD_NOT_ALLOWED: "Method Not Allowed",
        NOT_ACCEPTABLE: "Not Acceptable",
        PROXY_AUTHENTICATION_REQUIRED: "Proxy Authentication Required",
        REQUEST_TIMEOUT: "Request Timeout",
        CONFLICT: "Conflict",
        GONE: "Gone",
        LENGTH_REQUIRED: "Length Required",
        PRECONDITION_FAILED: "Precondition Failed",
        PAYLOAD_TOO_LARGE: "Payload Too Large",
        URI_TOO_LONG: "URI Too Long",
        UNSUPPORTED_MEDIA_TYPE: "Unsupported Media Type",
        RANGE_NOT_SATISFIABLE: "Range Not Satisfiable",
        EXPECTATION_FAILED: "Expectation Failed",
        IM_A_TEAPOT: "I'm a teapot",  # A humorous response indicating that the server refuses to brew coffee.
        MISDIRECTED_REQUEST: "Misdirected Request",
        UNPROCESSABLE_ENTITY: "Unprocessable Entity",
        LOCKED: "Locked",
        FAILED_DEPENDENCY: "Failed Dependency",
        UPGRADE_REQUIRED: "Upgrade Required",
        PRECONDITION_REQUIRED: "Precondition Required",
        TOO_MANY_REQUESTS: "Too Many Requests",
        REQUEST_HEADER_FIELDS_TOO_LARGE: "Request Header Fields Too Large",
        UNAVAILABLE_FOR_LEGAL_REASONS: "Unavailable For Legal Reasons",
    }
    return client_error_messages.get(status_code, "Unknown Client Error Status Code")
    # Retrieve the message for the given status code; return "Unknown Client Error Status Code" if the code is not found.

def get_server_error_status_message(status_code):
    """Return a message for server error responses."""
    server_error_messages = {  # Dictionary mapping status codes to their respective messages.
        INTERNAL_SERVER_ERROR: "Internal Server Error",
        NOT_IMPLEMENTED: "Not Implemented",
        BAD_GATEWAY: "Bad Gateway",
        SERVICE_UNAVAILABLE: "Service Unavailable",
        GATEWAY_TIMEOUT: "Gateway Timeout",
        HTTP_VERSION_NOT_SUPPORTED: "HTTP Version Not Supported",
        VARIANT_ALSO_NEGOTIATES: "Variant Also Negotiates",
        INSUFFICIENT_STORAGE: "Insufficient Storage",
        LOOP_DETECTED: "Loop Detected",
        NOT_EXTENDED: "Not Extended",
        NETWORK_AUTHENTICATION_REQUIRED: "Network Authentication Required",
    }
    return server_error_messages.get(status_code, "Unknown Server Error Status Code")
    # Retrieve the message for the given status code; return "Unknown Server Error Status Code" if the code is not found.

# Example of using the functions
def get_status_message(status_code):
    """Return a message for a given status code."""
    if 100 <= status_code < 200:  # Check if the status code is an informational response.
        return get_success_status_message(status_code)
    elif 200 <= status_code < 300:  # Check if the status code is a successful response.
        return get_success_status_message(status_code)
    elif 300 <= status_code < 400:  # Check if the status code is a redirection response.
        return get_redirection_status_message(status_code)
    elif 400 <= status_code < 500:  # Check if the status code is a client error response.
        return get_client_error_status_message(status_code)
    elif 500 <= status_code < 600:  # Check if the status code is a server error response.
        return get_server_error_status_message(status_code)
    else:  # Handle any unknown status codes.
        return "Unknown Status Code"
