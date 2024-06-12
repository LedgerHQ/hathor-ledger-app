import enum
from typing import Any, Dict, Union

from .errors import *


class BOLOSPathPrefixError(Exception):
    pass


class DeviceException(Exception):  # pylint: disable=too-few-public-methods
    exc: Dict[int, Any] = {
        0x6985: DenyError,
        0x6A86: WrongP1P2Error,
        0x6A87: WrongDataLengthError,
        0x6D00: InsNotSupportedError,
        0x6E00: ClaNotSupportedError,
        0xB000: WrongResponseLengthError,
        0xB001: DisplayBip32PathFailError,
        0xB002: DisplayAddressFailError,
        0xB003: DisplayAmountFailError,
        0xB004: WrongTxLengthError,
        0xB005: TxParsingFailError,
        0xB006: TxHashFail,
        0xB007: BadStateError,
        0xB008: SignatureFailError,
        0xB009: TxInvalidError,
        0xB00A: InvalidSignatureError,
        0xB00B: InternalError,
    }

    os_exc: Dict[int, Any] = {
        0x4215: BOLOSPathPrefixError,
    }

    def __new__(
        cls,
        error_code: int,
        ins: Union[int, enum.IntEnum, None] = None,
        message: str = "",
    ) -> Any:
        error_message: str = f"Error in {ins!r} command" if ins else "Error in command"

        if error_code in DeviceException.exc:
            return DeviceException.exc[error_code](
                hex(error_code), error_message, message
            )

        if error_code in DeviceException.os_exc:
            return DeviceException.os_exc[error_code](
                hex(error_code), error_message, message
            )

        return UnknownDeviceError(hex(error_code), error_message, message)
