from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Item
from users.models import User
from .serializers import *

class ItemListView(APIView):
    def get(self, request):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

class ItemPurchaseView(APIView):
    """아이템 구매를 처리하는 API View"""
    def post(self, request, *args, **kwargs):
        serializer = ItemPurchaseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() # Serializer의 create 메서드 호출
            return Response({"message": "아이템 구매에 성공했습니다."}, status=status.HTTP_200_OK)
        
        # 유효성 검증 실패 시 에러 메시지 반환
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class UpdateBaseView(APIView):
    def post(self, request):
        serializer = UpdateBaseSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data['user_instance']
        item_name = serializer.validated_data['item_name']

        if serializer.validated_data['is_character']:
            try:
                item = Item.objects.get(item_name=item_name, item_type=1)
            except Item.DoesNotExist:
                return Response({'error': '해당 캐릭터 아이템이 존재하지 않습니다.'}, status=status.HTTP_404_NOT_FOUND)

            user.base_character_name = item.item_name
            user.base_character_img = item.item_img
            user.save()
            return Response({'message': '캐릭터가 성공적으로 업데이트되었습니다.'}, status=status.HTTP_200_OK)

        elif serializer.validated_data['is_background']:
            try:
                item = Item.objects.get(item_name=item_name, item_type=2)
            except Item.DoesNotExist:
                return Response({'error': '해당 배경 아이템이 존재하지 않습니다.'}, status=status.HTTP_404_NOT_FOUND)

            # --- 이 부분을 수정합니다 ---
            # item_detail_img 대신 item_img를 리스트에 담아 저장합니다.
            user.base_background_name = item.item_name
            user.base_background_img = [item.item_img] 
            user.save()
            return Response({'message': '배경이 성공적으로 업데이트되었습니다.'}, status=status.HTTP_200_OK)
        
        else:
            return Response({'error': 'item_name의 유형을 확인할 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        