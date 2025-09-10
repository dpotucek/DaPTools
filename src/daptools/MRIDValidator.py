#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
mRID (Master Resource Identifier) Validator for Energy Systems
Validates UUID v4 format according to IEC 61970 CIM standards

Created on 03.09.2025 12:06

@author: David Potucek
"""

import re
import uuid
from typing import Union, Dict, Any


class MRIDValidator:
    """Validator for mRID (Master Resource Identifier) used in energy systems."""

    # Regex pattern for UUID v4 validation
    UUID_V4_PATTERN = re.compile(
        r'^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$',
        re.IGNORECASE
    )

    @classmethod
    def is_valid(cls, mrid: str) -> bool:
        """
        Check if provided mRID is valid UUID v4 format.

        Args:
            mrid: String to validate as mRID

        Returns:
            bool: True if valid mRID, False otherwise
        """
        if not isinstance(mrid, str):
            return False

        return bool(cls.UUID_V4_PATTERN.match(mrid))

    @classmethod
    def validate(cls, mrid: str) -> Dict[str, Any]:   # NOSONAR - too complex method warning overriden
        """
        Comprehensive validation with detailed results.

        Args:k
            mrid: String to validate as mRID

        Returns:
            dict: Validation results with details
        """
        result = {
            'is_valid': False,
            'mrid': mrid,
            'errors': [],
            'format_check': {},
            'uuid_object': None
        }

        # Basic type check
        if not isinstance(mrid, str):
            result['errors'].append('Input must be a string')
            return result

        # Length check
        if len(mrid) != 36:
            result['errors'].append(f'Invalid length: {len(mrid)} (expected 36)')
            result['format_check']['length'] = False
        else:
            result['format_check']['length'] = True

        # Hyphen positions check
        expected_hyphens = {8, 13, 18, 23}
        actual_hyphens = {i for i, char in enumerate(mrid) if char == '-'}

        if actual_hyphens != expected_hyphens:
            result['errors'].append('Hyphens not in correct positions (8,13,18,23)')
            result['format_check']['hyphens'] = False
        else:
            result['format_check']['hyphens'] = True

        # Hex characters check (excluding hyphens)
        hex_chars = mrid.replace('-', '')
        if not all(c in '0123456789abcdefABCDEF' for c in hex_chars):
            result['errors'].append('Contains non-hexadecimal characters')
            result['format_check']['hex_chars'] = False
        else:
            result['format_check']['hex_chars'] = True

        # Version check (14th character must be '4')
        if len(mrid) >= 15:
            if mrid[14] != '4':
                result['errors'].append(f'Invalid version: {mrid[14]} (expected 4)')
                result['format_check']['version'] = False
            else:
                result['format_check']['version'] = True

        # Variant check (19th character must be 8,9,a,b,A,B)
        if len(mrid) >= 20:
            variant_char = mrid[19].lower()
            if variant_char not in '89ab':
                result['errors'].append(f'Invalid variant: {mrid[19]} (expected 8,9,a,b)')
                result['format_check']['variant'] = False
            else:
                result['format_check']['variant'] = True

        # Overall regex pattern check
        if cls.UUID_V4_PATTERN.match(mrid):
            result['format_check']['pattern'] = True
            result['is_valid'] = True

            # Try to create UUID object
            try:
                result['uuid_object'] = uuid.UUID(mrid)
            except ValueError as e:
                result['errors'].append(f'UUID parsing error: {str(e)}')
                result['is_valid'] = False
        else:
            result['format_check']['pattern'] = False

        return result

    @classmethod
    def generate_valid_mrid(cls) -> str:
        """
        Generate a new valid mRID.

        Returns:
            str: New valid mRID in UUID v4 format
        """
        return str(uuid.uuid4())

    @classmethod
    def normalize_mrid(cls, mrid: str) -> Union[str, None]:
        """
        Normalize mRID to standard format (lowercase, proper structure).

        Args:
            mrid: mRID string to normalize

        Returns:
            str: Normalized mRID if valid, None if invalid
        """
        if not cls.is_valid(mrid):
            return None

        return mrid.lower()


# Convenience functions for direct use
def is_valid_mrid(mrid: str) -> bool:
    """Check if mRID is valid. Convenience function."""
    return MRIDValidator.is_valid(mrid)


def validate_mrid(mrid: str) -> Dict[str, Any]:
    """Validate mRID with detailed results. Convenience function."""
    return MRIDValidator.validate(mrid)


def generate_mrid() -> str:
    """Generate new valid mRID. Convenience function."""
    return MRIDValidator.generate_valid_mrid()


def normalize_mrid(mrid: str) -> Union[str, None]:
    """Normalize mRID format. Convenience function."""
    return MRIDValidator.normalize_mrid(mrid)


# Example usage and testing
if __name__ == "__main__":
    # Test cases
    test_cases = [
        "f47ac10b-58cc-4372-a567-0e02b2c3d479",  # Valid
        "F47AC10B-58CC-4372-A567-0E02B2C3D479",  # Valid (uppercase)
        "f47ac10b-58cc-5372-a567-0e02b2c3d479",  # Invalid version
        "f47ac10b-58cc-4372-1567-0e02b2c3d479",  # Invalid variant
        "f47ac10b58cc4372a5670e02b2c3d479",  # Missing hyphens
        "f47ac10b-58cc-4372-a567-0e02b2c3d47",  # Too short
        "not-a-valid-mrid-at-all",  # Invalid format
        "",  # Empty string
        123,  # Wrong type
    ]

    print("=== mRID Validation Tests ===\n")

    for i, test_mrid in enumerate(test_cases, 1):
        print(f"Test {i}: {test_mrid}")
        print(f"Valid: {is_valid_mrid(test_mrid)}")

        if isinstance(test_mrid, str) and test_mrid:
            validation_result = validate_mrid(test_mrid)
            if validation_result['errors']:
                print(f"Errors: {', '.join(validation_result['errors'])}")
        print("-" * 50)

    # Generate new mRID
    print(f"\nGenerated new mRID: {generate_mrid()}")
    print(f"Is generated mRID valid: {is_valid_mrid(generate_mrid())}")