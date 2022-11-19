from rest_framework import serializers

from classes.models import Class, ClassOccurrence


class ClassSerializer(serializers.ModelSerializer):
    schedule = serializers.SerializerMethodField()
    keywords = serializers.StringRelatedField(many=True)
    coach = serializers.CharField()

    class Meta:
        model = Class
        fields = ['name', 'description', 'coach', 'keywords', 'capacity', 'schedule']

    def get_schedule(self, obj):
        return f'Every {dict(Class.SCHEDULE_DAYS)[obj.schedule_day]} from {obj.start_time.strftime("%H:%M")} - {obj.end_time.strftime("%H:%M")}'


class ClassOccurrenceSerializer(serializers.ModelSerializer):
    class_name = serializers.StringRelatedField(source='class_obj')
    start_time = serializers.SerializerMethodField()
    end_time = serializers.SerializerMethodField()

    class Meta:
        model = ClassOccurrence
        fields = ['class_name', 'date', 'start_time', 'end_time']

    def get_start_time(self, obj):
        return obj.class_obj.start_time.strftime("%I:%M %p")

    def get_end_time(self, obj):
        return obj.class_obj.end_time.strftime("%I:%M %p")
