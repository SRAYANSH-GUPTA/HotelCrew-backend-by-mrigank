from rest_framework import serializers


class DailyHotelPerformanceSerializer(serializers.Serializer):
    date = serializers.DateField()
    performance_percentage = serializers.FloatField()


class MonthlyHotelPerformanceSerializer(serializers.Serializer):
    month = serializers.CharField()
    daily_stats = DailyHotelPerformanceSerializer(many=True)


class DailyStaffPerformanceSerializer(serializers.Serializer):
    date = serializers.DateField()
    performance_percentage = serializers.FloatField()


class MonthlyStaffPerformanceSerializer(serializers.Serializer):
    month = serializers.CharField()
    daily_stats = DailyStaffPerformanceSerializer(many=True)
