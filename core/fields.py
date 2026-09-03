from rest_framework import serializers


class StrictBooleanField(serializers.BooleanField):
    """BooleanField que acepta únicamente JSON true/false (bool Python)."""

    def to_internal_value(self, data):
        if isinstance(data, bool):
            return data
        self.fail('invalid', input=data)