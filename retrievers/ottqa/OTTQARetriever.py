#!/usr/bin/env python3
# Copyright 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
"""Interactive mode for the tfidf DrQA retriever module."""

from typing import Iterable, Iterator
from .drqa import retriever
from .utils import convert_table_representation, TFIDFBuilder
from ..AbsCustomEmbeddingRetriever import AbsCustomEmbeddingRetriever
import json
import os


class OTTQARetriever(AbsCustomEmbeddingRetriever):
    def __init__(
        self,
        script_dir: str,
        expected_corpus_format: str = "nested array",
    ):
        super().__init__(expected_corpus_format)
        self.rankers: dict[str, retriever.TfidfDocRanker] = {}
        self.out_dir = os.path.join(script_dir, "title_sectitle_schema/")

    def retrieve(
        self,
        query: str,
        dataset_name: str,
        top_k: int,
        **kwargs,
    ) -> list[str]:
        ranker = self.rankers[dataset_name]
        doc_names, doc_scores = ranker.closest_docs(query, top_k)
        return doc_names

    def embed_corpus(self, dataset_name: str, corpus: Iterable[dict]):
        if not os.path.exists(self.out_dir):
            os.mkdir(self.out_dir)
        converted_corpus = {}
        for corpus_dict in corpus:
            for key, value in corpus_dict.items():
                converted_corpus[key] = convert_table_representation(key, value)
        file_name = "fetaqa_data.json"

        # Write the dictionary to a file in JSON format
        with open(os.path.join(self.out_dir, file_name), "w") as f:
            json.dump(converted_corpus, f)
        builder = TFIDFBuilder()
        out_path = builder.build_tfidf(self.out_dir, converted_corpus)
        self.rankers[dataset_name] = retriever.get_class("tfidf")(tfidf_path=out_path)