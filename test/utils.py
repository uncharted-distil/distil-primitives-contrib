#
#   Copyright © 2021 Uncharted Software Inc.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import os.path as path

from d3m import container
from d3m.metadata import base as metadata_base
from d3m.base import utils as base_utils


def load_dataset(base_path: str) -> container.Dataset:
    # loads a d3m formatted dataset
    dataset_doc_path = path.join(base_path, "datasetDoc.json")
    dataset = container.Dataset.load(
        "file://{dataset_doc_path}".format(dataset_doc_path=dataset_doc_path)
    )
    return dataset


def get_dataframe(dataset: container.Dataset, resource_id: str) -> container.DataFrame:
    # extracts a dataframe from a dataset and ensures its metadata is transferred over

    # grab the resource and its metadata out of the dataset
    dataframe_resource_id, dataframe = base_utils.get_tabular_resource(
        dataset, resource_id
    )
    resource_metadata = dict(dataset.metadata.query((dataframe_resource_id,)))
    # copy the resource metadata from the dataset into the resource
    new_metadata = metadata_base.DataMetadata(resource_metadata)
    new_metadata = dataset.metadata.copy_to(new_metadata, (resource_id,))
    new_metadata = new_metadata.remove_semantic_type(
        (), "https://metadata.datadrivendiscovery.org/types/DatasetEntryPoint"
    )
    dataframe.metadata = new_metadata

    return dataframe
