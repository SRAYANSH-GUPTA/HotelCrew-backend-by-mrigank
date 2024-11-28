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

class DailyFinanceSerializer(serializers.Serializer):
    date = serializers.DateField()
    total_revenue = serializers.DecimalField(max_digits=10, decimal_places=2)

class MonthlyFinanceSerializer(serializers.Serializer):
    month = serializers.CharField(max_length=20)
    daily_stats = DailyFinanceSerializer(many=True)