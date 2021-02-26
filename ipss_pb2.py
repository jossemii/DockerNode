# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ipss.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import descriptor_pb2 as google_dot_protobuf_dot_descriptor__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='ipss.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\nipss.proto\x1a google/protobuf/descriptor.proto\"b\n\tMultihash\x12&\n\x06hashes\x18\x01 \x03(\x0b\x32\x16.Multihash.HashesEntry\x1a-\n\x0bHashesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"!\n\x0cProtocolMesh\x12\x11\n\tsomething\x18\x01 \x01(\t\"\x80\x01\n\x04Slot\x12\x0c\n\x04port\x18\x01 \x01(\x05\x12?\n\x13\x61plication_protocol\x18\x02 \x01(\x0b\x32\".google.protobuf.FileDescriptorSet\x12)\n\x12transport_protocol\x18\x03 \x01(\x0b\x32\r.ProtocolMesh\"\x1a\n\x03\x41pi\x12\x13\n\x04slot\x18\x01 \x03(\x0b\x32\x05.Slot\"!\n\x0c\x41rchitecture\x12\x11\n\tsomething\x18\x01 \x01(\t\"\x82\x01\n\tContainer\x12#\n\x0c\x61rchitecture\x18\x01 \x01(\x0b\x32\r.Architecture\x12\x1e\n\nfilesystem\x18\x02 \x01(\x0b\x32\n.Multihash\x12\x1c\n\x14\x65nviroment_variables\x18\x03 \x03(\t\x12\x12\n\nentrypoint\x18\x04 \x01(\t\"\xa9\x01\n\x06Tensor\x12)\n\x0foutput_variable\x18\x01 \x03(\x0b\x32\x10.Tensor.Variable\x12(\n\x0einput_variable\x18\x02 \x03(\x0b\x32\x10.Tensor.Variable\x1aJ\n\x08Variable\x12\x0b\n\x03tag\x18\x01 \x03(\t\x12\x31\n\x05\x66ield\x18\x02 \x01(\x0b\x32\".google.protobuf.FileDescriptorSet\"\x15\n\x06Ledger\x12\x0b\n\x03tag\x18\x01 \x01(\t\"\xc3\x01\n\x07Service\x12\x32\n\x06syntax\x18\x01 \x01(\x0b\x32\".google.protobuf.FileDescriptorSet\x12\x1d\n\tcontainer\x18\x02 \x01(\x0b\x32\n.Container\x12\x11\n\x03\x61pi\x18\x03 \x01(\x0b\x32\x04.Api\x12\x17\n\x06tensor\x18\x04 \x01(\x0b\x32\x07.Tensor\x12\x17\n\x06ledger\x18\x05 \x01(\x0b\x32\x07.Ledger\x12 \n\x0c\x64\x65pencencies\x18\x06 \x03(\x0b\x32\n.Multihash\"K\n\x0f\x45xtendedService\x12\x1d\n\tmultihash\x18\x01 \x01(\x0b\x32\n.Multihash\x12\x19\n\x07service\x18\x02 \x01(\x0b\x32\x08.Service\"(\n\x07Gateway\x12\n\n\x02ip\x18\x01 \x01(\t\x12\x11\n\x03\x61pi\x18\x02 \x01(\x0b\x32\x04.Api\"b\n\rConfiguration\x12\x1e\n\x0chost_gateway\x18\x01 \x01(\x0b\x32\x08.Gateway\x12\x1c\n\x14\x65nviroment_variables\x18\x02 \x03(\t\x12\x13\n\x04slot\x18\x03 \x03(\x0b\x32\x05.Slotb\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_descriptor__pb2.DESCRIPTOR,])




_MULTIHASH_HASHESENTRY = _descriptor.Descriptor(
  name='HashesEntry',
  full_name='Multihash.HashesEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='Multihash.HashesEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='Multihash.HashesEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=101,
  serialized_end=146,
)

_MULTIHASH = _descriptor.Descriptor(
  name='Multihash',
  full_name='Multihash',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='hashes', full_name='Multihash.hashes', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_MULTIHASH_HASHESENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=48,
  serialized_end=146,
)


_PROTOCOLMESH = _descriptor.Descriptor(
  name='ProtocolMesh',
  full_name='ProtocolMesh',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='something', full_name='ProtocolMesh.something', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=148,
  serialized_end=181,
)


_SLOT = _descriptor.Descriptor(
  name='Slot',
  full_name='Slot',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='port', full_name='Slot.port', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='aplication_protocol', full_name='Slot.aplication_protocol', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='transport_protocol', full_name='Slot.transport_protocol', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=184,
  serialized_end=312,
)


_API = _descriptor.Descriptor(
  name='Api',
  full_name='Api',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='slot', full_name='Api.slot', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=314,
  serialized_end=340,
)


_ARCHITECTURE = _descriptor.Descriptor(
  name='Architecture',
  full_name='Architecture',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='something', full_name='Architecture.something', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=342,
  serialized_end=375,
)


_CONTAINER = _descriptor.Descriptor(
  name='Container',
  full_name='Container',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='architecture', full_name='Container.architecture', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='filesystem', full_name='Container.filesystem', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='enviroment_variables', full_name='Container.enviroment_variables', index=2,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='entrypoint', full_name='Container.entrypoint', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=378,
  serialized_end=508,
)


_TENSOR_VARIABLE = _descriptor.Descriptor(
  name='Variable',
  full_name='Tensor.Variable',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='tag', full_name='Tensor.Variable.tag', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='field', full_name='Tensor.Variable.field', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=606,
  serialized_end=680,
)

_TENSOR = _descriptor.Descriptor(
  name='Tensor',
  full_name='Tensor',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='output_variable', full_name='Tensor.output_variable', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='input_variable', full_name='Tensor.input_variable', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_TENSOR_VARIABLE, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=511,
  serialized_end=680,
)


_LEDGER = _descriptor.Descriptor(
  name='Ledger',
  full_name='Ledger',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='tag', full_name='Ledger.tag', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=682,
  serialized_end=703,
)


_SERVICE = _descriptor.Descriptor(
  name='Service',
  full_name='Service',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='syntax', full_name='Service.syntax', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='container', full_name='Service.container', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='api', full_name='Service.api', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='tensor', full_name='Service.tensor', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ledger', full_name='Service.ledger', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='depencencies', full_name='Service.depencencies', index=5,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=706,
  serialized_end=901,
)


_EXTENDEDSERVICE = _descriptor.Descriptor(
  name='ExtendedService',
  full_name='ExtendedService',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='multihash', full_name='ExtendedService.multihash', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='service', full_name='ExtendedService.service', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=903,
  serialized_end=978,
)


_GATEWAY = _descriptor.Descriptor(
  name='Gateway',
  full_name='Gateway',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='ip', full_name='Gateway.ip', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='api', full_name='Gateway.api', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=980,
  serialized_end=1020,
)


_CONFIGURATION = _descriptor.Descriptor(
  name='Configuration',
  full_name='Configuration',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='host_gateway', full_name='Configuration.host_gateway', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='enviroment_variables', full_name='Configuration.enviroment_variables', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='slot', full_name='Configuration.slot', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1022,
  serialized_end=1120,
)

_MULTIHASH_HASHESENTRY.containing_type = _MULTIHASH
_MULTIHASH.fields_by_name['hashes'].message_type = _MULTIHASH_HASHESENTRY
_SLOT.fields_by_name['aplication_protocol'].message_type = google_dot_protobuf_dot_descriptor__pb2._FILEDESCRIPTORSET
_SLOT.fields_by_name['transport_protocol'].message_type = _PROTOCOLMESH
_API.fields_by_name['slot'].message_type = _SLOT
_CONTAINER.fields_by_name['architecture'].message_type = _ARCHITECTURE
_CONTAINER.fields_by_name['filesystem'].message_type = _MULTIHASH
_TENSOR_VARIABLE.fields_by_name['field'].message_type = google_dot_protobuf_dot_descriptor__pb2._FILEDESCRIPTORSET
_TENSOR_VARIABLE.containing_type = _TENSOR
_TENSOR.fields_by_name['output_variable'].message_type = _TENSOR_VARIABLE
_TENSOR.fields_by_name['input_variable'].message_type = _TENSOR_VARIABLE
_SERVICE.fields_by_name['syntax'].message_type = google_dot_protobuf_dot_descriptor__pb2._FILEDESCRIPTORSET
_SERVICE.fields_by_name['container'].message_type = _CONTAINER
_SERVICE.fields_by_name['api'].message_type = _API
_SERVICE.fields_by_name['tensor'].message_type = _TENSOR
_SERVICE.fields_by_name['ledger'].message_type = _LEDGER
_SERVICE.fields_by_name['depencencies'].message_type = _MULTIHASH
_EXTENDEDSERVICE.fields_by_name['multihash'].message_type = _MULTIHASH
_EXTENDEDSERVICE.fields_by_name['service'].message_type = _SERVICE
_GATEWAY.fields_by_name['api'].message_type = _API
_CONFIGURATION.fields_by_name['host_gateway'].message_type = _GATEWAY
_CONFIGURATION.fields_by_name['slot'].message_type = _SLOT
DESCRIPTOR.message_types_by_name['Multihash'] = _MULTIHASH
DESCRIPTOR.message_types_by_name['ProtocolMesh'] = _PROTOCOLMESH
DESCRIPTOR.message_types_by_name['Slot'] = _SLOT
DESCRIPTOR.message_types_by_name['Api'] = _API
DESCRIPTOR.message_types_by_name['Architecture'] = _ARCHITECTURE
DESCRIPTOR.message_types_by_name['Container'] = _CONTAINER
DESCRIPTOR.message_types_by_name['Tensor'] = _TENSOR
DESCRIPTOR.message_types_by_name['Ledger'] = _LEDGER
DESCRIPTOR.message_types_by_name['Service'] = _SERVICE
DESCRIPTOR.message_types_by_name['ExtendedService'] = _EXTENDEDSERVICE
DESCRIPTOR.message_types_by_name['Gateway'] = _GATEWAY
DESCRIPTOR.message_types_by_name['Configuration'] = _CONFIGURATION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Multihash = _reflection.GeneratedProtocolMessageType('Multihash', (_message.Message,), {

  'HashesEntry' : _reflection.GeneratedProtocolMessageType('HashesEntry', (_message.Message,), {
    'DESCRIPTOR' : _MULTIHASH_HASHESENTRY,
    '__module__' : 'ipss_pb2'
    # @@protoc_insertion_point(class_scope:Multihash.HashesEntry)
    })
  ,
  'DESCRIPTOR' : _MULTIHASH,
  '__module__' : 'ipss_pb2'
  # @@protoc_insertion_point(class_scope:Multihash)
  })
_sym_db.RegisterMessage(Multihash)
_sym_db.RegisterMessage(Multihash.HashesEntry)

ProtocolMesh = _reflection.GeneratedProtocolMessageType('ProtocolMesh', (_message.Message,), {
  'DESCRIPTOR' : _PROTOCOLMESH,
  '__module__' : 'ipss_pb2'
  # @@protoc_insertion_point(class_scope:ProtocolMesh)
  })
_sym_db.RegisterMessage(ProtocolMesh)

Slot = _reflection.GeneratedProtocolMessageType('Slot', (_message.Message,), {
  'DESCRIPTOR' : _SLOT,
  '__module__' : 'ipss_pb2'
  # @@protoc_insertion_point(class_scope:Slot)
  })
_sym_db.RegisterMessage(Slot)

Api = _reflection.GeneratedProtocolMessageType('Api', (_message.Message,), {
  'DESCRIPTOR' : _API,
  '__module__' : 'ipss_pb2'
  # @@protoc_insertion_point(class_scope:Api)
  })
_sym_db.RegisterMessage(Api)

Architecture = _reflection.GeneratedProtocolMessageType('Architecture', (_message.Message,), {
  'DESCRIPTOR' : _ARCHITECTURE,
  '__module__' : 'ipss_pb2'
  # @@protoc_insertion_point(class_scope:Architecture)
  })
_sym_db.RegisterMessage(Architecture)

Container = _reflection.GeneratedProtocolMessageType('Container', (_message.Message,), {
  'DESCRIPTOR' : _CONTAINER,
  '__module__' : 'ipss_pb2'
  # @@protoc_insertion_point(class_scope:Container)
  })
_sym_db.RegisterMessage(Container)

Tensor = _reflection.GeneratedProtocolMessageType('Tensor', (_message.Message,), {

  'Variable' : _reflection.GeneratedProtocolMessageType('Variable', (_message.Message,), {
    'DESCRIPTOR' : _TENSOR_VARIABLE,
    '__module__' : 'ipss_pb2'
    # @@protoc_insertion_point(class_scope:Tensor.Variable)
    })
  ,
  'DESCRIPTOR' : _TENSOR,
  '__module__' : 'ipss_pb2'
  # @@protoc_insertion_point(class_scope:Tensor)
  })
_sym_db.RegisterMessage(Tensor)
_sym_db.RegisterMessage(Tensor.Variable)

Ledger = _reflection.GeneratedProtocolMessageType('Ledger', (_message.Message,), {
  'DESCRIPTOR' : _LEDGER,
  '__module__' : 'ipss_pb2'
  # @@protoc_insertion_point(class_scope:Ledger)
  })
_sym_db.RegisterMessage(Ledger)

Service = _reflection.GeneratedProtocolMessageType('Service', (_message.Message,), {
  'DESCRIPTOR' : _SERVICE,
  '__module__' : 'ipss_pb2'
  # @@protoc_insertion_point(class_scope:Service)
  })
_sym_db.RegisterMessage(Service)

ExtendedService = _reflection.GeneratedProtocolMessageType('ExtendedService', (_message.Message,), {
  'DESCRIPTOR' : _EXTENDEDSERVICE,
  '__module__' : 'ipss_pb2'
  # @@protoc_insertion_point(class_scope:ExtendedService)
  })
_sym_db.RegisterMessage(ExtendedService)

Gateway = _reflection.GeneratedProtocolMessageType('Gateway', (_message.Message,), {
  'DESCRIPTOR' : _GATEWAY,
  '__module__' : 'ipss_pb2'
  # @@protoc_insertion_point(class_scope:Gateway)
  })
_sym_db.RegisterMessage(Gateway)

Configuration = _reflection.GeneratedProtocolMessageType('Configuration', (_message.Message,), {
  'DESCRIPTOR' : _CONFIGURATION,
  '__module__' : 'ipss_pb2'
  # @@protoc_insertion_point(class_scope:Configuration)
  })
_sym_db.RegisterMessage(Configuration)


_MULTIHASH_HASHESENTRY._options = None
# @@protoc_insertion_point(module_scope)
