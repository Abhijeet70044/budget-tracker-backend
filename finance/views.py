from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import Transaction, Budget
from .serializers import TransactionSerializer, BudgetSerializer

class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

class TransactionListCreateAPIView(APIView):
    def get(self, request):
        transactions = Transaction.objects.filter(user=request.user)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        if not data.get('category'):
            # Assign default category based on type
            from .models import Category
            if data.get('type') == 'income':
                income_cat = Category.objects.get(name="Income")
                data['category'] = income_cat.id
            elif data.get('type') == 'expense':
                expense_cat = Category.objects.get(name="Expense")
                data['category'] = expense_cat.id
        serializer = TransactionSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BudgetRetrieveUpdateAPIView(APIView):

    def get(self, request):
        try:
            budget = request.user.budget
            serializer = BudgetSerializer(budget)
            return Response(serializer.data)
        except Budget.DoesNotExist:
            return Response({'error': 'No budget set.'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        try:
            # Try to get existing budget
            budget = Budget.objects.get(user=request.user)
            serializer = BudgetSerializer(budget, data=request.data)
        except Budget.DoesNotExist:
            # If none, create new
            serializer = BudgetSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FinancialSummaryAPIView(APIView):
    def get(self, request):
        transactions = Transaction.objects.filter(user=request.user)
        income = sum(t.amount for t in transactions if t.type == 'income')
        expenses = sum(t.amount for t in transactions if t.type == 'expense')
        balance = income - expenses
        return Response({'income': income, 'expenses': expenses, 'balance': balance})
