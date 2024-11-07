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
            
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            hotel = serializer.save()
            
            if hotel.staff_excel_sheet:
                try:
                    # Read the Excel file using pandas
                    df = pd.read_excel(hotel.staff_excel_sheet.path)

                    # Iterate over the DataFrame rows and create Staff/Manager instances
                    for _, row in df.iterrows():
                        role = row.get('Role', 'Staff')  # Default to 'Staff' if not specified
                        email = row['Email']
                        name = row['Name']
                        department = row['department']  # Default to 'General' if not specified

                        user=User.objects.create(
                            email=email,
                            user_name=name,
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