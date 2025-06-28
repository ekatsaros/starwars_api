from rest_framework import serializers


class RegistrationValidationErrorSerializer(serializers.Serializer):
    email = serializers.ListField(
        default=["Enter a valid email", "This field is required"],
        help_text="List of error messages for this field.",
    )
    username = serializers.ListField(
        default=["This field is required"], help_text="List of error messages for username field."
    )
    first_name = serializers.ListField(
        default=["This field is required"], help_text="List of error messages for first_name field."
    )
    last_name = serializers.ListField(
        default=["This field is required"], help_text="List of error messages for last_name field."
    )
    password = serializers.ListField(
        default=["This field is required"], help_text="List of error messages for password field."
    )


class LoginValidationErrorSerializer(serializers.Serializer):
    email = serializers.ListField(
        default=["Enter a valid email", "This field is required"],
        help_text="List of error messages for email field.",
    )
    password = serializers.ListField(
        default=["This field is required"], help_text="List of error messages for password field."
    )


class AuthenticationErrorSerializer(serializers.Serializer):
    detail = serializers.CharField(
        help_text="Error message detailing the authentication failure.", default="Invalid credentials."
    )
