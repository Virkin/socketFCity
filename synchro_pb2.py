# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: synchro.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import fcityDatabase_pb2 as fcityDatabase__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='synchro.proto',
  package='',
  syntax='proto2',
  serialized_pb=_b('\n\rsynchro.proto\x1a\x13\x66\x63ityDatabase.proto\"\x13\n\x11\x43onnectionRequest\"\"\n\x12\x43onnectionResponse\x12\x0c\n\x04port\x18\x01 \x02(\x05\"\x14\n\x12SynchronizeRequest\"3\n\x13SynchronizeResponse\x12\x1c\n\x07\x65lement\x18\x01 \x01(\x0b\x32\x0b.db.element\"3\n\x12StartOfRideRequest\x12\n\n\x02id\x18\x01 \x02(\x05\x12\x11\n\tstartDate\x18\x02 \x02(\t\"\'\n\x13StartOfRideResponse\x12\x10\n\x08taskDone\x18\x01 \x02(\x08\"M\n\x10\x45ndOfRideRequest\x12\n\n\x02id\x18\x01 \x02(\x05\x12\x0f\n\x07\x65ndDate\x18\x02 \x02(\t\x12\x1c\n\x07\x65lement\x18\x03 \x01(\x0b\x32\x0b.db.element\"%\n\x11\x45ndOfRideResponse\x12\x10\n\x08taskDone\x18\x01 \x02(\x08\"\x16\n\x14\x45ndConnectionRequest\"\xfe\x01\n\tCarToServ\x12-\n\x11\x63onnectionRequest\x18\x01 \x01(\x0b\x32\x12.ConnectionRequest\x12/\n\x12synchronizeRequest\x18\x02 \x01(\x0b\x32\x13.SynchronizeRequest\x12/\n\x12startOfRideRequest\x18\x03 \x01(\x0b\x32\x13.StartOfRideRequest\x12+\n\x10\x65ndOfRideRequest\x18\x04 \x01(\x0b\x32\x11.EndOfRideRequest\x12\x33\n\x14\x65ndConnectionRequest\x18\x05 \x01(\x0b\x32\x15.EndConnectionRequest\"\xd1\x01\n\tServToCar\x12/\n\x12\x63onnectionResponse\x18\x01 \x01(\x0b\x32\x13.ConnectionResponse\x12\x31\n\x13synchronizeResponse\x18\x02 \x01(\x0b\x32\x14.SynchronizeResponse\x12\x31\n\x13startOfRideResponse\x18\x03 \x01(\x0b\x32\x14.StartOfRideResponse\x12-\n\x11\x65ndOfRideResponse\x18\x04 \x01(\x0b\x32\x12.EndOfRideResponse*L\n\x05table\x12\t\n\x05users\x10\x01\x12\x0b\n\x07vehicle\x10\x02\x12\x08\n\x04ride\x10\x03\x12\n\n\x06sensor\x10\x04\x12\x0b\n\x07measure\x10\x05\x12\x08\n\x04\x64\x61ta\x10\x06')
  ,
  dependencies=[fcityDatabase__pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

_TABLE = _descriptor.EnumDescriptor(
  name='table',
  full_name='table',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='users', index=0, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='vehicle', index=1, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ride', index=2, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='sensor', index=3, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='measure', index=4, number=5,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='data', index=5, number=6,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=875,
  serialized_end=951,
)
_sym_db.RegisterEnumDescriptor(_TABLE)

table = enum_type_wrapper.EnumTypeWrapper(_TABLE)
users = 1
vehicle = 2
ride = 3
sensor = 4
measure = 5
data = 6



_CONNECTIONREQUEST = _descriptor.Descriptor(
  name='ConnectionRequest',
  full_name='ConnectionRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=38,
  serialized_end=57,
)


_CONNECTIONRESPONSE = _descriptor.Descriptor(
  name='ConnectionResponse',
  full_name='ConnectionResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='port', full_name='ConnectionResponse.port', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=59,
  serialized_end=93,
)


_SYNCHRONIZEREQUEST = _descriptor.Descriptor(
  name='SynchronizeRequest',
  full_name='SynchronizeRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=95,
  serialized_end=115,
)


_SYNCHRONIZERESPONSE = _descriptor.Descriptor(
  name='SynchronizeResponse',
  full_name='SynchronizeResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='element', full_name='SynchronizeResponse.element', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=117,
  serialized_end=168,
)


_STARTOFRIDEREQUEST = _descriptor.Descriptor(
  name='StartOfRideRequest',
  full_name='StartOfRideRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='StartOfRideRequest.id', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='startDate', full_name='StartOfRideRequest.startDate', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=170,
  serialized_end=221,
)


_STARTOFRIDERESPONSE = _descriptor.Descriptor(
  name='StartOfRideResponse',
  full_name='StartOfRideResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='taskDone', full_name='StartOfRideResponse.taskDone', index=0,
      number=1, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=223,
  serialized_end=262,
)


_ENDOFRIDEREQUEST = _descriptor.Descriptor(
  name='EndOfRideRequest',
  full_name='EndOfRideRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='EndOfRideRequest.id', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='endDate', full_name='EndOfRideRequest.endDate', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='element', full_name='EndOfRideRequest.element', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=264,
  serialized_end=341,
)


_ENDOFRIDERESPONSE = _descriptor.Descriptor(
  name='EndOfRideResponse',
  full_name='EndOfRideResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='taskDone', full_name='EndOfRideResponse.taskDone', index=0,
      number=1, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=343,
  serialized_end=380,
)


_ENDCONNECTIONREQUEST = _descriptor.Descriptor(
  name='EndConnectionRequest',
  full_name='EndConnectionRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=382,
  serialized_end=404,
)


_CARTOSERV = _descriptor.Descriptor(
  name='CarToServ',
  full_name='CarToServ',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='connectionRequest', full_name='CarToServ.connectionRequest', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='synchronizeRequest', full_name='CarToServ.synchronizeRequest', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='startOfRideRequest', full_name='CarToServ.startOfRideRequest', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='endOfRideRequest', full_name='CarToServ.endOfRideRequest', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='endConnectionRequest', full_name='CarToServ.endConnectionRequest', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=407,
  serialized_end=661,
)


_SERVTOCAR = _descriptor.Descriptor(
  name='ServToCar',
  full_name='ServToCar',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='connectionResponse', full_name='ServToCar.connectionResponse', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='synchronizeResponse', full_name='ServToCar.synchronizeResponse', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='startOfRideResponse', full_name='ServToCar.startOfRideResponse', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='endOfRideResponse', full_name='ServToCar.endOfRideResponse', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=664,
  serialized_end=873,
)

_SYNCHRONIZERESPONSE.fields_by_name['element'].message_type = fcityDatabase__pb2._ELEMENT
_ENDOFRIDEREQUEST.fields_by_name['element'].message_type = fcityDatabase__pb2._ELEMENT
_CARTOSERV.fields_by_name['connectionRequest'].message_type = _CONNECTIONREQUEST
_CARTOSERV.fields_by_name['synchronizeRequest'].message_type = _SYNCHRONIZEREQUEST
_CARTOSERV.fields_by_name['startOfRideRequest'].message_type = _STARTOFRIDEREQUEST
_CARTOSERV.fields_by_name['endOfRideRequest'].message_type = _ENDOFRIDEREQUEST
_CARTOSERV.fields_by_name['endConnectionRequest'].message_type = _ENDCONNECTIONREQUEST
_SERVTOCAR.fields_by_name['connectionResponse'].message_type = _CONNECTIONRESPONSE
_SERVTOCAR.fields_by_name['synchronizeResponse'].message_type = _SYNCHRONIZERESPONSE
_SERVTOCAR.fields_by_name['startOfRideResponse'].message_type = _STARTOFRIDERESPONSE
_SERVTOCAR.fields_by_name['endOfRideResponse'].message_type = _ENDOFRIDERESPONSE
DESCRIPTOR.message_types_by_name['ConnectionRequest'] = _CONNECTIONREQUEST
DESCRIPTOR.message_types_by_name['ConnectionResponse'] = _CONNECTIONRESPONSE
DESCRIPTOR.message_types_by_name['SynchronizeRequest'] = _SYNCHRONIZEREQUEST
DESCRIPTOR.message_types_by_name['SynchronizeResponse'] = _SYNCHRONIZERESPONSE
DESCRIPTOR.message_types_by_name['StartOfRideRequest'] = _STARTOFRIDEREQUEST
DESCRIPTOR.message_types_by_name['StartOfRideResponse'] = _STARTOFRIDERESPONSE
DESCRIPTOR.message_types_by_name['EndOfRideRequest'] = _ENDOFRIDEREQUEST
DESCRIPTOR.message_types_by_name['EndOfRideResponse'] = _ENDOFRIDERESPONSE
DESCRIPTOR.message_types_by_name['EndConnectionRequest'] = _ENDCONNECTIONREQUEST
DESCRIPTOR.message_types_by_name['CarToServ'] = _CARTOSERV
DESCRIPTOR.message_types_by_name['ServToCar'] = _SERVTOCAR
DESCRIPTOR.enum_types_by_name['table'] = _TABLE

ConnectionRequest = _reflection.GeneratedProtocolMessageType('ConnectionRequest', (_message.Message,), dict(
  DESCRIPTOR = _CONNECTIONREQUEST,
  __module__ = 'synchro_pb2'
  # @@protoc_insertion_point(class_scope:ConnectionRequest)
  ))
_sym_db.RegisterMessage(ConnectionRequest)

ConnectionResponse = _reflection.GeneratedProtocolMessageType('ConnectionResponse', (_message.Message,), dict(
  DESCRIPTOR = _CONNECTIONRESPONSE,
  __module__ = 'synchro_pb2'
  # @@protoc_insertion_point(class_scope:ConnectionResponse)
  ))
_sym_db.RegisterMessage(ConnectionResponse)

SynchronizeRequest = _reflection.GeneratedProtocolMessageType('SynchronizeRequest', (_message.Message,), dict(
  DESCRIPTOR = _SYNCHRONIZEREQUEST,
  __module__ = 'synchro_pb2'
  # @@protoc_insertion_point(class_scope:SynchronizeRequest)
  ))
_sym_db.RegisterMessage(SynchronizeRequest)

SynchronizeResponse = _reflection.GeneratedProtocolMessageType('SynchronizeResponse', (_message.Message,), dict(
  DESCRIPTOR = _SYNCHRONIZERESPONSE,
  __module__ = 'synchro_pb2'
  # @@protoc_insertion_point(class_scope:SynchronizeResponse)
  ))
_sym_db.RegisterMessage(SynchronizeResponse)

StartOfRideRequest = _reflection.GeneratedProtocolMessageType('StartOfRideRequest', (_message.Message,), dict(
  DESCRIPTOR = _STARTOFRIDEREQUEST,
  __module__ = 'synchro_pb2'
  # @@protoc_insertion_point(class_scope:StartOfRideRequest)
  ))
_sym_db.RegisterMessage(StartOfRideRequest)

StartOfRideResponse = _reflection.GeneratedProtocolMessageType('StartOfRideResponse', (_message.Message,), dict(
  DESCRIPTOR = _STARTOFRIDERESPONSE,
  __module__ = 'synchro_pb2'
  # @@protoc_insertion_point(class_scope:StartOfRideResponse)
  ))
_sym_db.RegisterMessage(StartOfRideResponse)

EndOfRideRequest = _reflection.GeneratedProtocolMessageType('EndOfRideRequest', (_message.Message,), dict(
  DESCRIPTOR = _ENDOFRIDEREQUEST,
  __module__ = 'synchro_pb2'
  # @@protoc_insertion_point(class_scope:EndOfRideRequest)
  ))
_sym_db.RegisterMessage(EndOfRideRequest)

EndOfRideResponse = _reflection.GeneratedProtocolMessageType('EndOfRideResponse', (_message.Message,), dict(
  DESCRIPTOR = _ENDOFRIDERESPONSE,
  __module__ = 'synchro_pb2'
  # @@protoc_insertion_point(class_scope:EndOfRideResponse)
  ))
_sym_db.RegisterMessage(EndOfRideResponse)

EndConnectionRequest = _reflection.GeneratedProtocolMessageType('EndConnectionRequest', (_message.Message,), dict(
  DESCRIPTOR = _ENDCONNECTIONREQUEST,
  __module__ = 'synchro_pb2'
  # @@protoc_insertion_point(class_scope:EndConnectionRequest)
  ))
_sym_db.RegisterMessage(EndConnectionRequest)

CarToServ = _reflection.GeneratedProtocolMessageType('CarToServ', (_message.Message,), dict(
  DESCRIPTOR = _CARTOSERV,
  __module__ = 'synchro_pb2'
  # @@protoc_insertion_point(class_scope:CarToServ)
  ))
_sym_db.RegisterMessage(CarToServ)

ServToCar = _reflection.GeneratedProtocolMessageType('ServToCar', (_message.Message,), dict(
  DESCRIPTOR = _SERVTOCAR,
  __module__ = 'synchro_pb2'
  # @@protoc_insertion_point(class_scope:ServToCar)
  ))
_sym_db.RegisterMessage(ServToCar)


# @@protoc_insertion_point(module_scope)
