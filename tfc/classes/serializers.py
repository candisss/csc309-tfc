from rest_framework import serializers

from classes.models import Class, ClassOccurrence


class ClassSerializer(serializers.ModelSerializer):
    schedule = serializers.SerializerMethodField()
    keywords = serializers.StringRelatedField(many=True)

    class Meta:
        model = Class
        fields = ['name', 'description', 'coach', 'keywords', 'capacity', 'schedule']

    def get_schedule(self, obj):
        return f'Every {dict(Class.SCHEDULE_DAYS)[obj.schedule_day]} from {obj.start_time.strftime("%H:%M")} - {obj.end_time.strftime("%H:%M")}'


class ClassOccurrenceSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField(source='class_obj.name')
    description = serializers.StringRelatedField(source='class_obj.description')
    coach = serializers.StringRelatedField(source='class_obj.coach')
    keywords = serializers.StringRelatedField(source='class_obj.keywords', many=True)
    capacity = serializers.StringRelatedField(source='class_obj.capacity')
    start_time = serializers.SerializerMethodField()
    end_time = serializers.SerializerMethodField()

    class Meta:
        model = ClassOccurrence
        fields = ['name', 'description', 'coach', 'keywords', 'capacity', 'date', 'start_time', 'end_time']

    def get_start_time(self, obj):
        return obj.class_obj.start_time.strftime("%I:%M %p")

    def get_end_time(self, obj):
        return obj.class_obj.end_time.strftime("%I:%M %p")
