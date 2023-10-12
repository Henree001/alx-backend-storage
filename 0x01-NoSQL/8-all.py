#!/usr/bin/env python3
"""This script defines the function list_all."""


def list_all(mongo_collection):
    """This function lists all documents in a collection."""
    all_documents = mongo_collection.find()
    return list(all_documents)
