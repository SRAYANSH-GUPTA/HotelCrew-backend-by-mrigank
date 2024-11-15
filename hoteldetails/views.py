from rest_framework.generics import CreateAPIView
from .models import *
from .serializers import *
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
from authentication.models import Staff, Manager,Receptionist,User


class HotelDetailView(CreateAPIView):
   queryset = HotelDetails.objects.all()
   serializer_class = HotelSerializer
   permission_classes = [AllowAny]

   def post(self, request):
        if not request.user.is_authenticated:
            return Response({
                'status': 'error',
                'message': 'User must be authenticated.'
            }, status=status.HTTP_403_FORBIDDEN)
            
        serializer = self.get_serializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            hotel = serializer.save()
            
            excel_file = request.FILES.get('staff_excel_sheet')
            
            if excel_file:
                try:
                    df = pd.read_excel(excel_file)

                    
                    for _, row in df.iterrows():
                        role = row.get('Role', 'Staff')  # Default to 'Staff' if not specified
                        email = row['Email']
                        name = row['Name']
                        department = row['department']  

                        user=User.objects.create_user(
                            email=email,
                            user_name=name,
                            role=role,
                        )
                        # department = Department.objects.create(
                        #     name=sub_role,
                        # )
                        # Check the role and create the appropriate user
                        if role.lower() == 'manager':
                            manager = Manager.objects.create(
                                user=user,
                                # email=user.email,
                                # name=user.user_name,
                                hotel=hotel,
                            )
                            
                        elif role.lower()=='receptionist':
                            receptionist=Receptionist.objects.create(
                                user=user,
                                # email=user.email,
                                # name=user.user_name,
                                hotel=hotel,
                            )
                        else:  # For staff
                            staff = Staff.objects.create(
                                user=user,
                                # email=user.email,
                                # name=user.user_name,
                                hotel=hotel,
                                department=department,
                            )

                except Exception as e:
                    return Response({
                        'status': 'error',
                        'message': f"Error processing Excel file: {str(e)}"
                    }, status=status.HTTP_400_BAD_REQUEST)
                    
            return Response({
                'status': 'success',
                'message': 'Hotel registered successfully',
                'hotel': serializer.data,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)