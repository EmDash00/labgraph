#!/usr/bin/env python3
# Copyright (c) Meta Platforms, Inc. and affiliates.

import numpy as np

from abc import ABC, abstractmethod
from dataclasses import dataclass
from argparse import ArgumentParser, Namespace
from typing import Any

@dataclass
class ExtensionResult():
    """
    Produced by `PoseVisExtension`

    Attributes:
        `data`: `Any`
    """
    data: Any

class PoseVisExtensionBase(ABC):
    """
    Abstract base class for `PoseVisExtension`

    Abstract methods:
        `register_args(self, parser: ArgumentParser) -> None`

        `check_enabled(self, args: Namespace) -> bool`

        `setup(self) -> None`

        `process_frame(self, frame: np.ndarray) -> ExtensionResult`
        
        `cleanup(self) -> None`

        `draw_overlay(cls, result: ExtensionResult) -> None`

        `check_output(cls, result: ExtensionResult) -> bool`
    """
    @abstractmethod
    def register_args(self, parser: ArgumentParser) -> None:
        """
        Called before graph initialization and argument parsing
        
        Use this to register an argument that will allow this extension to be enabled or disabled
        """
        raise NotImplementedError

    @abstractmethod
    def check_enabled(self, args: Namespace) -> bool:
        """
        Check the `ArgumentParser.parse_args()` result to determine if this extension should be enabled
        """
        raise NotImplementedError

    @abstractmethod
    def setup(self) -> None:
        """
        Called on video stream setup
        """
        pass

    @abstractmethod
    def process_frame(self, frame: np.ndarray) -> ExtensionResult:
        """
        Called once per frame inside of a video stream node
        """
        raise NotImplementedError

    @abstractmethod
    def cleanup(self) -> None:
        """
        Called on graph shutdown
        """
        pass

    @classmethod
    @abstractmethod
    def draw_overlay(cls, frame: np.ndarray, result: ExtensionResult) -> None:
        """
        Called upon displaying extension results
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def check_output(cls, result: ExtensionResult) -> bool:
        """
        Method for extensions to check their output via assertions
        
        Called during test execution
        """
        raise NotImplementedError

class PoseVisExtension(PoseVisExtensionBase):
    """
    An extension of the base class that Pose Vis uses to automatically initialize the following variables:

    Attributes:
        `extension_id`: `int`, a contiguous identifier for each enabled extension
    
    Methods:
        `set_enabled(self, extension_id: int) -> None`
    """
    extension_id: int

    def set_enabled(self, extension_id: int) -> None:
        """
        Called if this extension passes the `check_enabled` method
        """
        self.extension_id = extension_id
