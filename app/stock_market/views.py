from decimal import Decimal
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import os
from .models import StockModel, StockPriceModel

import requests


# Create your views here.
@api_view(["POST"])
def get_price(request):
    payload = request.data
    symbol = payload.get("symbol")
    quant: str = payload.get("quantity")

    if not symbol or not isinstance(symbol, str):
        return Response(
            {"message": "symbol not found."}, status=status.HTTP_400_BAD_REQUEST
        )

    if not quant or not isinstance(quant, int):
        return Response(
            {"message": "quantity not found."}, status=status.HTTP_400_BAD_REQUEST
        )

    resp = requests.get(
        "https://www.alphavantage.co/query",
        params={
            "function": "GLOBAL_QUOTE",
            "symbol": symbol,
            "apikey": os.getenv("API_KEY"),
        },
    )

    if resp.status_code != 200:
        return Response(
            {"message": "cannot fetch api."}, status=status.HTTP_400_BAD_REQUEST
        )

    body = resp.json()
    price = body["Global Quote"].get("05. price")
    if not price:
        return Response(
            {"message": "invalid symbol."}, status=status.HTTP_400_BAD_REQUEST
        )

    stock, created = StockModel.objects.get_or_create(stock_symbol=symbol)
    if not created:
        stock.save()

    try:
        dec_price = Decimal(price) * quant
        price = dec_price.quantize(Decimal("0.00"))
    except Exception as e:
        return Response(
            {"message": "quantity invalid."}, status=status.HTTP_400_BAD_REQUEST
        )

    stock_price = StockPriceModel.objects.create(
        stock=stock, quantity=quant, price=price
    )
    stock_price.save()

    return Response(
        {"message": "Fetch successfully.", "data": stock_price.to_dict()},
        status=status.HTTP_200_OK,
    )
