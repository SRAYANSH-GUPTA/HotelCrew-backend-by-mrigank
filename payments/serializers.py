from .models import wallet, Transaction
from rest_framework import serializers
from hoteldetails.views import hotelname

class walletserializer(serializers.ModelSerializer):
    class Meta:
        model = wallet
        fields = ['id','user', 'hotel', 'balance', 'created_at', 'wallet_id']

    def create(self, validated_data):
        user = self.context['request'].user        
        hotel = hotelname(user)
        validated_data['user'] = user
        validated_data['hotel'] = hotel
        print(validated_data)
        super().create(validated_data)
        
    
class Transactionserializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['wallet', 'amount', 'transaction_id', 'transaction_type', 'created_at']
 
