from rest_framework.generics import CreateAPIView
from .models import *
from .serializers import *
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status


class HotelDetailView(CreateAPIView):
   queryset = HotelDetails.objects.all()
   serializer_class = HotelSerializer
   permission_classes = [AllowAny]

   def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            hotel = serializer.save()
            return Response({
                'status': 'success',
                'message': 'Hotel registered successfully',
                'hotel': serializer.data,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)