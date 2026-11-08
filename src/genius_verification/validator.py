from __future__ import annotations

import re
from typing import Any


class ContractSchemaValidator:
    SEMVER_PATTERN = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$")

    @classmethod
    def is_valid_semver(cls, version: str) -> bool:
        return bool(cls.SEMVER_PATTERN.match(str(version).strip()))

    @classmethod
    def validate_capability_manifest(cls, manifest: dict[str, Any]) -> tuple[bool, list[str]]:
        errors: list[str] = []
        if not isinstance(manifest, dict):
            return False, ["Manifest must be a dictionary"]

        required_keys = ["name", "version", "capabilities"]
        for key in required_keys:
            if key not in manifest:
                errors.append(f"Missing required manifest key: {key}")

        if "version" in manifest and not cls.is_valid_semver(manifest["version"]):
            errors.append(f"Invalid semantic version: {manifest['version']}")

        capabilities = manifest.get("capabilities")
        if not isinstance(capabilities, list):
            errors.append("Capabilities must be a list")
        elif not capabilities:
            errors.append("Capabilities list must not be empty")

        return len(errors) == 0, errors

    @classmethod
    def detect_dependency_cycles(cls, graph: dict[str, list[str]]) -> tuple[bool, list[str] | None]:
        visited: dict[str, int] = {}
        path: list[str] = []

        def dfs(node: str) -> bool:
            visited[node] = 1
            path.append(node)
            for neighbor in graph.get(node, []):
                if visited.get(neighbor) == 1:
                    path.append(neighbor)
                    return True
                if visited.get(neighbor) != 2 and dfs(neighbor):
                    return True
            path.pop()
            visited[node] = 2
            return False

        for node in list(graph.keys()):
            if visited.get(node) != 2 and dfs(node):
                return True, path
        return False, None
