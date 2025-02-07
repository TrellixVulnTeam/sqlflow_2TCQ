# Copyright 2020 The SQLFlow Authors. All rights reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
""" This module provides two APIs to compress and decompress a
directory.
"""
import os
import tarfile


def zip_dir(src_dir, tarball, arcname=None, filter=None):
    """To compress a directory into tarball.

    Args:
        src_dir: string
            The source directory to compress.

        tarball: string
            The output tarball name.

        arcname: string
            The output name of src_dir in the tarball.
    """
    with tarfile.open(tarball, "w:gz") as tar:
        tar.add(src_dir, arcname=arcname, recursive=True, filter=filter)


def unzip_dir(tarball, dest_dir=None):
    """To decompress a tarball to a directory.

    Args:
        tarball: string
            The tarball to decompress.

        dest_dir: string
            The output path.
    """
    if dest_dir is None:
        dest_dir = os.getcwd()

    with tarfile.open(tarball, 'r:gz') as tar:
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(tar, path=dest_dir)
