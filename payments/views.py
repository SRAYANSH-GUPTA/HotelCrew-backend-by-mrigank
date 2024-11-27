# from .models import wallet, Transaction
# from rest_framework.views import APIView
# from .serializers import walletSerializer, TransactionSerializer
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response, status


# class walletView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         wallet = wallet.objects.filter(user=request.user)
#         serializer = walletSerializer(wallet, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = walletSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# class TransactionView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         transaction = Transaction.objects.filter(wallet__user=request.user)
#         serializer = TransactionSerializer(transaction, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = TransactionSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(wallet__user=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)