/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

import { PipelineSelector } from "./../../types/globalTypes";

// ====================================================
// GraphQL query operation: PartitionStepStatusPipelineQuery
// ====================================================

export interface PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineNotFoundError {
  __typename: "PipelineNotFoundError" | "PipelineSnapshotNotFoundError" | "PythonError";
}

export interface PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition_SolidDefinition_metadata {
  __typename: "MetadataItemDefinition";
  key: string;
  value: string;
}

export interface PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition_SolidDefinition_assetNodes_assetKey {
  __typename: "AssetKey";
  path: string[];
}

export interface PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition_SolidDefinition_assetNodes {
  __typename: "AssetNode";
  id: string;
  assetKey: PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition_SolidDefinition_assetNodes_assetKey;
}

export interface PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition_SolidDefinition_inputDefinitions_type {
  __typename: "ListDagsterType" | "NullableDagsterType" | "RegularDagsterType";
  displayName: string;
}

export interface PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition_SolidDefinition_inputDefinitions {
  __typename: "InputDefinition";
  name: string;
  type: PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition_SolidDefinition_inputDefinitions_type;
}

export interface PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition_SolidDefinition_outputDefinitions_type {
  __typename: "ListDagsterType" | "NullableDagsterType" | "RegularDagsterType";
  displayName: string;
}

export interface PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition_SolidDefinition_outputDefinitions {
  __typename: "OutputDefinition";
  name: string;
  isDynamic: boolean | null;
  type: PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition_SolidDefinition_outputDefinitions_type;
}

export interface PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition_SolidDefinition_configField_configType {
  __typename: "ArrayConfigType" | "CompositeConfigType" | "EnumConfigType" | "NullableConfigType" | "RegularConfigType" | "ScalarUnionConfigType" | "MapConfigType";
  key: string;
  description: string | null;
}

export interface PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition_SolidDefinition_configField {
  __typename: "ConfigTypeField";
  configType: PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition_SolidDefinition_configField_configType;
}

export interface PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition_SolidDefinition {
  __typename: "SolidDefinition";
  name: string;
  description: string | null;
  metadata: PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition_SolidDefinition_metadata[];
  assetNodes: PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition_SolidDefinition_assetNodes[];
  inputDefinitions: PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition_SolidDefinition_inputDefinitions[];
  outputDefinitions: PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition_SolidDefinition_outputDefinitions[];
  configField: PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition_SolidDefinition_configField | null;
}

export interface PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition_CompositeSolidDefinition_metadata {
  __typename: "MetadataItemDefinition";
  key: string;
  value: string;
}

export interface PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition_CompositeSolidDefinition_assetNodes_assetKey {
  __typename: "AssetKey";
  path: string[];
}

export interface PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition_CompositeSolidDefinition_assetNodes {
  __typename: "AssetNode";
  id: string;
  assetKey: PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition_CompositeSolidDefinition_assetNodes_assetKey;
}

export interface PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition_CompositeSolidDefinition_inputDefinitions_type {
  __typename: "ListDagsterType" | "NullableDagsterType" | "RegularDagsterType";
  displayName: string;
}

export interface PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition_CompositeSolidDefinition_inputDefinitions {
  __typename: "InputDefinition";
  name: string;
  type: PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition_CompositeSolidDefinition_inputDefinitions_type;
}

export interface PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition_CompositeSolidDefinition_outputDefinitions_type {
  __typename: "ListDagsterType" | "NullableDagsterType" | "RegularDagsterType";
  displayName: string;
}

export interface PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition_CompositeSolidDefinition_outputDefinitions {
  __typename: "OutputDefinition";
  name: string;
  isDynamic: boolean | null;
  type: PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition_CompositeSolidDefinition_outputDefinitions_type;
}

export interface PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition_CompositeSolidDefinition_inputMappings_definition {
  __typename: "InputDefinition";
  name: string;
}

export interface PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition_CompositeSolidDefinition_inputMappings_mappedInput_definition {
  __typename: "InputDefinition";
  name: string;
}

export interface PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition_CompositeSolidDefinition_inputMappings_mappedInput_solid {
  __typename: "Solid";
  name: string;
}

export interface PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition_CompositeSolidDefinition_inputMappings_mappedInput {
  __typename: "Input";
  definition: PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition_CompositeSolidDefinition_inputMappings_mappedInput_definition;
  solid: PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition_CompositeSolidDefinition_inputMappings_mappedInput_solid;
}

export interface PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition_CompositeSolidDefinition_inputMappings {
  __typename: "InputMapping";
  definition: PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition_CompositeSolidDefinition_inputMappings_definition;
  mappedInput: PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition_CompositeSolidDefinition_inputMappings_mappedInput;
}

export interface PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition_CompositeSolidDefinition_outputMappings_definition {
  __typename: "OutputDefinition";
  name: string;
}

export interface PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition_CompositeSolidDefinition_outputMappings_mappedOutput_definition {
  __typename: "OutputDefinition";
  name: string;
}

export interface PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition_CompositeSolidDefinition_outputMappings_mappedOutput_solid {
  __typename: "Solid";
  name: string;
}

export interface PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition_CompositeSolidDefinition_outputMappings_mappedOutput {
  __typename: "Output";
  definition: PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition_CompositeSolidDefinition_outputMappings_mappedOutput_definition;
  solid: PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition_CompositeSolidDefinition_outputMappings_mappedOutput_solid;
}

export interface PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition_CompositeSolidDefinition_outputMappings {
  __typename: "OutputMapping";
  definition: PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition_CompositeSolidDefinition_outputMappings_definition;
  mappedOutput: PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition_CompositeSolidDefinition_outputMappings_mappedOutput;
}

export interface PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition_CompositeSolidDefinition {
  __typename: "CompositeSolidDefinition";
  name: string;
  description: string | null;
  metadata: PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition_CompositeSolidDefinition_metadata[];
  assetNodes: PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition_CompositeSolidDefinition_assetNodes[];
  inputDefinitions: PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition_CompositeSolidDefinition_inputDefinitions[];
  outputDefinitions: PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition_CompositeSolidDefinition_outputDefinitions[];
  id: string;
  inputMappings: PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition_CompositeSolidDefinition_inputMappings[];
  outputMappings: PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition_CompositeSolidDefinition_outputMappings[];
}

export type PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition = PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition_SolidDefinition | PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition_CompositeSolidDefinition;

export interface PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_inputs_dependsOn_solid {
  __typename: "Solid";
  name: string;
}

export interface PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_inputs_dependsOn_definition_type {
  __typename: "ListDagsterType" | "NullableDagsterType" | "RegularDagsterType";
  displayName: string;
}

export interface PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_inputs_dependsOn_definition {
  __typename: "OutputDefinition";
  name: string;
  type: PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_inputs_dependsOn_definition_type;
}

export interface PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_inputs_dependsOn {
  __typename: "Output";
  solid: PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_inputs_dependsOn_solid;
  definition: PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_inputs_dependsOn_definition;
}

export interface PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_inputs_definition {
  __typename: "InputDefinition";
  name: string;
}

export interface PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_inputs {
  __typename: "Input";
  dependsOn: PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_inputs_dependsOn[];
  definition: PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_inputs_definition;
  isDynamicCollect: boolean;
}

export interface PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_outputs_dependedBy_solid {
  __typename: "Solid";
  name: string;
}

export interface PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_outputs_dependedBy_definition_type {
  __typename: "ListDagsterType" | "NullableDagsterType" | "RegularDagsterType";
  displayName: string;
}

export interface PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_outputs_dependedBy_definition {
  __typename: "InputDefinition";
  name: string;
  type: PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_outputs_dependedBy_definition_type;
}

export interface PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_outputs_dependedBy {
  __typename: "Input";
  solid: PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_outputs_dependedBy_solid;
  definition: PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_outputs_dependedBy_definition;
}

export interface PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_outputs_definition {
  __typename: "OutputDefinition";
  name: string;
}

export interface PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_outputs {
  __typename: "Output";
  dependedBy: PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_outputs_dependedBy[];
  definition: PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_outputs_definition;
}

export interface PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid {
  __typename: "Solid";
  name: string;
  definition: PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_definition;
  inputs: PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_inputs[];
  outputs: PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid_outputs[];
  isDynamicMapped: boolean;
}

export interface PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles {
  __typename: "SolidHandle";
  handleID: string;
  solid: PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles_solid;
}

export interface PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot {
  __typename: "PipelineSnapshot";
  id: string;
  name: string;
  solidHandles: PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot_solidHandles[];
}

export type PartitionStepStatusPipelineQuery_pipelineSnapshotOrError = PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineNotFoundError | PartitionStepStatusPipelineQuery_pipelineSnapshotOrError_PipelineSnapshot;

export interface PartitionStepStatusPipelineQuery {
  pipelineSnapshotOrError: PartitionStepStatusPipelineQuery_pipelineSnapshotOrError;
}

export interface PartitionStepStatusPipelineQueryVariables {
  pipelineSelector?: PipelineSelector | null;
}