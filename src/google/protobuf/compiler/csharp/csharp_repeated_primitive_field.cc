// Protocol Buffers - Google's data interchange format
// Copyright 2008 Google Inc.  All rights reserved.
// https://developers.google.com/protocol-buffers/
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are
// met:
//
//     * Redistributions of source code must retain the above copyright
// notice, this list of conditions and the following disclaimer.
//     * Redistributions in binary form must reproduce the above
// copyright notice, this list of conditions and the following disclaimer
// in the documentation and/or other materials provided with the
// distribution.
//     * Neither the name of Google Inc. nor the names of its
// contributors may be used to endorse or promote products derived from
// this software without specific prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
// "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
// LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
// A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
// OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
// SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
// LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
// DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
// THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
// (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
// OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#include <google/protobuf/compiler/csharp/csharp_repeated_primitive_field.h>

#include <sstream>

#include <google/protobuf/compiler/code_generator.h>
#include <google/protobuf/descriptor.h>
#include <google/protobuf/wire_format.h>
#include <google/protobuf/compiler/csharp/csharp_doc_comment.h>
#include <google/protobuf/compiler/csharp/csharp_helpers.h>
#include <google/protobuf/descriptor.pb.h>
#include <google/protobuf/io/printer.h>
#include <google/protobuf/io/zero_copy_stream.h>

namespace google {
namespace protobuf {
namespace compiler {
namespace csharp {

RepeatedPrimitiveFieldGenerator::RepeatedPrimitiveFieldGenerator(
    const FieldDescriptor* descriptor, int presenceIndex, const Options *options)
    : FieldGeneratorBase(descriptor, presenceIndex, options) {
}

RepeatedPrimitiveFieldGenerator::~RepeatedPrimitiveFieldGenerator() {

}

void RepeatedPrimitiveFieldGenerator::GenerateMembers(io::Printer* printer) {
  printer->Print(
    variables_,
    "private static readonly pb::FieldCodec<$type_name$> _repeated_$name$_codec\n"
    "    = pb::FieldCodec.For$capitalized_type_name$($tag$);\n");
  printer->Print(variables_,
    "private readonly pbc::RepeatedField<$type_name$> $name$_ = new pbc::RepeatedField<$type_name$>();\n");
  WritePropertyDocComment(printer, descriptor_);
  AddPublicMemberAttributes(printer);
  printer->Print(
    variables_,
    "$access_level$ pbc::RepeatedField<$type_name$> $property_name$ {\n"
    "  get { return $name$_; }\n"
    "}\n");
}

void RepeatedPrimitiveFieldGenerator::GenerateMergingCode(io::Printer* printer) {
  printer->Print(
    variables_,
    "$name$_.Add(other.$name$_);\n");
}

void RepeatedPrimitiveFieldGenerator::GenerateParsingCode(io::Printer* printer) {
  GenerateParsingCode(printer, true);
}

void RepeatedPrimitiveFieldGenerator::GenerateParsingCode(io::Printer* printer, bool use_parse_context) {
  printer->Print(
    variables_,
    use_parse_context
    ? "$name$_.AddEntriesFrom(ref input, _repeated_$name$_codec);\n"
    : "$name$_.AddEntriesFrom(input, _repeated_$name$_codec);\n");
}

void RepeatedPrimitiveFieldGenerator::GenerateSerializationCode(io::Printer* printer) {
  GenerateSerializationCode(printer, true);
}

void RepeatedPrimitiveFieldGenerator::GenerateSerializationCode(io::Printer* printer, bool use_write_context) {
  printer->Print(
    variables_,
    use_write_context
    ? "$name$_.WriteTo(ref output, _repeated_$name$_codec);\n"
    : "$name$_.WriteTo(output, _repeated_$name$_codec);\n");
}

void RepeatedPrimitiveFieldGenerator::GenerateSerializedSizeCode(io::Printer* printer) {
  printer->Print(
    variables_,
    "size += $name$_.CalculateSize(_repeated_$name$_codec);\n");
}

void RepeatedPrimitiveFieldGenerator::WriteHash(io::Printer* printer) {
  printer->Print(
    variables_,
    "hash ^= $name$_.GetHashCode();\n");
}
void RepeatedPrimitiveFieldGenerator::WriteEquals(io::Printer* printer) {
  printer->Print(
    variables_,
    "if(!$name$_.Equals(other.$name$_)) return false;\n");
}
void RepeatedPrimitiveFieldGenerator::WriteToString(io::Printer* printer) {
  printer->Print(variables_,
    "PrintField(\"$descriptor_name$\", $name$_, writer);\n");
}

void RepeatedPrimitiveFieldGenerator::GenerateCloningCode(io::Printer* printer) {
  printer->Print(variables_,
    "$name$_ = other.$name$_.Clone();\n");
}

void RepeatedPrimitiveFieldGenerator::GenerateFreezingCode(io::Printer* printer) {
}

void RepeatedPrimitiveFieldGenerator::GenerateExtensionCode(io::Printer* printer) {
  WritePropertyDocComment(printer, descriptor_);
  AddDeprecatedFlag(printer);
  printer->Print(
    variables_,
    "$access_level$ static readonly pb::RepeatedExtension<$extended_type$, $type_name$> $property_name$ =\n"
    "  new pb::RepeatedExtension<$extended_type$, $type_name$>($number$, pb::FieldCodec.For$capitalized_type_name$($tag$));\n");
}

}  // namespace csharp
}  // namespace compiler
}  // namespace protobuf
}  // namespace google
