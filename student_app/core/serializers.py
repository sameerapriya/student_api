from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from core.models import Course, CourseEnroll


class StudentRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('username', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True, 'min_length': 5
            }
        }

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()
        return user


class StudentAuthTokenSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=255)
    password = serializers.CharField(
        style={'input_type': 'password'}, trim_whitespace=False
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=username, password=password
        )
        if not user:
            msg = _('Unable to Authenticate with provided Credentials')
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'name')
        read_only_fields = ('id',)


class CourseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'name', 'description')
        read_only_fields = ('id',)


class CourseEnrollSerializer(serializers.ModelSerializer):

    course = serializers.PrimaryKeyRelatedField(
        required=True, queryset=Course.objects.all())

    class Meta:
        model = CourseEnroll
        fields = ('id', 'course', 'created_on')
        read_only_fields = ('id',)

    def create(self, validated_data):
        course = validated_data.pop('course')
        student = validated_data.pop('student')
        try:
            CourseEnroll.objects.get(course=course, student=student)
            raise serializers.ValidationError('Already Enrolled')
        except CourseEnroll.DoesNotExist:
            if course.max_student_count > course.student_count:
                course.student_count += 1
                course.save()
                course_enroll = CourseEnroll.objects.create(
                    course=course, student=student, **validated_data)
                course_enroll.save()
                return course_enroll
            raise serializers.ValidationError('Slots full')


class CourseEnrollDetailSerializer(serializers.ModelSerializer):
    course = CourseDetailSerializer(many=False)

    class Meta:
        model = CourseEnroll
        fields = ('id', 'course', 'created_on')
        read_only_fields = ('id',)
